"""Estrutura de dados do mapa (grid de tiles)."""

MAP_WIDTH = 80
MAP_HEIGHT = 20


def create_tile(tile_type="wall"):
    """Cria um tile novo, seguindo a estrutura definida em 03-arquitetura.md."""
    symbols = {
        "wall": "#",
        "floor": ".",
        "stairs": ">",
    }

    return {
        "type": tile_type,
        "symbol": symbols[tile_type],
        "occupant": None,
        "item": None,
    }


def create_empty_map(width=MAP_WIDTH, height=MAP_HEIGHT):
    """Cria um grid width x height, todo preenchido de parede ('wall').

    Acesso: map_grid[y][x]
    """
    return [
        [create_tile("wall") for _x in range(width)]
        for _y in range(height)
    ]


def set_tile(map_grid, x, y, tile_type):
    """Substitui o tile na posição (x, y) por um novo tile do tipo informado."""
    map_grid[y][x] = create_tile(tile_type)


def get_tile(map_grid, x, y):
    """Retorna o tile na posição (x, y)."""
    return map_grid[y][x]

def is_walkable(map_grid, x, y):
    """Retorna True se a posição existir no grid e não for parede."""
    height = len(map_grid)
    width = len(map_grid[0])

    if x < 0 or x >= width or y < 0 or y >= height:
        return False

    return get_tile(map_grid, x, y)["type"] != "wall"