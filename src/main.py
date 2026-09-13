"""Ponto de entrada do jogo."""

import curses

from render import render_blank_screen


def main(stdscr):
    # Configurações iniciais do terminal
    curses.curs_set(0)     # esconde o cursor
    stdscr.nodelay(False)  # espera o input do jogador (bloqueante)
    stdscr.keypad(True)    # permite capturar teclas especiais (setas, etc)

    running = True
    while running:
        render_blank_screen(stdscr)

        key = stdscr.getch()

        if key == 27:  # tecla ESC
            running = False


if __name__ == "__main__":
    curses.wrapper(main)