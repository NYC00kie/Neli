import pygame
import sys
from Logic import Table
from threading import Thread
import time


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
        table = Table(2, 0)
        table.startgame()
        commonmemdict = {"rungame": True}
        print(id(commonmemdict))
        gamethread = Thread(target=table.gameloop, args=(commonmemdict,))
        gamethread.start()
        time.sleep(0.01)
        commonmemdict["rungame"] = False
        gamethread.join()


if __name__ == "__main__":
    d = Draw()
    d.drawgame()
