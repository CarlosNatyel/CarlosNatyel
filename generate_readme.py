"""Gera o README.md com o tabuleiro em SVG e os links de jogada."""

from urllib.parse import quote

from connect4 import COLS, EMPTY, RED, YELLOW
from render_svg import render_svg


PLAYER_NAME = {RED: "🔴 Vermelho", YELLOW: "🟡 Amarelo"}


def available_columns(state):
    return [c for c in range(COLS) if state["board"][0][c] == EMPTY]


def _issue_url(repo, col):
    title = quote(f"Move: {col + 1}")
    body = quote(f"Jogada: coluna {col + 1}")
    return f"https://github.com/{repo}/issues/new?title={title}&body={body}"


def _reset_url(repo):
    title = quote("Reset")
    body = quote("Reiniciar o jogo")
    return f"https://github.com/{repo}/issues/new?title={title}&body={body}"


def generate(state, repo):
    # 1) Escreve o SVG do tabuleiro em disco
    svg_content = render_svg(state["board"], last_move=state.get("last_move"))
    with open("board.svg", "w", encoding="utf-8") as f:
        f.write(svg_content)

    # 2) CACHE BUSTING — a URL muda a cada jogada
    version = len(state["move_history"])
    svg_url = f"board.svg?v={version}"

    # 3) Cabeçalho de status + seção de jogadas
    if state["status"] == "in_progress":
        status_line = f"🎮 **É a vez do jogador:** {PLAYER_NAME[state['current_player']]}"
        cols = available_columns(state)
        links = [f"[▶ Jogar na coluna {c + 1}]({_issue_url(repo, c)})" for c in cols]
        moves_section = (
            "### 🎯 Escolha uma coluna\n\n"
            + " &nbsp;&nbsp; ".join(links)
            + "\n\n_Clique em um link, confirme a Issue e o tabuleiro será atualizado automaticamente._"
        )
    elif state["winner"] == "draw":
        status_line = "🤝 **Empate!** O tabuleiro está cheio."
        moves_section = (
            f"### 🔄 Reiniciar\n\n[▶ Começar nova partida]({_reset_url(repo)})"
        )
    else:
        winner_emoji = "🔴" if state["winner"] == RED else "🟡"
        status_line = f"🏆 **Vitória do jogador {winner_emoji}!**"
        moves_section = (
            f"### 🔄 Reiniciar\n\n[▶ Começar nova partida]({_reset_url(repo)})"
        )

    # 4) Últimos movimentos
    if state["move_history"]:
        recent = state["move_history"][-5:]
        hist_lines = ["### 📜 Últimos movimentos", ""]
        for m in reversed(recent):
            emoji = "🔴" if m["player"] == RED else "🟡"
            hist_lines.append(f"- {emoji} coluna **{m['column']}** (linha {m['row']})")
        history = "\n".join(hist_lines)
    else:
        history = "_Nenhum movimento ainda — seja o primeiro a jogar!_"

    # 5) README com o SVG e a URL versionada
    readme = f"""# 🔴🟡 Connect 4 — Jogo Comunitário

Bem-vindo ao **Connect 4 colaborativo**! Qualquer pessoa pode jogar — basta abrir uma *Issue*.

{status_line}

## 🎲 Tabuleiro

<p align="center">
  <img src="{svg_url}" alt="Tabuleiro Connect 4" width="450"/>
</p>

{moves_section}

{history}

---

## 📖 Como jogar

1. Escolha uma coluna clicando em um dos links acima.
2. Uma **Issue** será aberta com o movimento pré-preenchido.
3. Clique em **Submit new issue**.
4. Um **GitHub Action** processa a jogada, atualiza o tabuleiro e fecha a Issue automaticamente. ✨

## 📏 Regras

- Tabuleiro de **6 linhas × 7 colunas**.
- Os jogadores alternam entre 🔴 e 🟡.
- Vence quem alinhar **4 peças consecutivas** na horizontal, vertical ou diagonal.
- Se o tabuleiro encher sem vencedor, é **empate**.

## ⚙️ Como funciona

Este jogo usa **GitHub Issues** como interface de entrada e **GitHub Actions** como motor. Cada Issue é interpretada por um workflow que valida a jogada, atualiza `game_state.json`, regenera o SVG do tabuleiro e o README.

Inspirado no [xadrez comunitário de Tim Burgan](https://github.com/timburgan/timburgan).
"""
    return readme
