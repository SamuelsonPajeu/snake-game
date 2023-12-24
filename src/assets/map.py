from dataclasses import dataclass, field

@dataclass
class Map:
    x: int = 20
    y: int = 20
    grid: list = field(default_factory=list)
    
    def __post_init__(self):
        for x in range(self.x):
            for y in range(self.y):
                self.grid.append((x,y))
