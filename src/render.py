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

def render_entity(stdscr, entity):
    """Desenha uma entidade (jogador ou monstro) por cima do mapa."""
    stdscr.addstr(entity["y"], entity["x"], entity["symbol"])


def render_items(stdscr, map_grid):
    """Desenha os itens que estao no chao do mapa."""
    for y, row in enumerate(map_grid):
        for x, tile in enumerate(row):
            if tile["item"] is not None:
                stdscr.addstr(y, x, tile["item"]["symbol"])

STATUS_START_Y = 21
LOG_START_Y = 21
LOG_START_X = 41
LOG_WIDTH = 38
LOG_MAX_LINES = 4  # 08-interface.md: area de log tem 4 linhas uteis (linhas 20-23)


def render_status(stdscr, player, floor):
    """Desenha o painel de status: HP, andar e itens equipados (08-interface.md, secao 1)."""
    # Limpa a area do status antes de redesenhar
    for i in range(4):
        stdscr.addstr(STATUS_START_Y + i, 0, " " * 40)

    stdscr.addstr(STATUS_START_Y, 0, f"HP: {player['hp']}/{player['max_hp']}    Andar: {floor}")

    equipped_names = [
        item["name"] for item in player["equipped"].values() if item is not None
    ]
    equipped_text = ", ".join(equipped_names) if equipped_names else "nenhum"
    stdscr.addstr(STATUS_START_Y + 1, 0, f"Equipado: {equipped_text}"[:39])


def render_log(stdscr, messages):
    """Desenha as ultimas mensagens do log (08-interface.md, secao 1)."""
    for i in range(LOG_MAX_LINES):
        stdscr.addstr(LOG_START_Y + i, LOG_START_X, " " * LOG_WIDTH)

    recent = messages[-LOG_MAX_LINES:]
    for i, message in enumerate(recent):
        stdscr.addstr(LOG_START_Y + i, LOG_START_X, message[:LOG_WIDTH])