# Manual de Comandos e Mecânicas — Roguelike de Terminal

Documento de referência técnica/completa das mecânicas do jogo. Para uma
versão resumida voltada ao jogador, veja o `README.md`.

## 1. Comandos

| Tecla           | Ação                                                |
|-----------------|-------------------------------------------------------|
| `↑` `↓` `←` `→` | Move o jogador. Se o destino tiver um monstro, ataca em vez de mover |
| `Espaço`        | Passa o turno sem agir (esperar)                       |
| `i`             | Abre/fecha a tela de inventário                         |
| `Enter`         | Confirma seleção (usar/equipar item nos menus, iniciar jogo, reiniciar) |
| `Esc` / `q`     | Cancela, volta ao menu anterior, ou sai do jogo          |
| `S` / `N`       | Responde prompts de sim/não (ex: ativar o Coração Pulsante) |

## 2. Loop de Turno

1. O jogador escolhe uma ação (mover/atacar, usar item, esperar)
2. Cada monstro vivo no andar age em sequência, conforme seu `ai_type`
   e acumulador de energia (velocidade)
3. O ciclo se repete até vitória, derrota, ou saída pro menu

Detalhes completos em `docs/05-combate.md` e `docs/06-entidades.md`.

## 3. Combate

- **Dano:** `max(1, ataque - defesa)`, com variação aleatória de ±20%
- **Morte:** ocorre quando o HP chega a 0 (jogador ou monstro)
- **Permadeath:** ao morrer, a run termina — não há save/load

## 4. Monstros

| Monstro | Símbolo | Comportamento |
|---------|---------|-----------------|
| Perturbado de Energia | `p` | Movimento errático (não persegue de propósito) |
| Mulher Afogada | `w` | Persegue o jogador; foge se ficar com menos de 40% HP |
| O Deus da MOrte (chefe) | `D` | Persegue o jogador; só aparece no andar 4 |

Monstros ficam mais fortes a cada andar (dificuldade progressiva) e podem
reaparecer periodicamente enquanto você explora um andar (respawn a cada
25 turnos, se a quantidade estiver abaixo do limite daquele andar).

## 5. Itens

| Item | Símbolo | Tipo | Efeito |
|------|---------|------|--------|
| Cicatrizante | `!` | Consumível | Cura 4-18HP  (em você mesmo) |
| Instrumental | `/` | Equipável | Reduz 25% a chance de falha de outros itens |
| Machadinha | `\` | Arremessável | 1-6 de dano no monstro mais próximo (alcance 4) |
| Proteção Leve | `[` | Equipável | +5 de defesa |
| Coração Pulsante | `h` | Equipável (reativo) | Reduz dano recebido pela metade, com chance de falha e de ser destruído |

O inventário tem **8 slots**. Itens equipáveis funcionam como um "toggle"
(selecionar equipa, selecionar de novo desequipa) e continuam ocupando
um slot do inventário mesmo enquanto equipados.

Detalhes completos (incluindo a lógica de chance de falha do Coração
Pulsante) em `docs/07-itens.md`.

## 6. Progressão

Não há sistema de níveis/experiência. O jogador fica mais forte
encontrando e equipando itens ao longo da masmorra, enquanto os andares
ficam progressivamente mais difíceis (mais monstros, monstros mais
fortes). Ver `docs/03-arquitetura.md` (nota de balanceamento) para os
valores atuais de atributos.

## 7. Vitória e Derrota
- **Vitória:** chegar ao andar 4 e derrotar O Deus da Morte
- **Derrota:** HP do jogador chega a 0, em qualquer andar
- Em ambos os casos, é possível reiniciar (nova masmorra) ou sair