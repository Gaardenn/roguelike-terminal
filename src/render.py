"""Funções de renderização da tela do jogo."""

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 24
MAP_HEIGHT = 20


def render_blank_screen(stdscr):
    """Limpa a tela e desenha o layout em branco (mapa, status, log)."""
    stdscr.clear()

    # Linha divisória horizontal entre o mapa e o painel inferior
    stdscr.addstr(MAP_HEIGHT, 0, "-" * SCREEN_WIDTH)

    # Linha divisória vertical entre status (esquerda) e log (direita)
    for y in range(MAP_HEIGHT + 1, SCREEN_HEIGHT):
        stdscr.addstr(y, 40, "|")

    # Mensagem temporária, só pra confirmar que a tela está renderizando
    stdscr.addstr(0, 0, "Setup base OK - pressione ESC para sair")

    stdscr.refresh()

def render_map(stdscr, map_grid):
    """Desenha o grid do mapa na tela, linha por linha."""
    for y, row in enumerate(map_grid):
        line = "".join(tile["symbol"] for tile in row)
        stdscr.addstr(y, 0, line)