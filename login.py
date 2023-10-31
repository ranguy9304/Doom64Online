import pygame as pg
from settings import *
# Initialize Pygame
pg.init()


FONT_NAME = pg.font.get_default_font()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

class TextInput:
    def __init__(self, x, y, width, height, text=''):
        self.rect = pg.Rect(x, y, width, height)
        self.color = WHITE
        self.text = text
        self.font = pg.font.Font(FONT_NAME, 32)
        self.txt_surface = self.font.render(text, True, self.color)

    def handle_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
            self.txt_surface = self.font.render(self.text, True, self.color)

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pg.draw.rect(screen, self.color, self.rect, 2)

class Button:
    def __init__(self, x, y, width, height, text, action=None):
        self.rect = pg.Rect(x, y, width, height)
        self.text = text
        self.color = RED
        self.font = pg.font.Font(FONT_NAME, 32)
        self.txt_surface = self.font.render(text, True, BLACK)
        self.action = action

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if self.action:
                    return self.action()
        return None

    def draw(self, screen):
        screen.fill(self.color, self.rect)
        screen.blit(self.txt_surface, (self.rect.x + (self.rect.width - self.txt_surface.get_width()) // 2,
                                       self.rect.y + (self.rect.height - self.txt_surface.get_height()) // 2))
        pg.draw.rect(screen, self.color, self.rect, 2)

class LoginState:
    def __init__(self):
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Login Screen")

        self.background = pg.image.load('background.jpeg')
        self.background = pg.transform.scale(self.background, (WIDTH, HEIGHT))

        self.username_input = TextInput(WIDTH // 4, HEIGHT // 4, WIDTH // 2, 40)
        self.play_button = Button(WIDTH // 4, HEIGHT // 2, WIDTH // 2, 50, 'Play', self.play_game)
        # self.change_res_button = Button(WIDTH // 4, HEIGHT // 2 + 70, WIDTH // 2, 50, 'Change Resolution', self.change_resolution)
        self.done = False

    def play_game(self):
        print("Playing game...")
        self.done = True

    def change_resolution(self):
        global WIDTH, HEIGHT, RES
        if WIDTH == 1920:
            RES = WIDTH, HEIGHT = 860, 540
        else:
            RES = WIDTH, HEIGHT = 1920, 1080
        print("Changing resolution... to ", RES)

    def run(self):
        while not self.done:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.done = True
                self.username_input.handle_event(event)
                action_result = self.play_button.handle_event(event)
                if action_result is not None:
                    return action_result
                # action_result = self.change_res_button.handle_event(event)
                # if action_result is not None:
                #     return action_result
            self.screen.blit(self.background, (0, 0))
            
            self.username_input.draw(self.screen)
            self.play_button.draw(self.screen)
            # self.change_res_button.draw(self.screen)
            pg.display.flip()
        return self.username_input.text


# For testing
# if __name__ == '__main__':
#     print(LoginState().run())

