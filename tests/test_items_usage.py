"""Testes funcionais de uso de todos os itens implementados (07-itens.md)."""

from unittest.mock import patch

from entities import (
    create_player,
    create_perturbado,
    add_item_to_inventory,
    toggle_equip,
    throw_item,
    get_effective_defense,
)
from items import (
    create_item,
    ITEM_INSTRUMENTAL,
    ITEM_MACHADINHA,
    ITEM_PROTECAO,
    ITEM_CORACAO,
)
from map import create_empty_map, set_tile
from main import handle_coracao_prompt


class FakeStdscr:
    """Stub minimo de stdscr do curses, so pra testar prompts sem terminal real."""

    def __init__(self, key_to_return):
        self.key_to_return = key_to_return

    def addstr(self, *args, **kwargs):
        pass

    def refresh(self):
        pass

    def getch(self):
        return self.key_to_return


# --- Instrumental ---

def test_instrumental_equip_and_unequip_toggle():
    player = create_player(0, 0)
    item = create_item(ITEM_INSTRUMENTAL)
    add_item_to_inventory(player, item)

    msg_equip = toggle_equip(player, 0)
    assert player["equipped"]["instrumental"] is item
    assert "equipado" in msg_equip.lower()

    msg_unequip = toggle_equip(player, 0)
    assert player["equipped"]["instrumental"] is None
    assert "desequipado" in msg_unequip.lower()


# --- Protecao Leve ---

def test_protecao_leve_increases_effective_defense():
    player = create_player(0, 0)
    base_defense = get_effective_defense(player)

    item = create_item(ITEM_PROTECAO)
    add_item_to_inventory(player, item)
    toggle_equip(player, 0)

    assert get_effective_defense(player) == base_defense + 5


def test_protecao_leve_bonus_removed_after_unequip():
    player = create_player(0, 0)
    base_defense = get_effective_defense(player)

    item = create_item(ITEM_PROTECAO)
    add_item_to_inventory(player, item)
    toggle_equip(player, 0)
    toggle_equip(player, 0)

    assert get_effective_defense(player) == base_defense


# --- Machadinha ---

def build_open_map_with_monster(monster_x, monster_y):
    map_grid = create_empty_map(10, 10)
    for y in range(1, 9):
        for x in range(1, 9):
            set_tile(map_grid, x, y, "floor")

    monster = create_perturbado(monster_x, monster_y)
    map_grid[monster_y][monster_x]["occupant"] = monster
    return map_grid, monster


def test_machadinha_hits_target_within_range_and_is_consumed():
    map_grid, monster = build_open_map_with_monster(monster_x=6, monster_y=5)
    player = create_player(5, 5)  # distancia 1, dentro do alcance de 4

    item = create_item(ITEM_MACHADINHA)
    add_item_to_inventory(player, item)

    monsters = [monster]

    with patch("random.randint", return_value=6):  # forca dano maximo (1-6)
        message = throw_item(player, 0, map_grid, monsters)

    assert player["inventory"][0] is None  # item consumido
    assert "arremessa" in message.lower()


def test_machadinha_no_target_in_range():
    map_grid, monster = build_open_map_with_monster(monster_x=9, monster_y=9)
    player = create_player(1, 1)  # bem longe, fora do alcance de 4

    item = create_item(ITEM_MACHADINHA)
    add_item_to_inventory(player, item)

    message = throw_item(player, 0, map_grid, [monster])

    assert "nenhum alvo" in message.lower()
    assert player["inventory"][0] is not None  # item NAO foi consumido


def test_machadinha_kills_weak_monster_and_removes_from_list():
    map_grid, monster = build_open_map_with_monster(monster_x=6, monster_y=5)
    monster["hp"] = 1  # qualquer dano mata
    player = create_player(5, 5)

    item = create_item(ITEM_MACHADINHA)
    add_item_to_inventory(player, item)

    monsters = [monster]

    with patch("random.randint", return_value=6):
        message = throw_item(player, 0, map_grid, monsters)
    
    assert monster not in monsters
    assert "morreu" in message.lower()
    assert map_grid[5][6]["occupant"] is None


