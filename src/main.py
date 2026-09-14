"""Ponto de entrada do jogo."""

import curses
import random

from render import render_blank_screen, render_map, render_entity, render_message, render_items
from map import generate_dungeon, is_walkable, get_occupant, move_occupant
from input import (
    get_player_action,
    ACTION_CANCEL,
    ACTION_MOVE_UP,
    ACTION_MOVE_DOWN,
    ACTION_MOVE_LEFT,
    ACTION_MOVE_RIGHT,
    ACTION_WAIT,
    ACTION_INVENTORY,
)
from entities import (
    create_player,
    spawn_monsters,
    gain_energy,
    can_act,
    consume_energy,
    monster_take_turn,
    add_item_to_inventory,
    toggle_equip,
    use_consumable,
    throw_item,
    INVENTORY_SIZE,
)
from items import spawn_items, TYPE_CONSUMABLE, TYPE_EQUIPABLE, TYPE_THROWABLE
from combat import resolve_attack

MOVE_DELTAS = {
    ACTION_MOVE_UP: (0, -1),
    ACTION_MOVE_DOWN: (0, 1),
    ACTION_MOVE_LEFT: (-1, 0),
    ACTION_MOVE_RIGHT: (1, 0),
}


def move_player(player, dx, dy, map_grid, monsters):
    """Move o jogador, respeitando colisão com paredes.
    
    Se o destino tiver um monstro, resolve o ataque no lugar. Se tiver
    um item, tenta coletar automaticamente.
    """
    new_x = player["x"] + dx
    new_y = player["y"] + dy

    if not is_walkable(map_grid, new_x, new_y):
        return None

    occupant = get_occupant(map_grid, new_x, new_y)

    if occupant is not None:
        message, died = resolve_attack(player, occupant)
        if died:
            map_grid[new_y][new_x]["occupant"] = None
            if occupant in monsters:
                monsters.remove(occupant)
        return message

    move_occupant(map_grid, player, new_x, new_y)

    tile = map_grid[new_y][new_x]
    if tile["item"] is not None:
        item = tile["item"]
        if add_item_to_inventory(player, item):
            tile["item"] = None
            return f"Voce pegou {item['name']}."
        return f"Inventario cheio. Nao foi possivel pegar {item['name']}."
    
    return None


def handle_coracao_prompt(stdscr, player, damage):
    """Oferece a opcao de espremer o Coracao Pulsante ao levar dano
    (07-itens.md, secao 5). Retorna (dano final, mensagem_extra)."""
    coracao = player["equipped"].get("coracao")
    if coracao is None:
        return damage, ""

    stdscr.addstr(22, 41, "Espremer Coracao Pulsante? (S/N)"[:38])
    stdscr.refresh()

    key = stdscr.getch()
    stdscr.addstr(22, 41, " " * 38)

    if key not in (ord("s"), ord("S")):
        return damage, ""

    player["coracao_uses"] += 1
    fail_chance = 0.75 if player["coracao_uses"] == 1 else 1.0

    if player["equipped"].get("instrumental") is not None:
        fail_chance = max(0.0, fail_chance - 0.25)

    if random.random() < fail_chance:
        player["equipped"]["coracao"] = None
        for i, item in enumerate(player["inventory"]):
            if item is coracao:
                player["inventory"][i] = None
                break
        return damage, " O Coracao Pulsante falhou e foi destruido!"

    return damage // 2, " Voce espreme o Coracao Pulsante, reduzindo o dano pela metade!"



def render_inventory_screen(stdscr, player, selected_index):
    stdscr.clear()
    stdscr.addstr(0, 0, "INVENTARIO - Enter: usar/equipar/arremessar | Esc: fechar")

    for i in range(INVENTORY_SIZE):
        item = player["inventory"][i]
        marker = ">" if i == selected_index else " "

        if item is None:
            line = f"{marker} {i + 1}. (vazio)"
        else:
            equipped_tag = ""
            if item["type"] == TYPE_EQUIPABLE and player["equipped"].get(item["item_id"]) is item:
                equipped_tag = " [E]"
            line = f"{marker} {i + 1}. {item['name']}{equipped_tag}"

        stdscr.addstr(2 + i, 0, line)

    stdscr.refresh()


def open_inventory(stdscr, player, map_grid, monsters):
    """Abre a tela de inventario. Retorna mensagem de log, se houver acao."""
    selected = 0
    message = None

    while True:
        render_inventory_screen(stdscr, player, selected)
        key = stdscr.getch()

        if key == 27:
            break
        elif key == curses.KEY_UP:
            selected = (selected - 1) % INVENTORY_SIZE
        elif key == curses.KEY_DOWN:
            selected = (selected + 1) % INVENTORY_SIZE
        elif key in (10, 13):
            item = player["inventory"][selected]
            if item is None:
                continue

            if item["type"] == TYPE_CONSUMABLE:
                message = use_consumable(player, selected)
                break
            elif item["type"] == TYPE_EQUIPABLE:
                message = toggle_equip(player, selected)
            elif item["type"] == TYPE_THROWABLE:
                message = throw_item(player, selected, map_grid, monsters)
                break

    return message


def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(False)
    stdscr.keypad(True)

    test_map, rooms, player_start = generate_dungeon()
    player = create_player(x=player_start[0], y=player_start[1])
    test_map[player["y"]][player["x"]]["occupant"] = player

    monsters = spawn_monsters(test_map, rooms, floor=1)
    spawn_items(test_map, rooms, floor=1)

    last_message = None

    running = True
    while running:
        render_blank_screen(stdscr)
        render_map(stdscr, test_map)
        render_items(stdscr, test_map)
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
            last_message = move_player(player, dx, dy, test_map, monsters)
            turn_taken = True
        elif action == ACTION_WAIT:
            last_message = "Voce espera."
            turn_taken = True
        elif action == ACTION_INVENTORY:
            result = open_inventory(stdscr, player, test_map, monsters)
            if result:
                last_message = result

        if turn_taken and running:
            for monster in list(monsters):
                gain_energy(monster)
                while can_act(monster):
                    message, player_died = monster_take_turn(
                        monster, player, test_map,
                        on_player_damage=lambda dmg: handle_coracao_prompt(stdscr, player, dmg),
                    )
                    consume_energy(monster)

                    if message:
                        last_message = message

                    if player_died:
                        last_message = "Voce morreu."
                        running = False
                        break

                if not running:
                    break


if __name__ == "__main__":
    curses.wrapper(main)