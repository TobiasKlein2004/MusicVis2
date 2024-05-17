import pygame
import math

from game import Box, Ball, Track

CLOCK = pygame.time.Clock()
FPS = 60

BG_COLOR = (100, 100, 255)


screen = pygame.display.set_mode((400, 400))
pygame.display.set_caption("Gravity")
screen.fill(BG_COLOR)

box1 = Box(100, 200, 100, 25, 30, screen)
box2 = Box(350, 200, 100, 25, -30, screen)
track = Track(screen, lambda x: -0.05*(x**2))
ball = Ball(screen, world=[box1, box2], position=(100, 50))

worldOffset = (0, 0)

running = True
while running: 
    for event in pygame.event.get():     
        if event.type == pygame.QUIT: running = False
    
    deltaTime = CLOCK.tick(FPS) / 1000

    # ball.updatePhysics(deltaTime)
    worldOffset = ball.worldOffset
    ball.draw()

    box1.draw(worldOffset)
    box2.draw(worldOffset)
    track.draw(worldOffset)
    # x, y = 155, 170
    # print(box.checkCollision([(x,y)]))
    # pygame.draw.circle(screen, (255,0,0), (x,y), 2)

    pygame.display.flip()
    screen.fill(BG_COLOR)
