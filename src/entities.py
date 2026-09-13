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