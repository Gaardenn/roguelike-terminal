"""Testes funcionais de movimento e colisao do jogador (3.3 do roadmap)."""

from map import create_empty_map, set_tile
from entities import create_player
from main import move_player


def build_open_room_map(width=10, height=10):
    """Cria um mapa 10x10 todo de piso, exceto a borda (paredes ao redor)."""
    map_grid = create_empty_map(width, height)
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            set_tile(map_grid, x, y, "floor")
    return map_grid


def place_player(map_grid, x, y):
    player = create_player(x, y)
    map_grid[y][x]["occupant"] = player
    return player


def test_move_up():
    map_grid = build_open_room_map()
    player = place_player(map_grid, 5, 5)

    move_player(player, 0, -1, map_grid, monsters=[])

    assert (player["x"], player["y"]) == (5, 4)


def test_move_down():
    map_grid = build_open_room_map()
    player = place_player(map_grid, 5, 5)

    move_player(player, 0, 1, map_grid, monsters=[])

    assert (player["x"], player["y"]) == (5, 6)


def test_move_left():
    map_grid = build_open_room_map()
    player = place_player(map_grid, 5, 5)

    move_player(player, -1, 0, map_grid, monsters=[])

    assert (player["x"], player["y"]) == (4, 5)


def test_move_right():
    map_grid = build_open_room_map()
    player = place_player(map_grid, 5, 5)

    move_player(player, 1, 0, map_grid, monsters=[])

    assert (player["x"], player["y"]) == (6, 5)


def test_move_blocked_by_wall():
    """Jogador colado na parede (x=1) nao consegue ir mais pra esquerda (parede em x=0)."""
    map_grid = build_open_room_map()
    player = place_player(map_grid, 1, 5)

    move_player(player, -1, 0, map_grid, monsters=[])

    assert (player["x"], player["y"]) == (1, 5)  # nao se moveu


def test_move_blocked_by_map_border_top():
    """Jogador no topo do mapa (y=0, fora da area jogavel) nao vai alem da borda."""
    map_grid = build_open_room_map()
    player = place_player(map_grid, 5, 1)  # colado na parede superior

    move_player(player, 0, -1, map_grid, monsters=[])

    assert (player["x"], player["y"]) == (5, 1)  # nao se moveu


def test_move_blocked_by_map_border_right():
    """Jogador colado na borda direita nao ultrapassa os limites do mapa."""
    width = 10
    map_grid = build_open_room_map(width=width)
    player = place_player(map_grid, width - 2, 5)  # ultima coluna de piso valida

    move_player(player, 1, 0, map_grid, monsters=[])

    assert (player["x"], player["y"]) == (width - 2, 5)  # nao se moveu


def test_sequential_movement_returns_to_origin():
    """Move em um quadrado completo (cima, direita, baixo, esquerda) e confere
    que o jogador volta exatamente pra posicao original."""
    map_grid = build_open_room_map()
    player = place_player(map_grid, 5, 5)
    origin = (player["x"], player["y"])

    move_player(player, 0, -1, map_grid, monsters=[])  # cima
    move_player(player, 1, 0, map_grid, monsters=[])   # direita
    move_player(player, 0, 1, map_grid, monsters=[])   # baixo
    move_player(player, -1, 0, map_grid, monsters=[])  # esquerda

    assert (player["x"], player["y"]) == origin