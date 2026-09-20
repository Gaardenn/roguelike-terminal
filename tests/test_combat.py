"""Testes funcionais de combate com valores extremos (05-combate.md, 07-itens.md)."""

from unittest.mock import patch

from combat import calculate_damage, apply_damage, resolve_attack
from entities import create_entity, create_player, use_consumable, add_item_to_inventory
from items import create_item, ITEM_CICATRIZANTE


def make_entity(hp=10, attack=5, defense=0, name="Teste"):
    return create_entity(name=name, symbol="x", x=0, y=0, hp=hp, attack=attack, defense=defense)


def test_damage_is_never_below_one_event_with_zero_net_attack():
    """Ataque igual a defesa (dano base 0) deve sempre resultar em pelo menos 1 de dano."""
    for _ in range(200):
        damage = calculate_damage(attack=5, defense=5)
        assert damage >= 1


def test_damage_is_never_below_one_when_defense_exceeds_attack():
    """Defesa maior que ataque tambem nunca deve gerar dano zero ou negativo."""
    for _ in range(200):
        damage = calculate_damage(attack=3, defense=20)
        assert damage >= 1


def test_damage_stays_within_expected_variance_range():
    """Dano deve variar dentro da faixa de +-20% (05-combate.md, secao 4),
    com uma folga de arredondamento."""
    attack, defense = 20, 0
    base_damage = attack - defense

    for _ in range(500):
        damage = calculate_damage(attack, defense)
        assert base_damage * 0.8 - 1 <= damage <= base_damage * 1.2 + 1


def test_apply_damage_kills_entity_with_exactly_one_hp():
    """HP = 1 tomando 1 de dano deve morrer, com HP final exatamente 0."""
    entity = make_entity(hp=1)

    died = apply_damage(entity, 1)

    assert died is True
    assert entity["hp"] == 0


def test_apply_damage_does_not_go_negative_with_overkill():
    """HP = 1 tomando dano muito maior que o HP nao deve deixar HP negativo."""
    entity = make_entity(hp=1)

    died = apply_damage(entity, 999)

    assert died is True
    assert entity["hp"] == 0


def test_apply_damage_survives_with_hp_remaining():
    """Dano menor que o HP atual nao deve matar a entidade."""
    entity = make_entity(hp=10)

    died = apply_damage(entity, 3)

    assert died is False
    assert entity["hp"] == 7


def test_resolve_attack_message_reports_death_when_hp_reaches_zero():
    """A mensagem de resolve_attack deve indicar morte quando o HP zera."""
    attacker = make_entity(hp=10, attack=999, name="Atacante")
    defender = make_entity(hp=1, attack=1, defense=0, name="Defensor")

    message, died = resolve_attack(attacker, defender)

    assert died is True
    assert defender["hp"] == 0
    assert "morreu" in message.lower()


def test_resolve_attack_does_not_report_death_when_entity_survives():
    """A mensagem nao deve mencionar morte se a entidade sobreviver."""
    attacker = make_entity(hp=10, attack=1, name="Atacante")
    defender = make_entity(hp=100, attack=1, defense=50, name="Defensor")

    message, died = resolve_attack(attacker, defender)

    assert died is False
    assert "morreu" not in message.lower()


def test_healing_does_not_exceed_max_hp():
    """Cicatrizante nao deve curar acima do HP maximo (07-itens.md, secao 1)."""
    player = create_player(0, 0)
    player["hp"] = player["max_hp"] - 5

    item = create_item(ITEM_CICATRIZANTE)
    add_item_to_inventory(player, item)

    with patch("random.randint", return_value=18):  # forca a cura maxima possivel
        use_consumable(player, slot_index=0)

    assert player["hp"] == player["max_hp"]  # nao ultrapassou o teto


def test_healing_with_full_hp_stays_at_max():
    """Usar Cicatrizante com HP ja cheio nao deve estourar o max_hp."""
    player = create_player(0, 0)
    assert player["hp"] == player["max_hp"]

    item = create_item(ITEM_CICATRIZANTE)
    add_item_to_inventory(player, item)

    with patch("random.randint", return_value=18):
        use_consumable(player, slot_index=0)

    assert player["hp"] == player["max_hp"]


def test_healing_consumes_the_item():
    """Apos usar o Cicatrizante, o slot do inventario deve ficar vazio."""
    player = create_player(0, 0)
    player["hp"] = 5

    item = create_item(ITEM_CICATRIZANTE)
    add_item_to_inventory(player, item)

    use_consumable(player, slot_index=0)

    assert player["inventory"][0] is None