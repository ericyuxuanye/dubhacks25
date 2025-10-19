#!/usr/bin/env python3
"""Test script to verify the visualizer can load sequences from URL parameters."""

import webbrowser
import os
import urllib.parse


def test_visualizer_with_params():
    # Get the path to the HTML file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    html_path = os.path.join(current_dir, "sequence_transformation_viz.html")
    
    # Test sequences
    initial_seq = "ACGTACGTACGTACGTACGT"  # 20 bases
    target_seq = "TGCATGCATGCATGCATGCA"   # 20 bases
    
    # URL encode the sequences
    params = urllib.parse.urlencode({
        'initial': initial_seq,
        'target': target_seq
    })
    
    # Create file:// URL
    file_url = f"file://{html_path}?{params}"
    
    print(f"Opening visualizer with URL:")
    print(f"  Initial sequence: {initial_seq}")
    print(f"  Target sequence:  {target_seq}")
    print(f"\nURL: {file_url}")
    
    # Open in browser
    webbrowser.open(file_url)
    print("\nVisualizer should open in your browser with the specified sequences.")


if __name__ == "__main__":
    test_visualizer_with_params()
