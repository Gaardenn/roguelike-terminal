"""Ponto de entrada do jogo."""

import curses

from render import render_blank_screen, render_map
from map import create_empty_map, set_tile
from input import get_player_action, ACTION_CANCEL


def build_test_map():
    """Mapa fixo (hardcoded) só pra testar a renderização."""
    map_grid = create_empty_map()

    # Desenha uma "sala" retangular de piso no meio do grid
    for y in range(5, 15):
        for x in range(10, 40):
            set_tile(map_grid, x, y, "floor")

    # Um corredor horizontal saindo da sala
    for x in range(40, 60):
        set_tile(map_grid, x, 10, "floor")

    # Uma segunda salinha no fim do corredor
    for y in range(7, 13):
        for x in range(60, 70):
            set_tile(map_grid, x, y, "floor")

    # Escada no canto da segunda sala
    set_tile(map_grid, 68, 8, "stairs")

    return map_grid


def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(False)
    stdscr.keypad(True)

    test_map = build_test_map()

    running = True
    while running:
        render_blank_screen(stdscr)
        render_map(stdscr, test_map)
        stdscr.refresh()

        action = get_player_action(stdscr)

        if action == ACTION_CANCEL:
            running = False


if __name__ == "__main__":
    curses.wrapper(main)