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

## 6. Crash com terminal menor que 81x25 (4.3)
O jogo assume tamanho fixo de tela (80 colunas x 24 linhas), mas o
`curses` na prática precisa de **81x25** para não travar (comportamento
conhecido do curses: a ultima celula do canto inferior direito da janela
nao pode ser escrita livremente sem tratamento especial, entao o jogo
precisa de uma linha/coluna de folga). Confirmado nos testes de 4.3:
exatamente 80x24 já falha; funciona a partir de 81x25. Janelas menores
(ex: 60x20) e redimensionamento em tempo real para abaixo do mínimo
também causam o mesmo crash (`addwstr() returned ERR`).
Precisa de uma checagem no início (`curses.LINES >= 25` e `curses.COLS >= 81`) com mensagem amigável pedindo para redimensionar,
em vez de crashar - e essa checagem deveria rodar continuamente durante
o jogo, não só na abertura, já que redimensionar em tempo real também
quebra.

## 7. Cores inconsistentes no PowerShell (Windows) (4.3)
Alguns pares de cor não aparecem corretamente no PowerShell (itens e HP
médio ficam brancos; Perturbado de Energia fica invisível mesmo tendo
cor diferente do fundo.) Suspeita: limitação do `windows-curses` com
`use_default_colors()` nesse terminal específico. Precisa de investigação
mais profunda — pode não ter solução 100% garantida entre todos os
terminais Windows.


## 8. Respawn periódico disparando com mais frequência que o esperado (4.3)
Relato no teste de tamanho de janela: monstros parecem respawnar a cada
poucos turnos (relatado como "de 2 em 2"), não a cada 25 turnos como
configurado em `RESPAWN_CHECK_INTERVAL` (`src/entities.py`).

**Hipóteste a investigar:** o contador `turn_count` em `main.py` só deveria
incrementar uma vez por turno real do jogador (dentro do bloco
`if turn_taken and running:`). Possíveis causas a checar:
- Alguma chamada duplicada de `maybe_respawn_monster` em outro ponto do
  código além do loop principal.
- O jogador percebendo turnos passando rápido (ex: segurando uma tecla
  de movimento) sem perceber que já passaram 25 ações, gerando uma falsa
  impressão de frequência maior.
- `turn_count` sendo resetado incorretamente em algum outro fluxo (ex:
  ao abrir/fechar o inventário, que não deveria mexer no contador).

Precisa de investigação com prints/logs de debug temporários na 4.5,
rastreando o valor de `turn_count` a cada chamada.


## 9. Crash em `curses.curs_set(0)` em terminais sem suporte a esse controle (4.3)
Testado com `TERM=vt100`, o jogo crasha logo no início, na chamada
`curses.curs_set(0)` em `main.py` (usada para esconder o cursor). Isso
acontece porque `curs_set()` lança `curses.error` quando o terminal não
suporta a visibilidade de cursor solicitada — não é especificamente sobre
cor, mas impediu completar o teste 4.3 "com/sem suporte a cores"
(`13-teste-cores.md`).

**Correção sugerida:** envolver a chamada em `try/except curses.error:
pass`, já que esconder o cursor é algo "bom ter" mas não essencial pro
jogo funcionar.

**Pendência adicional:** depois de corrigir esse crash, refazer o teste
de "com/sem suporte a cores" (`13-teste-cores.md`), que não pôde ser
completado por causa desse bug.