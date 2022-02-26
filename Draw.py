import pygame
import sys
from Logic import Table
from threading import Thread
import threading
import time


class Draw():

    def __init__(self):
        pygame.init()
        self.pygame = pygame
        self.menudimension = (700, 600)
        self.clock = pygame.time.Clock()

    def drawmenu(self):
        self.screen = self.pygame.display.set_mode(self.menudimension)

        while True:
            self.clock.tick(30)
            events = pygame.event.get()
            pressed_keys = pygame.key.get_pressed()
            for event in events:
                if event.type == pygame.QUIT or pressed_keys[pygame.K_ESCAPE]:
                    sys.exit()

            self.screen.fill((60, 25, 60))
            self.pygame.display.update()
        pass

    def drawgame(self):

        #
        # Draw the current Card in the Middle of the screen
        # Draw the Players Cards in the Bottom of the Screen
        # Move the hovered over Card a bit up
        #

        table = Table(playercount=2, npccount=0)

        font = pygame.font.SysFont("dejavusans", 12)
        cards_and_text = {}
        for card in [str(x) for x in table.deck.undrawncards]:
            cards_and_text[card] = font.render(card, True, "BLUE")
        commonmemdict = {"rungame": True}

        print(id(commonmemdict))

        # init the game and start the gameloop thread
        table.startgame()
        eventobj = threading.Event()
        gamethread = Thread(target=table.gameloop,
                            args=(commonmemdict, eventobj))

        gamethread.start()

        self.screen = self.pygame.display.set_mode(self.menudimension)
        width, height = self.screen.get_width(), self.screen.get_height()

        while True:
            self.clock.tick(30)
            self.screen.fill((60, 25, 60))
            events = pygame.event.get()
            pressed_keys = pygame.key.get_pressed()

            for event in events:
                if event.type == pygame.QUIT or pressed_keys[pygame.K_ESCAPE]:
                    eventobj.set()
                    commonmemdict["rungame"] = False
                    gamethread.join()
                    sys.exit()

            hand = table.players[commonmemdict["curr_player_index"]].holding

            cords = [[int((width/len(hand))*x), int(height - height/10)]
                     for x in range(len(hand))]

            for index, cord in enumerate(cords):
                self.screen.blit(cards_and_text[str(hand[index])], cord)

            self.pygame.display.update()


if __name__ == "__main__":
    d = Draw()
    d.drawgame()
