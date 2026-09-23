# Bugs Pendentes — Registrados no Playtest (09-playtest-log.md)

Pendências para resolver na etapa 4.5 (Correção de Bugs).

## 1. Paredes pouco visíveis
Cor das paredes (`COLOR_WALL`, preto) se mistura com o fundo escuro de
muitos terminais. Precisa de uma cor com mais contraste (ex: cinza claro
explícito, em vez de depender da cor padrão do terminal).

## 2. Linha "Equipado" corta/some com muitos itens
Diferente do log de mensagens (que já tem quebra de linha, ver
`08-interface.md` + correção do polimento de interface), a linha de
status "Equipado: ..." ainda usa `[:39]` (corte simples), fazendo nomes
sumirem quando há vários itens equipados.

## 3. Prompt do Coração Pulsante inconsistente
Relato: às vezes o monstro ataca e o prompt "Espremer Coração Pulsante?"
não aparece, ou parece capturar uma tecla que não era a resposta
pretendida. Suspeita: buffer de input do curses acumulando teclas
digitadas rapidamente antes do prompt aparecer. Investigar uso de
`curses.flushinp()` antes de `stdscr.getch()` no prompt.

## 4. Monstro parecendo "teleportar" perto do jogador
Relato pontual (partida 3): jogador longe de qualquer Mulher Afogada,
mas ao se mover already levou ataque. Susperita principal: respawn
periódico posicionando um monstro em sala adjacente à posição atual do
jogador, sem checagem de distância mínima do jogador (a regra de
distância mínima da entrada, em `04-geracao-mapas.md`, não cobre a
posição atual do jogador durante o respawn, só a sala de entrada do
andar). Investigar se `maybe_respawn_monster` precisa de uma checagem
extra de distância em relação à posição atual do jogador.


## 5. Mensagem resídual "Setup base OK" piscando (4.3)
Sobrou de um teste manual da 3.1 (Setup Base): `render_blank_screen` ainda
tem `stdscr.addstr(0, 0, "Setup base OK - pressione ESC para sair")`,
redesenhada a cada frame por cima do mapa. Precisa ser removida.

## 6. Crash com terminal menor que 80x24 (4.3)
O jogo assume tamanho fixo de tela (80 colunas x 24 linhas) e não valida
o tamanho real da janela do terminal antes de rodar. Em janelas menores,
`curses` lança `addwstr() returned ERR` e o jogo fecha com traceback.
Precisa de uma checagem no início (`curses.LINES`, `curses.COLS`) com
mensagem amigável pedindo para redimensionar, em vez de crashar.

## 7. Cores inconsistentes no PowerShell (Windows) (4.3)
Alguns pares de cor não aparecem corretamente no PowerShell (itens e HP
médio ficam brancos; Perturbado de Energia fica invisível mesmo tendo
cor diferente do fundo.) Suspeita: limitação do `windows-curses` com
`use_default_colors()` nesse terminal específico. Precisa de investigação
mais profunda — pode não ter solução 100% garantida entre todos os
terminais Windows.