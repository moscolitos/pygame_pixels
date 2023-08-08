# -*- coding: utf-8 -*-
"""
Created on Tue Aug  8 18:06:40 2023

@author: Mosco
"""

import pygame
import random

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SQUARE_SIZE = 50
COIN_SIZE = 25
ENEMY_SIZE = 35
SPEED = 5

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([SQUARE_SIZE, SQUARE_SIZE])
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = (SCREEN_WIDTH - SQUARE_SIZE) // 2
        self.rect.y = (SCREEN_HEIGHT - SQUARE_SIZE) // 2

    def update(self, keys_pressed):
        if keys_pressed[pygame.K_UP] and self.rect.y > 0:
            self.rect.y -= SPEED
        if keys_pressed[pygame.K_DOWN] and self.rect.y < SCREEN_HEIGHT - SQUARE_SIZE:
            self.rect.y += SPEED
        if keys_pressed[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= SPEED
        if keys_pressed[pygame.K_RIGHT] and self.rect.x < SCREEN_WIDTH - SQUARE_SIZE:
            self.rect.x += SPEED

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([COIN_SIZE, COIN_SIZE])
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - COIN_SIZE)
        self.rect.y = random.randint(0, SCREEN_HEIGHT - COIN_SIZE)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([ENEMY_SIZE, ENEMY_SIZE])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - ENEMY_SIZE)
        self.rect.y = random.randint(0, SCREEN_HEIGHT - ENEMY_SIZE)
        self.direction = random.choice(["left", "right", "up", "down"])

    def update(self):
        if self.direction == "left" and self.rect.x > 0:
            self.rect.x -= SPEED
        elif self.direction == "right" and self.rect.x < SCREEN_WIDTH - ENEMY_SIZE:
            self.rect.x += SPEED
        elif self.direction == "up" and self.rect.y > 0:
            self.rect.y -= SPEED
        elif self.direction == "down" and self.rect.y < SCREEN_HEIGHT - ENEMY_SIZE:
            self.rect.y += SPEED
        else:
            self.direction = random.choice(["left", "right", "up", "down"])

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Pixel Game')

    all_sprites = pygame.sprite.Group()
    coins = pygame.sprite.Group()
    enemies = pygame.sprite.Group()

    player = Player()
    all_sprites.add(player)

    for _ in range(5):
        coin = Coin()
        coins.add(coin)
        all_sprites.add(coin)

    for _ in range(3):
        enemy = Enemy()
        enemies.add(enemy)
        all_sprites.add(enemy)

    score = 0
    running = True
    clock = pygame.time.Clock()

    while running:
        screen.fill(WHITE)

        keys_pressed = pygame.key.get_pressed()
        player.update(keys_pressed)
        enemies.update()

        coin_collision = pygame.sprite.spritecollide(player, coins, True)
        score += len(coin_collision)
        for _ in range(len(coin_collision)):
            coin = Coin()
            coins.add(coin)
            all_sprites.add(coin)

        enemy_collision = pygame.sprite.spritecollide(player, enemies, False)
        if enemy_collision:
            running = False

        all_sprites.draw(screen)

        font = pygame.font.SysFont(None, 55)
        score_display = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_display, (10, 10))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main()
