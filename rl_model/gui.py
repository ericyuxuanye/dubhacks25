"""Simple Tkinter GUI to start training with a fake progress bar.

This GUI launches the same toy training loop in a background thread but
displays a simulated progress bar so the UI remains responsive and
predictable for demos.

Note: This is a demo UI. It does not provide any wet-lab instructions.
"""

import threading
import time
import random
import tkinter as tk
from tkinter import ttk
import webbrowser
import os
import urllib.parse
import http.server
import socketserver
from functools import partial

from .train import train as train_fn


class TrainingGUI:
    def __init__(self, master, episodes=200, seq_len=20, max_edits=8):
        self.master = master
        self.episodes = episodes
        self.seq_len = seq_len
        self.max_edits = max_edits
        
        # HTTP server for serving visualizer
        self.httpd = None
        self.server_port = 8765
        self.server_thread = None

        master.title("BloomSync AI — Training Demo")

        self.frame = ttk.Frame(master, padding=12)
        self.frame.grid(row=0, column=0, sticky="nsew")

        self.start_btn = ttk.Button(self.frame, text="Start Training", command=self.start_training)
        self.start_btn.grid(row=0, column=0, pady=(0, 8))

        self.progress = tk.IntVar(value=0)
        self.pbar = ttk.Progressbar(self.frame, orient="horizontal", length=400, mode="determinate", variable=self.progress)
        self.pbar.grid(row=1, column=0, pady=(0, 8))

        self.status_lbl = ttk.Label(self.frame, text="Idle")
        self.status_lbl.grid(row=2, column=0)

        self.initial_lbl = ttk.Label(self.frame, text="Initial seq: -")
        self.initial_lbl.grid(row=3, column=0, pady=(8, 0))

        self.result_lbl = ttk.Label(self.frame, text="Final seq: -")
        self.result_lbl.grid(row=4, column=0, pady=(4, 0))
        
        # Button to open visualizer
        self.viz_btn = ttk.Button(self.frame, text="🧬 Open Visualizer", command=self.open_visualizer, state="disabled")
        self.viz_btn.grid(row=5, column=0, pady=(8, 0))

        # Objectives: checkboxes to allow any combination
        self.objectives_frame = ttk.LabelFrame(self.frame, text="Objectives", padding=8)
        self.objectives_frame.grid(row=6, column=0, pady=(8, 0), sticky="w")

        # BooleanVars for each objective
        self.obj_vars = {
            "flowers": tk.BooleanVar(value=False),
            "wood_strength": tk.BooleanVar(value=False),
            "height": tk.BooleanVar(value=False),
            "concentrate_zone": tk.BooleanVar(value=False),
        }

        ttk.Checkbutton(self.objectives_frame, text="Cause flowers / fruit on new wood", variable=self.obj_vars["flowers"]).grid(row=0, column=0, sticky="w")
        ttk.Checkbutton(self.objectives_frame, text="Change wood strength for single-wire training", variable=self.obj_vars["wood_strength"]).grid(row=1, column=0, sticky="w")
        ttk.Checkbutton(self.objectives_frame, text="Change height to facilitate picking", variable=self.obj_vars["height"]).grid(row=2, column=0, sticky="w")
        ttk.Checkbutton(self.objectives_frame, text="Concentrate fruit zone for efficient picking", variable=self.obj_vars["concentrate_zone"]).grid(row=3, column=0, sticky="w")

        # Preset combobox to quickly select common combinations (also supports "Custom")
        presets = [
            "Custom",
            "All",
            "None",
            "Only: Cause flowers / fruit on new wood",
            "Only: Change wood strength",
            "Only: Change height",
            "Only: Concentrate fruit zone",
        ]
        self.preset_var = tk.StringVar(value="Custom")
        self.preset_combo = ttk.Combobox(self.frame, values=presets, textvariable=self.preset_var, state="readonly", width=60)
        self.preset_combo.grid(row=7, column=0, pady=(8, 0))
        self.preset_combo.bind("<<ComboboxSelected>>", self._on_preset_selected)

        self.training_thread = None
        self.training_done = False
        self.agent = None
        self.env = None
        self.initial_sequence = None  # Store initial sequence for visualizer

    def start_training(self):
        if self.training_thread and self.training_thread.is_alive():
            return
        self.start_btn.config(state="disabled")
        self.status_lbl.config(text="Training started...")
        self.progress.set(0)
        self.training_done = False

        # create a fresh env and show the initial sequence
        # we create it here so the GUI can display the starting seq immediately
        try:
            from .env import SequenceEnv
            self.env = SequenceEnv(seq_len=self.seq_len, max_edits=self.max_edits)
            # attach selected objectives to the env (non-intrusive attribute)
            self.env.objectives = self.get_selected_objectives()
            # Store the initial sequence for the visualizer
            self.initial_sequence = self.env.sequence
            # show initial sequence and selected objectives
            selected = self._format_selected_objectives(self.env.objectives)
            if selected:
                self.initial_lbl.config(text=f"Initial seq: {self.env.sequence} | Objectives: {selected}")
            else:
                self.initial_lbl.config(text=f"Initial seq: {self.env.sequence}")
        except Exception:
            self.initial_lbl.config(text="Initial seq: N/A")

        # start real training in background thread
        self.training_thread = threading.Thread(target=self._run_training)
        self.training_thread.daemon = True
        self.training_thread.start()

        # start fake progress animation
        self._simulate_progress()

    def _run_training(self):
        # Run the existing toy training loop; this may take a few seconds.
        try:
            # pass pre-created env so GUI and training reference the same sequence
            self.agent, self.env = train_fn(episodes=self.episodes, seq_len=self.seq_len, max_edits=self.max_edits, env=self.env)
        except Exception as e:
            # capture error and show in UI thread
            self.master.after(0, lambda: self._on_failure(str(e)))
            return
        self.training_done = True
        # ensure UI finalization runs on main thread
        self.master.after(0, self._on_done)

    def _simulate_progress(self):
        # Increment progress by a small random amount, cap below 100 until done.
        cur = self.progress.get()
        if self.training_done:
            self.progress.set(100)
            return

        # increase quickly at first, then slower
        step = random.randint(2, 5) if cur < 60 else random.randint(1, 3)
        new = min(cur + step, 95)
        self.progress.set(new)
        # schedule next update
        self.master.after(100, self._simulate_progress)

    def _on_done(self):
        self.progress.set(100)
        self.status_lbl.config(text="Training finished")
        final = getattr(self.env, 'sequence', 'N/A')
        # display final sequence and the objectives that were used
        objectives = getattr(self.env, 'objectives', [])
        selected = self._format_selected_objectives(objectives)
        if selected:
            self.result_lbl.config(text=f"Final seq: {final} | Objectives: {selected}")
        else:
            self.result_lbl.config(text=f"Final seq: {final}")
        self.start_btn.config(state="normal")
        # Enable visualizer button
        self.viz_btn.config(state="normal")

    def _on_failure(self, msg):
        self.status_lbl.config(text=f"Error: {msg}")
        self.start_btn.config(state="normal")
    
    def _start_server(self):
        """Start a simple HTTP server to serve the visualizer HTML."""
        if self.httpd is not None:
            return  # Server already running
        
        # Get the parent directory path
        script_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(script_dir)
        
        # Create a custom handler that serves from parent_dir
        handler = partial(http.server.SimpleHTTPRequestHandler, directory=parent_dir)
        
        # Find an available port
        for port in range(self.server_port, self.server_port + 10):
            try:
                self.httpd = socketserver.TCPServer(("", port), handler)
                self.server_port = port
                break
            except OSError:
                continue
        
        if self.httpd is None:
            print("Error: Could not find available port for server")
            return
        
        # Start server in background thread
        self.server_thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        self.server_thread.start()
        print(f"[INFO] HTTP server started on port {self.server_port}")
    
    def open_visualizer(self):
        """Open the HTML visualizer with the initial and final sequences as URL parameters."""
        if not self.initial_sequence or not self.env:
            return
        
        # Start the HTTP server if not already running
        self._start_server()
        
        if self.httpd is None:
            self.status_lbl.config(text="Error: Could not start server")
            return
        
        # Get the path to the HTML file to verify it exists
        script_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(script_dir)
        html_path = os.path.join(parent_dir, "sequence_transformation_viz.html")
        
        # Check if file exists
        if not os.path.exists(html_path):
            self.status_lbl.config(text="Error: Visualizer HTML not found")
            return
        
        # Build URL with query parameters
        final_seq = self.env.sequence
        
        print(f"\n[DEBUG] Opening visualizer:")
        print(f"  Initial sequence: {self.initial_sequence}")
        print(f"  Final sequence:   {final_seq}")
        
        # URL encode the sequences
        params = urllib.parse.urlencode({
            'initial': self.initial_sequence,
            'target': final_seq
        })
        
        # Use localhost URL instead of file://
        url = f"http://localhost:{self.server_port}/sequence_transformation_viz.html?{params}"
        
        print(f"  URL: {url}")
        
        # Open in browser
        webbrowser.open_new_tab(url)
        self.status_lbl.config(text=f"Visualizer opened at localhost:{self.server_port}")

    def _on_preset_selected(self, event=None):
        """Apply a preset to the checkbox vars."""
        preset = self.preset_var.get()
        if preset == "All":
            for v in self.obj_vars.values():
                v.set(True)
        elif preset == "None":
            for v in self.obj_vars.values():
                v.set(False)
        elif preset.startswith("Only: "):
            # clear all then set the matching one
            for k, v in self.obj_vars.items():
                v.set(False)
            if "flowers" in preset:
                self.obj_vars["flowers"].set(True)
            elif "wood strength" in preset:
                self.obj_vars["wood_strength"].set(True)
            elif "height" in preset:
                self.obj_vars["height"].set(True)
            elif "Concentrate" in preset:
                self.obj_vars["concentrate_zone"].set(True)
        else:
            # Custom -> leave user-controlled
            return

    def get_selected_objectives(self):
        """Return a list of selected objective keys (non-destructive).

        This attaches to the env as a simple attribute; the training loop
        itself is unchanged and will run the same way.
        """
        return [k for k, v in self.obj_vars.items() if v.get()]

    def _format_selected_objectives(self, obj_list):
        if not obj_list:
            return ""
        labels = {
            "flowers": "flowers/fruit on new wood",
            "wood_strength": "wood strength (single-wire)",
            "height": "height (pickable)",
            "concentrate_zone": "concentrate fruit zone",
        }
        return ", ".join(labels.get(k, k) for k in obj_list)


def main():
    root = tk.Tk()
    app = TrainingGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
