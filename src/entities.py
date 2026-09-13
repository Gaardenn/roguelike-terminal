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