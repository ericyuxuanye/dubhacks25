# Integration Architecture Diagram

## System Components

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              Tkinter GUI (gui.py)                        │  │
│  │                                                          │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │  │
│  │  │ Start Train  │  │  Progress    │  │ Open         │  │  │
│  │  │   Button     │  │    Bar       │  │ Visualizer   │  │  │
│  │  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  │  │
│  │         │                 │                 │           │  │
│  │         │                 │                 │           │  │
│  │  ┌──────▼──────────────────▼─────────────────▼────────┐ │  │
│  │  │         Training Status & Sequences                │ │  │
│  │  │  Initial seq: ACGTACGT...                         │ │  │
│  │  │  Final seq:   TGCATGCA...                         │ │  │
│  │  └────────────────────────────────────────────────────┘ │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ 1. User clicks "Open Visualizer"
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                     URL CONSTRUCTION                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  def open_visualizer():                                         │
│      initial = self.initial_sequence  # "ACGTACGT..."          │
│      final = self.env.sequence        # "TGCATGCA..."          │
│                                                                 │
│      params = urllib.parse.urlencode({                          │
│          'initial': initial,                                    │
│          'target': final                                        │
│      })                                                         │
│                                                                 │
│      url = f"file://{html_path}?{params}"                       │
│      # file:///path/viz.html?initial=ACGT&target=TGCA          │
│                                                                 │
│      webbrowser.open(url)                                       │
│                                                                 │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ 2. Browser opens URL
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      WEB BROWSER                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  URL: file:///.../sequence_transformation_viz.html?             │
│       initial=ACGTACGTACGTACGTACGT&                             │
│       target=TGCATGCATGCATGCATGCA                               │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │         HTML Page Loads (viz.html)                        │ │
│  └───────────────────────────────────────────────────────────┘ │
│                             │                                   │
│                             │ 3. JavaScript init() runs         │
│                             ▼                                   │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  const urlParams = new URLSearchParams(                   │ │
│  │      window.location.search                               │ │
│  │  );                                                        │ │
│  │  const initial = urlParams.get('initial');                │ │
│  │  const target = urlParams.get('target');                  │ │
│  │                                                            │ │
│  │  if (isValidSequence(initial) &&                          │ │
│  │      isValidSequence(target)) {                           │ │
│  │      // Use URL sequences ✓                               │ │
│  │  } else {                                                  │ │
│  │      // Generate random ✗                                 │ │
│  │  }                                                         │ │
│  └───────────────────────────────────────────────────────────┘ │
│                             │                                   │
│                             │ 4. Render visualization           │
│                             ▼                                   │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │                                                            │ │
│  │         3D DNA SEQUENCE VISUALIZATION                      │ │
│  │                                                            │ │
│  │    Initial:  A C G T A C G T ...  (Red/Blue/Green/Yellow) │ │
│  │               ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓                            │ │
│  │    Current:  A C G T A C G T ...  (Animated)              │ │
│  │               ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓                            │ │
│  │    Target:   T G C A T G C A ...  (Goal)                  │ │
│  │                                                            │ │
│  │    Stats: 0/10 edits | 0% similarity | Play/Pause/Reset   │ │
│  │                                                            │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow

```
┌─────────────┐
│  RL Model   │
│   Training  │
└──────┬──────┘
       │
       │ Generates
       │
       ├─────────────────┐
       │                 │
       ▼                 ▼
┌─────────────┐   ┌─────────────┐
│  Initial    │   │   Final     │
│  Sequence   │   │  Sequence   │
│             │   │             │
│ ACGTACGT... │   │ TGCATGCA... │
└──────┬──────┘   └──────┬──────┘
       │                 │
       └────────┬────────┘
                │
                │ Stored in GUI
                │
                ▼
        ┌───────────────┐
        │  GUI Memory   │
        │               │
        │ initial_seq   │
        │ env.sequence  │
        └───────┬───────┘
                │
                │ URL Encoding
                │
                ▼
    ┌───────────────────────┐
    │   Query Parameters    │
    │                       │
    │ ?initial=ACGT...      │
    │ &target=TGCA...       │
    └───────┬───────────────┘
            │
            │ Browser Navigation
            │
            ▼
    ┌──────────────────────┐
    │   HTML Document      │
    │                      │
    │ URLSearchParams API  │
    └───────┬──────────────┘
            │
            │ Parse & Validate
            │
            ▼
    ┌──────────────────────┐
    │  JavaScript Objects  │
    │                      │
    │  initialSequence     │
    │  targetSequence      │
    │  currentSequence     │
    └───────┬──────────────┘
            │
            │ Render
            │
            ▼
    ┌──────────────────────┐
    │   Three.js Scene     │
    │                      │
    │   3D Visualization   │
    └──────────────────────┘
```

## Component Interaction Sequence

