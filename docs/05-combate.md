# Sistema de Combate por Turnos — Roguelike de Terminal

## 1. Atributos de Combate

Além dos atributos já definidos em `03-arquitetura.md` (`hp`, `max_hp`,
`attack`, `defense`), as entidades ganham mais um:

| Campo    | Tipo | Descrição                                                |
|----------|------|------------------------------------------------------------|
| `speed`  | int  | Velocidade da entidade. Base = 100 (velocidade "normal")    |

O `speed` não decide quem age primeiro (isso é fixo, ver seção 2), mas
sim **quantas vezes** a entidade age por rodada, através de um acumulador
de energia:

- Cada entidade tem um contador interno `energy`, iniciando em 0.
- A cada rodada, soma-se `speed` ao `energy` da entidade.
- Enquanto `energy >= 100`, a entidade realiza uma ação e subtrai 100 do `energy`.

Exemplos:
- `speed = 100` → age exatamente 1 vez por rodada (comportamento padrão).
- `speed = 150` → acumula 150, age 1 vez, sobra 50; na rodada seguinte
  acumula mais 150 (total 200), age 2 vezes seguidas, sobra 0. Ou seja,
  a cada 2 rodadas, age 3 vezes — mais rápido que o normal.
- `speed = 50` → acumula 50 numa rodada (não age), na próxima acumula
  100 (age 1 vez). Ou seja, age a cada 2 rodadas — mais lento.

O jogador tem `speed = 100` fixo (não varia). Apenas monstros podem ter velocidades diferentes, definidas individualmente conforme o tipo.

## 2. Ordem dos Turnos

A ordem dentro de cada rodada é **fixa e simples**, sem depender de velocidade:

1. **Jogador age primeiro** (move, ataca, usa item, ou espera).
2. **Depois, cada monstro vivo age**, na ordem em que foi criado no andar,
  respeitando seu acumulador de energia (podendo agir 0, 1 ou mais vezes
  naquela rodada, conforme a seção 1).

Esse fluxo já está alinhado com o loop principal descrito em
`03-arquitetura.md`. A única mudança é que o passo "processar turno dos
monstros" agora consulta o acumulador de energia de cada um antes de
decidir se ele age ou não naquela rodada.

## 3. Resolução de um Ataque

Quando uma entidade ataca outra (jogador → monstro ou monstro → jogador),
usa-se a fórmula já definida em `03-arquitetura.md`:
```
dano = max(1, atacante.attack - defensor.defense)
defensor.hp -= dano
```

Se `defensor.hp <= 0` após o ataque, a entidade morre (ver GDD, seção de
condições de derrota/vitória para o caso do jogador ou do chefe final).