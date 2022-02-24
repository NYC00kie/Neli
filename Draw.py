import pygame
import sys


class Draw():

    def __init__(self):
        pygame.init()
        self.pygame = pygame
        self.menudimension = (700, 600)

    def drawmenu(self):
        self.screen = self.pygame.display.set_mode(self.menudimension)
        while True:
            events = pygame.event.get()
            pressed_keys = pygame.key.get_pressed()
            for event in events:
                if event.type == pygame.QUIT or pressed_keys[pygame.K_ESCAPE]:
                    sys.exit()

            self.screen.fill((60, 25, 60))
            self.pygame.display.update()
        pass

    def drawgame(self):
        pass


if __name__ == "__main__":
    d = Draw()
    d.drawmenu()
