from typing import Callable
from player import Player

class Cell:
    def __init__(self, on_player_step: Callable[[Player], None] | Callable[[], None] = (lambda _: None), color: str = 'dark green'):
        self.on_player_step = on_player_step
        self.color = color
