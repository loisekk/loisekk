"""
generate_pixel_name.py
Particles scattered like stars across the canvas,
then fly together and assemble into "YASH B.",
hold, then scatter back out. Loops forever.
"""

import random
import os

random.seed(42)

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
CELL   = 20
GAP    = 5
RADIUS = 3
ROWS   = 7

GREENS = ["#0e4429", "#006d32", "#26a641", "#39d353"]
EMPTY  = "#161b22"

# Timing
SCATTER_DUR = 1.5   # scattered phase before flying in
FLY_DUR     = 1.2   # fly-in duration
HOLD_DUR    = 2.8   # hold assembled
SCATTER_OUT = 1.2   # scatter back out
PAUSE       = 0.5   # pause before loop restart
TOTAL       = SCATTER_DUR + FLY_DUR + HOLD_DUR + SCATTER_OUT + PAUSE


def build_svg(text):
    columns = []
    for ch in text:
        glyph = PIXEL_FONT.get(ch, PIXEL_FONT[" "])
        columns.append(glyph)

    total_cols = sum(len(col[0]) for col in columns) + (len(columns) - 1)
    width  = total_cols * (CELL + GAP) + GAP
    height = ROWS * (CELL + GAP) + GAP + 10

    # Collect all ON block final positions
    blocks = []
    x_offset = GAP
    for li, glyph in enumerate(columns):
        cols_in_letter = len(glyph[0])
        for col in range(cols_in_letter):
            for row in range(ROWS):
                if glyph[row][col]:
                    fx = x_offset + col * (CELL + GAP)
                    fy = GAP + row * (CELL + GAP)
                    blocks.append((fx, fy))
        x_offset += cols_in_letter * (CELL + GAP) + (CELL + GAP)

    styles = []
    rects  = []

    # Background star particles (decorative, always scattered)
    for si in range(30):
        sx = random.randint(5, width - 10)
        sy = random.randint(5, height - 10)
        sr = round(random.uniform(1.0, 2.2), 1)
        sd = round(random.uniform(0, 3.0), 2)
        styles.append(f"""
  @keyframes star{si} {{
    0%   {{ opacity: 0.0; }}
    50%  {{ opacity: {round(random.uniform(0.3, 0.7), 1)}; }}
    100% {{ opacity: 0.0; }}
  }}""")
        rects.append(
            f'<circle cx="{sx}" cy="{sy}" r="{sr}" fill="#26a641" '
            f'style="animation: star{si} {round(random.uniform(2.0, 4.5), 1)}s ease-in-out {sd}s infinite;"/>'
        )

    # Main blocks — scatter → assemble → scatter
    for i, (fx, fy) in enumerate(blocks):
        # Random scattered position
        rx = random.randint(CELL, width  - CELL * 2)
        ry = random.randint(CELL, height - CELL * 2)

        color    = random.choice(GREENS)
        fly_delay = round(SCATTER_DUR + random.uniform(0, 0.35), 2)
        fly_dur   = round(random.uniform(FLY_DUR * 0.75, FLY_DUR), 2)
        out_start = fly_delay + fly_dur + HOLD_DUR
        out_dur   = round(random.uniform(SCATTER_OUT * 0.7, SCATTER_OUT), 2)

        # Random exit position (different from entry)
        ex = random.randint(CELL, width  - CELL * 2)
        ey = random.randint(CELL, height - CELL * 2)

        # Convert times to keyframe percentages
        t = TOTAL
        p0  = 0
        p1  = round(SCATTER_DUR / t * 100, 1)
        p2  = round(fly_delay / t * 100, 1)
        p3  = round((fly_delay + fly_dur) / t * 100, 1)
        p4  = round((fly_delay + fly_dur + HOLD_DUR * 0.85) / t * 100, 1)
        p5  = round(out_start / t * 100, 1)
        p6  = round((out_start + out_dur) / t * 100, 1)
        p7  = 100

        anim = f"blk{i}"
        styles.append(f"""
  @keyframes {anim} {{
    {p0}%  {{ transform: translate({rx-fx}px,{ry-fy}px); opacity:0.9; filter:blur(0px); }}
    {p1}%  {{ transform: translate({rx-fx}px,{ry-fy}px); opacity:0.9; filter:blur(0px); }}
    {p2}%  {{ transform: translate({rx-fx}px,{ry-fy}px); opacity:0.6; filter:blur(1px); }}
    {p3}%  {{ transform: translate(0px,0px);              opacity:1;   filter:blur(0px); }}
    {p4}%  {{ transform: translate(0px,0px);              opacity:1;   filter:blur(0px); }}
    {p5}%  {{ transform: translate(0px,0px);              opacity:1;   filter:blur(0px); }}
    {p6}%  {{ transform: translate({ex-fx}px,{ey-fy}px); opacity:0;   filter:blur(2px); }}
    {p7}%  {{ transform: translate({rx-fx}px,{ry-fy}px); opacity:0.9; filter:blur(0px); }}
  }}""")

        rects.append(
            f'<rect x="{fx}" y="{fy}" width="{CELL}" height="{CELL}" '
            f'rx="{RADIUS}" ry="{RADIUS}" fill="{color}" '
            f'style="animation: {anim} {t}s ease-in-out 0s infinite;"/>'
        )

    # Empty cell grid (always visible, faint)
    x_offset = GAP
    for li, glyph in enumerate(columns):
        cols_in_letter = len(glyph[0])
        for col in range(cols_in_letter):
            for row in range(ROWS):
                if not glyph[row][col]:
                    x = x_offset + col * (CELL + GAP)
                    y = GAP + row * (CELL + GAP)
                    rects.insert(0,
                        f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" '
                        f'rx="{RADIUS}" ry="{RADIUS}" fill="{EMPTY}" opacity="0.3"/>'
                    )
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
    print("✅ Star-scatter-assemble pixel-name.svg generated!")
