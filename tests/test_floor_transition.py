"""Testes funcionais de transicao entre andares (3.7 do roadmap, 04-geracao-mapas.md)."""

from map import generate_dungeon
from entities import create_player, spawn_monsters, descend_floor, TOTAL_FLOORS

BOSS_NAME = "O Deus da Morte"


def start_game():
    """Monta o estado inicial de uma partida, igual ao main.py faz."""
    map_grid, rooms, player_start = generate_dungeon()
    player = create_player(x=player_start[0], y=player_start[1])
    map_grid[player["y"]][player["x"]]["occupant"] = player
    monsters = spawn_monsters(map_grid, rooms, floor=1)
    return map_grid, rooms, monsters, player


def test_descend_floor_increments_floor_number():
    map_grid, rooms, monsters, player = start_game()

    new_map, new_rooms, new_monsters, new_floor = descend_floor(player, map_grid, current_floor=1)

    assert new_floor == 2


def test_descend_floor_preserves_player_hp():
    map_grid, rooms, monsters, player = start_game()
    player["hp"] = 12  # simula dano recebido no andar anterior

    descend_floor(player, map_grid, current_floor=1)

    assert player["hp"] == 12  # HP nao e resetado ao descer


def test_descend_floor_preserves_inventory_and_equipment():
    from items import create_item, ITEM_PROTECAO
    from entities import add_item_to_inventory, toggle_equip

    map_grid, rooms, monsters, player = start_game()
    item = create_item(ITEM_PROTECAO)
    add_item_to_inventory(player, item)
    toggle_equip(player, 0)

    descend_floor(player, map_grid, current_floor=1)

    assert player["inventory"][0] is item
    assert player["equipped"]["protecao"] is item


def test_descend_floor_repositions_player_on_walkable_tile():
    map_grid, rooms, monsters, player = start_game()

    new_map, new_rooms, new_monsters, new_floor = descend_floor(player, map_grid, current_floor=1)

    tile = new_map[player["y"]][player["x"]]
    assert tile["type"] in ("floor", "stairs")
    assert tile["occupant"] is player


def test_descend_floor_generates_a_different_map_each_time():
    map_grid, rooms, monsters, player = start_game()

    new_map_1, _rooms1, _monsters1, _floor1 = descend_floor(player, map_grid, current_floor=1)
    new_map_2, _rooms2, _monsters2, _floor2 = descend_floor(player, new_map_1, current_floor=2)

    assert new_map_1 is not new_map_2  # mapas gerados sao objetos diferentes


def test_repeated_descent_through_all_floors():
    """Desce do andar 1 ate o andar 4, varias vezes seguidas, sem erro."""
    map_grid, rooms, monsters, player = start_game()
    current_floor = 1

    for expected_floor in range(2, TOTAL_FLOORS + 1):
        map_grid, rooms, monsters, current_floor = descend_floor(player, map_grid, current_floor)
        assert current_floor == expected_floor


def test_boss_appears_only_on_florr_4():
    map_grid, rooms, monsters, player = start_game()
    current_floor = 1

    for _ in range(2, TOTAL_FLOORS + 1):
        map_grid, rooms, monsters, current_floor = descend_floor(player, map_grid, current_floor)

        boss_present = any(m["name"] == BOSS_NAME for m in monsters)

        if current_floor == TOTAL_FLOORS:
            assert boss_present is True
        else:
            assert boss_present is False


def test_monster_list_is_replaced_on_each_descent():
    """Os monstros do andar anterior nao devem persistir apos descer."""
    map_grid, rooms, monsters_floor_1, player = start_game()

    _new_map, _new_rooms, monster_floor_2, _floor = descend_floor(player, map_grid, current_floor=1)

    for monster in monster_floor_2:
        assert monster not in monsters_floor_1