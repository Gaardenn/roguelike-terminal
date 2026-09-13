# Itens — Roguelike de Terminal

Cada item tem um `type` (categoria de uso) que vai orientar o sistema de
inventário e uso (definidos nos próximos itens da 2.4).

## 1. Cicatrizante

> Um spray contendo um remédio com potente efeito cicatrizante.

| Atributo    | Valor                                                        |
|-------------|---------------------------------------------------------------|
| `symbol`    | `!`                                                            |
| `type`      | Consumível (uso único, some após usar)                        |
| `effect`    | Cura entre **4 e 18 HP** (aleatório), aplicável em si mesmo ou em um ser adjacente |
| `cost`      | Gasta 1 ação do turno + o próprio item                         |

## 2. Instrumental

> Melhoria que aumenta a precisão no manuseio de itens.

| Atributo    | Valor                                                        |
|-------------|---------------------------------------------------------------|
| `symbol`    | `/`                                                             |
| `type`      | Equipável — permanente (não se gasta ao usar)                  |
| `effect`    | Reduz em **25%** a chance de falha ao usar qualquer item que tenha chance de falha (ex: Coração Pulsante) |

## 3. Machadinha

> Ferramenta comum em fazendas e canteiros de obra, usada para cortar madeira — mas serve bem como arma de arremesso.

| Atributo         | Valor                                          |
|------------------|--------------------------------------------------|
| `symbol`         | `\`                                              |
| `type`           | Arremessável (consumível ao ser lançada)          |
| `damage`         | **1 a 6** (aleatório)                             |
| `throw_range`    | **4 tiles** de alcance                            |
| `effect`         | Ao arremessar, causa dano à distância no monstro atingido; o item é perdido após o lançamento (não pode ser recuperado no MVP) |

## 4. Proteção Leve

> Uma jaqueta de couro pesada, ou um colete à prova de balas — do tipo usado por seguranças e policiais.

| Atributo    | Valor                                     |
|-------------|---------------------------------------------|
| `symbol`    | `[`                                          |
| `type`      | Equipável — permanente                       |
| `effect`    | `+5` de defesa enquanto equipado             |

## 5. Coração Pulsante

> Um coração humano banhado em sangue, pulsando como se ainda estivesse dentro de um corpo.

| Atributo         | Valor                                                                 |
|------------------|--------------------------------------------------------------------------|
| `symbol`         | `♥` (ou `h`, se o terminal não suportar o símbolo)                       |
| `type`           | Equipável — reativo (ação especial ao tomar dano)                        |
| `effect`         | Ao tomar dano, o jogador pode optar por "espremer" o coração para **reduzir o dano recebido pela metade** |
| `fail_chance`    | Começa em **75%** de chance de falha na primeira ativação. Se usar novamente depois (mesmo se a primeira tiver funcionado), a chance de falha sobe para **100%** na segunda ativação |
| `on_fail`        | Se a ativação falhar, o item é **destruído e perdido**, mesmo sem produzir efeito nenhum |
| `interaction`    | O item **Instrumental** reduz esse `fail_chance` em 25 pontos percentuais (ex: 75% → 50% na primeira ativação) |

Resumindo o Coração Pulsante: na prática, é uma aposta arriscada — 25% de
chance de funcionar na primeira vez (ou 50% se tiver o Instrumental
equipado), e praticamente garantido que se perca no uso seguinte.