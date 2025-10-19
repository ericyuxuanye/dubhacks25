"""Test script to verify the HTTP server works with query parameters."""
import http.server
import socketserver
import webbrowser
import time
import threading
from functools import partial
import os

def test_server():
    # Get the current directory
    directory = os.path.dirname(os.path.abspath(__file__))
    
    # Create handler
    handler = partial(http.server.SimpleHTTPRequestHandler, directory=directory)
    
    # Start server
    port = 8765
    httpd = socketserver.TCPServer(("", port), handler)
    
    # Start server in background
    server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    server_thread.start()
    
    print(f"Server started on http://localhost:{port}")
    
    # Test URL with parameters
    test_url = f"http://localhost:{port}/sequence_transformation_viz.html?initial=ACGTACGT&target=TGCATGCA"
    print(f"Opening: {test_url}")
    
    # Give server a moment to start
    time.sleep(0.5)
    
    # Open browser
    webbrowser.open_new_tab(test_url)
    
    print("\nServer is running. Press Ctrl+C to stop.")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down...")
        httpd.shutdown()

if __name__ == "__main__":
    test_server()
