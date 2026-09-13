"""Ponto de entrada do jogo."""

import curses

from render import render_blank_screen, render_map, render_entity
from map import generate_dungeon, is_walkable
from input import (
    get_player_action,
    ACTION_CANCEL,
    ACTION_MOVE_UP,
    ACTION_MOVE_DOWN,
    ACTION_MOVE_LEFT,
    ACTION_MOVE_RIGHT,
)
from entities import create_player, spawn_monsters

MOVE_DELTAS = {
    ACTION_MOVE_UP: (0, -1),
    ACTION_MOVE_DOWN: (0, 1),
    ACTION_MOVE_LEFT: (-1, 0),
    ACTION_MOVE_RIGHT: (1, 0),
}




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

    test_map, rooms, player_start = generate_dungeon()
    player = create_player(x=player_start[0], y=player_start[1])
    monsters = spawn_monsters(test_map, rooms, floor=1)

    running = True
    while running:
        render_blank_screen(stdscr)
        render_map(stdscr, test_map)
        for monster in monsters:
            render_entity(stdscr, monster)
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