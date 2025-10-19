# HTTP Server Integration for Visualizer

## Problem
Query parameters were not showing up in the browser when using `file://` URLs. Most modern browsers strip or ignore query parameters from local file URLs for security reasons.

## Solution
Implemented a lightweight HTTP server within the GUI that:
1. Serves the HTML files from the project directory
2. Properly handles query parameters in the URL
3. Runs in the background as a daemon thread
4. Automatically finds an available port (starting from 8765)

## Changes Made

### `rl_model/gui.py`

#### Added Imports
```python
import http.server
import socketserver
from functools import partial
```

#### Added Server Attributes to `__init__`
```python
# HTTP server for serving visualizer
self.httpd = None
self.server_port = 8765
self.server_thread = None
```

#### New `_start_server()` Method
- Starts a simple HTTP server in the background
- Serves files from the parent directory (where HTML files are located)
- Automatically finds an available port if 8765 is in use
- Runs as a daemon thread so it doesn't block the GUI

#### Updated `open_visualizer()` Method
- Now calls `_start_server()` to ensure server is running
- Uses `http://localhost:{port}/sequence_transformation_viz.html?initial=...&target=...` instead of `file://` URLs
- Properly passes query parameters that the browser will respect

## How It Works

1. When the user clicks "🧬 Open Visualizer", the GUI:
   - Starts an HTTP server (if not already running)
   - Constructs a URL with query parameters: `http://localhost:8765/sequence_transformation_viz.html?initial=ACGT&target=TGCA`
   - Opens the URL in the default browser

2. The browser:
   - Makes a standard HTTP request to localhost
   - Receives the HTML file
   - The JavaScript in the HTML reads the query parameters using `URLSearchParams(window.location.search)`
   - Displays the initial and target sequences

## Benefits

1. **Query Parameters Work**: Standard HTTP URLs properly support query parameters
2. **No Security Issues**: Browsers don't restrict query parameters on HTTP URLs
3. **Automatic Port Selection**: If port 8765 is busy, tries ports 8766-8774
4. **Minimal Overhead**: Lightweight built-in Python HTTP server
5. **Background Operation**: Server runs in a daemon thread and doesn't block the GUI

## Testing

You can test the server independently using:

```bash
python test_server.py
```

This will:
- Start a server on port 8765
- Open the visualizer with test sequences
- Verify that query parameters work correctly

## Usage

No changes required from the user's perspective:
1. Start the GUI: `python -m rl_model.gui`
2. Start training
3. Click "🧬 Open Visualizer"
4. The browser will open with the sequences properly loaded

The status label will show: `Visualizer opened at localhost:8765`
