# 🔴🟡 Connect 4 — Jogo Comunitário

Bem-vindo ao **Connect 4 colaborativo**! Qualquer pessoa pode jogar — basta abrir uma *Issue*.

🏆 **Vitória do jogador 🔴!**

## 🎲 Tabuleiro

<p align="center">
  <img src="board.svg?v=11" alt="Tabuleiro Connect 4" width="450"/>
</p>

### 🔄 Reiniciar

[▶ Começar nova partida](https://github.com/CarlosNatyel/CarlosNatyel/issues/new?title=Reset&body=Reiniciar%20o%20jogo)

### 📜 Últimos movimentos

- 🔴 coluna **6** (linha 6)
- 🟡 coluna **1** (linha 3)
- 🔴 coluna **5** (linha 6)
- 🟡 coluna **1** (linha 4)
- 🔴 coluna **4** (linha 5)

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
