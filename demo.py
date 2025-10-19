#!/usr/bin/env python3
"""
Demo script to showcase the RL Model + Visualizer integration.

This script provides a menu-driven interface to test different aspects
of the integration.
"""

import sys
import os

def print_header():
    print("=" * 70)
    print("🧬 RL Model + 3D DNA Visualizer Integration Demo")
    print("=" * 70)
    print()

def print_menu():
    print("\nChoose a demo option:")
    print()
    print("  1. Test Visualizer with Custom Sequences")
    print("     (Opens browser with predefined test sequences)")
    print()
    print("  2. Run Full Integration (GUI + Training + Visualizer)")
    print("     (Launch GUI, train model, then visualize)")
    print()
    print("  3. Quick Visualizer Test (Short URL)")
    print("     (Test with very short sequences)")
    print()
    print("  4. View Documentation")
    print("     (Open documentation files)")
    print()
    print("  5. Exit")
    print()

def test_visualizer_params():
    """Test the visualizer with custom URL parameters."""
    print("\n" + "─" * 70)
    print("Running Test 1: Visualizer with Custom Sequences")
    print("─" * 70)
    
    try:
        import webbrowser
        import urllib.parse
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        html_path = os.path.join(current_dir, "sequence_transformation_viz.html")
        
        # Test sequences - clearly different patterns
        initial_seq = "ACGTACGTACGTACGTACGT"  # Repeating ACGT
        target_seq = "TGCATGCATGCATGCATGCA"   # Repeating TGCA
        
        params = urllib.parse.urlencode({
            'initial': initial_seq,
            'target': target_seq
        })
        
        file_url = f"file://{html_path}?{params}"
        
        print(f"\n✓ HTML file found: {html_path}")
        print(f"\n✓ Test sequences:")
        print(f"  Initial: {initial_seq}")
        print(f"  Target:  {target_seq}")
        print(f"\n✓ Opening browser with URL:")
        print(f"  {file_url[:80]}...")
        
        webbrowser.open(file_url)
        
        print(f"\n✓ Browser should open with the visualizer")
        print(f"✓ You should see the transformation animation")
        print(f"✓ Try the Play, Step, and Reset buttons")
        
        input("\nPress Enter to return to menu...")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        input("\nPress Enter to return to menu...")

def run_full_integration():
    """Run the full GUI integration."""
    print("\n" + "─" * 70)
    print("Running Test 2: Full GUI Integration")
    print("─" * 70)
    
    print("\nThis will:")
    print("  1. Launch the training GUI")
    print("  2. You can configure objectives (optional)")
    print("  3. Click 'Start Training' to run training")
    print("  4. Wait for training to complete")
    print("  5. Click '🧬 Open Visualizer' to see results")
    print()
    
    response = input("Continue? (y/n): ").strip().lower()
    if response != 'y':
        print("Cancelled.")
        return
    
    try:
        import tkinter as tk
        from rl_model.gui import TrainingGUI
        
        print("\n✓ Launching GUI...")
        print("✓ Look for the new window!")
        
        root = tk.Tk()
        app = TrainingGUI(root, episodes=50, seq_len=20, max_edits=8)
        
        print("\n✓ GUI launched successfully")
        print("✓ Follow the steps in the GUI window")
        print("✓ Close the GUI window when done")
        
        root.mainloop()
        
        print("\n✓ GUI closed")
        input("\nPress Enter to return to menu...")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        input("\nPress Enter to return to menu...")

def quick_test():
    """Quick test with short sequences."""
    print("\n" + "─" * 70)
    print("Running Test 3: Quick Test with Short Sequences")
    print("─" * 70)
    
    try:
        import webbrowser
        import urllib.parse
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        html_path = os.path.join(current_dir, "sequence_transformation_viz.html")
        
        # Very short sequences for quick testing
        initial_seq = "AAAAAAAAAA"  # 10 A's
        target_seq = "TTTTTTTTTT"   # 10 T's
        
        params = urllib.parse.urlencode({
            'initial': initial_seq,
            'target': target_seq
        })
        
        file_url = f"file://{html_path}?{params}"
        
        print(f"\n✓ Quick test sequences:")
        print(f"  Initial: {initial_seq} (all A's)")
        print(f"  Target:  {target_seq} (all T's)")
        print(f"\n✓ This should show a simple A → T transformation")
        
        webbrowser.open(file_url)
        
        print(f"\n✓ Browser opened")
        input("\nPress Enter to return to menu...")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        input("\nPress Enter to return to menu...")

def view_docs():
    """View documentation."""
    print("\n" + "─" * 70)
    print("Documentation Files")
    print("─" * 70)
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    docs = {
        "1": ("QUICKSTART.md", "Quick start guide for users"),
        "2": ("INTEGRATION_README.md", "Detailed technical documentation"),
        "3": ("INTEGRATION_SUMMARY.md", "Summary of changes made"),
        "4": ("ARCHITECTURE.md", "System architecture diagrams"),
    }
    
    print("\nAvailable documentation:")
    for key, (filename, desc) in docs.items():
        filepath = os.path.join(current_dir, filename)
        exists = "✓" if os.path.exists(filepath) else "✗"
        print(f"  {key}. {exists} {filename}")
        print(f"     {desc}")
    
    print("\n  5. Return to main menu")
    
    choice = input("\nSelect a document to view (1-5): ").strip()
    
    if choice in docs:
        filename, _ = docs[choice]
        filepath = os.path.join(current_dir, filename)
        
        if os.path.exists(filepath):
            print(f"\n✓ Opening {filename}...")
            
            # Try to open with default editor
            if sys.platform == 'darwin':  # macOS
                os.system(f'open "{filepath}"')
            elif sys.platform == 'win32':  # Windows
                os.system(f'start "" "{filepath}"')
            else:  # Linux
                os.system(f'xdg-open "{filepath}"')
            
            input("\nPress Enter to return to menu...")
        else:
            print(f"\n✗ File not found: {filepath}")
            input("\nPress Enter to return to menu...")
    elif choice == "5":
        return
    else:
        print("\n✗ Invalid choice")
        input("\nPress Enter to return to menu...")

def main():
    """Main demo loop."""
    while True:
        print_header()
        print_menu()
        
        choice = input("Enter your choice (1-5): ").strip()
        
        if choice == "1":
            test_visualizer_params()
        elif choice == "2":
            run_full_integration()
        elif choice == "3":
            quick_test()
        elif choice == "4":
            view_docs()
        elif choice == "5":
            print("\n" + "─" * 70)
            print("Thank you for testing the integration!")
            print("─" * 70)
            print("\nFor more information, see:")
            print("  • QUICKSTART.md - User guide")
            print("  • INTEGRATION_README.md - Technical docs")
            print("  • ARCHITECTURE.md - System diagrams")
            print()
            sys.exit(0)
        else:
            print("\n✗ Invalid choice. Please enter 1-5.")
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Goodbye!")
        sys.exit(0)
