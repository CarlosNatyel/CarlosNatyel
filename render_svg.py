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
    def _column_labels():
    """Retorna os números das colunas no topo do SVG."""
    parts = []
    for c in range(COLS):
        cx = PADDING + c * CELL + CELL // 2
        cy = PADDING - 6
        parts.append(
            f'<text x="{cx}" y="{cy}" font-family="Arial, sans-serif" '
            f'font-size="14" font-weight="bold" fill="#FFFFFF" '
            f'text-anchor="middle">{c + 1}</text>'
        )
    return parts


def render_svg(board, last_move=None):
    """Gera o SVG completo do tabuleiro."""
    # Reserva um pequeno espaço no topo para os números de coluna
    top_offset = 20
    total_height = HEIGHT + top_offset

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{WIDTH}" height="{total_height}" '
        f'viewBox="0 0 {WIDTH} {total_height}">',
        '<defs>',
        '  <radialGradient id="redGrad" cx="35%" cy="35%" r="75%">',
        '    <stop offset="0%" stop-color="#FF6B6B"/>',
        '    <stop offset="60%" stop-color="#E53935"/>',
        '    <stop offset="100%" stop-color="#B71C1C"/>',
        '  </radialGradient>',
        '  <radialGradient id="yellowGrad" cx="35%" cy="35%" r="75%">',
        '    <stop offset="0%" stop-color="#FFF59D"/>',
        '    <stop offset="60%" stop-color="#FDD835"/>',
        '    <stop offset="100%" stop-color="#F9A825"/>',
        '  </radialGradient>',
        '</defs>',
        # Fundo azul
        f'<rect x="0" y="{top_offset}" width="{WIDTH}" height="{HEIGHT}" '
        f'fill="#1565C0" rx="18"/>',
        f'<rect x="2" y="{top_offset + 2}" width="{WIDTH - 4}" height="{HEIGHT - 4}" '
        f'fill="none" stroke="#0D47A1" stroke-width="3" rx="16"/>',
    ]

    # Números das colunas
    for c in range(COLS):
        cx = PADDING + c * CELL + CELL // 2
        cy = top_offset - 6
        parts.append(
            f'<text x="{cx}" y="{cy}" font-family="Arial, sans-serif" '
            f'font-size="14" font-weight="bold" fill="#1565C0" '
            f'text-anchor="middle">{c + 1}</text>'
        )

    radius = CELL // 2 - 6

    for r in range(ROWS):
        for c in range(COLS):
            cx = PADDING + c * CELL + CELL // 2
            cy = PADDING + r * CELL + CELL // 2 + top_offset
            parts.append(_piece_svg(cx, cy, radius, board[r][c]))

    # Destaca a última peça jogada com um anel branco
    if last_move and board[last_move["row"] - 1][last_move["column"] - 1] != EMPTY:
        cx = PADDING + (last_move["column"] - 1) * CELL + CELL // 2
        cy = PADDING + (last_move["row"] - 1) * CELL + CELL // 2 + top_offset
        parts.append(
            f'<circle cx="{cx}" cy="{cy}" r="{radius + 3}" fill="none" '
            f'stroke="#FFFFFF" stroke-width="3" opacity="0.85"/>'
        )

    parts.append('</svg>')
    return "\n".join(parts)
