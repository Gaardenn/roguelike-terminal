"""Definicao e criacao de itens do jogo, conforme 07-itens.md."""

import random

ITEM_CICATRIZANTE = "cicatrizante"
ITEM_INSTRUMENTAL = "instrumental"
ITEM_MACHADINHA = "machadinha"
ITEM_PROTECAO = "protecao"
ITEM_CORACAO = "coracao"

TYPE_CONSUMABLE = "consumable"
TYPE_EQUIPABLE = "equipable"
TYPE_THROWABLE = "throwable"

ITEM_TEMPLATES = {
    ITEM_CICATRIZANTE: {"name": "Cicatrizante", "symbol": "!", "type": TYPE_CONSUMABLE},
    ITEM_INSTRUMENTAL: {"name": "Instrumental", "symbol": "/", "type": TYPE_EQUIPABLE},
    ITEM_MACHADINHA: {"name": "Machadinha", "symbol": "\\", "type": TYPE_THROWABLE},
    ITEM_PROTECAO: {"name": "Protecao Leve", "symbol": "[", "type": TYPE_EQUIPABLE},
    ITEM_CORACAO: {"name": "Coracao Pulsante", "symbol": "h", "type": TYPE_EQUIPABLE},
}

ALL_ITEM_IDS = list(ITEM_TEMPLATES.keys())

FLOOR_ITEM_RANGES = {
    1: (1, 2),
    2: (1, 3),
    3: (2, 3),
    4: (2, 4),
}


def create_item(item_id):
    """Cria uma instancia de item a partir do seu template base."""
    template = ITEM_TEMPLATES[item_id]
    return {
        "item_id": item_id,
        "name": template["name"],
        "symbol": template["symbol"],
        "type": template["type"],
    }


def _find_free_floor_tile(map_grid, room, max_attempts=20):
    """Tenta achar um tile de piso sem item dentro da sala."""
    for _ in range(max_attempts):
        x = random.randint(room["x"], room["x"] + room["w"] - 1)
        y = random.randint(room["y"], room["y"] + room["h"] - 1)

        tile = map_grid[y][x]
        if tile["type"] == "floor" and tile["item"] is None:
            return x, y

    return None, None


def spawn_items(map_grid, rooms, floor=1):
    """Espalha itens aleatorios pelas salas ao andar (exceto a primeira,
    para nao aparecer em cima do jogador ao entrar). Retorna a lista de
    (x, y, item) criados."""
    items_on_map = []
    eligible_rooms = rooms[1:] if len(rooms) > 1 else rooms

    if not eligible_rooms:
        return items_on_map

    quantity = random.randint(*FLOOR_ITEM_RANGES.get(floor, (1, 2)))

    for _ in range(quantity):
        room = random.choice(eligible_rooms)
        x, y = _find_free_floor_tile(map_grid, room)

        if x is None:
            continue

        item_id = random.choice(ALL_ITEM_IDS)
        item = create_item(item_id)
        map_grid[y][x]["item"] = item
        items_on_map.append((x, y, item))

    return items_on_map