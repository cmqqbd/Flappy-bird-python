import pygame
import random
import time
from pygame.locals import *

# VARIABLES
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 20
GRAVITY = 2.5
GAME_SPEED = 15

GROUND_WIDTH = 2 * SCREEN_WIDTH
GROUND_HEIGHT = 100

PIPE_WIDTH = 80
PIPE_HEIGHT = 500

PIPE_GAP = 150

# Sound files
wing_sound = 'assets/audio/wing.wav'
hit_sound = 'assets/audio/hit.wav'

pygame.mixer.init()


class Bird(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        # Load bird images
        self.images = [pygame.image.load('assets/sprites/redbird-upflap.png').convert_alpha(),
                       pygame.image.load('assets/sprites/redbird-midflap.png').convert_alpha(),
                       pygame.image.load('assets/sprites/redbird-downflap.png').convert_alpha()]

        # Set bird's initial speed and image
        self.speed = SPEED
        self.current_image = 0
        self.image = pygame.image.load('assets/sprites/redbird-upflap.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)

        # Set bird's initial position
        self.rect = self.image.get_rect()
        self.rect[0] = SCREEN_WIDTH / 6
        self.rect[1] = SCREEN_HEIGHT / 2

    def update(self):
        # Update bird's animation
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[self.current_image]

        # Update bird's speed and position
        self.speed += GRAVITY
        self.rect[1] += self.speed

    def bump(self):
        # Make bird jump
        self.speed = -SPEED

    def begin(self):
        # Begin bird's animation
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[self.current_image]


class Pipe(pygame.sprite.Sprite):

    def __init__(self, inverted, xpos, ysize):
        pygame.sprite.Sprite.__init__(self)

        # Load pipe image
        self.image = pygame.image.load('assets/sprites/pipe-green.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (PIPE_WIDTH, PIPE_HEIGHT))

        # Set pipe's position
        self.rect = self.image.get_rect()
        self.rect[0] = xpos

        # Set pipe's orientation and position based on inversion
        if inverted:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect[1] = -(self.rect[3] - ysize)
        else:
            self.rect[1] = SCREEN_HEIGHT - ysize

        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        # Move pipe to the left
        self.rect[0] -= GAME_SPEED


class Ground(pygame.sprite.Sprite):

    def __init__(self, xpos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/sprites/base.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (GROUND_WIDTH, GROUND_HEIGHT))

        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        self.rect[1] = SCREEN_HEIGHT - GROUND_HEIGHT

    def update(self):
        # Move ground to the left
        self.rect[0] -= GAME_SPEED


def is_off_screen(sprite):
    return sprite.rect[0] < -(sprite.rect[2])


def get_random_pipes(xpos):
    size = random.randint(100, 300)
    pipe = Pipe(False, xpos, size)
    pipe_inverted = Pipe(True, xpos, SCREEN_HEIGHT - size - PIPE_GAP)
    return pipe, pipe_inverted


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird')

# Fill the screen with gradient background
background_color_top = (120, 200, 255)  # Light blue
background_color_bottom = (0, 80, 120)   # Dark blue

# Initialize bird sprite
bird_group = pygame.sprite.Group()
bird = Bird()
bird_group.add(bird)

# Initialize ground sprites
ground_group = pygame.sprite.Group()
for i in range(2):
    ground = Ground(GROUND_WIDTH * i)
    ground_group.add(ground)

# Initialize pipe sprites
pipe_group = pygame.sprite.Group()
for i in range(2):
    pipes = get_random_pipes(SCREEN_WIDTH * i + 800)
    pipe_group.add(pipes[0])
    pipe_group.add(pipes[1])

clock = pygame.time.Clock()

# Game start
begin = True

while begin:

    clock.tick(15)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE or event.key == K_UP:
                bird.bump()
                pygame.mixer.music.load(wing_sound)
                pygame.mixer.music.play()
                begin = False

    # Fill the screen with gradient background
    for y in range(SCREEN_HEIGHT):
        color = (
            background_color_top[0] + (background_color_bottom[0] - background_color_top[0]) * y // SCREEN_HEIGHT,
            background_color_top[1] + (background_color_bottom[1] - background_color_top[1]) * y // SCREEN_HEIGHT,
            background_color_top[2] + (background_color_bottom[2] - background_color_top[2]) * y // SCREEN_HEIGHT
        )
        pygame.draw.line(screen, color, (0, y), (SCREEN_WIDTH, y))

    # Move and update ground sprites
    if is_off_screen(ground_group.sprites()[0]):
        ground_group.remove(ground_group.sprites()[0])
        new_ground = Ground(GROUND_WIDTH - 20)
        ground_group.add(new_ground)

    bird.begin()
    ground_group.update()

    # Draw sprites on the screen
    bird_group.draw(screen)
    ground_group.draw(screen)

    pygame.display.update()

# Game loop
while True:

    clock.tick(15)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE or event.key == K_UP:
                bird.bump()
                pygame.mixer.music.load(wing_sound)
                pygame.mixer.music.play()

    # Fill the screen with gradient background
    for y in range(SCREEN_HEIGHT):
        color = (
            background_color_top[0] + (background_color_bottom[0] - background_color_top[0]) * y // SCREEN_HEIGHT,
            background_color_top[1] + (background_color_bottom[1] - background_color_top[1]) * y // SCREEN_HEIGHT,
            background_color_top[2] + (background_color_bottom[2] - background_color_top[2]) * y // SCREEN_HEIGHT
        )
        pygame.draw.line(screen, color, (0, y), (SCREEN_WIDTH, y))

    # Move and update ground sprites
    if is_off_screen(ground_group.sprites()[0]):
        ground_group.remove(ground_group.sprites()[0])
        new_ground = Ground(GROUND_WIDTH - 20)
        ground_group.add(new_ground)

    # Move and update pipe sprites
    if is_off_screen(pipe_group.sprites()[0]):
        pipe_group.remove(pipe_group.sprites()[0])
        pipe_group.remove(pipe_group.sprites()[0])
        pipes = get_random_pipes(SCREEN_WIDTH * 2)
        pipe_group.add(pipes[0])
        pipe_group.add(pipes[1])

    # Update bird, ground, and pipe sprites
    bird_group.update()
    ground_group.update()
    pipe_group.update()

    # Draw sprites on the screen
    bird_group.draw(screen)
    pipe_group.draw(screen)
    ground_group.draw(screen)

    pygame.display.update()

    # Check for collisions
    if (pygame.sprite.groupcollide(bird_group, ground_group, False, False, pygame.sprite.collide_mask) or
            pygame.sprite.groupcollide(bird_group, pipe_group, False, False, pygame.sprite.collide_mask)):
        pygame.mixer.music.load(hit_sound)
        pygame.mixer.music.play()
        time.sleep(1)
        break
