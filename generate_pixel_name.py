"""
generate_pixel_name.py
Generates a GitHub contribution-style pixel name SVG spelling "YASH  B."
Commit output to: output/pixel-name.svg
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

CELL   = 18   # px size of each square
GAP    = 4    # px gap between squares
RADIUS = 3    # corner radius

# GitHub contribution green palette
COLORS = {
    0: "#161b22",   # dark background (empty cell)
    1: "#39d353",   # bright green (filled cell)
}

ROWS = 7


def build_svg(text):
    columns = []
    for ch in text:
        glyph = PIXEL_FONT.get(ch, PIXEL_FONT[" "])
        columns.append(glyph)

    # Calculate total width
    total_cols = sum(len(col[0]) for col in columns) + (len(columns) - 1)  # 1 gap col between letters
    width  = total_cols * (CELL + GAP) + GAP
    height = ROWS * (CELL + GAP) + GAP + 20  # +20 for padding

    rects = []
    x_offset = GAP

    for li, glyph in enumerate(columns):
        cols_in_letter = len(glyph[0])
        for row in range(ROWS):
            for col in range(cols_in_letter):
                val = glyph[row][col]
                x = x_offset + col * (CELL + GAP)
                y = GAP + row * (CELL + GAP)
                color = COLORS[val]
                opacity = "1" if val else "0.15"
                rects.append(
                    f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" '
                    f'rx="{RADIUS}" ry="{RADIUS}" fill="{color}" opacity="{opacity}"/>'
                )
        x_offset += cols_in_letter * (CELL + GAP) + (CELL + GAP)  # letter gap

    rects_str = "\n  ".join(rects)

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
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
    print("✅ pixel-name.svg generated in output/")
