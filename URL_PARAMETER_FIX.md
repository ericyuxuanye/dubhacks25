# URL Parameter Fix for file:// URLs

## Problem
The GUI was opening the visualizer, but the URL in the browser showed:
```
file:///path/to/sequence_transformation_viz.html
```

Instead of:
```
file:///path/to/sequence_transformation_viz.html?initial=ACGT...&target=TGCA...
```

The query parameters were being stripped by `webbrowser.open()` on macOS.

## Root Cause
On macOS (and some other systems), when `webbrowser.open()` opens a `file://` URL with query parameters (`?key=value`), some browsers strip the query string before loading the page.

## Solution
Use **hash fragments** (`#`) instead of query strings (`?`) for passing parameters.

### Changes Made

**1. GUI (`rl_model/gui.py`)**
```python
# Before:
file_url = f"file://{html_path}?{params}"

# After:
file_url = f"file://{html_path}#{params}"
```

**2. HTML (`sequence_transformation_viz.html`)**
```javascript
// Now checks hash FIRST, then query string as fallback
if (window.location.hash) {
    const hashParams = new URLSearchParams(window.location.hash.substring(1));
    initialParam = hashParams.get('initial');
    targetParam = hashParams.get('target');
}
```

## Why This Works

Hash fragments (#) are:
- ✅ More reliable with file:// URLs
- ✅ Not stripped by browsers
- ✅ Work consistently across platforms
- ✅ Still accessible via JavaScript

Query strings (?) are:
- ❌ Sometimes stripped by webbrowser.open()
- ❌ May have security restrictions on file:// URLs
- ❌ Less reliable for local files

## Testing

1. Run the GUI:
   ```bash
   python -m rl_model.gui
   ```

2. Click "Start Training" and wait

3. Click "🧬 Open Visualizer"

4. Check the URL in browser - should now show:
   ```
   file:///path/to/viz.html#initial=ACGTACGT...&target=TGCATGCA...
   ```

5. Open browser console (F12) and check for:
   ```
   ✓ Loaded sequences from URL parameters
     Initial: ACGTACGT...
     Target: TGCATGCA...
   ```

## Alternative Solutions (if this doesn't work)

If hash fragments still don't work, we have these options:

### Option 1: Local Web Server
```python
import http.server
import threading

# Start local server
server = http.server.HTTPServer(('localhost', 8000), handler)
threading.Thread(target=server.serve_forever, daemon=True).start()

# Open with http://
webbrowser.open(f'http://localhost:8000/viz.html?{params}')
```

### Option 2: Temporary Data File
```python
import json
import tempfile

# Write data to temp file
data = {'initial': initial_seq, 'target': final_seq}
temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
json.dump(data, temp_file)
temp_file.close()

# HTML reads from data file
```

### Option 3: localStorage
```python
# Use browser's localStorage to pass data between pages
# Requires opening a loader page first that sets localStorage
```

## Status
✅ Fixed - Now using hash fragments for reliable parameter passing
