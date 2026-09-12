# Escopo do Projeto — Roguelike de Terminal

## Frase de uma linha
Um roguelike de masmorra em ASCII onde o jogador desce andares gerados proceduralmente, enfrentando monstros em combater por turnos, até alcançar o andar final e vencer — ou morrer na tentativa (permadeath).

## Plataforma-alvo
- Windows, Linux e Mac (via terminal), usando a mesma base de código.

## Linguagem e Bibliotecas
- Linguagem: Python 3
- Biblioteca de terminal: `curses` (nativa no Linux/Mac).

    No Windows, usar o pacot `windows-curses` (via `pip install windows-curses`)

## Features Obrigatória (MVP)
- [ ] Geração procedural de mapa (salas + corredores)
- [ ] Movimento do jogador pelo mapa (4 direções)
- [ ] Um tipo de monstro, com IA simples (persegue o jogador se estiver perto)
- [ ] Combate por turnos (ataque simples, dano com aleatoriedade leve)
- [ ] HP do jogador e do monstro, com morte ao chegar a 0
- [ ] Um item básico (ex: poção de cura)
- [ ] 3 a 5 andares, com dificuldade levemente crescente
- [ ] Tela de vitória (chegar ao último andar) e derrota (HP zerado)
- [ ] HUD simples (HP, andar atual, log de mensagens curto)

## Features Desejáveis (Backlog — pós-MVP)
- [ ] Múltiplos tipos de monstros e itens
- [ ] Sistema de inventário mais completo (múltiplos slots, equipar itens)
- [ ] Sistema de níveis/experiência
- [ ] Save/load de progresso
- [ ] Cores no terminal
- [ ] Mensagens de log com histórico navegável
- [ ] Itens/armadilhas especiais no mapa

## Critério de "Pronto" para a v1
A v1 está pronta quando for possível, do início ao fim, sem crashar:
1. Iniciar o jogo em um menu inicial;
2. Gerar um mapa procedural e se mover por ele;
3. Encontrar e lutar contra ao menos um monstro;
4. Usar ao menos um item;
5. Descer ao menos 3 andares;
6. Ganhar (chegar ao andar final) ou perder (HP zerado) e ver a tela correspondente;
7. Reiniciar ou sair do jogo a partir dessa tela final.