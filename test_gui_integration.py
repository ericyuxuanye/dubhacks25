#!/usr/bin/env python3
"""Test script to launch the GUI with visualizer integration."""

import tkinter as tk
from rl_model.gui import TrainingGUI


def main():
    root = tk.Tk()
    app = TrainingGUI(root, episodes=60, max_edits=8)
    root.mainloop()


if __name__ == "__main__":
    main()
