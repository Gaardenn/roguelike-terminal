# Roguelike de Terminal

**Versão:** 1.0.0

Um roguelike em ASCII, com geração procedural de masmorras e combate por
turnos, rodando em terminal (Windows/Linux/Mac).

## Requisitos
- Python 3.10 ou superior
- Um terminal com pelo menos **81 colunas x 25 linhas**

## Como rodar

### 1. Baixe o projeto
```
git clone https://github.com/Gaardenn/roguelike-terminal.git
cd roguelike-terminal
```

### 2. Crie o ambiente virtual

**Windows (cmd):**
```
python -m venv venv
```

**Windows (PowerShell):**
```
python -m venv venv
```

**Linux/Mac:**
```
python3 -m venv venv
```

### 3. Ative o ambiente virtual

**Windows (Prompt de Comando):**
```
venv\Scripts\activate.bat
```

**Windows (PowerShell):**
```
.\venv\Scripts\Activate.ps1
```
Se der erro de política de execução, rode uma vez antes:
```
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

**Linux/Mac:**
```
source venv/bin/activate
```

Em todos os casos, o nome `(venv)` deve aparecer no início da linha do
terminal, confirmando que está ativado.

### 4. Instale as dependências
```
pip install -r requirements.txt
```

### 5. Execute o jogo

**Windows:**
```
python src/main.py
```

**Linux/Mac:**
```
python3 src/main.py
```

## Como jogar

Você começa no andar 1 de uma masmorra gerada aleatoriamente. O objetivo
é descer os **4 andares** e derrotar o chefe final, **O Deus da Morte**,
no último andar.

O jogo funciona em **turnos**: nada se move até você agir. A cada turno,
escolhe uma ação (mover, atacar, usar item ou esperar) e os monstros
agem em seguida.

- Mover-se contra um monstro adjacente **ataca** automaticamente — não
  existe tecla separada de "atacar"
- Itens no chão são coletador automaticamente ao pisar neles
- Pise na escada (`>`) para descer de andar
- **Cuidado:** o jogo tem permadeath. Se você morrer, a run acaba e uma
  nova masmorra é gerada do zero na próxima partida

## Controles

| Tecla           | Ação                                             |
|-----------------|---------------------------------------------------|
| Setas (↑↓←→)    | Mover (mover contra um monstro = atacar)          |
| Espaço          | Esperar um turno parado                           |
| `i`             | Abrir/fechar o inventário                          |
| Enter           | Confirmar (usar/equipar item, iniciar jogo)        |
| Esc ou `q`      | Cancelar / voltar / sair                           |
| `S` / `N`       | Responder prompts de sim/não (ex: Coração Pulsante) |

Dentro do inventário, use as setas para navegar entre os itens e Enter
para usar/equipar/arremessar o item selecionado.

## Símbolos no mapa

| Símbolo | Significado          |
|---------|------------------------|
| `@`     | Você                    |
| `#`     | Parede                  |
| `.`     | Chão                    |
| `>`     | Escada (desce de andar) |
| `p`     | Perturbado de Energia (monstro comum) |
| `w`     | Mulher Afogada (monstro comum)        |
| `D`     | O Deus da Morte (chefe final)         |
| `!` `/` `\` `[` `h` | Itens (veja a descrição de cada um no inventário do jogo) |

## Rodar os testes
```
pytest -v
```

## Documentação
Veja a pasta `docs/` para escopo, GDD, arquitetura, e todos os
documentos de design e testes do projeto.