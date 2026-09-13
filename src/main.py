"""Ponto de entrada do jogo."""

import curses

from render import render_blank_screen, render_map, render_entity
from map import create_empty_map, set_tile, is_walkable
from input import (
    get_player_action,
    ACTION_CANCEL,
    ACTION_MOVE_UP,
    ACTION_MOVE_DOWN,
    ACTION_MOVE_LEFT,
    ACTION_MOVE_RIGHT,
)
from entities import create_player

MOVE_DELTAS = {
    ACTION_MOVE_UP: (0, -1),
    ACTION_MOVE_DOWN: (0, 1),
    ACTION_MOVE_LEFT: (-1, 0),
    ACTION_MOVE_RIGHT: (1, 0),
}


def build_test_map():
    """Mapa fixo (hardcoded) só pra testar a renderização."""
    map_grid = create_empty_map()

    for y in range(5, 15):
        for x in range(10, 40):
            set_tile(map_grid, x, y, "floor")

    for x in range(40, 60):
        set_tile(map_grid, x, 10, "floor")

    for y in range(7, 13):
        for x in range(60, 70):
            set_tile(map_grid, x, y, "floor")

    set_tile(map_grid, 68, 8, "stairs")

    return map_grid


def move_player(player, dx, dy, map_grid):
    """Move o jogador, respeitando colisão com paredes."""
    new_x = player["x"] + dx
    new_y = player["y"] + dy

    if is_walkable(map_grid, new_x, new_y):
        player["x"] = new_x
        player["y"] = new_y


def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(False)
    stdscr.keypad(True)

    test_map = build_test_map()
    player = create_player(x=15, y=8)

    running = True
    while running:
        render_blank_screen(stdscr)
        render_map(stdscr, test_map)
        render_entity(stdscr, player)
        stdscr.refresh()

        action = get_player_action(stdscr)

        if action == ACTION_CANCEL:
            running = False
        elif action in MOVE_DELTAS:
            dx, dy = MOVE_DELTAS[action]
            move_player(player, dx, dy, test_map)


if __name__ == "__main__":
    curses.wrapper(main)