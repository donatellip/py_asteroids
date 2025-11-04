import pygame
import sys
import random
import math

pygame.font.init()
font = pygame.font.SysFont('JetBrains Mono Medium', 30)  # Font name and size

# Initialize
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Asteroids")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
PURPLE = (170, 0, 255)

messages = {"score": "",
            "end": "Good Job all destroyed.",
            "directions": "MOVE: 🞀, 🞁, 🞃, 🞂  SHOOT: Space"
            }

# Ship class
class Ship:
    def __init__(self):
        self.x = WIDTH / 2
        self.y = HEIGHT / 2
        self.angle = 0
        self.speed = 0
        self.vel_x = 0
        self.vel_y = 0

    def update(self):
        self.vel_x += math.cos(math.radians(self.angle)) * self.speed
        self.vel_y += math.sin(math.radians(self.angle)) * self.speed
        self.x += self.vel_x
        self.y += self.vel_y
        self.x %= WIDTH
        self.y %= HEIGHT

    def draw(self):
        tip = (self.x + math.cos(math.radians(self.angle)) * 20,
               self.y + math.sin(math.radians(self.angle)) * 20)
        left = (self.x + math.cos(math.radians(self.angle + 140)) * 20,
                self.y + math.sin(math.radians(self.angle + 140)) * 20)
        right = (self.x + math.cos(math.radians(self.angle - 140)) * 20,
                 self.y + math.sin(math.radians(self.angle - 140)) * 20)
        pygame.draw.polygon(screen, RED, [tip, left, right])

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


# Game setup
# create instance of class ship, attr are default
ship = Ship()

### create instances of class asteroid, attr are default
##asteroids = [Asteroid() for _ in range(10)]
##
### create an empty list of bullet instances
##bullets = []

### Game loop
##running = True
##while running:
##    screen.fill(BLACK)
##    for event in pygame.event.get():
##        if event.type == pygame.QUIT:
##            running = False

##    # Controls
##    keys = pygame.key.get_pressed()
##    if keys[pygame.K_LEFT]:
##        ship.angle -= 5
##    if keys[pygame.K_RIGHT]:
##        ship.angle += 5
##    if keys[pygame.K_UP]:
##        ship.speed = 0.1
##    elif keys[pygame.K_DOWN]:
##        ship.speed = -0.1   
##    else:
##        ship.speed = 0
##    if keys[pygame.K_SPACE]:
##        # each bullet instance starts at the ship position
##        # and fires in the direction of the ship
##        bullets.append(Bullet(ship.x, ship.y, ship.angle))

    # Update and draw
    ship.update()
    ship.draw()

    for asteroid in asteroids:
        asteroid.update()
        asteroid.draw()

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

    if len(asteroids) == 0:
        running = False
    pygame.display.flip()
    clock.tick(300)

pygame.quit()
