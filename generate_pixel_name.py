"""
generate_pixel_name.py
Generates a gitartwork-style SVG spelling "YASH B."
- Contribution graph green shades (4 levels like GitHub)
- Each block fades in with a left-to-right wave
- Clean, minimal, exactly like jasmeri/gitartwork style
"""

import random
import os

random.seed(99)

PIXEL_FONT = {
    "Y": [
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [0, 1, 0, 1, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
    ],
    "A": [
        [0, 0, 1, 0, 0],
        [0, 1, 0, 1, 0],
        [1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
    ],
    "S": [
        [0, 1, 1, 1, 1],
        [1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 0, 0, 1],
        [0, 0, 0, 0, 1],
        [1, 1, 1, 1, 0],
    ],
    "H": [
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
    ],
    " ": [
        [0, 0],
        [0, 0],
        [0, 0],
        [0, 0],
        [0, 0],
        [0, 0],
        [0, 0],
    ],
    "B": [
        [1, 1, 1, 1, 0],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 1, 1, 1, 0],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 1, 1, 1, 0],
    ],
    ".": [
        [0],
        [0],
        [0],
        [0],
        [0],
        [1],
        [1],
    ],
}

TEXT   = "YASH  B."
CELL   = 22
GAP    = 4
RADIUS = 3
ROWS   = 7

# GitHub contribution graph green palette (4 levels)
GREENS = ["#0e4429", "#006d32", "#26a641", "#39d353"]

# Empty cell color
EMPTY  = "#161b22"


def build_svg(text):
    columns = []
    for ch in text:
        glyph = PIXEL_FONT.get(ch, PIXEL_FONT[" "])
        columns.append(glyph)

    total_cols = sum(len(col[0]) for col in columns) + (len(columns) - 1)
    width  = total_cols * (CELL + GAP) + GAP
    height = ROWS * (CELL + GAP) + GAP + 10

    styles = []
    rects  = []

    x_offset  = GAP
    col_index = 0  # global column counter for wave delay

    for li, glyph in enumerate(columns):
        cols_in_letter = len(glyph[0])

        for col in range(cols_in_letter):
            # Stagger delay left → right (wave effect)
            delay = round(col_index * 0.07, 2)

            anim_name = f"fadein{col_index}"
            styles.append(f"""
  @keyframes {anim_name} {{
    0%   {{ opacity: 0; transform: scale(0.4); }}
    60%  {{ opacity: 1; transform: scale(1.1); }}
    80%  {{ transform: scale(0.95); }}
    100% {{ opacity: 1; transform: scale(1.0); }}
  }}""")

            for row in range(ROWS):
                val = glyph[row][col]
                x = x_offset + col * (CELL + GAP)
                y = GAP + row * (CELL + GAP)

                if val:
                    # Pick a random green shade per block (like real gitartwork)
                    color = random.choice(GREENS)
                    rects.append(
                        f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" '
                        f'rx="{RADIUS}" ry="{RADIUS}" fill="{color}" '
                        f'style="opacity:0; animation: {anim_name} 0.6s ease-out {delay}s forwards;"/>'
                    )
                else:
                    rects.append(
                        f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" '
                        f'rx="{RADIUS}" ry="{RADIUS}" fill="{EMPTY}" opacity="0.5"/>'
                    )

            col_index += 1

        x_offset += cols_in_letter * (CELL + GAP) + (CELL + GAP)

    styles_str = "\n".join(styles)
    rects_str  = "\n  ".join(rects)

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <style>
  {styles_str}
  </style>
  <rect width="{width}" height="{height}" rx="12" ry="12" fill="#0d1117"/>
  {rects_str}
</svg>'''


if __name__ == "__main__":
    os.makedirs("output", exist_ok=True)
    svg = build_svg(TEXT)
    with open("output/pixel-name.svg", "w") as f:
        f.write(svg)
    print("✅ Gitartwork-style pixel-name.svg generated in output/")
