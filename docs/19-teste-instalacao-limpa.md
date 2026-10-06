# Teste de Instalação em Ambiente Limpo — 5.1

## Como foi testado
1. Clonado o repositório numa pasta nova e separada (`git clone`), sem
   reaproveitar nenhum arquivo local
2. Seguido o `README.md` do zero: criar venv, `pip install -r requirements.txt`,
   `python src/main.py`
3. Rodado `pytest -v` para confirmar a suíte completa de testes

## Resultado
Passou sem nenhum ajuste manual

## Observações
O README não especifica quais comandos rodar em cada tipo de terminal/SO.
Também não cita nada sobre ativar o venv. Talvez alguem que saiba python
consiga saber o que fazer, mas o README não cita nada.