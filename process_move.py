
import os
import re
import sys

from connect4 import load_state, save_state, apply_move, new_state
from generate_readme import generate


RESULT_FILE = "result.txt"


def _write_result(msg):
    with open(RESULT_FILE, "w", encoding="utf-8") as f:
        f.write(msg)


def parse_move(title, body):
    """Extrai a coluna (1-7) do texto da Issue. Retorna int ou None."""
    text = f"{title} {body}"

    # Evita casar o "1" de "10": exige que depois do dígito não venha outro dígito
    m = re.search(
        r"(?:coluna|move|jogada|column)\D*([1-7])(?![0-9])",
        text,
        re.IGNORECASE,
    )
    if m:
        return int(m.group(1))

    # Fallback: número 1-7 isolado
    m = re.search(r"\b([1-7])\b", text)
    if m:
        return int(m.group(1))

    return None


def is_reset(title, body):
    return "reset" in f"{title} {body}".lower()


def main():
    title = os.environ.get("ISSUE_TITLE", "") or ""
    body = os.environ.get("ISSUE_BODY", "") or ""
    repo = os.environ.get("REPO", "") or ""

    if not repo:
        _write_result("❌ Erro interno: variável REPO não definida.")
        return 1

    state = load_state()

    # Caso especial: Reset
    if is_reset(title, body):
        state = new_state()
        save_state(state)
        with open("README.md", "w", encoding="utf-8") as f:
            f.write(generate(state, repo))
        _write_result("🔄 Jogo reiniciado com sucesso!")
        return 0

    col = parse_move(title, body)
    if col is None:
        _write_result(
            "❌ Não consegui identificar a coluna na sua Issue. "
            "Use o formato `Move: 3` (número de 1 a 7)."
        )
        return 1

    success, message = apply_move(state, col - 1)
    if not success:
        _write_result(f"❌ {message}")
        return 1

    save_state(state)
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(generate(state, repo))

    _write_result(f"✅ {message} O tabuleiro foi atualizado!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