```
User                GUI                 File System          Browser             Visualizer
 │                   │                       │                  │                   │
 │ Click "Train"     │                       │                  │                   │
 ├──────────────────>│                       │                  │                   │
 │                   │                       │                  │                   │
 │                   │ Create RL Env         │                  │                   │
 │                   │ Store initial_seq     │                  │                   │
 │                   │                       │                  │                   │
 │                   │ Train model...        │                  │                   │
 │                   │ (background thread)   │                  │                   │
 │                   │                       │                  │                   │
 │ <Progress updates>│                       │                  │                   │
 │                   │                       │                  │                   │
 │                   │ Training done         │                  │                   │
 │                   │ Enable viz button     │                  │                   │
 │ <─────────────────┤                       │                  │                   │
 │                   │                       │                  │                   │
 │ Click "Visualizer"│                       │                  │                   │
 ├──────────────────>│                       │                  │                   │
 │                   │                       │                  │                   │
 │                   │ Build URL             │                  │                   │
 │                   │ with sequences        │                  │                   │
 │                   │                       │                  │                   │
 │                   │ Check file exists     │                  │                   │
 │                   ├──────────────────────>│                  │                   │
 │                   │ <File exists: OK>     │                  │                   │
 │                   │<──────────────────────┤                  │                   │
 │                   │                       │                  │                   │
 │                   │ webbrowser.open(url)  │                  │                   │
 │                   ├─────────────────────────────────────────>│                   │
 │                   │                       │                  │                   │
 │                   │                       │                  │ Load HTML file    │
 │                   │                       │                  ├──────────────────>│
 │                   │                       │                  │                   │
 │                   │                       │                  │ Parse URL params  │
 │                   │                       │                  │ Validate sequences│
 │                   │                       │                  │                   │
 │                   │                       │                  │ Render 3D scene   │
 │                   │                       │                  │<──────────────────┤
 │                   │                       │                  │                   │
 │ <────────────────────────────────────────────Browser opens with visualization──┤
 │                   │                       │                  │                   │
 │ Interact with viz │                       │                  │                   │
 ├──────────────────────────────────────────────────────────────────────────────────>│
 │                   │                       │                  │                   │
```

## File Structure

```
dubhacks25/
│
├── sequence_transformation_viz.html    ← 3D Visualizer (modified)
│   └── Reads URL parameters
│       └── Validates DNA sequences
│           └── Renders 3D scene
│
├── rl_model/
│   ├── gui.py                          ← GUI (modified)
│   │   ├── Stores initial sequence
│   │   ├── Runs training
│   │   └── Opens visualizer with URLs
│   │
│   ├── env.py                          ← Environment (unchanged)
│   │   └── Generates sequences
│   │
│   ├── train.py                        ← Training (unchanged)
│   │   └── Trains RL agent
│   │
│   └── [other files...]
│
├── test_gui_integration.py             ← New test script
│   └── Launches GUI for testing
│
├── test_visualizer_params.py           ← New test script
│   └── Tests URL parameters directly
│
├── INTEGRATION_README.md               ← Detailed docs
├── QUICKSTART.md                       ← User guide
└── INTEGRATION_SUMMARY.md              ← Technical summary
```

## Communication Protocol

### GUI → Browser
**Method**: URL Query Parameters
**Format**: `file://path?key=value&key=value`
**Data**: 
- `initial`: Starting DNA sequence
- `target`: Goal DNA sequence

**Example**:
```
file:///Users/user/project/viz.html?initial=ACGTACGT&target=TGCATGCA
```

### Browser → Visualizer
**Method**: URLSearchParams API
**Process**:
1. Extract query string from `window.location.search`
2. Parse using `URLSearchParams`
3. Validate sequences (regex: `^[ACGT]+$`)
4. Use if valid, else generate random

**Example Code**:
```javascript
const params = new URLSearchParams(window.location.search);
const initial = params.get('initial');  // "ACGTACGT"
const target = params.get('target');    // "TGCATGCA"
```

## Security & Validation

### GUI Side
- ✓ File path validation (check exists)
- ✓ URL encoding (prevent injection)
- ✓ Error handling (graceful fallback)

### Visualizer Side
- ✓ Regex validation (`/^[ACGT]+$/`)
- ✓ Length check (non-empty)
- ✓ Fallback to random if invalid
- ✓ Console logging for debugging

## Performance Considerations

### GUI
- **Non-blocking**: Uses `webbrowser.open()` which doesn't block
- **Fast**: Simple file path resolution
- **Memory**: Stores only two short strings

### Visualizer
- **Efficient**: Three.js for hardware-accelerated 3D
- **Responsive**: ~60 FPS animation
- **Scalable**: Works with various sequence lengths

## Browser Compatibility Matrix

| Feature              | Chrome | Firefox | Safari | Edge |
|---------------------|--------|---------|--------|------|
| File URLs           | ✅     | ✅      | ✅     | ✅   |
| Query Parameters    | ✅     | ✅      | ✅     | ✅   |
| URLSearchParams     | ✅     | ✅      | ✅     | ✅   |
| Three.js            | ✅     | ✅      | ✅     | ✅   |
| Import Maps         | ✅     | ✅      | ✅     | ✅   |
| ES6 Modules         | ✅     | ✅      | ✅     | ✅   |

All modern browsers (2020+) are fully supported.
