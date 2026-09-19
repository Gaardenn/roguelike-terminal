"""Estrutura de entidades (jogador e monstros), conforme 03-arquitetura.md."""

import random

from map import is_walkable, get_occupant, move_occupant
from combat import calculate_incoming_damage, apply_damage
from items import TYPE_CONSUMABLE, TYPE_EQUIPABLE, TYPE_THROWABLE, ITEM_CICATRIZANTE

INVENTORY_SIZE = 8
ENERGY_THRESHOLD = 100
FLEE_HP_THRESHOLD = 0.3  # 06-entidades.md, secao 5
THROW_RANGE = 4

FLOOR_MONSTER_RANGES = {
    1: (3, 5),
    2: (4, 6),
    3: (5, 7),
    4: (5, 8),
}

FLOOR_WEIGHTS = {
    1: {"perturbado": 0.70, "mulher": 0.30},
    2: {"perturbado": 0.55, "mulher": 0.45},
    3: {"perturbado": 0.40, "mulher": 0.60},
    4: {"perturbado": 0.25, "mulher": 0.75},
}

MIN_ROOM_INDEX_FOR_SPAWN = 2


def create_entity(name, symbol, x, y, hp, attack, defense, speed=100, is_player=False, ai_type=None):
    """Cria uma entidade (jogador ou monstro)."""
    return {
        "name": name,
        "symbol": symbol,
        "x": x,
        "y": y,
        "hp": hp,
        "max_hp": hp,
        "attack": attack,
        "defense": defense,
        "speed": speed,
        "is_player": is_player,
        "ai_type": ai_type,
        "energy": 0,
    }


def create_player(x, y):
    """Cria a entidade do jogador com atributos base e inventario vazio."""
    player = create_entity(
        name="Jogador", symbol="@", x=x, y=y,
        hp=20, attack=4, defense=1, speed=100, is_player=True,
    )
    player["inventory"] = [None] * INVENTORY_SIZE
    player["equipped"] = {"instrumental": None, "protecao": None, "coracao": None}
    player["coracao_uses"] = 0
    return player


DIFFICULTY_SCALING_PER_FLOOR = 0.10  # 3.7: +10% de HP/ataque por andar acima do 1o


def _scale_for_floor(base_value, floor):
    """Aplica o escalonamento leve de dificuldade a um atributo base."""
    multiplier = 1 + (floor - 1) * DIFFICULTY_SCALING_PER_FLOOR
    return max(1, round(base_value * multiplier))


def create_perturbado(x, y, floor=1):
    """Cria um Perturbado de Energia (06-entidades.md, secao 1), escalado pelo andar."""
    return create_entity(
        name="Perturbado de Energia", symbol="p", x=x, y=y,
        hp=_scale_for_floor(8, floor),
        attack=_scale_for_floor(3, floor),
        defense=0, speed=90, ai_type="erratic",
    )


def create_mulher_afogada(x, y, floor=1):
    """Cria uma Mulher Afogada (06-entidades.md, secao 2), escalada pelo andar."""
    return create_entity(
        name="Mulher Afogada", symbol="w", x=x, y=y,
        hp=_scale_for_floor(14, floor),
        attack=_scale_for_floor(5, floor),
        defense=2, speed=100, ai_type="chase",
    )


def create_deus_da_morte(x, y):
    """Cria O Deus da Morte / Parasita de Dimensoes, chefe final (06-entidades.md, secao 3)."""
    return create_entity(
        name="O Deus da Morte", symbol="D", x=x, y=y,
        hp=60, attack=12, defense=4, speed=120, ai_type="chase",
    )


def _find_free_tile_in_room(map_grid, room, max_attempts=20):
    """Tenta achar um tile de piso livre (sem ocupante) dentro da sala."""
    for _ in range(max_attempts):
        x = random.randint(room["x"], room["x"] + room["w"] - 1)
        y = random.randint(room["y"], room["y"] + room["h"] - 1)

        tile = map_grid[y][x]
        if tile["type"] == "floor" and tile["occupant"] is None:
            return x, y

    return None, None


