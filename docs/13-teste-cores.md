# Testes de Compatibilidade — Com/Sem Suporte a Cores

O jogo usa `curses.start_color()` e pares de cor (`08-interface.md`, seção 2)
sem nenhuma checagem prévia de se o terminal realmente suporta cores.
Este teste verifica o que acontece num terminal sem esse suporte.

## Como simular um terminal sem suporte a cores

**Linux/Mac:** force a variável de ambiente `TERM` para um tipo de terminal sem cores antes de rodar o jogo:
```
TERM=vt100 python3 src/main.py
```
(`vt100` é um terminal antigo que não suporta cores — o `curses` deve
detectar isso automaticamente)

**Windows:** não há uma forma simples de simular ausência de cor (o
`windows-curses` geralmente assume supote). Se não conseguir testar,
marque como "não testável no Windows" e siga em frente.

## Checklist
- [ ] O jogo abre sem crash mesmo sem suporte a cores
- [ ] Os símbolos e o layout continuam legíveis (mesmo sem cor, tudo
      monocromático deveria funcionar, já que os símbolos ASCII por si
      só diferenciam os elementos)
- [ ] Nenhum erro relacionado a `start_color()` ou `init_pair()` aparece

---

## Teste — Terminal sem suporte a cores

**Ambiente testado:** *Linux com TERM=vt100*

**Resultado:**
*Falhou, com crash ao iniciar*

**Observações:**
*Traceback (most recent call last):
File "/home/devops/Documentos/jogos/roguelike-terminal/src/main.py", line 340,
in <module>
curses.wrapper (main)
File "/usr/lib/python3.13/curses/ init.py", line 94, in wrapper return func(stdscr, *args, **kwds)
in main
File "/home/devops/Documentos/jogos/roguelike-terminal/src/main.py", line 308, curses.curs_set (0)*

---

## Teste — Terminal COM suporte a cores (controle, pra comparar)

Já testamos isso implicitamente nos itens anteriores (4.2 e no início da
4.3), mas vale confirmar mais uma vez rapidamente aqui.

**Resultado:**
*(preencha aqui, deve ser igual ao que já vimos antes: passou / passou com ressalvas
por causa dos bugs de cor já registrados)*

---

## Resumo Geral
- **Jogo funciona sem suporte a cores?** Não foi possível testar
- **Erros encontrados:** Crash ao iniciar jogo
- **Novos bugs a registrar:** Sim — ver bug #9 em `10-bugs-pendentes.md`
  (crash em `curses.curs_set(0)`, não relacionado a cor em si, mas que impediu completar este teste)