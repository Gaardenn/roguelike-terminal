"""Script utilitário para gerar e visualizar mapas no terminal comum (sem curses).

Uso: python3 scripts/preview_dungeon.py [quantidade]
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from map import generate_dungeon


def print_map(map_grid):
    for row in map_grid:
        print("".join(tile["symbol"] for tile in row))


def main():
    quantidade = int(sys.argv[1]) if len(sys.argv) > 1 else 3

    for i in range(quantidade):
        print(f"\n===== Mapa {i + 1} =====")
        map_grid, rooms = generate_dungeon()
        print_map(map_grid)
        print(f"Numero de salas geradas: {len(rooms)}")


if __name__ == "__main__":
    main()