def spawn_monsters(map_grid, rooms, floor=1):
    """Spawna monstros comuns (e o chefe, se for o andar 4)"""
    monsters = []
    eligible_rooms = rooms[MIN_ROOM_INDEX_FOR_SPAWN:]

    if not eligible_rooms:
        return monsters

    quantity = random.randint(*FLOOR_MONSTER_RANGES[floor])
    weights = FLOOR_WEIGHTS[floor]

    for _ in range(quantity):
        room = random.choice(eligible_rooms)
        x, y = _find_free_tile_in_room(map_grid, room)

        if x is None:
            continue

        if random.random() < weights["perturbado"]:
            monster = create_perturbado(x, y, floor=floor)
        else:
            monster = create_mulher_afogada(x, y, floor=floor)

        map_grid[y][x]["occupant"] = monster
        monsters.append(monster)

    if floor == 4:
        boss_room = rooms[-1]
        bx = boss_room["x"] + boss_room["w"] // 2
        by = boss_room["y"] + boss_room["h"] // 2
        boss = create_deus_da_morte(bx, by)
        map_grid[by][bx]["occupant"] = boss
        monsters.append(boss)

    return monsters


def gain_energy(entity):
    """Acumula energia no inicio de cada rodada, conforme 05-combate.md."""
    entity["energy"] += entity["speed"]


def can_act(entity):
    """Retorna True se a entidade tiver energia suficiente para agir."""
    return entity["energy"] >= ENERGY_THRESHOLD


def consume_energy(entity):
    """Consome a energia necessaria para uma acao."""
    entity["energy"] -= ENERGY_THRESHOLD


def get_effective_defense(player):
    """Defesa efetiva do jogador, somando o bonus da Protecao Leve se equipada."""
    bonus = 5 if player["equipped"].get("protecao") is not None else 0
    return player["defense"] + bonus


def add_item_to_inventory(player, item):
    """Adiciona um item ao primeiro slot livre. Retorna True se coube."""
    for i in range(INVENTORY_SIZE):
        if player["inventory"][i] is None:
            player["inventory"][i] = item
            return True
    return False


def toggle_equip(player, slot_index):
    """Equipa ou desequipa o item equipavel no slot informado."""
    item = player["inventory"][slot_index]
    if item is None or item["type"] != TYPE_EQUIPABLE:
        return None

    key = item["item_id"]

    if player["equipped"].get(key) is item:
        player["equipped"][key] = None
        if key == "coracao":
            player["coracao_uses"] = 0
        return f"{item['name']} desequipado."

    player["equipped"][key] = item
    if key == "coracao":
        player["coracao_uses"] = 0
        return f"{item['name']} equipado."


def use_consumable(player, slot_index):
    """Usa um item consumivel (Cicatrizante)."""
    item = player["inventory"][slot_index]
    if item is None or item["type"] != TYPE_CONSUMABLE:
        return None

    if item["item_id"] == ITEM_CICATRIZANTE:
        heal = random.randint(4, 18)
        player["hp"] = min(player["max_hp"], player["hp"] + heal)
        player["inventory"][slot_index] = None
        return f"Voce usa Cicatrizante e recupera {heal} HP."

    return None


def throw_item(player, slot_index, map_grid, monsters):
    """Arremessa um item (Machadinha) no monstro vivo mais proximo dentro do alcance."""
    item = player["inventory"][slot_index]
    if item is None or item["type"] != TYPE_THROWABLE:
        return None

    target = None
    best_dist = None

    for monster in monsters:
        dist = _distance((player["x"], player["y"]), (monster["x"], monster["y"]))
        if dist <= THROW_RANGE and (best_dist is None or dist < best_dist):
            best_dist = dist
            target = monster

    if target is None:
        return "Nenhum alvo ao alcance"

    damage = random.randint(1, 6)
    target["hp"] -= damage
    player["inventory"][slot_index] = None

    message = f"Voce arremessa {item['name']} em {target['name']}: {damage} de dano."

    if target["hp"] <= 0:
        target["hp"] = 0
        map_grid[target["y"]][target["x"]]["occupant"] = None
        monsters.remove(target)
        message += f" {target['name']} morreu."

    return message


def _distance(pos_a, pos_b):
    """Distancia Manhattan entre duas posicoes."""
    return abs(pos_a[0] - pos_b[0]) + abs(pos_a[1] - pos_b[1])


