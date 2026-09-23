# Testes de Compatibilidade — Terminais

## Checklist a verificar em cada terminal
- [ ] O jogo abre sem erro (`python3 src/main.py`)
- [ ] O layout aparece correto (mapa, status, log nas posições certas)
- [ ] As cores aparecem (jogador ciano, paredes, monstros coloridos, etc)
- [ ] Os símbolos ASCII aparecem corretos (`@`, `#`, `.`, `>`, `p`, `w`, `D`, `!`, `/`, `\`, `[`, `h`)
- [ ] As setas do teclado movem o jogador corretamente
- [ ] `Espaço`, `i`, `Enter`, `Esc` funcionam como esperado
- [ ] Nenhum erro/crash aparece durante uma partida curta (uns 2-3 minutos jogando)

---

## Windows - Prompt de Comando (cmd)

**Como testar:**
1. Abra o "Prompt de Comando"
2. Ative o venv: `venv\Scripts\activate.bat`
3. Rode: `python src/main.py`
4. Percorra o checklist acima

**Resultado:**
*Passou*

**Observações:**
*Paredes nao aparecem (fundo preto); Aquela implementação de print inicial fica piscando a cada renderização no canto superior esquerdo da tela*

---

## Windows - PowerShell

**Como testar:**
1. Abra o "PowerShell"
2. Ative o venv: `.\venv\Scripts\Activate.ps1`
   - Se der erro de política de execução, rode antes (uma vez só):
     `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`
3. Rode: `python src/main.py`
4. Percorra o checklist acima

**Resultado:**
*Passou com ressalvas*

**Observações:**
*Cores inconsistentes (itens e hp médio estão brancos, mulher afogada fica difícil de ver pois o fundo também é azul e perturbado de energia não aparece, mesmo sendo cor diferente do fundo, nem a letra em branco não aparece)*

---

## Linux - Terminal padrão

**Como testar:**
1. Abra o terminal da sua distro
2. Ative o venv: `source venv/bin/activate`
3. Rode: `python3 src/main.py`
4. Percorra o checklist acima

**Resultado:**
*Falhou*

**Observações:**
*Abre o menu, mas ao iniciar com o Enter, ele crasha com os erros abaixo:*
```
(venv) devops@scm-dev:~/Documentos/jogos/roguelike-terminal$ python3 src/main.py
Traceback (most recent call last):
File "/home/devops/Documentos/jogos/roguelike-terminal/src/main.py", line 340, in <module>
curses.wrapper(main)
File "/usr/lib/python3.13/curses/ init .py", line 94, in wrapper return func(stdscr, *args, **kwds)
File "/home/devops/Documentos/jogos/roguelike-terminal/src/main.py", line 321,
in main
outcome, floor_reached = run_game(stdscr)
File "/home/devops/Documentos/jogos/roguelike-terminal/src/main.py", line 210, in run game
render_status (stdscr, player, current_floor)
File "/home/devops/Documentos/jogos/roguelike-terminal/src/render.py", line 62
, in render_status stdscr.addstr (STATUS_START_Y + 1, 0, "" * 40)
AAA
curses.error: addwstr() returned ERR
```

---

## Mac - Terminal padrão

**Como testar:**
1. Abra o app "Terminal"
2. Ative o venv: `source venv/bin/activate`
3. Rode: `python3 src/main.py`
4. Percorra o checklist acima

**Resultado:**
*"não testado - sem acesso a Mac no momento"*

**Observações:**
*Nenhuma*

---

## Resumo Geral
- **Terminais testados com sucesso:**
- **Terminais com problemas:**
- **Terminais não testados (pendência):**
- **Problemas encontrados que precisam virar bug (4.5):**