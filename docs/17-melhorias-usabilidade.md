# Melhorias de Usabilidade — Identificadas em 4.4

Com base nos testes de controles (`14-usabilidade-controles.md`) e no
feedback externo (`16-feedback-externo.md`), identificamos 3 melhorias
de onboarding/clareza que não são bugs, mas lacunas de comunicação com
o jogador:

## 1. Falta de orientação inicial sobre os controles
O jogador não descobre `i` (inventário) nem `Espaço` (esperar) sozinho.
Nenhuma tela do jogo lista os controles — eles só existem em
`08-interface.md`, que o jogador nunca vê.

**Melhoria sugerida:** adicionar um resumo de controles na tela de Menu
Inicial (`render_menu_screen`).

## 2. Itens sem descrição visível no jogo
O jogador não consegue saber o que um item faz (cura? dano? defesa?) sem
ter memorizado o símbolo de antemão. Isso causa hesitação e medo de usar
itens errado.

**Melhoria sugerida:** mostrar uma descrição curta do item selecionado
na tela de inventário (ex: abaixo da lista, mostrar "Cicactrizante: cura
4-18HP").

## 3. Tecla `Esc` sem alternativa
Levantado na autoavaliação: alguns teclados (ex: layouts compactos como
60%) remapeiam ou dificultam o acesso ao `Esc`. Embora pontual, é barato
resolver.

**Melhoria sugerida:** aceitar `q` como tecla alternativa para cancelar/
sair, em paralelo ao `Esc` (sem remover o `Esc`).

## Observação sobre dificuldade (Mulher Afogada)
O feedback externo relata dificuldade alta contra a Mulher Afogada, mas
o teste foi feito "no meio" dos ajustes de balanceamento da 4.2 (o
testador relata ter mexido no código entre tentatvias). Não dá pra
concluir se o problema persiste com os valores atuais — recomenda-se
um novo teste externo depois dessas melhorias, para isolar a variável.