def _step_towards(mx, my, tx, ty):
    """Calcula um passo (dx, dy) na direcao do alvo, um eixo por vez."""
    dx = 1 if tx > mx else -1 if tx < mx else 0
    dy = 1 if ty > my else -1 if ty < my else 0

    if dx != 0 and dy != 0:
        if random.choice([True, False]):
            dy = 0
        else:
            dx = 0

    return dx, dy


def _random_step():
    """Passo aleatorio, para o comportamento 'erratic'."""
    return random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])


def monster_take_turn(monster, player, map_grid, on_player_damage=None):
    """Executa a acao de um monstro no turno dele, conforme ai_type
    (06-entidades.md, secao 5). Retorna (mensagem, jogador_morreu).
    """
    if monster["hp"] <= 0:
        return None, False

    is_adjacent = _distance((monster["x"], monster["y"]), (player["x"], player["y"])) == 1

    if is_adjacent:
        effective_defense = get_effective_defense(player)
        raw_damage = calculate_incoming_damage(monster, effective_defense)

        if on_player_damage is not None:
            final_damage, extra_message = on_player_damage(raw_damage)
        else:
            final_damage, extra_message = raw_damage, ""

        died = apply_damage(player, final_damage)
        message = f"{monster['name']} atacou {player['name']}: {final_damage} de dano.{extra_message}"
        if died:
            message += " Voce morreu."

        return message, died

    ai_type = monster["ai_type"]
    is_fleeing = monster["hp"] < monster["max_hp"] * FLEE_HP_THRESHOLD and ai_type == "chase"

    if is_fleeing:
        dx, dy = _step_towards(monster["x"], monster["y"], player["x"], player["y"])
        dx, dy = -dx, -dy
    elif ai_type == "chase":
        dx, dy = _step_towards(monster["x"], monster["y"], player["x"], player["y"])
    elif ai_type == "erratic":
        dx, dy = _random_step()
    else:
        dx, dy = (0, 0)

    new_x = monster["x"] + dx
    new_y = monster["y"] + dy

    if (dx != 0 or dy != 0) and is_walkable(map_grid, new_x, new_y) \
            and get_occupant(map_grid, new_x, new_y) is None:
        move_occupant(map_grid, monster, new_x, new_y)

    return None, False

TOTAL_FLOORS = 4


def descend_floor(player, map_grid, current_floor):
    """Gera o proximo andar, reposiciona o jogador e retorna os novos
    dados do jogo: (novo_map, novos_rooms, novos_monstros, novo_andar).
    
    O jogador mantem HP, inventario e equipamentos entre andares -
    so o mapa e os monstros/itens sao regenerados (04-geracao-mapas.md).
    """
    from map import generate_dungeon
    from items import spawn_items

    next_floor = current_floor + 1
    new_map, new_rooms, player_start = generate_dungeon()

    player["x"], player["y"] = player_start
    new_map[player["y"]][player["x"]]["occupant"] = player

    new_monsters = spawn_monsters(new_map, new_rooms, floor=next_floor)
    spawn_items(new_map, new_rooms, floor=next_floor)

    return new_map, new_rooms, new_monsters, next_floor

RESPAWN_CHECK_INTERVAL = 15  # 04-geracao-mapas.md, secao 6


def maybe_respawn_monster(map_grid, rooms, monsters, floor, turn_count):
    """A cada RESPAWN_CHECK_INTERVAL turnos, spawna 1 novo monstro se a
    quantidade viva estiver abaixo do maximo da faixa do andar
    (04-geracao-mapas.md, secao 6). Retorna o monstro criado, ou None.
    """
    if turn_count & RESPAWN_CHECK_INTERVAL != 0:
        return None

    _min_range, max_range = FLOOR_MONSTER_RANGES[floor]

    living_common_monsters = [m for m in monsters if m["name"] != "O Deus da Morte"]
    if len(living_common_monsters) >= max_range:
        return None

    eligible_rooms = rooms[MIN_ROOM_INDEX_FOR_SPAWN:]
    if not eligible_rooms:
        return None

    room = random.choice(eligible_rooms)
    x, y = _find_free_tile_in_room(map_grid, room)
    if x is None:
        return None

    weights = FLOOR_WEIGHTS[floor]
    if random.random() < weights["perturbado"]:
        monster = create_perturbado(x, y, floor=floor)
    else:
        monster = create_mulher_afogada(x, y, floor=floor)

    map_grid[y][x]["occupant"] = monster
    monsters.append(monster)
    return monster