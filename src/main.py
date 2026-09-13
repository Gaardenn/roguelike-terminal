"""Ponto de entrada do jogo."""

import curses

from render import render_blank_screen, render_map, render_entity, render_message
from map import generate_dungeon, is_walkable, get_occupant
from input import (
    get_player_action,
    ACTION_CANCEL,
    ACTION_MOVE_UP,
    ACTION_MOVE_DOWN,
    ACTION_MOVE_LEFT,
    ACTION_MOVE_RIGHT,
    ACTION_WAIT,
)
from entities import (
    create_player,
    spawn_monsters,
    gain_energy,
    can_act,
    consume_energy,
    monster_take_turn,
)
from combat import attempt_attack

MOVE_DELTAS = {
    ACTION_MOVE_UP: (0, -1),
    ACTION_MOVE_DOWN: (0, 1),
    ACTION_MOVE_LEFT: (-1, 0),
    ACTION_MOVE_RIGHT: (1, 0),
}




def move_player(player, dx, dy, map_grid):
    """Move o jogador, respeitando colisão com paredes.
    
    Se o destino tiver um monstro, nao move: inicia combate no lugar
    (conforme 05-combate.md, secao 2 - "atacar" e implicito ao mover
    contra um monstro adjacente). Retorna uma mensagem de log, se houver.
    """
    new_x = player["x"] + dx
    new_y = player["y"] + dy

    if not is_walkable(map_grid, new_x, new_y):
        return None

    occupant = get_occupant(map_grid, new_x, new_y)

    if occupant is not None:
        return attempt_attack(player, occupant)

    player["x"] = new_x
    player["y"] = new_y
    return None

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(False)
    stdscr.keypad(True)

    test_map, rooms, player_start = generate_dungeon()
    player = create_player(x=player_start[0], y=player_start[1])
    monsters = spawn_monsters(test_map, rooms, floor=1)
    last_message = None

    running = True
    while running:
        render_blank_screen(stdscr)
        render_map(stdscr, test_map)
        for monster in monsters:
            render_entity(stdscr, monster)
        render_entity(stdscr, player)
        render_message(stdscr, last_message)
        stdscr.refresh()

        action = get_player_action(stdscr)
        turn_taken = False

        if action == ACTION_CANCEL:
            running = False
        elif action in MOVE_DELTAS:
            dx, dy = MOVE_DELTAS[action]
            last_message = move_player(player, dx, dy, test_map)
            turn_taken = True
        elif action == ACTION_WAIT:
            last_message = "Voce espera."
            turn_taken = True

        if turn_taken:
            for monster in monsters:
                gain_energy(monster)
                while can_act(monster):
                    monster_take_turn(monster, player, test_map)
                    consume_energy(monster)


if __name__ == "__main__":
    curses.wrapper(main)