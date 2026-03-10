"""
generate_pixel_name.py
Gitartwork-style SVG spelling "YASH B."
- 4 GitHub green shades per block
- Left-to-right wave fade-in
- Loops forever: fade in → hold → fade out → repeat
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

# GitHub contribution graph green palette
GREENS = ["#0e4429", "#006d32", "#26a641", "#39d353"]
EMPTY  = "#161b22"

# Loop timing (seconds)
FADE_IN_DUR  = 0.6   # each block fade-in duration
WAVE_SPREAD  = 0.07  # stagger per column
HOLD_TIME    = 2.5   # how long name stays fully visible
FADE_OUT_DUR = 0.8   # fade out duration


def build_svg(text):
    columns = []
    for ch in text:
        glyph = PIXEL_FONT.get(ch, PIXEL_FONT[" "])
        columns.append(glyph)

    total_cols = sum(len(col[0]) for col in columns) + (len(columns) - 1)
    num_cols   = total_cols
    max_delay  = round((num_cols - 1) * WAVE_SPREAD, 2)

    width  = total_cols * (CELL + GAP) + GAP
    height = ROWS * (CELL + GAP) + GAP + 10

    styles = []
    rects  = []

    x_offset  = GAP
    col_index = 0

    for li, glyph in enumerate(columns):
        cols_in_letter = len(glyph[0])

        for col in range(cols_in_letter):
            delay = round(col_index * WAVE_SPREAD, 2)

            # Total loop duration = delay + fade_in + hold + fade_out + pause before restart
            loop_dur = round(delay + FADE_IN_DUR + HOLD_TIME + FADE_OUT_DUR + 0.5, 2)

            # Keyframe percentages
            p_start    = 0
            p_fadein   = round((delay + FADE_IN_DUR) / loop_dur * 100, 1)
            p_hold_end = round((delay + FADE_IN_DUR + HOLD_TIME) / loop_dur * 100, 1)
            p_fadeout  = round((delay + FADE_IN_DUR + HOLD_TIME + FADE_OUT_DUR) / loop_dur * 100, 1)
            p_end      = 100

            anim_name = f"loop{col_index}"
            styles.append(f"""
  @keyframes {anim_name} {{
    {p_start}%   {{ opacity: 0; transform: scale(0.3); }}
    {p_fadein}%  {{ opacity: 1; transform: scale(1.0); }}
    {p_hold_end}% {{ opacity: 1; transform: scale(1.0); }}
    {p_fadeout}% {{ opacity: 0; transform: scale(0.3); }}
    {p_end}%     {{ opacity: 0; transform: scale(0.3); }}
  }}""")

            for row in range(ROWS):
                val = glyph[row][col]
                x = x_offset + col * (CELL + GAP)
                y = GAP + row * (CELL + GAP)

                if val:
                    color = random.choice(GREENS)
                    rects.append(
                        f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" '
                        f'rx="{RADIUS}" ry="{RADIUS}" fill="{color}" '
                        f'style="opacity:0; animation: {anim_name} {loop_dur}s ease-in-out 0s infinite;"/>'
                    )
                else:
                    rects.append(
                        f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" '
                        f'rx="{RADIUS}" ry="{RADIUS}" fill="{EMPTY}" opacity="0.4"/>'
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
    print("✅ Looping gitartwork-style pixel-name.svg generated in output/")
