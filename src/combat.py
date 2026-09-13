"""Logica de combate por turnos, conforme 05-combate.md."""


def attempt_attack(attacker, defender):
    """Inicia um ataque entre duas entidades.

    Por enquanto, so registra que o combate comecou (sem calculo de dano
    ainda - isso e implementado no proximo passo). Retorna uma mensagem
    para o log.
    """
    return f"{attacker['name']} ataca {defender['name']}!"