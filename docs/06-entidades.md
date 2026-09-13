# Entidades e Inimigos — Roguelike de Terminal

Todos os monstros seguem a estrutura de entidade definida em
`03-arquitetura.md` (`name`, `symbol`, `x`, `y`, `hp`, `max_hp`, `attack`,
`defense`, `speed`, `ai_type`).

## 1. Perturbado de Energia (monstro comum — fraco)

> Uma alma enlouquecida de forma brusca, cuja psique se esvaiu antes de
> perceber que não está mais viva. Uma forma plasmática inconsistente,
> confusa e desesperada.

| Atributo   | Valor       |
|------------|-------------|
| `symbol`   | `p`         |
| `hp`       | 8           |
| `attack`   | 3           |
| `defense`  | 0           |
| `speed`    | 90 (levemente lento — sua confusão o atrasa) |
| `ai_type`  | `"erratic"` |

**Comportamento (`erratic`):** a cada turno, tem alta chance de se mover
em uma direção aleatória, ignorando a posição do jogador. Só ataca se
o jogador acabar adjacente a ele (por acaso, ou porque o jogador se
aproximou). Não persegue de forma deliberada.

**Aparece em:** todos os 4 andares, com maior concentração nos andares iniciais (1 e 2).

## 2. Mulher Afogada (monstro comum — moderado)

> Uma lenda urbana que ganhou proporções terríveis: a lembrança de algo
> que deveria ser só um aviso, agora manifestada como uma ameaça real e
> deliberada.

| Atributo   | Valor       |
|------------|-------------|
| `symbol`   | `w`         |
| `hp`       | 14          |
| `attack`   | 5           |
| `defense`  | 2           |
| `speed`    | 100         |
| `ai_type`  | `"chase"`   |

**Comportamento (`chase`):** persegue o jogador ativamente quando o
percebe (dentro de um raio de detecção), de forma direta e implacável.

**Aparece em:** todos os 4 andares, com maior concentração nos andares
finais (3 e 4).

## 3. O Deus da Morte / Parasita de Dimensões (chefe final)

> Uma entidade suprema que se manifesta em forma disforme, infectando o
> ambiente ao redor ao consumir a entropia — a energia potencial e o
> tempo de tudo que é vivo.

| Atributo   | Valor       |
|------------|-------------|
| `symbol`   | `D`         |
| `hp`       | 60          |
| `attack`   | 12          |
| `defense`  | 4           |
| `speed`    | 120 (mais rápido que o normal — age mais de uma vez por rodada, ver `05-combate.md`) |
| `ai_type`  | `"chase"`   |

**Comportamento:** persegue o jogador de forma agressiva e implacável,
sem padrão especial de atque no MVP (habilidades únicas — como drenar
HP à distância — ficam registradas como ideia de backlog).

**Aparece em:** exclusivamente no andar 4, na sala final. Derrotá-lo é a
condição de vitória do jogo (ver `02-gdd.md`).

## 4. Distribuição por Andar
A quantidade total de monstros por andar segue a tabela já definida em
`04-geracao-mapas.md`. Dentro desse total, a proporção entre os dois
tipos comuns muda conforme o andar:
| Andar | Peso Perturbado de Energia | Peso Mulher Afogada |
|-------|------------------------------|------------------------|
| 1     | 70%                          | 30%                    |
| 2     | 55%                          | 45%                    |
| 3     | 40%                          | 60%                    |
| 4     | 25%                          | 75% (+ chefe fixo)     |

Ao gerar os monstros de um andar (dentro da faixa de quantidade da tabela
de `04-geracao-mapas.md`), cada monstro sorteado tem essa chance percentual
de ser um tipo ou outro.