# --- Coracao Pulsante ---

def test_coracao_reduces_damage_on_success():
    player = create_player(0, 0)
    item = create_item(ITEM_CORACAO)
    add_item_to_inventory(player, item)
    toggle_equip(player, 0)

    stdscr = FakeStdscr(key_to_return=ord("s"))

    # fail_chance da 1a ativacao e 75%. Sucesso ocorre quando random() >= fail_chance,
    # entao um valor alto (0.99) forca o sucesso.
    with patch("random.random", return_value=0.99):
        final_damage, extra_message = handle_coracao_prompt(stdscr, player, damage=10)

    assert final_damage == 5  # metade de 10
    assert "reduzindo o dano" in extra_message.lower()
    assert player["equipped"]["coracao"] is item  # nao foi destruido


def test_coracao_destroyed_on_failure():
    player = create_player(0, 0)
    item = create_item(ITEM_CORACAO)
    add_item_to_inventory(player, item)
    toggle_equip(player, 0)

    stdscr = FakeStdscr(key_to_return=ord("s"))

    # fail_chance da 1a ativacao e 75%. Falha ocorre quando random() < fail_chance,
    # entao um valor baixo (0.0) forca a falha.
    with patch("random.random", return_value=0.0):
        final_damage, extra_message = handle_coracao_prompt(stdscr, player, damage=10)

    assert final_damage == 10  # dano nao reduzido
    assert "destruido" in extra_message.lower()
    assert player["equipped"]["coracao"] is None
    assert item not in player["inventory"]


def test_coracao_second_use_always_fails():
    """Segunda ativacao tem 100% de chance de falha, mesmo com sorte maxima."""
    player = create_player(0, 0)
    item = create_item(ITEM_CORACAO)
    add_item_to_inventory(player, item)
    toggle_equip(player, 0)
    player["coracao_uses"] = 1  # ja usou uma vez antes

    stdscr = FakeStdscr(key_to_return=ord("s"))

    with patch("random.random", return_value=0.0):  # mesmo com a melhor sorte possivel
        final_damage, extra_message = handle_coracao_prompt(stdscr, player, damage=10)

    assert final_damage == 10
    assert "destruido" in extra_message.lower()


def test_coracao_declining_prompt_does_not_consume_item():
    player = create_player(0, 0)
    item = create_item(ITEM_CORACAO)
    add_item_to_inventory(player, item)
    toggle_equip(player, 0)

    stdscr = FakeStdscr(key_to_return=ord("n"))  # recusa o prompt

    final_damage, extra_message = handle_coracao_prompt(stdscr, player, damage=10)

    assert final_damage == 10
    assert extra_message == ""
    assert player["equipped"]["coracao"] is item  # continua equipado


def test_instrumental_reduces_coracao_fail_chance():
    """Com Instrumental equipado, a chance de falha cai 25 pontos percentuais."""
    player = create_player(0, 0)

    coracao = create_item(ITEM_CORACAO)
    add_item_to_inventory(player, coracao)
    toggle_equip(player, 0)

    instrumental = create_item(ITEM_INSTRUMENTAL)
    add_item_to_inventory(player, instrumental)
    toggle_equip(player, 1)

    stdscr = FakeStdscr(key_to_return=ord("s"))

    # Sem Instrumental, fail_chance seria 75%. Com Instrumental, cai pra 50%.
    # Um valor de 0.60 deve FALHAR sem Instrumental, mas SUCEDER com ele.
    with patch("random.random", return_value=0.60):
        final_damage, extra_message = handle_coracao_prompt(stdscr, player, damage=10)

    assert final_damage == 5  # sucesso: dano reduzido pela metade
    assert player["equipped"]["coracao"] is coracao  # nao foi destruido