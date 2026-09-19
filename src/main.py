"""Ponto de entrada do jogo."""

import curses
import random

from render import (
    render_blank_screen,
    render_map,
    render_entity,
    render_items,
    render_status,
    render_log,
    render_menu_screen,
    render_game_over_screen,
    render_victory_screen,
    init_colors,
)
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
    descend_floor,
    maybe_respawn_monster,
    INVENTORY_SIZE,
    TOTAL_FLOORS,
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

    if tile["type"] == "stairs":
        return "STAIRS"
    
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


BOSS_NAME = "O Deus da Morte"


def run_game(stdscr):
    """Executa uma partida completa. Retorna ('defeat', andar) ou ('victory', andar) ou ('menu', andar)."""
    test_map, rooms, player_start = generate_dungeon()
    player = create_player(x=player_start[0], y=player_start[1])
    test_map[player["y"]][player["x"]]["occupant"] = player

    current_floor = 1
    monsters = spawn_monsters(test_map, rooms, floor=current_floor)
    spawn_items(test_map, rooms, floor=current_floor)
    turn_count = 0

    message_log = []

    def push_message(msg):
        if msg:
            message_log.append(msg)

    running = True
    while running:
        render_blank_screen(stdscr)
        render_map(stdscr, test_map)
        render_items(stdscr, test_map)
        for monster in monsters:
            render_entity(stdscr, monster)
        render_entity(stdscr, player)
        render_status(stdscr, player, current_floor)
        render_log(stdscr, message_log)
        stdscr.refresh()

        action = get_player_action(stdscr)
        turn_taken = False

        if action == ACTION_CANCEL:
            return "menu", current_floor
        elif action in MOVE_DELTAS:
            dx, dy = MOVE_DELTAS[action]
            result = move_player(player, dx, dy, test_map, monsters)
            
            if result == "STAIRS":
                if current_floor >= TOTAL_FLOORS:
                    push_message("Voce esta no ultimo andar!")
                else:
                    test_map, rooms, monsters, current_floor = descend_floor(
                        player, test_map, current_floor
                    )
                    turn_count = 0
                    push_message(f"Voce desce para o andar {current_floor}.")
                turn_taken = False
            else:
                push_message(result)
                turn_taken = True
        elif action == ACTION_WAIT:
            push_message("Voce espera.")
            turn_taken = True
        elif action == ACTION_INVENTORY:
            result = open_inventory(stdscr, player, test_map, monsters)
            if result:
                push_message(result)

        if turn_taken and running:
            turn_count += 1
            new_monster = maybe_respawn_monster(test_map, rooms, monsters, current_floor, turn_count)
            if new_monster:
                push_message(f"Algo se move nas sombras... ({new_monster['name']} apareceu)")
            
            for monster in list(monsters):
                gain_energy(monster)
                while can_act(monster):
                    message, player_died = monster_take_turn(
                        monster, player, test_map,
                        on_player_damage=lambda dmg: handle_coracao_prompt(stdscr, player, dmg),
                    )
                    consume_energy(monster)

                    if message:
                        push_message(message)

                    if player_died:
                        return "defeat", current_floor

                if not running:
                    break

            if current_floor == TOTAL_FLOORS and not any(m["name"] == BOSS_NAME for m in monsters):
                return "victory", current_floor


def show_menu(stdscr):
    render_menu_screen(stdscr)
    while True:
        key = stdscr.getch()
        if key in (10, 13):
            return "start"
        if key == 27:
            return "quit"


def show_game_over(stdscr, floor_reached):
    render_game_over_screen(stdscr, floor_reached)
    while True:
        key = stdscr.getch()
        if key in (10, 13):
            return "restart"
        if key == 27:
            return "quit"


def show_victory(stdscr):
    render_victory_screen(stdscr)
    while True:
        key = stdscr.getch()
        if key in (10, 13):
            return "restart"
        if key == 27:
            return "quit"


def main(stdscr):
    # Decisao de design (02-gdd.md, secao "Permadeath"): o jogo nao tem
    # save/load. Cada partida e criada do zero em run_game() e descartada
    # ao morrer ou vencer - nao ha nenhum arquivo de save sendo escrito
    # em disco. "Reiniciar" (Enter na tela de derrota/vitoria) apenas
    # inicia uma nova partida, sem qualquer continuidade com a anterior.
    curses.curs_set(0)
    stdscr.nodelay(False)
    stdscr.keypad(True)
    init_colors()

    state = "menu"

    while state != "exit":
        if state == "menu":
            choice = show_menu(stdscr)
            state = "playing" if choice == "start" else "exit"

        elif state == "playing":
            outcome, floor_reached = run_game(stdscr)
            if outcome == "menu":
                state = "menu"
            elif outcome == "defeat":
                state = "game_over"
                last_floor_reached = floor_reached
            elif outcome == "victory":
                state = "victory"

        elif state == "game_over":
            choice = show_game_over(stdscr, last_floor_reached)
            state = "menu" if choice == "restart" else "exit"

        elif state == "victory":
            choice = show_victory(stdscr)
            state = "menu" if choice == "restart" else "exit"


if __name__ == "__main__":
    curses.wrapper(main)