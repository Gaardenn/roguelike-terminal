# Arquitetura e Estruturas de Dados — Roguelike de Terminal

## 1. Estrutura de Dados do Mapa

O mapa é representado como uma **matriz 2D** (lista de listas, `grid[y][x]`),
onde cada posição guarda um **tile**.

Como o jogod não tem fog of war, o mapa inteiro é conhecido pelo jogador
assim que gerado (sem conceito de "explorado" ou "visível" por enquanto).

Cada **tile** guarda:

| Campo       | Tipo            | Descrição                                              |
|-------------|-----------------|---------------------------------------------------------|
| `type`      | string/enum     | Tipo do tile: `"wall"`, `"floor"`, `"stairs"`            |
| `symbol`    | char            | Caractere ASCII usado para renderizar (`#`, `.`, `>`)    |
| `occupant`  | referência/None | Referência à entidade ocupando o tile (jogador/monstro), ou `None` se vazio |
| `item`      | referência/None | Referência a um item no chão nesse tile, ou `None`       |

Exemplo de representação de um tile (como dicionário/objeto):
```
{
  "type":"floor",
  "symbol":".",
  "occupant":None,
  "item":None
}
```

O mapa completo é: `map = [[tile, tile, ...], [tile, tile, ...], ...]`,
acessado como `map[y][x]`.

## 2. Estrutura de Dados das Entidades

Jogador e monstros compartilham uma estrutura comum de **entidade**,
com os seguintes atributos:

| Campo       | Tipo   | Descrição                                      |
|-------------|--------|-------------------------------------------------|
| `name`      | string | Nome da entidade (ex: "Jogador", "Rato")        |
| `symbol`    | char   | Caractere ASCII usado para renderizar (`@`, `r`) |
| `x`, `y`    | int    | Posição atual no mapa                           |
| `hp`        | int    | HP atual                                        |
| `max_hp`    | int    | HP máximo                                       |
| `attack`    | int    | Poder de ataque (usado no cálculo de dano)      |
| `defense`   | int    | Redução de dano recebido                        |
| `is_player` | bool   | Diferencia jogador (`True`) de monstro (`False`) |

Cálculo de dano básico (referência para a etapa de combate, item 2.2 do
roadmap): `dano = max(1, atacante.attack - defensor.defense)`, garantindo
que todo ataque cause ao menos 1 de dano.

Monstros podem ter um campo adicional futuro `ai_typ` (ex: `"chase"`,
`"idle"`) quando a IA for implementada — não é necessário defini-lo ainda,
só reservar o espaço conceitual na estrutura.


**Nota de balanceamento (4.2):** o HP base do jogador foi ajustado de 20
para 28 após playtests mostrarem 0 vitórias em 5 partidas, com mortes
recorrentes por cerco de múltiplos monstros. Ver `09-playtest-log.md`.

## 3. Arquitetura Geral

O projeto usa uma arquitetura de **game loop simples**, sem ECS
(Entity-Component-System). Essa escolha é adequada ao escopo do MVP:
poucos tipos de entidade, poucas mecânicas, e prioridade em terminar rápido.

Estrutura do loop principal (módulo `main`):
```
inicializar jogo (mapa, jogador, monstros)
enquanto jogo estiver rodando:
renderizar tela atual (render)
ler ação do jogador (input)
processar ação do jogador (mover, atacar, usar item, esperar)
se ação envolveu ataque: resolver combate (combat)
processar turno dos monstros (mover/atacar, se aplicável)
verificar condição de vitória/derrota
se vitória ou derrota: mudar estado do jogo (ver diagrama de estados)
```

Cada módulo (`map`, `entities`, `combat`, `render`, `input`) opera sobre
essas estruturas de dados compartilhadas (o mapa e a lista de entidades),
sem necessidade de sistemas separados por componente — a lógica fica
concentrada e simples, alinhada ao restante do escopo do projeto.