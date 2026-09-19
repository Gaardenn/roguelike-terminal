"""Testes funcionais de geracao procedural de mapa (04-geracao-mapas.md)."""

from map import generate_dungeon, is_fully_connected, MIN_ROOMS, MAX_ROOMS

NUM_EXECUTIONS = 500


def test_generation_does_not_hand_and_returns_valid_data():
    """Roda a geracao muitas vezes seguidas, garantindo que nunca trava
    (sem loop infinito) e que sempre retorna uma estrutura valida."""
    for _ in range(NUM_EXECUTIONS):
        map_grid, rooms, player_start = generate_dungeon()

        assert map_grid is not None
        assert rooms is not None
        assert player_start is not None


def test_generated_maps_have_valid_room_count():
    """Confere que o numero de salas geradas respeita a faixa definida
    (04-geracao-mapas.md, secao 1: MIN_ROOMS a MAX_ROOMS)."""
    for _ in range(NUM_EXECUTIONS):
        _map_grid, rooms, _player_start = generate_dungeon()

        assert MIN_ROOMS <= len(rooms) <= MAX_ROOMS


def test_generated_maps_are_fully_connected():
    """Confere que todo mapa gerado passa na validacao de flood fill
    (04-geracao-mapas.md, secao 5) - ou seja, nao ha mapa quebrado."""
    for _ in range(NUM_EXECUTIONS):
        map_grid, rooms, _player_start = generate_dungeon()

        assert is_fully_connected(map_grid, rooms)


def test_player_start_is_walkable():
    """Confere que o jogador sempre nasce em cima de um tile de piso."""
    for _ in range(NUM_EXECUTIONS):
        map_grid, _rooms, player_start = generate_dungeon()
        x, y = player_start

        tile = map_grid[y][x]
        assert tile["type"] in ("floor", "stairs")


def test_map_has_exactly_one_stairs_tile():
    """Confere que existe exatamente uma escada no mapa gerado."""
    for _ in range(NUM_EXECUTIONS):
        map_grid, _rooms, _player_start = generate_dungeon()

        stairs_count = sum(
            1 for row in map_grid for tile in row if tile["type"] == "stairs"
        )
        assert stairs_count == 1