"""Logica de combate por turnos, conforme 05-combate.md."""

import random

DAMAGE_VARIANCE = 0.2


def calculate_damage(attacker, defender):
    """Calcula o dano final de um ataque, com variacao aleatoria de +-20%
    (05-combate.md, secao 4)."""
    base_damage = max(1, attacker["attack"] - defender["defense"])
    variance = random.uniform(-DAMAGE_VARIANCE, DAMAGE_VARIANCE) * base_damage
    return max(1, round(base_damage + variance))


def resolve_attack(attacker, defender):
    """Resolve um ataque entre duas entidades, aplicando dano e checando morte.
    
    Retorna (mensagem, defensor_morreu).
    """
    damage = calculate_damage(attacker, defender)
    defender["hp"] -= damage

    message = f"{attacker['name']} atacou {defender['name']}: {damage} de dano."

    died = defender["hp"] <= 0
    if died:
        defender["hp"] = 0
        message += f" {defender['name']} morreu."

    return message, died