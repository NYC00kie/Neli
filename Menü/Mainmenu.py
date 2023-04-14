import pygame
import sys
import button


class Button:
    """Create a button, then blit the surface in the while loop"""

    def __init__(self, text: str,  pos: list, font: int, assignedfunc: object, bg="black", feedback=""):
        self.x, self.y = pos
        self.font = pygame.font.SysFont("Arial", font)
        self.assignedfunc = assignedfunc
        if feedback == "":
            self.feedback = "text"
        else:
            self.feedback = feedback
        self.change_text(text, bg)

    def change_text(self, text: str, bg="black"):
        """Change the text whe you click"""
        self.text = self.font.render(text, 1, pygame.Color("White"))
        self.size = self.text.get_size()
        print(self.size)
        self.surface = pygame.Surface(self.size)
        self.surface.fill(bg)
        self.surface.blit(self.text, (0, 0))
        self.rect = pygame.Rect(
            self.x-0.5*self.size[0], self.y, self.size[0], self.size[1])

    def show(self, screen):
        screen.blit(self.surface, (self.x-(0.5*self.size[0]), self.y))

    def click(self, event, pygame):
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if self.rect.collidepoint(x, y):
                    self.change_text(self.feedback, bg="red")
                    self.assignedfunc()

    def hover(self, screen):
        pass


def SettingsMenu():
    pass


def startgame():
    pass


def Mainmenu(callback, screen):  # Mainmenu
    HEIGHT = 1280
    WIDTH = 720
    screen = pygame.display.set_mode((HEIGHT, WIDTH))
    #load images
    bg_1_img = pygame.image.load('./Menü/Images/Bg_1.png')
    bg_2_img = pygame.image.load('./Menü/Images/Bg_2.png')
    bg_3_img = pygame.image.load('./Menü/Images/Bg_3.png')
    bg_4_img = pygame.image.load('./Menü/Images/Bg_4.png')
    bg_5_img = pygame.image.load('./Menü/Images/Bg_5.png')
    background = bg_1_img

    btns = [
        Button(text="Start", pos=(WIDTH/2, HEIGHT/2), font=35, assignedfunc=)
    ]

    menu = True

    while menu:
        events = pygame.event.get()
        pressed_keys = pygame.key.get_pressed()
        for event in events:
            if event.type == pygame.QUIT or pressed_keys[pygame.K_ESCAPE]:
                sys.exit()
            for btn in btns:
                btn.click(event, pygame)

    return callback, background
