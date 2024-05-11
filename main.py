import pygame
import math

from game import Box

CLOCK = pygame.time.Clock()
FPS = 60

BG_COLOR = (100, 100, 255)



class Ball():
    def __init__(self, surface, position=(200, 50), radius=10) -> None:
        self.surface = surface
        self.x_pos, self.y_pos = position
        self.x_velocity = 0
        self.y_velocity = 0
        self.gravity = 4
        self.radius = radius

    def calcAngle(self) -> float:
        Vx, Vy = self.x_velocity, self.y_velocity*-1  # *-1 because growing y means down not up
        return math.degrees(math.atan2(Vx,Vy))

    def updatePhysics(self, deltaTime) -> None:
        self.y_velocity += self.gravity * deltaTime
        self.y_pos += self.y_velocity
        self.x_pos += self.x_velocity

    def draw(self) -> None:
        pygame.draw.circle(self.surface, (255,255,255), (self.x_pos, self.y_pos), self.radius)



screen = pygame.display.set_mode((400, 400))
pygame.display.set_caption("Gravity")
screen.fill(BG_COLOR)


ball = Ball(screen)
box = Box(200, 200, 100, 25, 30, screen)


running = True
while running: 
    for event in pygame.event.get():     
        if event.type == pygame.QUIT: running = False
    
    deltaTime = CLOCK.tick(FPS) / 1000

    ball.updatePhysics(deltaTime)
    ball.draw()

    box.draw()
    x, y = 155, 170
    print(box.checkCollision([(x,y)]))
    pygame.draw.circle(screen, (255,0,0), (x,y), 2)

    pygame.display.flip()
    screen.fill(BG_COLOR)
