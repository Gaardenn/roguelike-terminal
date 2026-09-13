# Geração Procedural de Mapas — Roguelike de Terminal

## 1. Algoritmo

**Salas + Corredores simples**, no estilo do Rogue clássico:

1. Gerar um número aleatório de salas retangulares (com largura/altura
dentro de uma faixa razoável), em posições aleatórias no grid, evitando
sobreposição entre elas.
2. Conectar as salas **em sequência** (sala 1 → sala 2 → sala 3 → ...),
ligando o centro de uma sala ao centro da próxima.
3. Cada conexão é um **corredor em L**: primeiro anda na horizontal até
  alinhar com a coluna da sala de destino, depois anda na vertical (ou
  vice-versa, escolhido aleatoriamente) até alcançá-la.

Esse método já garante conectividade por construção (toda sala tem pelo
menos um caminho até as outras), mas ainda assim será validado (ver item 5).

## 2. Tamanho da Masmorra e Número de Andares

- **Tamanho do mapa:** 80 colunas x 24 linhas (cabe inteiro num terminal
  padrão, sem necessidade de câmera/scroll). Um pequeno espaço da tela
  fica reservado pro HUD (status do jogador e log de mensagens), então o
  grid de jogo em si deve ocupar algo como 80x20, com as 4 linhas restantes
  para a interface.
- **Número de andares:** 4 andares fixos, com dificuldade crescente do
  andar 1 ao 4. O andar 4 contém o chefe final (ver GDD, seção de vitória).

## 3. Regras de Conexão entre Salas

- Corredores são sempre **retos em L** (um segmento horizontal + um
  vertical), nunca diagonais ou tortos.
- Cada sala se conecta a pelo menos a sala anterior e a próxima na sequência
  de geração (garantindo uma "espinha dorsal" percorrível).
- Não há requisito de conexões extras/loops no MVP — isso pode entrar no
  backlog como melhoria de variedade de exploração.

## 4. Posições Especiais

- **Entrada:** centro da primeira sala gerada. É onde o jogador aparece
  ao entrar no andar.`
- **Saída/escada:** centro da última sala gerada (ou, no andar 4, a sala
  onde o chefe final é posicionado).
- **Monstros e tesouros:** distribuídos em quantidade **aleatória dentro
  de uma faixa crescente por andar**, em posições aleatórias dentro das
  salas (exceto na sala de entrada, pra não spawnar em cima do jogador):

  | Andar | Monstros | Tesouros (itens) |
  |-------|----------|-------------------|
  | 1     | 3 a 5    | 1 a 2             |
  | 2     | 4 a 6    | 1 a 3             |
  | 3     | 5 a 7    | 2 a 3             |
  | 4     | 5 a 8 + chefe | 2 a 4        |

## 5. Validação de Conectividade

Após gerar o mapa (salas, corredores e posições especiais), rodar uma
validação por **flood fill** (busca em largura/profundidade a partir da
entrada) sobre os tiles de piso (`floor`). Se algum tile relevante (saída,
sala com monstro/tesouro) não for alcançado pelo flood fill, o mapa é
**descartado e regenerado do zero**, até passar na validação.

Essa checagem é uma segurança extra: mesmo a geração por construção já
devendo garantir conectividade, o flood fill garante que nenhum bug de
sobreposição de salas ou corredor mal calculado deixe algo inacessível.

## 6. Regras de Spawn de Monstros

### Spawn Inicial
Ao gerar um andar, os monstros são posicionados em salas aleatórias,
respeitando as faixas de quantidade e proporção de tipo já definidas
(seção 4 deste documento e `06-entidades.md`, seção 4).

**Distância mínima da entrada:** nenhum monstro pode spawnar nas duas
primeiras salas da sequência de geração (contando a partir da sala de
entrada, índice 0). Ou seja, monstros só spawnam a partir da 3ª sala
gerada em diante, dando um espaço inicial seguro pro jogador se orientar.

O chefe final (andar 4) é exceção: sempre spawna fixo na última sala
(sala de saída), independente dessa regra.

### Respawn Periódico
Enquanto o jogador estiver no mesmo andar, o jogo verifica periodicamente
se deve gerar novos monstros, simulando uma masmorra "viva":

- **Intervalo de verificação:** a cada **15 turnos** do jogador.
- **Condição:** só spawna um novo monstro se a quantidade de monstros
  vivos no andar estiver **abaixo do limite máximo** da faixa daquele
  andar (ex: andar 1 tem no máximo 5 — se houver 3 vivos, pode spawnar
  até 2 novos ao longo do tempo).
- **Quando ocorre:** se a condição for satisfeita, spawna **1 monstro**
  por verificação (não vários de uma vez), respeitando a mesma regra de
  distância mínima da entrada e a mesma proporção de tipos da tabela do
  andar atual.
- **Chefe final:** nunca sofre respawn (é único, fixo no andar 4).

Essa regra incentiva o jogador a não demorar excessivamente em um andar, sem punir exploração moderada.