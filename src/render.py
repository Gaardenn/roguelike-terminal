import curses
import textwrap
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
    """Desenha o grid do mapa na tela, linha por linha, com cores."""
    for y, row in enumerate(map_grid):
        for x, tile in enumerate(row):
            color = COLOR_STAIRS if tile["type"] == "stairs" else COLOR_WALL if tile["type"] == "wall" else 0
            attr = curses.color_pair(color) if color else 0
            stdscr.addstr(y, x, tile["symbol"], attr)

def render_entity(stdscr, entity):
    """Desenha uma entidade (jogador ou monstro) por cima do mapa, com cor."""
    if entity.get("is_player"):
        color = COLOR_PLAYER
    else:
        color = MONSTER_COLORS.get(entity["name"], 0)

    attr = curses.color_pair(color) if color else 0
    stdscr.addstr(entity["y"], entity["x"], entity["symbol"], attr)


def render_items(stdscr, map_grid):
    """Desenha os itens que estao no chao do mapa, com cor."""
    for y, row in enumerate(map_grid):
        for x, tile in enumerate(row):
            if tile["item"] is not None:
                stdscr.addstr(y, x, tile["item"]["symbol"], curses.color_pair(COLOR_ITEM))

STATUS_START_Y = 21
LOG_START_Y = 21
LOG_START_X = 41
LOG_WIDTH = 39  # colunas 41 a 79 (borda direita da tela de 80 colunas)
LOG_MAX_LINES = 4  # 08-interface.md: area de log tem 4 linhas uteis (linhas 20-23)


def render_status(stdscr, player, floor):
    """Desenha o painel de status: HP, andar e itens equipados (08-interface.md, secao 1)."""
    for i in range(4):
        stdscr.addstr(STATUS_START_Y + i, 0, " " * 40)

    hp_ratio = player["hp"] / player["max_hp"] if player["max_hp"] else 0
    if hp_ratio > 0.6:
        hp_color = COLOR_HP_HIGH
    elif hp_ratio > 0.3:
        hp_color = COLOR_HP_MID
    else:
        hp_color = COLOR_HP_LOW
    
    stdscr.addstr(STATUS_START_Y, 0, "HP: ")
    stdscr.addstr(f"{player['hp']}/{player['max_hp']}", curses.color_pair(hp_color))
    stdscr.addstr(f"    Andar: {floor}")

    equipped_names = [
        item["name"] for item in player["equipped"].values() if item is not None
    ]
    equipped_text = ", ".join(equipped_names) if equipped_names else "nenhum"
    stdscr.addstr(STATUS_START_Y + 1, 0, f"Equipado: {equipped_text}"[:39])


def render_log(stdscr, messages):
    """Desenha as mensagens mais recentes do log, quebrando mensagens
    longas em multiplas linhas (08-interface.md, secao 1)."""
    for i in range(LOG_MAX_LINES):
        stdscr.addstr(LOG_START_Y + i, LOG_START_X, " " * LOG_WIDTH)

    wrapped_lines = []
    for message in messages:
        wrapped_lines.extend(textwrap.wrap(message, LOG_WIDTH) or [""])

    visible_lines = wrapped_lines[-LOG_MAX_LINES:]
    for i, line in enumerate(visible_lines):
        stdscr.addstr(LOG_START_Y + i, LOG_START_X, line)

def render_menu_screen(stdscr):
    """Tela de Menu Inicial (estados-jogo.drawio)."""
    stdscr.clear()
    lines = [
        "ROGUELIKE DE TERMINAL",
        "",
        "Desca os 4 andares da masmorra e derrote O Deus da Morte.",
        "",
        "Enter - Iniciar jogo",
        "Esc - Sair",
    ]
    for i, line in enumerate(lines):
        stdscr.addstr(5 + i, 10, line)
    stdscr.refresh()


def render_game_over_screen(stdscr, floor_reached):
    """Tela de Derrota (game over)."""
    stdscr.clear()
    lines = [
        "VOCE MORREU",
        "",
        f"Voce chegou ate o andar {floor_reached}.",
        "",
        "Enter - Reiniciar",
        "Esc - Sair",
    ]
    for i, line in enumerate(lines):
        stdscr.addstr(5 + i, 10, line)
    stdscr.refresh()


def render_victory_screen(stdscr):
    """Tela de Vitoria (chefe final derrotado)."""
    stdscr.clear()
    lines = [
        "VOCE VENCEU!",
        "",
        "Voce derrotou O Deus da Morte e escapou da masmorra.",
        "",
        "Enter - Reiniciar",
        "Esc - Sair",
    ]
    for i, line in enumerate(lines):
        stdscr.addstr(5 + i, 10, line)
    stdscr.refresh()

COLOR_PLAYER = 1
COLOR_WALL = 2
COLOR_STAIRS = 3
COLOR_PERTURBADO = 4
COLOR_MULHER = 5
COLOR_BOSS = 6
COLOR_ITEM = 7
COLOR_HP_HIGH = 8
COLOR_HP_MID = 9
COLOR_HP_LOW = 10
COLOR_LOG_DAMAGE = 11
COLOR_LOG_NEUTRAL = 12


def init_colors():
    """Inicializa os pares de cor do curses (08-interface.md, secao 2)."""
    curses.start_color()
    curses.use_default_colors()

    curses.init_pair(COLOR_PLAYER, curses.COLOR_CYAN, -1)
    curses.init_pair(COLOR_WALL, curses.COLOR_BLACK, -1)
    curses.init_pair(COLOR_STAIRS, curses.COLOR_YELLOW, -1)
    curses.init_pair(COLOR_PERTURBADO, curses.COLOR_MAGENTA, -1)
    curses.init_pair(COLOR_MULHER, curses.COLOR_BLUE, -1)
    curses.init_pair(COLOR_BOSS, curses.COLOR_RED, -1)
    curses.init_pair(COLOR_ITEM, curses.COLOR_YELLOW, -1)
    curses.init_pair(COLOR_HP_HIGH, curses.COLOR_GREEN, -1)
    curses.init_pair(COLOR_HP_MID, curses.COLOR_YELLOW, -1)
    curses.init_pair(COLOR_HP_LOW, curses.COLOR_RED, -1)
    curses.init_pair(COLOR_LOG_DAMAGE, curses.COLOR_RED, -1)
    curses.init_pair(COLOR_LOG_NEUTRAL, curses.COLOR_WHITE, -1)


MONSTER_COLORS = {
    "Perturbado de Energia": COLOR_PERTURBADO,
    "Mulher Afogada": COLOR_MULHER,
    "O Deus da Morte": COLOR_BOSS,
}