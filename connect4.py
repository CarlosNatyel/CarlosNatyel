
import json
from pathlib import Path

ROWS = 6
COLS = 7
EMPTY = "."
RED = "R"
YELLOW = "Y"

STATE_FILE = Path("game_state.json")


def new_state():
    """Retorna um estado inicial zerado."""
    return {
        "board": [[EMPTY] * COLS for _ in range(ROWS)],
        "current_player": RED,
        "status": "in_progress",
        "winner": None,
        "move_history": [],
        "last_move": None,
    }


def load_state(path=STATE_FILE):
    if not Path(path).exists():
        state = new_state()
        save_state(state, path)
        return state
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_state(state, path=STATE_FILE):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


def is_valid_column(state, col):
    if not (0 <= col < COLS):
        return False
    return state["board"][0][col] == EMPTY


def available_columns(state):
    return [c for c in range(COLS) if state["board"][0][c] == EMPTY]


def drop_piece(state, col):
    if not is_valid_column(state, col):
        return None
    for r in range(ROWS - 1, -1, -1):
        if state["board"][r][col] == EMPTY:
            state["board"][r][col] = state["current_player"]
            return r
    return None


def check_win(board, row, col, player):
    """Verifica se o jogador venceu a partir da última peça colocada."""
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dr, dc in directions:
        count = 1
        for sign in (1, -1):
            r, c = row + sign * dr, col + sign * dc
            while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
                count += 1
                r += sign * dr
                c += sign * dc
        if count >= 4:
            return True
    return False


def is_full(board):
    return all(board[0][c] != EMPTY for c in range(COLS))


def apply_move(state, col):
    """
    Aplica uma jogada. Retorna (sucesso: bool, mensagem: str).
    `col` é 0-indexado.
    """
    if state["status"] != "in_progress":
        return False, "O jogo já foi encerrado. Abra uma issue com o título `Reset` para reiniciar."

    player = state["current_player"]
    row = drop_piece(state, col)
    if row is None:
        return False, f"A coluna {col + 1} está cheia ou é inválida."

    state["move_history"].append({
        "player": player,
        "column": col + 1,
        "row": row + 1,
    })
    state["last_move"] = {
        "player": player,
        "column": col + 1,
        "row": row + 1,
    }

    if check_win(state["board"], row, col, player):
        state["status"] = "finished"
        state["winner"] = player
        return True, f"Vitória do jogador {'🔴' if player == RED else '🟡'}!"

    if is_full(state["board"]):
        state["status"] = "finished"
        state["winner"] = "draw"
        return True, "Empate! O tabuleiro está cheio."

    state["current_player"] = YELLOW if player == RED else RED
    return True, f"Jogada registrada na coluna {col + 1}."
