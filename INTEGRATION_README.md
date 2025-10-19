# RL Model and Visualizer Integration

This document describes how the RL model GUI is integrated with the 3D DNA sequence transformation visualizer.

## Overview

The integration allows the GUI to automatically open the HTML visualizer with the initial and final gene sequences from the training process. The visualizer displays a beautiful 3D animation showing the transformation from the initial sequence to the target (final) sequence.

## How It Works

### 1. GUI Changes (`rl_model/gui.py`)

The GUI has been enhanced with:

- **Visualizer Button**: A new "🧬 Open Visualizer" button that appears after training completes
- **Sequence Storage**: The initial sequence is stored when training starts
- **URL Parameter Generation**: When the button is clicked, the GUI:
  - Retrieves the initial sequence (stored at training start)
  - Retrieves the final sequence (from the environment after training)
  - Encodes both sequences as URL query parameters
  - Opens the HTML file in the default browser with these parameters

### 2. HTML Visualizer Changes (`sequence_transformation_viz.html`)

The visualizer has been enhanced to:

- **Read URL Parameters**: On initialization, check for `initial` and `target` query parameters
- **Validate Sequences**: Ensure the sequences are valid (contain only A, C, G, T)
- **Use Provided Sequences**: If valid sequences are found in the URL, use them instead of generating random ones
- **Fallback to Random**: If no valid sequences are provided, generate random ones as before

### 3. Integration Flow

```
User clicks "Start Training"
    ↓
GUI creates environment with random initial sequence
    ↓
Initial sequence is stored in GUI
    ↓
Training runs in background thread
    ↓
Training completes with final sequence
    ↓
"Open Visualizer" button becomes enabled
    ↓
User clicks "Open Visualizer"
    ↓
GUI builds URL: file://path/to/sequence_transformation_viz.html?initial=ACGT...&target=TGCA...
    ↓
Browser opens with visualizer
    ↓
Visualizer reads query parameters and displays sequences
    ↓
User can interact with the 3D visualization
```

## Usage

### Running the GUI

```bash
python test_gui_integration.py
```

Or from the rl_model directory:

```bash
python -m rl_model.gui
```

### Testing the Visualizer with Custom Sequences

You can test the visualizer with specific sequences:

```bash
python test_visualizer_params.py
```

Or manually open with URL parameters:
```
file:///path/to/sequence_transformation_viz.html?initial=ACGTACGTACGTACGTACGT&target=TGCATGCATGCATGCATGCA
```

### Using the Integrated System

1. Launch the GUI
2. (Optional) Select objectives using checkboxes or presets
3. Click "Start Training"
4. Wait for training to complete
5. Click "🧬 Open Visualizer" button
6. The visualizer opens in your browser showing the transformation
7. Use the controls to:
   - ▶️ Start Transformation: Automatically transform from initial to target
   - ⏭️ Next Edit: Step through one edit at a time
   - ⏸️ Pause: Pause the automatic transformation
   - 🔄 Reset: Reset to initial sequence
   - 🎲 Random Sequences: Generate new random sequences (overrides URL params)

## Technical Details

### URL Parameter Format

The visualizer expects two query parameters:
- `initial`: The starting DNA sequence (e.g., `ACGTACGTACGTACGTACGT`)
- `target`: The target DNA sequence (e.g., `TGCATGCATGCATGCATGCA`)

Both sequences must:
- Contain only the characters A, C, G, T
- Be non-empty strings
- Match in length (though the visualizer is flexible)

### Sequence Validation

The HTML file validates sequences using a regular expression:
```javascript
const isValidSequence = (seq) => {
    return seq && seq.length > 0 && /^[ACGT]+$/.test(seq);
};
```

### File Path Resolution

The GUI automatically finds the HTML file by:
1. Getting the directory of the `gui.py` file (`rl_model/`)
2. Going up one directory to the parent directory
3. Looking for `sequence_transformation_viz.html` in the parent directory

This works as long as the directory structure is maintained:
```
project_root/
├── sequence_transformation_viz.html
└── rl_model/
    └── gui.py
```

## Troubleshooting

### Visualizer Opens but Shows Random Sequences

- Check that the URL contains the query parameters: `?initial=...&target=...`
- Verify the sequences contain only A, C, G, T characters
- Check the browser console for any errors

### "Visualizer HTML not found" Error

- Ensure `sequence_transformation_viz.html` is in the parent directory of `rl_model/`
- Check the file path in the error message
- Verify file permissions

### Browser Doesn't Open

- Check your default browser settings
- Try manually opening the URL shown in the GUI status label
- On some systems, you may need to use a local web server instead of file:// URLs

### Query Parameters Not Working

- Some browsers may have restrictions on accessing query parameters from file:// URLs
- If this is the case, consider serving the HTML through a local web server:
  ```bash
  python -m http.server 8000
  ```
  Then modify the GUI to use `http://localhost:8000/sequence_transformation_viz.html?...`

## Future Enhancements

Potential improvements:
- Add intermediate steps to show the transformation sequence
- Include edit history from the RL agent
- Display objectives used during training
- Add export functionality for sequences
- Integrate reward scores and other metrics
- Support for longer sequences with scrolling/pagination
- Multiple visualization modes (2D, 3D helix, etc.)
