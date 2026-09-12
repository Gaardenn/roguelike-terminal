# Documento de Design (GDD Simplificado) — Roguelike de Terminal

## 1. Loop Principal do Jogo

O jogo funciona em **turnos**: o tempo só passa quando o jogador age.
A cada turno, o jogador escolhe **uma** das seguintes ações:

1. **Mover-se** (cima, baixo, esquerda, direita)
    - Se o destino tiver um monstro, o movimento vira um **ataque** (entra em combate).
    - Se o destino for parede, a ação é inválida (não gasta turno).
2. **Atacar** (implícito ao mover-se em direção a um monstro adjacente)
3. **Usar item** (ex: beber poção do inventário)
4. **Esperar** (passar o turno parado, sem se mover)

Após a ação do jogador, todos os monstros vivos no andar agem uma vez
(perseguir o jogador, atacar se adjacente, ou ficar parados, dependendo da IA).
Esse ciclo se repete até o jogador vencer, morrer, ou sair do jogo.

Fora do combate, o jogador também pode:
- Pisar em itens para coletá-los automaticamente
- Pisar na escada para descer de andar (se já tiver explorado o suficiente/decidido ir)

## 2. Condições de Vitória e Derrota

### Vitória
O jogador vence ao **chegar ao último andar da masmorra E derrotar o chefe final** presente nesse andar. Ao derrotá-lo, o jogo exibe a tela de vitória.

### Derrota
O jogador perde quando seu **HP chega a 0**, em qualquer andar, seja por ataque de monstro comum ou do chefe.

### Permadeath
Ao morrer, **não há continuar**: o jogo exibe a tela de game over e, a partir dela, só é possível **reiniciar do zero** (nova masmorra gerada, novo personagem) ou sair. Não existe save de prograsso a meio da run.

## 3. Sistema de Progressão

O jogador **não tem sistema de níveis/experiência** (isso fica pro backlog).
Em vez disso, a progressão acontece de duas formas:

- **Jogador fica mais forte:** ao encontrar e usar itens (ex: poções permanentes, equipamentos), atributos como HP máximo e ataque podem aumentar.
- **Andares ficam mais difíceis:** a cada andar, a quantidade e/ou força dos monstros aumenta levemente, criando uma curva de dificuldade crescente até o chefe final.

O equilíbrio do jogo depende do jogador conseguir itens suficientes ao longo da descida para companhar o aumento de dificuldade dos andares.

## 4. Tom e Estética

O jogo tem tom **sério e sombrio**: a masmorra é um lugar ameaçador, sem alívio cômico. Mesmo sendo puramente em ASCII (minimalista visualmente), os textos (mensagens de log, descrições, nome de monstros/itens) devem
reforçar esse clima pesado — evitar humor ou leveza no texto.

## 5. Referências

- **Rogue (1980):** referência mecânica principal. Base para o loop de turnos, geração de mapa em salas+corredores, e simplicidade geral do
    sistema. É o modelo a seguir para manter o escopo enxuto.
- **Brogue:** referência de atmosfera e "elegância minimalista" — usar
  como inspiração para nomear itens/monstros e escrever mensagens de log
  com peso narrativo, mesmo dentro de um sistema simples.
- NetHack e DCSS **não** são referências diretas neste projeto — sua
  complexidade foge do escopo definido (MVP simples).