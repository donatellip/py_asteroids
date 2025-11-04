"""
Movement in Pygame
"""
import pygame
import sys
import math
import random

pygame.init()

vertices = []

BLACK = (0, 0, 0)
ORANGE = (255, 165, 0)
WHITE = (255, 255, 255, .60)


# screen setup
WIDTH, HEIGHT = 1000, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill(BLACK) # black

level_settings = {1: 12,
                  2: 20,
                  3: 31,
                  }
powers = []

# Draw Character - SHIP
class Polygon:
    def __init__(self, sides, x, y, radius):
        self.sides = sides
        self.x = x
        self.y = y
        self.angle = 0
        self.radius = radius
        self.vertices = self.get_vertices(self.sides)

    def get_vertices(self, n):
        verts = []
        for i in range(self.sides):
            base_angle = 2 * math.pi * i / n
            total_angle = base_angle + self.angle
            vx = int(self.x + self.radius * math.cos(total_angle))
            vy = int(self.y + self.radius * math.sin(total_angle))
            verts.append((vx, vy))
        return verts
    
    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.vertices = self.get_vertices(self.sides)

pentagon = Polygon(5, WIDTH // 2, HEIGHT // 2, 30)

class Missile:
    def __init__(self, level, quantity, power):
        self.level = level
        self.quantity = level_settings[level]
        self.power = powers[power]
    def update_screen(self, quantity):
        self.image = pygame.image.load("missile.png")
        self.image = pygame.transform.scale_by(screen, .5)
        self.x = 10
        self.y = 10
        screen.blit(self.image, (self.x, self.y))  # top-left corner at (x, y)

#missile_icon = Missile(1, 

class Star:
    def __init__(self, x, y, size, speed_x, speed_y):
        self.x = x
        self.y = y
        self.size = size
        self.speed_x = speed_x
        self.speed_y = speed_y
        
    def draw(self,surface):
        pygame.draw.circle(surface, WHITE, (self.x, self.y), self.size, self.size)

    def move(self):
        self.x += self.speed_x / 2
        self.y += self.speed_y / 2
        if self.x < -20 or self.x > WIDTH + 20:
            self.speed_x *= -1
        if self.y < -20 or self.y > HEIGHT + 20:
            self.speed_y *= -1
        

stars = []
# stars
for i in range(150):
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    speed_x = random.randint(-2, 2)
    speed_y = random.randint(-2, 2)
    size = random.randint(1, 3)
    star = Star(x, y, size, speed_x, speed_y)
    stars.append(star)
    

clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEWHEEL:
            step = math.radians(10)
            pentagon.angle += event.y * step
            pentagon.vertices = pentagon.get_vertices(pentagon.sides)
    # Arrow Keys to move
    dist = 2
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RSHIFT] or keys[pygame.K_LSHIFT]:
        dist = 10
    if keys[pygame.K_DOWN]:
        pentagon.move(0, +dist)
    if keys[pygame.K_UP]:
        pentagon.move(0, -dist)
    if keys[pygame.K_LEFT]:
        pentagon.move(-dist, 0)
    if keys[pygame.K_RIGHT]:
        pentagon.move(+dist, 0)
  
        

    screen.fill(BLACK)
    # Screen components
    for star in stars:
        star.move()
        star.draw(screen)
    clock.tick(30)

    pygame.draw.polygon(screen, ORANGE, pentagon.vertices)           
    pygame.display.flip()


pygame.quit()
sys.exit()
