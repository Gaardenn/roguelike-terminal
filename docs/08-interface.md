# Interface e Experiência (UI/UX) — Roguelike de Terminal

## 1. Layout da Tela

A tela do terminal usa **80 colunas x 24 linhas** (padrão), dividida em
duas regiões:
```
┌──────────────────────────────────────────────────────────────────────────┐
|                                                                          |
|                                                                          |
|                              MAPA (80 x 20)                              |
|                                                                          |
|                                                                          |
|                                                                          |
├─────────────────────────────────┬──────────────────────────────────────┤
|         STATUS (40 x 4)         |             LOG (40 x 4)             |
└─────────────────────────────────┴──────────────────────────────────────┘
```

- **Mapa:** ocupa as linhas 0-19 (20 linhas), largura total (80 colunas).
  Área principal e maior da tela
- **Status do jogador:** linhas 20-23 (4 linhas), colunas 0-39 (metade
  esquerda). Mostra HP atual/máximo, andar atual, e itens equipados.
- **Log de mensagens:** linhas 20-23 (4 linhas), colunas 40-79 (metade
  direita). Mostra as últimas 5 mensagens (`05-combate.md`, seção 6),
  com quebra de linha/scroll simples dentro do espaço disponível.

Exemplo de conteúdo do painel de status:
```
HP: 14/14 Andar: 2
Equipado: Protecao Leve, Instrumental
```

## 2. Esquema de Cores

O jogo usa cores via `curses` (pares de cor definidos na inicialização),
mesmo mantendo o tom sombrio — as cores reforçam legibilidade e dão peso
a momentos-chave (dano, itens raros), sem parecer alegre ou vibrante.

| Elemento                         | Cor                         |
|----------------------------------|-------------------------------|
| Jogador (`@`)                    | Branco/ciano                  |
| Paredes (`#`)                    | Cinza escuro                  |
| Chão (`.`)                       | Cinza (padrão do terminal)     |
| Escada (`>`)                     | Amarelo                       |
| Perturbado de Energia (`p`)      | Magenta/roxo (plasma confuso)  |
| Mulher Afogada (`w`)             | Azul                          |
| O Deus da Morte (`D`)            | Vermelho escuro, em negrito    |
| Itens no chão (genérico)         | Dourado                       |
| HP alto (>60%)                   | Verde                         |
| HP médio (30-60%)                | Amarelo                       |
| HP baixo (<30%)                  | Vermelho, piscando se possível |
| Mensagens de dano no log         | Vermelho                      |
| Mensagens neutras/informativas   | Branco/cinza claro             |

## 3. Símbolos ASCII (tabela consolidada)

| Elemento                  | Símbolo | Categoria       |
|----------------------------|---------|------------------|
| Jogador                    | `@`     | Entidade         |
| Parede                     | `#`     | Tile             |
| Chão                       | `.`     | Tile             |
| Escada (saída)             | `>`     | Tile especial    |
| Perturbado de Energia      | `p`     | Monstro          |
| Mulher Afogada             | `w`     | Monstro          |
| O Deus da Morte            | `D`     | Chefe            |
| Cicatrizante                | `!`     | Item             |
| Instrumental                | `/`     | Item             |
| Machadinha                  | `\`     | Item             |
| Proteção Leve                | `[`     | Item             |
| Coração Pulsante             | `♥` (fallback: `h`) | Item |

## 4. Controles

| Tecla            | Ação                                                |
|-------------------|-------------------------------------------------------|
| `↑`, `↓`, `←`, `→` | Mover o jogador (ou atacar, se houver monstro no destino) |
| `Espaço`          | Esperar (passar o turno parado)                        |
| `i`               | Abrir/fechar o inventário                               |
| `Enter`           | Confirmar seleção (usar/equipar item, confirmar em menus) |
| `Esc`             | Cancelar / fechar tela atual (inventário, menus)         |
| `S` / `N`         | Responder prompts de sim/não (ex: ativar Coração Pulsante) |

Dentro da tela de inventário, `↑`/`↓` navegam entre os itens listados, e
`Enter` executa a ação correspondente ao tipo do item selecionado
(conforme `07-itens.md`, seção 7).