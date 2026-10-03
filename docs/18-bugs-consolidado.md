# Bugs Consolidados e Priorizados — 4.5

Baseado em `10-bugs-pendentes.md` (gerado ao longo dos testes de 4.1 a 4.4).

## Critério de priorização
- **Crítico:"** causa crash ou quebra uma mecânica central do jogo
- **Médio:** afeta a experiência/clareza, mas não quebra o jogo
- **Cosmético:** visual, não afeta funcionamento

---

## 🔴 Crítico

### C1. Crash com terminal menor que 81x25
`curses.error: addwstr() returned ERR`. Bloqueia o jogo inteiramente em
terminais pequenos. (Origem: 4.3, bug #6)

### C2. Crash em `curses.curs_set(0)` em terminais sem suporte
Jogo fecha ao iniciar em terminais como `vt100`. (Origem: 4.3, bug #9)

### C3. ~~Respawn periódico disparando com mais frequência que o esperado~~ — RESOLVIDO
Causa raiz encontrada: `maybe_respawn_monster` usava o operador bit a bit
`&` em vez do operador de módulo: `%` na checagem do intervalo
(`turn_count & RESPAWN_CHECK_INTERVAL` ao invés de
`turn_count % RESPAWN_CHECK_INTERVAL`). Corrigido em 4.5.

### C4. ~~Monstro aparentando "teleportar" perto do jogador~~ — RESOLVIDO (mesma causa do C3)
Era o mesmo bug do C3: respawn disparando com frequência muito maior que
o esperado, não um problema de distância/teleporte de verdade. Resolvido
junto com C3.

---

## 🟡 Médio

### M1. Prompt do Coração Pulsante inconsistente
Às vezes não aparece ou parece capturar tecla errada — suspeita de
buffer de input acumulado. Afeta uma mecânica central (mas não crasha).
(Origem: playtest 4.2, bug #3)

### M2. Linha "Equipado" corta/some com muitos itens
Informação importante fica ilegível quando o jogador tem vários itens
equipados. (Origem: playtest 4.2, bug #2)

### M3. Paredes pouco visíveis (contrate de cor)
Dificulta a leitura do mapa, mas o jogo continua jogável. (Origem:
playtest 4.2, bug #1)

---

## 🟢 Cosmético

### CO1. Mensagem residual "Setup base OK" piscando
Sobra visual no canto superior esquerdo, não afeta jogabilidade.
(Origem: 4.3, bug #5)

### CO2. Cores inconsistentes no PowerShell
Limitação de compatibilidade específica de terminal — correção pode ser
parcial. (Origem: 4.3, bug #7)

---

## Ordem de correção sugerida
1. C1, C2 (crashes — bloqueiam até testar o resto)
2. C3, C4 (provavelmente a mesma causa raiz — corrigir junto)
3. M1 (mecânica importante)
4. M2, M3 (clareza visual)
5. CO1, CO2 (polimento final)