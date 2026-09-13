import random
"""Estrutura de entidades (jogador e monstros), conforme 03-arquitetura.md."""


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
    """Cria a entidade do jogador com atributos base."""
    return create_entity(
        name="Jogador",
        symbol="@",
        x=x,
        y=y,
        hp=20,
        attack=4,
        defense=1,
        speed=100,
        is_player=True,
    )

def create_perturbado(x, y):
    """Cria um Perturbado de Energia (06-entidades.md, secao 1)."""
    return create_entity(
        name="Perturbado de Energia",
        symbol="p",
        x=x,
        y=y,
        hp=8,
        attack=3,
        defense=0,
        speed=90,
        ai_type="erratic",
    )


def create_mulher_afogada(x, y):
    """Cria uma Mulher Afogada (06-entidades.md, secao 2)."""
    return create_entity(
        name="Mulher Afogada",
        symbol="w",
        x=x,
        y=y,
        hp=13,
        attack=5,
        defense=2,
        speed=100,
        ai_type="chase",
    )


def create_deus_da_morte(x, y):
    """Cria O Deus da Morte / Parasita de Dimensoes, chefe final (06-entidades.md, secao 3)."""
    return create_entity(
        name="O Deus da Morte",
        symbol="D",
        x=x,
        y=y,
        hp=60,
        attack=12,
        defense=4,
        speed=120,
        ai_type="chase",
    )

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

MIN_ROOM_INDEX_FOR_SPAWN = 2 # nao spawna nas duas primeiras salas (04-geracao-mapas.md)


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
    """Spawna monstros comuns (e o chefe, se for o andar 4), respeitando
    as faixas de quantidade e proporcao definidas em 04-geracao-mapas.md
    e 06-entidades.md. Retorna a lista de monstros criados.
    """
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
            continue  # sala sem espaco livre, pula esse spawn

        if random.random() < weights["perturbado"]:
            monster = create_perturbado(x, y)
        else:
            monster = create_mulher_afogada(x, y)

        map_grid[y][x]["occupant"] = monster
        monsters.append(monster)

    if floor == 4:
        boss_room = rooms[-1]
        bx, by = _room_center(boss_room) if "_room_center" in globals() else (
            boss_room["x"] + boss_room["w"] // 2,
            boss_room["y"] + boss_room["h"] // 2,
        )
        boss = create_deus_da_morte(bx, by)
        map_grid[by][bx]["occupant"] = boss
        monsters.append(boss)

    return monsters

ENERGY_THRESHOLD = 100


def gain_energy(entity):
    """Acumula energia no inicio de cada rodada, conforme 05-combate.md."""
    entity["energy"] += entity["speed"]


def can_act(entity):
    """Retorna True se a entidade tiver energia suficiente para agir."""
    return entity["energy"] >= ENERGY_THRESHOLD


def consume_energy(entity):
    """Consome a energia necessaria para uma acao."""
    entity["energy"] -= ENERGY_THRESHOLD


def monster_take_turn(monster, player, map_grid):
    """Executa a acao de um monstro no turno dele.
    
    Ainda e um placeholder - o comportamento de IA de verdade (chase,
    erratic, flee) e implementado no proximo passo do roadmap
    """
    pass