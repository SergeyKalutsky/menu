import pygame
from constants import *


class Button():
    def __init__(
            self, x, y, w, h, name,
            font_color=WHITE,
            normal_color=BLUE,
            highlight_color=GREEN,
            active_color=BLACK,
            size=24,
            font='Arial',
            padding=5
    ):
        # Текущее состояние кнопки. Все состояния: normal'   'highlight'  'active'
        self.state = 'normal'
        # Задаем цвета кнопки в нормальном, веделенном и активном состоянии:
        self.normal_color = normal_color
        self.highlight_color = highlight_color
        self.active_color = active_color
        # Задаем название  - текст на кнопке
        self.name = name
        pygame.font.init()
        self.font = pygame.font.SysFont(font, size, True)
        # Создаем надпись на кнопке
        self.text = self.font.render(name, True, font_color)
        # Задаем размеры прямоугольника
        self.image = pygame.Surface([w, h])
        self.image.fill(normal_color)
        # Задаем положение верхней панели на экране
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        # Задаем поля - отступы от границы кнопки для текста
        self.padding = padding

    # Рисуем прямоугольник кнопки и надпись на ней
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.text, (self.rect.x + self.padding,
                    self.rect.y + self.padding))

    # В методе update меняем цвет кнокпи в зависимости от состояния

    def update(self):
        if self.state == 'normal':
            self.image.fill(self.normal_color)
        elif self.state == 'highlight':
            self.image.fill(self.highlight_color)
        elif self.state == 'active':
            self.image.fill(self.active_color)

    # Обработка событий кнопки:  меняем состояние в зависимости от события

    def handle_mouse_action(self, event=None):
        # Получаем текущее положение курсора
        pos_x, pos_y = pygame.mouse.get_pos()
        # Проверяем, находится курсор над кнопкой или нет:
        check_pos = self.rect.left <= pos_x <= self.rect.right and self.rect.top <= pos_y <= self.rect.bottom
        # Курсор движется над кнопкой:
        if event == pygame.MOUSEMOTION:
            if check_pos:
                self.state = 'highlight'
            else:
                self.state = 'normal'
        # На кнопку кликнули:
        elif event == pygame.MOUSEBUTTONDOWN:
            if check_pos:
                self.state = 'active'
            else:
                self.state = 'normal'
        # На кнопку кликнули и отпустили:
        elif event == pygame.MOUSEBUTTONUP:
            if check_pos:
                self.state = 'highlight'
            else:
                self.state = 'normal'


class MainMenu():
    def __init__(self, w, h):
        # Создаем список пунктов меню:
        self.labels = [
            "START",
            "CONTINUE",
            "QUIT"
        ]
        # Задаем координаты верхнего левого угла меню:
        self.x = (WIN_WIDTH - w) // 2
        self.y = (WIN_HEIGHT - h) // 2
        # Создаем список кнопок:
        self.buttons = []
        # Рассчитываем высоту для каждой кнопки меню, исходя и общей высоты:
        button_height = int(h / (len(self.labels) + 1))
        # Локальная переменная, хранит y координату для текущей кнопки:
        current_y = self.y
        for label in self.labels:
            # Создаем новую кнопку:
            new_button = Button(self.x, current_y, w, button_height, label)
            # Переходим по вертикали к следующей кнопке с отступом в 2 пикселя,
            # чтобы кнопки визуально не "слиплись" между собой:
            current_y += button_height + 2
            # Добавляем новую кнопку в список всех кнопок меню:
            self.buttons.append(new_button)

    # Вызвать метод update() для всех кнопок в меню:
    def update(self):
        for button in self.buttons:
            button.update()

    # Вызвать метод обработки события для всех кнопок в меню:
    def handle_mouse_event(self, event):
        for button in self.buttons:
            button.handle_mouse_action(event)
        # запоминаем и возвращаем кнопку, н которую сейчас нажали:
            if button.state == "active":
                return button
        
    # Вызвать метод draw для всех кнопок в меню
    def draw(self, screen):
        for button in self.buttons:
            button.draw(screen)

class TopPanel():
    def __init__(self, x=5, y=5):
        self.font = pygame.font.SysFont('Arial', 25, True)
        self.text = self.font.render('ПРИВЕТ', True, YELLOW)

        self.surface = pygame.Surface([WIN_WIDTH, 40])
        self.surface.fill(BLUE)

        self.rect = self.surface.get_rect()
        self.rect.x, self.rect.y = x, y
    
    def draw(self, screen):
        screen.blit(self.surface, self.rect)
        screen.blit(self.text, (self.rect.x+10, self.rect.y+2))

