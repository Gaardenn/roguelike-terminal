# Testes de Compatibilidade — Tamanhos de Janela de Terminal

O jogo foi projetado para uma tela fixa de **80 colunas x 24 linhas**
(`04-geracao-mapas.md`, seção 2). Este teste verifica o que acontece quando a janela real do terminal é diferente disso.

## Checklist por tamanho
- [ ] O jogo abre sem crash
- [ ] Se a janela for menor que 80x24: o jogo deveria avisar e não travar (comportamento esperado, ainda não implementado — ver bug #6 em `10-bugs-pendentes.md`)
- [ ] Se a janela for maior que 80x24: o jogo deveria funcionar normalmente, só sobrando espaço em branco ao redor
- [ ] Redimensionar a janela **com o jogo já aberto** não deveria travar

---

## Teste 1 — Janela exatamente 80x24 (tamanho padrão)

**Como testar:** redimensione o terminal para 80 colunas x 24 linhas antes
de abrir o jogo (a maioria dos terminais mostra o tamanho atual no título
da janela, ou aceita `resize -s 24 80` no Linux/Mac).

**Resultado:**
*Não passou, o tamanho mínimo aceito é 81x25*

---

## Teste 2 — Janela menor que 80x24 (ex: 60x20)

**Como testar:** diminua a janela do terminal antes de abrir o jogo.

**Resultado:**
*Crashou da mesma maneira que antes*

---

## Teste 3 — Janela maior que 80x24 (ex: 120x40)

**Como testar:** aumente a janela do terminal antes de abrir o jogo.

**Resultado:**
*Jogo funciona, sobrando ao redor*

---

## Teste 4 — Redimensionar com o jogo já em execução

**Como testar:** abra o jogo numa janela de tamanho normal, jogue um
pouco, e então redimensione a janela do terminal (encolher e esticar)
sem fechar o jogo.

**Resultado:**
*Funciona normal, a não ser que seja redimensionado para menor do que o aceito, a partir disso ele crasha*

---

## Resumo Geral
- **Tamanho ideal confirmado (80x24):** 81x25
- **Comportamento com janela menor:** Crash
- **Comportamento com janela maior:** Sobra espaço
- **Comportamento ao redimensionar em tempo real:** Normal, a não ser que reduzido pra menor que o suportado
- **Novos bugs encontrados (além do #6 já registrado):** Spawn de monstros era pra ser de 25 rodadas, mas ele tá spawnanado de 2 em 2 quando é menor que o limite