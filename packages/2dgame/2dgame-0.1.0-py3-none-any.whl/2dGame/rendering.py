import colorama

from .utils import *
from typing import Optional
import threading
import keyengine

def _key_listening(plr: Player):
    match keyengine.current_key:
        case 'up':
            plr.y += 1
        case 'down':
            plr.y -= 1
        case 'left':
            plr.x -= 1
        case 'right':
            plr.x += 1

player_color: str = 'white'

def create_map(max_x: int, max_y: int, start: Optional[list[list[Cell]]] = None, base_color: Optional[str] = 'dark green') -> list[list[Cell]]:
    '''
    Returns the map in a map[y][x] format.
    :param max_x:
    :param max_y:
    :param start:
    :return:
    '''
    if start:
        return start
    else:
        a = []
        for y in range(max_y):
            a.append([])
            for x in range(max_x):
                a[-1].append(Cell(color=base_color))
        return a

def render(map: list[list[Cell]], plr: Player) -> None:
    global player_color
    for yi, y in enumerate(map):
        for xi, x in enumerate(y):
            if plr.x == xi and plr.y == yi:
                print(f'{colorama.Fore.__dict__[player_color.upper()]}██{colorama.Fore.RESET}', end='')
                continue
            print(f'{colorama.Fore.__dict__[x.color.upper()]}██{colorama.Fore.RESET}', end='')
        print('\n', end='')
