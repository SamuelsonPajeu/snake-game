from dataclasses import dataclass, field
from src.game.game_event import Error, GameOver, nil
from src.assets.map import Map



@dataclass
class Snake:
    map: Map = field(default_factory = Map)
    pos: list = field(default_factory = lambda: [(0,0)])
    direction: str = 'R'
    max_size : int = 4
    x : int = 0
    y : int = 0

    def __post_init__(self):
        # Set start position based on x, y
        self.pos.append((self.x, self.y))

    def Move(self) -> None:
        match self.direction:
            case 'R':
                self.x = self.x + 1 if (self.x + 1) <= self.map.x else 0
            case 'L':
                self.x = self.x - 1 if (self.x - 1) >= 0 else self.map.x
            case 'U':
                self.y = self.y + 1 if (self.y + 1) <= self.map.y else 0
            case 'D':
                self.y = self.y - 1 if (self.y - 1) >= 0 else self.map.y
        
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
            self.direction = dir

        return nil()

    def CheckColission (self) -> bool:
        if (self.x, self.y) in self.pos: 
            # print(f'tried to walk ok ({self.x}, {self.y})')
            return True
        self.pos.append((self.x, self.y))

        if len(self.pos) > self.max_size:
            self.pos.pop(0)

        return False

    def CheckGameOver (self) -> None:
        if self.CheckColission():
            err = GameOver('Game Over')
            raise(err)

s = Snake(max_size=1)
