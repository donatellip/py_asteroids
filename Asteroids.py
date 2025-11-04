"""
Movement in Pygame
"""
# Imports
import pygame
import sys
import math
import random

# Setup
pygame.init()
pygame.font.init()
font = pygame.font.SysFont('JetBrains Mono Medium', 30)  # Font name and size
clock = pygame.time.Clock()

# Variable Initializations
vertices = [(0, 10), (2, 0), (1, -1), (-1, -1), (-2, 0)]
powers = []
level = 1
bullets = []
asteroids = []
stars = []

# Data
BLACK = (0, 0, 0)
ORANGE = (255, 165, 0)
WHITE = (255, 255, 255, .60)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
PURPLE = (170, 0, 255)

messages = {"score": "",
            "end": "Good Job all destroyed.",
            "directions": "MOVE: 🞀, 🞁, 🞃, 🞂  SHOOT: Space"
            }

level_settings = {1: 12,
                  2: 20,
                  3: 31,
                  }

# screen setup
WIDTH, HEIGHT = 1000, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill(BLACK) # black


# Draw Character - SHIP
class Ship:
    def __init__(self, sides, x, y, radius):
        self.sides = sides
        self.x = x
        self.y = y
        self.angle = 0
        self.vertices = vertices
#        self.vertices = self.get_vertices(self.sides)

##    def get_vertices(self, n):
##        verts = []
##        for i in range(self.sides):
##            base_angle = 2 * math.pi * i / n
##            total_angle = base_angle + self.angle
##            vx = int(self.x + self.radius * math.cos(total_angle))
##            vy = int(self.y + self.radius * math.sin(total_angle))
##            verts.append((vx, vy))
##        return verts
    
    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.vertices = self.get_vertices(self.sides)

    def draw(self):
        

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

        
# Background Stars
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
        # Bounce if off screen
        if self.x < -20 or self.x > WIDTH + 20:
            self.speed_x *= -1
        if self.y < -20 or self.y > HEIGHT + 20:
            self.speed_y *= -1
        

# Create stars
for i in range(150):
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    speed_x = random.randint(-2, 2)
    speed_y = random.randint(-2, 2)
    size = random.randint(1, 3)
    star = Star(x, y, size, speed_x, speed_y)
    stars.append(star)

# Asteroid class
class Asteroid:
    def __init__(self, x=None, y=None, size=None):
        self.x = x if x is not None else random.randint(0, WIDTH)
        self.y = y if y is not None else random.randint(0, HEIGHT)
        self.dx = random.uniform(-2, 2)
        self.dy = random.uniform(-2, 2)
        self.size = size if size is not None else random.randint(30, 50)

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.x %= WIDTH
        self.y %= HEIGHT

    def draw(self):
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.size)

    def split(self):
        if self.size > 20:
            return [Asteroid(self.x, self.y, self.size // 2),
                    Asteroid(self.x, self.y, self.size // 2)]
        else:
            return []

# create instances of class asteroid, attr are default
asteroids = [Asteroid() for _ in range(10)]
    
# Bullet class
class Bullet:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.dx = math.cos(math.radians(angle)) * 10
        self.dy = math.sin(math.radians(angle)) * 10

    def update(self):
        self.x += self.dx
        self.y += self.dy

    def draw(self):
        pygame.draw.circle(screen, PURPLE, (int(self.x), int(self.y)), 3)

def check_collision(bullet, asteroid):
    dist = math.hypot(bullet.x - asteroid.x, bullet.y - asteroid.y)
    return dist < asteroid.size


# Screen components
screen.fill(BLACK)

### Game Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEWHEEL:
            step = math.radians(10)
            pentagon.angle += event.y * step
            pentagon.vertices = pentagon.get_vertices(pentagon.sides)

    # Controls
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
    if keys[pygame.K_SPACE]:
        bullets.append(Bullet(ship.x, ship.y, ship.angle))
  
    # Ship Update and Draw
    ship.update()
    ship.draw()        


    


    # Stars
    for star in stars:
        star.move()
        star.draw(screen)
    clock.tick(30)

    # Asteroids
    for asteroid in asteroids:
        asteroid.update()
        asteroid.draw()

    # Bullets
    for bullet in bullets[:]:
        bullet.update()
        bullet.draw()
        if bullet.x < 0 or bullet.x > WIDTH or bullet.y < 0 or bullet.y > HEIGHT:
            bullets.remove(bullet)
            continue

        for asteroid in asteroids[:]:
            if check_collision(bullet, asteroid):
                bullets.remove(bullet)
                asteroids.remove(asteroid)
                asteroids.extend(asteroid.split())
                break

    pygame.draw.polygon(screen, ORANGE, pentagon.vertices)           
    if len(asteroids) == 0:
        level += 1
    pygame.display.flip()
    clock.tick(300)


pygame.quit()
sys.exit()
