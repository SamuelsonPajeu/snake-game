import pygame
import sys

from dataclasses import dataclass, field

from src.assets import snake

from src.assets.snake import Snake
from src.assets.map import Map

from src.game.game_event import nil, GameOver
@dataclass(frozen=True)
class Colors:
    BLACK = (0,0,0)
    BLOCK_LINES = (50, 50, 50)
    WHITE = (255,255,255)
    TAIL = (96, 96, 96)
    HEAD = (0, 255, 0)
    FOOD = (255,0,0)
@dataclass
class Game:
    screen: pygame.Surface = field(init=False)
    font: pygame.font.Font = field(init=False)
    CLOCK: pygame.time.Clock = field(init=False)
    colors: Colors = field(default_factory=Colors)
    SCREEN_WIDTH: int = 800
    SCREEN_HEIGHT: int = 600

    player: list = field(default_factory = list)
    snake: Snake = field(default_factory = Snake)
    map: Map = field(default_factory = Map)
    
    block_size_x: int = 0
    block_size_y: int = 0

    run: bool = False

    def __post_init__(self) -> None:
        self.start()

    def start(self) -> None:
        pygame.init()

        self.run = True
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.font = pygame.font.SysFont(None, 48)

        self.screen.fill(self.colors.BLACK)
        
        self.CLOCK = pygame.time.Clock()
        
        self.snake = Snake(max_size=6, x=int(self.map.x/2), y=int(self.map.y/2))
        
        self.block_size_x = int(self.SCREEN_WIDTH / self.map.x)
        self.block_size_y = int(self.SCREEN_HEIGHT / self.map.y)
        
        self.update()

    def update(self) -> None:
        while self.run:
            # Screen
            self.CLOCK.tick(10)
            self.screen.fill(self.colors.BLACK)

            self.drawSnake()
            self.drawGrid()
            self.drawFood()


            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    self.checkInput(event.key)
                
                if event.type == pygame.QUIT:
                    self.run = False

            if self.snake.can_move:
                self.renderTextLabel(text=str(int(self.snake.score)), x=10,y=10)
                self.snake.Move()
            else:
                self.drawGameOver()

            pygame.display.update()

        pygame.quit()

    def drawGrid(self) -> None:
        for x in range(0, self.SCREEN_WIDTH, self.block_size_x):
            for y in range(0, self.SCREEN_WIDTH, self.block_size_y):
                rect = pygame.Rect(x , y,self. block_size_x, self.block_size_y)
                pygame.draw.rect(self.screen, self.colors.BLOCK_LINES, rect,1)

    def drawSnake(self) -> None:
        h = self.snake.pos[len(self.snake.pos)-1]
        rect = pygame.Rect(h[0] * self.block_size_x, h[1] * self.block_size_y, self.block_size_x, self.block_size_y)
        pygame.draw.rect(self.screen, self.colors.HEAD, rect)
        
        for i in range(len(self.snake.pos) - 1):
            t = self.snake.pos[i]
            rect = pygame.Rect(t[0] * self.block_size_x, t[1] * self.block_size_y, self.block_size_x, self.block_size_y)
            pygame.draw.rect(self.screen, self.colors.TAIL, rect)

    def drawFood(self) -> None:
        rect = pygame.Rect(self.snake.food.x * self.block_size_x, self.snake.food.y * self.block_size_y, self.block_size_x, self.block_size_y)
        pygame.draw.rect(self.screen, self.colors.FOOD ,rect)

    def drawGameOver(self) -> None:
        img = self.getTextImg(text="Press 'R' to restart")
        rect = img.get_rect()
        img2 = self.getTextImg(text=f"Score: {str(self.snake.score)}")
        rect2 = img2.get_rect()
        self.renderTextImg(img,
                            x=int(self.SCREEN_WIDTH/2) - rect.width / 2,
                            y=int(self.SCREEN_HEIGHT/2)- rect.height / 2 - 20)
        self.renderTextImg(img2,
                            x=int(self.SCREEN_WIDTH/2) - rect2.width / 2,
                            y=int(self.SCREEN_HEIGHT/2)- rect2.height / 2 + 20)

    def renderTextLabel(self, text: str,x: int = 0, y: int = 0, color: tuple = Colors.WHITE):
        img = self.getTextImg(text=text, color=color)
        self.renderTextImg(img=img, x=x, y=y)
    
    def getTextImg(self, text: str, color: tuple = Colors.WHITE) -> pygame.surface.Surface:
        return self.font.render(text, True, color)
    
    def renderTextImg(self, img: pygame.surface.Surface, x: int = 0, y: int=0) -> None:
        self.screen.blit(img, (x, y))

    def restartGame(self) -> None:
        if not self.snake.can_move:
            self.snake = Snake(max_size=6, x=int(self.map.x/2), y=int(self.map.y/2))
        
    def checkInput(self, key) -> None:
        _, err = nil()

        match key:
            case pygame.K_a | pygame.K_LEFT:
                _, err = self.snake.SetDirectionInput('L')
            case pygame.K_d | pygame.K_RIGHT:
                _, err = self.snake.SetDirectionInput('R')
            case pygame.K_w | pygame.K_UP:
                _, err = self.snake.SetDirectionInput('U')
            case pygame.K_s | pygame.K_DOWN:
                _, err = self.snake.SetDirectionInput('D')
            case pygame.K_r:
                self.restartGame()
            case pygame.K_ESCAPE:
                sys.exit()

        if err:
            raise(err)
