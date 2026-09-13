"""Captura e interpretação do input do teclado, conforme 08-interface.md."""

import curses

# Ações possíveis retornadas por get_player_action
ACTION_MOVE_UP = "move_up"
ACTION_MOVE_DOWN = "move_down"
ACTION_MOVE_LEFT = "move_left"
ACTION_MOVE_RIGHT = "move_right"
ACTION_WAIT = "wait"
ACTION_INVENTORY = "inventory"
ACTION_CONFIRM = "confirm"
ACTION_CANCEL = "cancel"
ACTION_UNKNOWN = "unknown"

KEY_MAP = {
    curses.KEY_UP: ACTION_MOVE_UP,
    curses.KEY_DOWN: ACTION_MOVE_DOWN,
    curses.KEY_LEFT: ACTION_MOVE_LEFT,
    curses.KEY_RIGHT: ACTION_MOVE_RIGHT,
    ord(" "): ACTION_WAIT,
    ord("i"): ACTION_INVENTORY,
    10: ACTION_CONFIRM,   # Enter (Linux/Mac)
    13: ACTION_CONFIRM,   # Enter (Windows)
    27: ACTION_CANCEL,    # ESC
}


def get_player_action(stdscr):
    """Lê uma tecla do jogador e retorna a ação correspondente."""
    key = stdscr.getch()
    return KEY_MAP.get(key, ACTION_UNKNOWN)