# 🧬 Quick Start Guide: RL Model + Visualizer Integration

## What's New?

Your RL model GUI now integrates with a beautiful 3D DNA sequence visualizer! After training completes, click the "🧬 Open Visualizer" button to see an animated transformation from your initial sequence to the final trained sequence.

## Quick Test

### Test 1: Run the Visualizer with Custom Sequences
```bash
python test_visualizer_params.py
```
This will open your browser showing a transformation between two predefined sequences.

### Test 2: Run the Full Integration
```bash
python test_gui_integration.py
```
This will:
1. Launch the training GUI
2. Click "Start Training" to run a short training session
3. After training, click "🧬 Open Visualizer"
4. Watch your sequences transform in 3D!

## Files Changed

### 1. `rl_model/gui.py`
**Added:**
- Import statements: `webbrowser`, `os`, `urllib.parse`
- `viz_btn`: Button to open visualizer (row 5)
- `initial_sequence`: Variable to store initial sequence
- `open_visualizer()`: Method to launch browser with sequences

**Modified:**
- Row numbers shifted for objectives frame (now row 6)
- Preset combo shifted (now row 7)
- `_on_done()`: Enables visualizer button after training

### 2. `sequence_transformation_viz.html`
**Modified:**
- `init()` function now:
  - Reads URL query parameters (`initial` and `target`)
  - Validates sequences (A, C, G, T only)
  - Uses URL sequences if valid, otherwise generates random

### 3. New Files
- `test_gui_integration.py`: Test script for full integration
- `test_visualizer_params.py`: Test script for URL parameters
- `INTEGRATION_README.md`: Detailed documentation
- `QUICKSTART.md`: This file

## Usage Flow

```
┌─────────────────────────────────┐
│   1. Launch GUI                 │
│   python test_gui_integration.py│
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│   2. Configure Training         │
│   - Select objectives           │
│   - Use preset or custom        │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│   3. Start Training             │
│   - Initial sequence displayed  │
│   - Progress bar shows status   │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│   4. Training Completes         │
│   - Final sequence displayed    │
│   - Visualizer button enabled   │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│   5. Click "🧬 Open Visualizer" │
│   - Browser opens automatically │
│   - Shows 3D transformation     │
└─────────────────────────────────┘
```

## Visualizer Controls

Once the visualizer opens:

| Button | Action |
|--------|--------|
| ▶️ Start Transformation | Auto-transform from initial to target |
| ⏭️ Next Edit | Step through one edit at a time |
| ⏸️ Pause | Pause automatic transformation |
| 🔄 Reset | Reset to initial sequence |
| 🎲 Random Sequences | Generate new random sequences |

## Features

### 3D Visualization
- **Color-coded bases**: A (red), C (blue), G (green), T (yellow)
- **Three rows**: Initial (top), Current (middle), Target (bottom)
- **Connection lines**: Show matching and changed bases
- **Bloom effects**: Beautiful glowing effects
- **Rotation**: Gentle rotation animation

### Stats Panel
- **Edit Step**: Current step / Max edits
- **Similarity**: Percentage match to target
- **Changes Made**: Total edits applied
- **Remaining**: Bases still different from target
- **Progress Bar**: Visual progress indicator

### Sequence Display
- **Color-coded bases**: Each base has its own color
- **Highlight changes**: Recent edits pulse/glow
- **Three sequences**: Initial, Current, Target
- **Wrapped display**: Long sequences wrap nicely

## URL Format

The visualizer uses this URL format:
```
file:///path/to/sequence_transformation_viz.html?initial=ACGTACGT...&target=TGCATGCA...
```

You can manually create URLs like this to visualize any sequences!

## Tips

1. **Short Training**: For quick demos, the default 50 episodes is good
2. **Watch Progress**: The progress bar in the GUI shows training status
3. **Multiple Runs**: You can run training multiple times and compare
4. **Manual Testing**: Use `test_visualizer_params.py` to test specific sequences
5. **Browser Compatibility**: Works best in Chrome, Firefox, Safari, or Edge

## Troubleshooting

### Visualizer shows random sequences
- Check that the URL has `?initial=...&target=...` parameters
- Verify sequences contain only A, C, G, T characters

### Button is disabled
- Make sure training has completed successfully
- Check that the status shows "Training finished"

### Browser doesn't open
- Check your default browser is set correctly
- Try manually copying the URL from the GUI status message
- On some systems, file:// URLs may need special permissions

### HTML file not found
- Verify `sequence_transformation_viz.html` is in the project root
- Check it's not in a subdirectory

## Next Steps

For detailed documentation, see:
- `INTEGRATION_README.md`: Complete technical details
- `rl_model/README.md`: Original RL model documentation

Enjoy your 3D DNA sequence visualizations! 🧬✨
