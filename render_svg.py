from connect4 import ROWS, COLS, EMPTY, RED, YELLOW

CELL = 60
PADDING = 15
WIDTH = COLS * CELL + 2 * PADDING
HEIGHT = ROWS * CELL + 2 * PADDING


def _piece_svg(cx, cy, radius, kind):
    """Retorna o SVG de uma peça (ou buraco vazio)."""
    if kind == EMPTY:
        return (
            f'<circle cx="{cx}" cy="{cy}" r="{radius}" fill="#0D47A1"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{radius}" fill="none" '
            f'stroke="#0A3D91" stroke-width="2"/>'
        )

    if kind == RED:
        grad = "redGrad"
        shadow = "#7F0000"
    else:
        grad = "yellowGrad"
        shadow = "#B8860B"

    return (
        f'<circle cx="{cx}" cy="{cy + 3}" r="{radius}" fill="{shadow}"/>'
        f'<circle cx="{cx}" cy="{cy}" r="{radius}" fill="url(#{grad})"/>'
        f'<ellipse cx="{cx - radius * 0.3}" cy="{cy - radius * 0.35}" '
        f'rx="{radius * 0.35}" ry="{radius * 0.22}" fill="white" opacity="0.45"/>'
    )
