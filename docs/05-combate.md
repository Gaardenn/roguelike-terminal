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

## 4. Fórmula de Dano (versão final)

O dano base continua sendo `max(1, atacante.attack - defensor.defense)`,
mas agora com uma variação aleatória de **±20%** aplicada em cima do
resultado, pra evitar que o combate fique previsível demais:
```
dano_base = max(1, atacante.attack - defensor.defense)
variacao = random entre -20% e +20% de dano_base
dano_final = max(1, round(dano_base + variacao))
```

O `max(1, ...)` é aplicado de novo no final pra garantir que a variação
nunca reduza o dano abaixo de 1, mesmo em casos de defesa alta.

Não há chance de erro (miss) nem crítico no MVP — fica registrado como
ideia de backlog, caso o jogo precise de mais profundidade depois.

## 5. Ações Disponíveis no Turno

- **Atacar:** mover-se em direção a um monstro adjacente (não precisa de
  comando separado — é automático ao tentar mover pra cima dele).
- **Usar item:** consumir um item do inventário (ex: poção).
- **Esperar:** passar o turno parado no lugar.

Não existe uma ação formal de "fugir". Se o jogador quiser deixar de lutar
contra um monstro, basta se afastar (mover-se pra longe) — o combate não
"prende" o jogador no lugar. Monstros com IA de perseguição (`ai_type =
"chase"`, ver `03-arquitetura.md`) podem continuar seguindo o jogador,
então fugir de fato depende da velocidade relativa entre os dois.

## 6. Feedback Visual/Textual do Combate

O jogo mantém um **log de mensagens com histórico**, exibindo as últimas
**4 mensagens** na área reservada da tela (ver `08-interface.md`, seção 1).
Mensagens muito longas quebram em múltiplas linhas visuais dentro do
espaço disponível (ver `08-interface.md`, seção 1).

Mensagens mais antigas saem da lista conforme novas são adicionadas
(estrutura tipo fila/lista com tamanho máximo de 5).

Exemplos de mensagens geradas durante o combate:
- `"Você atacou o Rato: 4 de dano."`
- `"O Rato atacou você: 2 de dano."`
- `"O Rato morreu."`
- `"Você morreu."` /  `"Você derrotou o chefe final!"`

Cada ação relevante do turno (ataque, uso de item, morte) gera uma nova
mensagem, adicionada ao topo do log.