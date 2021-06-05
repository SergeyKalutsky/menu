import pygame
from constants import *


class Player(pygame.sprite.Sprite):
    # Этот класс описывает управление и поведение спрайта игрока
    # Конструктор класса
    def __init__(self, x, y, img='chick.png'):
        super().__init__()
        # Задаем размеры прямоугольника
        self.image = pygame.image.load(img).convert_alpha()
        # Задаем положение спрайта игрока на экране
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        # Задаем скорость игрока по x и по y
        self.change_x = 0
        self.change_y = 0
        self.platforms = pygame.sprite.Group()
        # Добавляем поле artifacts:
        self.artifacts = pygame.sprite.Group()
        self.score = 0
    
    # Расчет гравитации
    def calc_grav(self):
        if self.change_y == 0:
            self.change_y = 1
        else:
            # Моделируем ускорение свободного падения:
            self.change_y += .35

        # Проверка: персонаж на земле или нет
        if self.rect.y >= WIN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = WIN_HEIGHT - self.rect.height
    
    def update(self):
        # учитываем эффект гравитации:
        self.calc_grav()
        # Пересчитываем положение спрайта игрока на экране
        # Смещение влево - вправо
        self.rect.x += self.change_x

        # Проверяем столкновение с препятствием
        block_hit_list = pygame.sprite.spritecollide(self, self.platforms, False)
        for block in block_hit_list:
            # Если персонаж двигался вправо, остановим его слева от препятствия
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # Наоборот, если движение было влево остановим его справа от препятствия
                self.rect.left = block.rect.right

        # Движение вверх-вниз
        self.rect.y += self.change_y

        # Проверяем столкновение с препятствием
        block_hit_list = pygame.sprite.spritecollide(self, self.platforms, False)
        for block in block_hit_list:
            # При движении вниз, персонаж упал на препятствие - он должен встать на него сверху
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom

            # В прыжке персонаж врезался в препятствия - движение вверх должно прекратиться.
            self.change_y = 0

        # Проверяем столкновение с артефактом
        artifact_hit_list = pygame.sprite.spritecollide(self, self.artifacts, False)
        for artifact in artifact_hit_list:
            self.score += 1
            artifact.kill()

    def jump(self):
        # двигаемся вниз на 2 пикселя, чтобы убедиться, что под игроком есть платформа
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.platforms, False)
        self.rect.y -= 2

        # если платформа есть, то можно прыгнуть, оттолкнувшись от нее
        if len(platform_hit_list) > 0 or self.rect.bottom >= WIN_HEIGHT:
            self.change_y = -10

    # Управление игроком:
    def go_left(self):
        # Нажатие кнопки влево. 
        self.change_x = -6

    def go_right(self):
        # Нажатие кнопки вправо. 
        self.change_x = 6

    def stop(self):
        # Отпустили кнопку, прекратили вижение по горизонтали 
        self.change_x = 0

class Artifact(pygame.sprite.Sprite):
    def __init__(self, x, y, img='coin.png'):
        super().__init__()
        super().__init__()
        # Задаем размеры прямоугольника
        self.image = pygame.image.load(img).convert_alpha()
        # Задаем положение спрайта игрока на экране
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

class Platform(pygame.sprite.Sprite):
# Препятствия, по которым моежт перемещаться персонаж, но не сквозь них

    def __init__(self, x, y, width, height, color=BLUE):
        super().__init__()
        # Создаем прямоугольник заданных параметров
        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        # Помещаем прямоугольник в заданне место на экране
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
