import random
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


MIN_ROOMS = 6
MAX_ROOMS = 10
MIN_ROOM_SIZE = 4
MAX_ROOM_WIDTH = 10
MAX_ROOM_HEIGHT = 6


def _rooms_overlap(a, b, padding=1):
    """Verifica se duas salas (com um espaco de folga) se sobrepoem."""
    return not (
        a["x"] + a["w"] + padding <= b["x"]
        or b["x"] + b["w"] + padding <= a["x"]
        or a["y"] + a["h"] + padding <= b["y"]
        or b["y"] + b["h"] + padding <= a["y"]
    )


def _generate_rooms(width, height, num_rooms):
    """Gera retangulos de sala aleatorios, sem sobreposicao entre eles."""
    rooms = []
    attempts = 0
    max_attempts = num_rooms * 20

    while len(rooms) < num_rooms and attempts < max_attempts:
        attempts += 1
        w = random.randint(MIN_ROOM_SIZE, MAX_ROOM_WIDTH)
        h = random.randint(MIN_ROOM_SIZE, MAX_ROOM_HEIGHT)
        x = random.randint(1, width - w - 2)
        y = random.randint(1, height - h - 2)

        new_room = {"x": x, "y": y, "w": w, "h": h}

        if any(_rooms_overlap(new_room, r) for r in rooms):
            continue

        rooms.append(new_room)

    return rooms


def _carve_room(map_grid, room):
    """Transforma os tiles de uma sala em piso."""
    for y in range(room["y"], room["y"] + room["h"]):
        for x in range(room["x"], room["x"] + room["w"]):
            set_tile(map_grid, x, y, "floor")


def _room_center(room):
    return (room["x"] + room["w"] // 2, room["y"] + room["h"] // 2)


def _carve_horizontal(map_grid, x1, x2, y):
    for x in range(min(x1, x2), max(x1, x2) + 1):
        set_tile(map_grid, x, y, "floor")


def _carve_vertical(map_grid, y1, y2, x):
    for y in range(min(y1, y2), max(y1, y2) + 1):
        set_tile(map_grid, x, y, "floor")


def _carve_corridor(map_grid, start, end):
    """Cria um corredor em L entre dois pontos, conforme 04-geracao-mapas.md."""
    x1, y1 = start
    x2, y2 = end

    if random.choice([True, False]):
        _carve_horizontal(map_grid, x1, x2, y1)
        _carve_vertical(map_grid, y1, y2, x2)
    else:
        _carve_vertical(map_grid, y1, y2, x1)
        _carve_horizontal(map_grid, x1, x2, y2)


def generate_dungeons(width=MAP_WIDTH, height=MAP_HEIGHT):
    """Gera um mapa completo (salas + corredores). Retorna (map_grid, rooms)."""
    map_grid = create_empty_map(width, height)
    num_rooms = random.randint(MIN_ROOMS, MAX_ROOMS)
    rooms = _generate_rooms(width, height, num_rooms)

    for room in rooms:
        _carve_room(map_grid, room)

    for i in range(len(rooms) - 1):
        start = _room_center(rooms[i])
        end = _room_center(rooms[i + 1])
        _carve_corridor(map_grid, start, end)

    return map_grid, rooms