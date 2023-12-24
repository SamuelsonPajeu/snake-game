from dataclasses import dataclass, field
from src.game.game_event import Error, GameOver, nil
from src.assets.map import Map
from src.assets.food import Food

import random

@dataclass
class Snake:
    map: Map = field(default_factory = Map)
    food: Food = field(default_factory = Food)
    pos: list = field(default_factory = lambda: [])
    direction: str = 'R'
    direction_input: str = ''
    processed_last_input: bool = False
    max_size : int = 4
    x : int = 0
    y : int = 0
    can_move: bool = True
    score = 0

    def __post_init__(self):
        # Set start position based on x, y
        self.pos.append((self.x, self.y))
        self.SpawFood()

    def Move(self) -> None:
        if not self.can_move:
            return

        match self.direction:
            case 'R':
                self.x = self.x + 1 if (self.x + 1) < self.map.x else 0
            case 'L':
                self.x = self.x - 1 if (self.x - 1) >= 0 else self.map.x - 1
            case 'U':
                self.y = self.y - 1 if (self.y - 1) >= 0 else self.map.y - 1
            case 'D':
                self.y = self.y + 1 if (self.y + 1) < self.map.y else 0

        self.processed_last_input = True
        self.CheckGameOver()

    def ValidateInput(self, input: str) -> tuple[None, Error]:
        if len(input) > 1:
            err = Error("Direction Input should contain only one Character (L,R,U,D)")
            return None, err

        valid_directions = ['L', 'R', 'U', 'D']
        if (input not in valid_directions):
            err = Error(f"{input} is not a valid direction (L,R,U,D)")
            return None, err

        return nil()

    def isReverseMove(self, desiredDirection: str) -> bool:
        atual_direction = self.direction
        reverse_moves = {
            'L' : 'R',
            'R' : 'L',
            'D' : 'U',
            'U' : 'D'
        }
        
        # print(f'Atual Dir: {atual_direction} | Desired Dir: {desiredDirection}')
        # print(f'Reverse Move for atualdir: {reverse_moves[atual_direction]}')
        
        return reverse_moves[atual_direction] == desiredDirection

    def SetDirectionInput (self, dir: str) -> tuple[None, Error]:
        _, err = self.ValidateInput(dir)

        if err:
            return _, err

        if not self.isReverseMove(dir):
            if self.processed_last_input:
                self.processed_last_input = False
                self.direction = dir


        return nil()

    def CheckColission (self) -> bool:

        if (self.x, self.y) in self.pos and len(self.pos) > 1:
            # print(self.__dict__)
            # print(f'tried to walk ok ({self.x}, {self.y})')
            return True
        self.pos.append((self.x, self.y))

        if (self.x == self.food.x and self.y == self.food.y):
            self.max_size += 1
            self.SpawFood()

        if len(self.pos) > self.max_size:
            self.pos.pop(0)

        return False

    def CheckGameOver (self) -> bool:
        if self.CheckColission():
            print('GAME OVER')
            self.can_move = False

            # err = GameOver('Game Over')
            # raise(err)

    def SpawFood (self) -> None:
        avaliable_space = [i for i in self.map.grid if (i[0], i[1]) not in self.pos]

        if avaliable_space:
            spawn_location = random.choice(avaliable_space)
            self.food.x, self.food.y = spawn_location[0], spawn_location[1]
        else:
            self.food.x = -1
            self.food.y = -1
