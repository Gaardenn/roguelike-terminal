# Log de Playtest — Testes de Balanceamento

Jogue do início (menu) até o fim (vitória ou derrota) pelo menos **5 vezes**,
preenchendo uma entrada abaixo para cada partida. Seja honesto na percepção
de dificuldade — é isso que vai guiar os ajustes do próximo passo.

## Como jogar cada rodada
1. Rode `python3 src/main.py`
2. Jogue normalmente, sem "facilitar" de propósito
3. Ao terminar (morrer ou vencer), preencha uma entrada usando o modelo abaixo
4. Repita

---

## Modelo de entrada (copie e preencha para cada partida)

### Partida N
- **Resultado:** vitória / derrota
- **Andar alcançado:** (1 a 4)
- **Causa da morte (se derrota):** ex: "cercado por 2 Mulheres Afogadas sem
  Cicatrizante no inventário"
- **Itens encontrados:** liste o que apareceu no caminho
- **Itens usados e quando:** ex: "usei Cicatrizante no andar 2 com 6 HP"
- **Momento mais difícil:** onde você sentiu mais perigo/aperto
- **Momento mais fácil/tedioso:** onde sobrou recurso ou nada ameaçou
- **Sensação geral de dificuldade:** muito fácil / fácil / equilibrado / difícil / muito difícil
- **Observações livres:** qualquer coisa que chamou atenção (bug, comportamento
  estranho de monstro, item que pareceu inútil ou overpowered, etc)

---

## Partida 1
- **Resultado:** derrota
- **Andar alcançado:** 1
- **Causa da morte (se derrota):** lutei contra uma mulher afogada e quando estava com pouca vida fugi, mas fui encurralado
- **Itens encontrados:**
  - Instrumental
  - Machadinha
- **Itens usados e quando:** nenhum
- **Momento mais difícil:** lutando contra a mulher afogada
- **Momento mais fácil/tedioso:** nenhum no começo
- **Sensação geral de dificuldade:** difícil
- **Observações livres:** paredes não estão muito visíveis, pois mistura com a cor do fundo do terminal

## Partida 2
- **Resultado:** derrota
- **Andar alcançado:** 1
- **Causa da morte (se derrota):** lutei contra uma mulher afogada e quando estava com pouca vida fugi. Indo em direçao até as escadas, o perturbado ficou no corredor, e a mulher me seguindo atrás, e morri pra ele, pois estava encurralado
- **Itens encontrados:**
  - Proteção Leve
  - Coraçao Pulsante
- **Itens usados e quando:** equipei a Proteçao assim que peguei
- **Momento mais difícil:** tentando passar de andar
- **Momento mais fácil/tedioso:** nenhum no começo
- **Sensação geral de dificuldade:** difícil
- **Observações livres:** de novo foi impossível ganhar da mulher afogada, quando fiquei com pouca vida tive que dar a volta pra ela não me matar

## Partida 3
- **Resultado:** quitei sem querer
- **Andar alcançado:** 3
- **Causa da morte (se derrota):** apertei ESC sem querer
- **Itens encontrados:**
  - Machadinha 3x
  - Coraçao Pulsante
  - Proteçao Leve 2x
  - Cicatrizante 4x
  - Instrumental
- **Itens usados e quando:** equipei as 2 Proteção assim que peguei, e usei uma machadinha quando a mulher afogada chegou perto
- **Momento mais difícil:** andares com muita mulher afogada
- **Momento mais fácil/tedioso:** nenhum percebido
- **Sensação geral de dificuldade:** difícil
- **Observações livres:** pra passar tive que desviar das mulheres afogadas. Alguns detalhes, os itens equipados estão sem quebra de linha, sumindo da tela. Uma hora eu tava longe de qualquer mulher afogada e apareceu quando me movi que tinha me atacado. O comportamento do coração está estranho, as vezes a criatura ataca e não aparece opção, e como o jogador também age, as vezes ele pede, mas ele já captura o andar do jogador, então impede de aceitar

## Partida 4
- **Resultado:** derrota
- **Andar alcançado:** 3
- **Causa da morte (se derrota):** fui encurralado num corredor por 4 mulheres afogadas, sem ter o que fazer
- **Itens encontrados:**
  - Proteçao Leve 3x
  - Machadinha 2x
- **Itens usados e quando:** equipei a Proteção assim que peguei
- **Momento mais difícil:** andares com muita mulher afogada
- **Momento mais fácil/tedioso:** nenhum percebido
- **Sensação geral de dificuldade:** difícil
- **Observações livres:** nenhum a mais

## Partida 5
- **Resultado:** derrota
- **Andar alcançado:** 3
- **Causa da morte (se derrota):** fui encurralado num corredor por 2 mulheres afogadas e 1 perturbado de energia, sem ter o que fazer
- **Itens encontrados:**
  - Coração Pulsante 2x
  - Machadinha 2x
  - Proteção Leve
- **Itens usados e quando:** equipei a Proteção e o Coraçao assim que peguei
- **Momento mais difícil:** andares com muita mulher afogada
- **Momento mais fácil/tedioso:** nenhum percebido
- **Sensação geral de dificuldade:** difícil
- **Observações livres:** o coraçao ta funcionando certo, ele congela a rodada antes de seguir, só tá meio confuso, ou pelo menos as vezes ta certo

---

## Resumo Geral (preencher após as 5 partidas)
- **Taxa de vitória:** 0 de 5 partidas
- **Andar onde mais se morre:** 3
- **Item mais usado:** Proteção Leve
- **Item menos usado (ou nunca usado):** Cicatrizante e Instrumental
- **Sensação de dificuldade predominante:** Mulher Afogada
- **Principais pontos a ajustar no próximo passo (2.2 do 4.2):** Balancear inimigos e player