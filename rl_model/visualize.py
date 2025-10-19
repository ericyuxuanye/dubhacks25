"""3D visualization utilities for sequences and edit histories.

This module provides a simple, interactive 3D helix renderer using Plotly.
It is intentionally lightweight and meant for demo/visualization purposes — it
does not attempt to create atomistic or biophysically accurate DNA models.

Install requirements:

    pip install plotly

Usage examples:

    # show a single sequence (interactive HTML will be written)
    python -m rl_model.visualize --sequence ACGTACGTACGT --out seq.html

    # animate an edit history
    python -m rl_model.visualize --sequence AAAAAAAAAA --edits "0:G,3:C,5:T" --out edits.html

    # if you have an env.history list like [(pos, base), ...] you can create
    # a CSV or simple string and pass via --edits

The animation works by creating a helix path and coloring bases by type.
Each frame represents the sequence after each successive edit.
"""

from __future__ import annotations

import argparse
import math
from typing import List, Tuple

try:
    import plotly.graph_objects as go
except Exception as e:
    raise ImportError("plotly is required for visualization. Install with 'pip install plotly'") from e

# base color map
BASE_COLORS = {
    "A": "#1f77b4",
    "C": "#ff7f0e",
    "G": "#2ca02c",
    "T": "#d62728",
    "N": "#7f7f7f",
}


def sequence_to_coords(seq: str, rise=3.4, bases_per_turn=10.5, radius=10.0):
    """Return (x,y,z) coords for each base along a simple helical path."""
    xs, ys, zs = [], [], []
    for i in range(len(seq)):
        angle = 2 * math.pi * (i / bases_per_turn)
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        z = i * rise
        xs.append(x)
        ys.append(y)
        zs.append(z)
    return xs, ys, zs


def build_snapshots(initial_seq: str, edits: List[Tuple[int, str]]):
    """Return a list of sequence snapshots starting with initial_seq and
    applying edits sequentially.

    edits: list of (pos, base) tuples.
    """
    snapshots = [list(initial_seq)]
    cur = list(initial_seq)
    for pos, base in edits:
        pos = int(pos)
        cur[pos] = base
        snapshots.append(list(cur.copy()))
    return ["".join(s) for s in snapshots]


def plot_sequence_3d(seq: str, out_html: str = "sequence.html"):
    xs, ys, zs = sequence_to_coords(seq)
    colors = [BASE_COLORS.get(b.upper(), BASE_COLORS["N"]) for b in seq]

    fig = go.Figure()
    # backbone line
    fig.add_trace(go.Scatter3d(x=xs, y=ys, z=zs, mode="lines", line=dict(color="#444444", width=4), name="backbone"))
    # bases
    fig.add_trace(go.Scatter3d(x=xs, y=ys, z=zs, mode="markers+text", marker=dict(size=8, color=colors), text=list(seq), textposition="top center", name="bases"))

    fig.update_layout(scene=dict(xaxis=dict(visible=False), yaxis=dict(visible=False), zaxis=dict(title="base index")), title="Sequence 3D (helix-like)")
    fig.write_html(out_html, include_plotlyjs="cdn")
    print(f"Wrote {out_html}")


def animate_edit_history(initial_seq: str, edits: List[Tuple[int, str]], out_html: str = "edits.html"):
    snapshots = build_snapshots(initial_seq, edits)
    xs, ys, zs = sequence_to_coords(snapshots[0])

    # Create base frame (initial)
    init_colors = [BASE_COLORS.get(b.upper(), BASE_COLORS["N"]) for b in snapshots[0]]
    data = [
        go.Scatter3d(x=xs, y=ys, z=zs, mode="lines", line=dict(color="#444444", width=4), name="backbone"),
        go.Scatter3d(x=xs, y=ys, z=zs, mode="markers+text", marker=dict(size=8, color=init_colors), text=list(snapshots[0]), textposition="top center", name="bases"),
    ]

    frames = []
    for idx, snap in enumerate(snapshots):
        colors = [BASE_COLORS.get(b.upper(), BASE_COLORS["N"]) for b in snap]
        frames.append(go.Frame(data=[
            go.Scatter3d(x=xs, y=ys, z=zs, mode="lines", line=dict(color="#444444", width=4)),
            go.Scatter3d(x=xs, y=ys, z=zs, mode="markers+text", marker=dict(size=8, color=colors), text=list(snap), textposition="top center"),
        ], name=f"frame{idx}"))

    fig = go.Figure(data=data, frames=frames)

    # Animation controls
    fig.update_layout(
        updatemenus=[
            dict(
                type="buttons",
                showactive=False,
                y=1,
                x=1.05,
                xanchor="right",
                yanchor="top",
                buttons=[
                    dict(label="Play", method="animate", args=[None, dict(frame=dict(duration=600, redraw=True), fromcurrent=True, mode="immediate")]),
                    dict(label="Pause", method="animate", args=[[None], dict(frame=dict(duration=0, redraw=False), mode="immediate")]),
                ],
            )
        ]
    )

    fig.update_layout(scene=dict(xaxis=dict(visible=False), yaxis=dict(visible=False), zaxis=dict(title="base index")), title="Edit history animation")
    fig.write_html(out_html, include_plotlyjs="cdn")
    print(f"Wrote {out_html}")


def parse_edits_string(s: str) -> List[Tuple[int, str]]:
    """Parse a simple edits string like '0:G,3:C,5:T' into [(0,'G'), (3,'C'), (5,'T')]."""
    if not s:
        return []
    parts = [p.strip() for p in s.split(",") if p.strip()]
    edits = []
    for part in parts:
        if ":" in part:
            pos, base = part.split(":", 1)
            edits.append((int(pos), base.strip().upper()))
    return edits


def _cli():
    p = argparse.ArgumentParser(description="3D visualize sequences and edit histories (demo)")
    p.add_argument("--sequence", help="Initial sequence (required for edits or single view)")
    p.add_argument("--edits", help="Comma-separated edits like '0:G,3:C,5:T' (optional)")
    p.add_argument("--out", default="sequence.html", help="Output HTML file")
    args = p.parse_args()

    if not args.sequence:
        p.error("--sequence is required")

    if args.edits:
        edits = parse_edits_string(args.edits)
        animate_edit_history(args.sequence, edits, out_html=args.out)
    else:
        plot_sequence_3d(args.sequence, out_html=args.out)


if __name__ == "__main__":
    _cli()
