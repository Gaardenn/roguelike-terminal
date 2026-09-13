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

## 6. Sistema de Inventário

### Limite
O inventário do jogador tem **8 slots**. Cada item (independente do tipo)
ocupa **1 slot**, sem sistema de peso.

Não há empilhamento de itens iguais no MVP: dois "Cicatrizante" ocupam
2 slots separados (empilhamento pode entrar como melhoria no backlog).

### Estrutura
Todos os itens ficam numa **lista única** de até 8 posições — não existem
slots separados de "equipamento" vs "consumíveis". Um item equipável
(Instrumental, Proteção Leve, Coração Pulsante) ocupa um slot normal do
inventário mesmo enquanto está equipado/ativo.

Estrutura de dados do inventário:
```
inventory = [item, item, None, None, ...] # lista de tamanho fixo 8
```
Onde cada `item` é uma referência à definição do item (ver seção 1-5
deste documento) e `None` representa um slot vazio.

### Inventário Cheio
Se o jogador tentar coletar um item com o inventário cheio (8/8 ocudpados),
a coleta falha e uma mensagem aparece no log de combate/eventos (ver
`05-combate.md`, seção 6): `"Inventário cheio. Não foi possível pegar [item]."`
O item permanece no chão, podendo ser coletado depois se um slot for liberado.

### Equipáveis Ativos
Mesmo sem slots separados, o jogo precisa saber **quais itens equipáveis
estão ativos** no momento (já que Instrumental, Proteção Leve e Coração
Pulsante dão efeitos passivos/reativos só enquanto equipados). Isso é
resolvido com uma referência simples no jogador:
```
player.equipped = {
    "instrumental": None ou referência ao item,
    "protecao": None ou referência ao item,
    "coracao": None ou referência ao item,
}
```

Um item equipável só concede seu efeito se estiver referenciado em
`player.equipped`, mesmo que ainda ocupe um slot comum do inventário. A
lógica de "equipar" (como o jogador ativa isso) é o próximo ponto da 2.4.

## 7. Como o Jogador Equipa/Usa Itens

### Abrindo o Inventário
O jogador abre a tela de inventário com uma tecla dedicada (ex: `i`).
Essa tela lista os até 8 slots, mostrando os itens ocupados e indicando
quais equipáveis estão atualmente ativos (ex: com um marcador `[E]` ao lado do nome).

Abrir/fechar o inventário **não gasta turno** — só as ações executadas
a partir dele (usar, equipar, arremessar) gastam.

### Selecionar um Item
O jogador navega pela lista (ex: setas cima/baixo) e pressiona uma tecla
de confirmação (ex: Enter) sobre o item desejado. O comportamento após
selecionar depende do `type` do item (ver `07-itens.md`, seções 1-5):

- **Consumível (Cicatrizante):** usa o item imediatamente. Cura o próprio
  jogador (entre 4 e 18 HP), fecha o inventário, gasta o turno, e o item
  é removido do slot.
- **Equipável (Instrumental, Proteção Leve, Coração Pulsante):** a seleção
  funciona como um **toggle**:
  - Se não estiver equipado, o item é adicionado a `player.equipped` e
    passa a valer seu efeito passivo/reativo.
  - Se já estiver quipado, selecioná-lo de novo **desequipa** (remove
    de `player.equipped`), mas o item continua no inventário normalmente.
  - Equipar/desequipar **não gasta turno** (é só uma troca de estado,
    já que não é uma ação "física" no mundo do jogo).
- **Arremessável (Machadinha):** ao selecionar, o jogo automaticamente
  mira no **monstro vivo mais próximo dentro do alcance de 4 tiles**
  (usando distância em linha reta/Manhattan a partir do jogador). Se
  houver um alvo válido, o item é lançado (causa 1-6 de dano, é removido
  do inventário) e o turno é gasto. **Se não houver nenhum monstro dentro
  do alcance**, a ação é cancelada (não gasta turno) e uma mensagem
  aparece no log: `"Nenhum alvo ao alcance."`

### Ação Especial do Coração Pulsante
Diferente dos outros equipáveis, o Coração Pulsante não faz nada sozinho
ao ser equipado — seu efeito (reduzir dano pela metade) só é **oferecido
como opção ao jogador no momento em que ele recebe dano**, dentro da
resolução de combate (`05-combate.md`, seção 3):

1. Jogador leva um ataque.
2. Se o Coração Pulsante estiver equipado, o jogo pergunta: "Espremer o
   Coração Pulsante para reduzir o dano pela metade? (S/N)".
3. Se sim, sorteia a chance de falha (75% na primeira vez, 100% na
   segunda vez em diante — reduzida em 25 pontos se o Instrumental
   também estiver equipado).
4. Se der certo: dano é reduzido pela metade. Se falhar: dano é aplicado
   normalmente **e** o Coração Pulsante é destruído (removido do
   inventário).

Essa decisão acontece **dentro do mesmo turno do ataque recebido** — não
consome uma ação própria do jogador (é uma reação, não uma ação).

## 8. Sistema de Progressão

Conforme já estabelecido em `02-gdd.md` (seção 3), o jogo **não tem XP
nem sistema de níveis**. A progressão do jogador acontece inteiramente
através dos itens encontrados na masmorra:

- **Proteção Leve** aumenta a defesa (`+5`), tornando o jogador mais
  resistente a dano.
- **Instrumental** melhora a confiabilidade de outros itens (reduz chance
  de falha), tornando o uso de recursos mais consistente.
- **Coração Pulsante** oferece uma rede de segurança situacional (reduzir
  dano pela metade), mesmo sendo arriscado e de uso limitado.
- **Cicatrizante** sustenta o jogador ao longo da exploração, permitindo
  enfrentar mais combater sem morrer.
- **Machadinha** oferece uma opção de dano à distância, ajudando a lidar
  com monstros antes que cheguem ao corpo a corpo.

Não há necessidade de um item que aumente HP máximo ou ataque diretamente:
a combinação de **defesa, confiabilidade e opções táticas** já cumpre o
papel de "ficar mais forte" ao longo da run, equilibrando com o aumento
de dificuldade dos andares (mais e mais fortes monstros, ver
`04-geracao-mapas.md` e `06-entidades.md`).

A run inteira segue, portanto, uma progressão baseada em **build**: o
jogador fica mais forte não por acumular pontos, mas por administrar bem
os 8 slots de inventário e decidir quais itens equipar/usar em cada
situação.