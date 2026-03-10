"""
generate_pixel_name.py
Generates an animated GitHub contribution-style pixel name SVG spelling "YASH  B."
Each green block pulses with a glow animation — staggered per column for wave effect.
"""

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

TEXT = "YASH  B."

CELL   = 18
GAP    = 4
RADIUS = 3
ROWS   = 7

COLOR_ON  = "#39d353"
COLOR_OFF = "#161b22"


def build_svg(text):
    columns = []
    for ch in text:
        glyph = PIXEL_FONT.get(ch, PIXEL_FONT[" "])
        columns.append(glyph)

    total_cols = sum(len(col[0]) for col in columns) + (len(columns) - 1)
    width  = total_cols * (CELL + GAP) + GAP
    height = ROWS * (CELL + GAP) + GAP + 20

    # Build animation keyframes — one per column index for wave effect
    animations = []
    col_index = 0
    rects = []
    x_offset = GAP

    for li, glyph in enumerate(columns):
        cols_in_letter = len(glyph[0])
        for col in range(cols_in_letter):
            delay = round((col_index * 0.08) % 2.0, 2)  # stagger delay per column
            anim_id = f"glow{col_index}"
            animations.append(f"""
    @keyframes {anim_id} {{
      0%   {{ filter: brightness(1);   opacity: 1; }}
      50%  {{ filter: brightness(1.9) drop-shadow(0 0 6px #39d353); opacity: 0.85; }}
      100% {{ filter: brightness(1);   opacity: 1; }}
    }}""")

            for row in range(ROWS):
                val = glyph[row][col]
                x = x_offset + col * (CELL + GAP)
                y = GAP + row * (CELL + GAP)
                if val:
                    rects.append(
                        f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" '
                        f'rx="{RADIUS}" ry="{RADIUS}" fill="{COLOR_ON}" '
                        f'style="animation: {anim_id} 2s ease-in-out {delay}s infinite;"/>'
                    )
                else:
                    rects.append(
                        f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" '
                        f'rx="{RADIUS}" ry="{RADIUS}" fill="{COLOR_OFF}" opacity="0.15"/>'
                    )
            col_index += 1

        x_offset += cols_in_letter * (CELL + GAP) + (CELL + GAP)

    animations_str = "\n".join(animations)
    rects_str = "\n  ".join(rects)

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <style>
    {animations_str}
  </style>
  <rect width="{width}" height="{height}" rx="10" ry="10" fill="#0d1117"/>
  {rects_str}
</svg>'''
    return svg


if __name__ == "__main__":
    import os
    os.makedirs("output", exist_ok=True)
    svg_content = build_svg(TEXT)
    with open("output/pixel-name.svg", "w") as f:
        f.write(svg_content)
    print("✅ Animated pixel-name.svg generated in output/")
