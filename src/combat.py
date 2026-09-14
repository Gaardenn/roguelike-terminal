"""Logica de combate por turnos, conforme 05-combate.md."""

import random

DAMAGE_VARIANCE = 0.2


def calculate_damage(attack, defense):
    """Calcula o dano final com variacao aleatoria de +-20% (05-combate.md, secao 4)."""
    base_damage = max(1, attack - defense)
    variance = random.uniform(-DAMAGE_VARIANCE, DAMAGE_VARIANCE) * base_damage
    return max(1, round(base_damage + variance))


def calculate_incoming_damage(attacker, defense):
    """Calcula o dano de 'attacker' contra uma defesa especifica (permite
    usar a defesa efetiva do jogador, incluindo bonus de equipamento)."""
    return calculate_damage(attacker["attack"], defense)


def apply_damage(defender, damage):
    """Aplica dano a uma entidade. Retorna True se ela morreu."""
    defender["hp"] -= damage
    died = defender["hp"] <= 0
    if died:
        defender["hp"] = 0
    return died


def resolve_attack(attacker, defender, defender_defense=None):
    """Resolve um ataque completo: calcula dano, aplica e monta a mensagem.
    Retorna (mensagem, defensor_morreu)."""
    defense = defender_defense if defender_defense is not None else defender["defense"]
    damage = calculate_damage(attacker["attack"], defense)
    died = apply_damage(defender, damage)

    message = f"{attacker['name']} atacou {defender['name']}: {damage} de dano."
    if died:
        message += f" {defender['name']} morreu."

    return message, died