import pygame
import game_object
import game_menu
from constants import *

class Game:
    def __init__(self):
        # инициализируем библиотеку pygame
        pygame.init()
        # создаем графическое окно
        self.screen = pygame.display.set_mode([WIN_WIDTH, WIN_HEIGHT])
        self.background_img = pygame.image.load("background.png").convert()
        pygame.display.set_caption("Platformer")
        # создаем группу для всех спрайтов в игре
        self.all_sprite_list = pygame.sprite.Group()
        # Создаем спрайт игрока
        self.player = game_object.Player(20, 540)
        self.all_sprite_list.add(self.player)
        # создаем группу спрайтов - препятствий (платформ)
        self.platform_list = pygame.sprite.Group()
        # Создаем платформы
        self.create_walls()
        # Создаем артефакты
        self.artifact_list = pygame.sprite.Group()
        self.create_artifacts()
        # Задаем группу спрайтов - препятствий для игрока
        self.player.platforms = self.platform_list
        self.player.artifacts = self.artifact_list
        self.clock = pygame.time.Clock()
        # Задаем текущие состоятния игры ("START", "GAME", "PAUSE" или "FINISH")
        self.state = "START"

        self.main_menu = game_menu.MainMenu(300, 200)

    def create_artifacts(self):
        # Создаем артефакты (монеты) в игре
        artifact_coords = [
            [170, 405],
            [320, 410],
            [370, 510],
            [420, 310],
            [565, 505],
            [745, 485]
        ]
        for coord in artifact_coords:
            artifact = game_object.Artifact(coord[0], coord[1])
            self.artifact_list.add(artifact)
            self.all_sprite_list.add(artifact)

    def create_walls(self):
        # Создаем стены и платформы
        platform_coords = [
            [0, 0, 10, 600],
            [790, 0, 10, 600],
            [0, 590, 600, 10],
            [450, 500, 20, 100],
            [250, 550, 20, 60],
            [550, 450, 250, 10]
        ]
        for coord in platform_coords:
            platform = game_object.Platform(coord[0], coord[1], coord[2], coord[3])
            self.platform_list.add(platform)
            self.all_sprite_list.add(platform)
        

    def handle_scene(self, event):
        active_button = self.main_menu.handle_mouse_event(event.type)
        # обрабатываем сцену Идет Игра
        if self.state == "GAME":
            # обрабатываем нажатие клавиш - стрелок
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.go_left()
                elif event.key == pygame.K_RIGHT:
                    self.player.go_right()
                elif event.key == pygame.K_UP:
                    self.player.jump()

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and self.player.change_x < 0:
                    self.player.stop()
                if event.key == pygame.K_RIGHT and self.player.change_x > 0:
                    self.player.stop()

        # Обрабатываем сцену Стартовый экран
        elif self.state == "START" :
            pass
        # обрабатываем сцену Игра Закончена
        elif self.state == "FINISH":
            pass

    def draw_scene(self):
        # Выполняем заливку экрана
        self.screen.blit(self.background_img, (0, 0))
        # Обрабатываем сцену Идет Игра
        if self.state == "GAME":
            self.all_sprite_list.draw(self.screen)
        # Обрабатываем сцену Стартовый экран
        elif self.state == "START":
            self.main_menu.draw(self.screen)
        # Обрабатываем сцену Пауза
        elif self.state == "PAUSE": pass
        # Обрабатываем сцену Игра Окончена
        elif self.state == "FINISH": pass
    
    def run(self):
        done = False
        while not done:
            for event in pygame.event.get():
                # Обрабатываем закрытие окна
                if event.type == pygame.QUIT:
                    done = True
                # Обрабатываем события для разных состояний игры:
                self.handle_scene(event)
            # Если идет игра, обновляем положение всех спрайтов в игре:
            if self.state == "GAME":
                self.all_sprite_list.update()
                # Проверяем, не достиг ли игрок выхода:
                if self.player.rect.x > WIN_WIDTH - 70 and self.player.rect.y > WIN_HEIGHT - 70:
                    self.state = "FINISH"
                    done = True
            # Прорисовываем экран в зависимости от состояния игры 
            self.main_menu.update()
            self.draw_scene()
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()

game = Game()
game.run()
