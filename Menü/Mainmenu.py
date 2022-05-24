import pygame
import sys
import button

# Julia


class Buetton():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(
            image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):
        action = False
        #mouse position
        mouse_pos = pygame.mouse.get_pos()

        #mouseover and conditions
        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        #button on surface
        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action


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
    bg_1_button_img = pygame.image.load('./Menü/Images/Bg_button_1.png')
    bg_2_button_img = pygame.image.load('./Menü/Images/Bg_button_2.png')
    bg_3_button_img = pygame.image.load('./Menü/Images/Bg_button_3.png')
    bg_4_button_img = pygame.image.load('./Menü/Images/Bg_button_4.png')
    bg_5_button_img = pygame.image.load('./Menü/Images/Bg_button_5.png')
    start_img = pygame.image.load('./Menü/Images/Start_img.png')
    nein_img = pygame.image.load('./Menü/Images/ja2.png')
    ja_img = pygame.image.load('./Menü/Images/ja.png')
    anleitung_img = pygame.image.load(
        './Menü/Images/Anleitung_img.png').convert_alpha()

    mod_1_img = pygame.image.load('./Menü/Images/Mod_1.png')
    mod_2_img = pygame.image.load('./Menü/Images/Mod_2.png')

    #Create  Buettons
    #@param x , y , image , scale
    start_button = Buetton(900, 100, start_img, 1)
    bg_1_button = Buetton(100, 450, bg_1_button_img, 0.3)
    bg_2_button = Buetton(250, 450, bg_2_button_img, 0.3)
    bg_3_button = Buetton(400, 450, bg_3_button_img, 0.3)
    bg_4_button = Buetton(550, 450, bg_4_button_img, 0.3)
    bg_5_button = Buetton(700, 450, bg_5_button_img, 0.3)

    #Text
    font = pygame.font.Font(None, 32)
    text1 = 'Willst du mit einem Partner spielen?'
    text = font.render(text1, True, (0, 0, 0), None)
    text_rect = text.get_rect()
    text_rect.topleft = (600, 600)

    input_rect = pygame.Rect(100, 100, 150, 28)

    #Mainloop
    #var
    background = bg_1_img

    #modus für Kartenstil True = 1 und False = 2
    Mode = False

    gameActive = True

    while gameActive:

        #background
        screen.fill((255, 255, 255))
        screen.blit(background, (0, 0))

        #buttons
        if start_button.draw(screen):
            #hier Start def einfügen,
            gameActive = False

        if bg_1_button.draw(screen):
            background = bg_1_img
        if bg_2_button.draw(screen):
            background = bg_2_img
        if bg_3_button.draw(screen):
            background = bg_3_img
        if bg_4_button.draw(screen):
            background = bg_4_img
        if bg_5_button.draw(screen):
            background = bg_5_img

        #Partner spielen

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameActive = False
                sys.exit()

        pygame.display.update()

    return callback, background


def Anleitung(background, screen):  # anleitung

    running = True
    anleitung_text_img = pygame.image.load(
        './Menü/Images/Anleitung_text.png').convert_alpha()
    anleitung_text_button = Buetton(50, 50, anleitung_text_img, 0.5)
    while running:

        screen.blit(background, (0, 0))

        #place anleitung
        if anleitung_text_button.draw(screen):
            running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        pygame.display.update()
