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

    def update_fps(self, clock, font):
        fps = str(int(clock.get_fps()))
        fps_text = font.render(fps, 1, pygame.Color("coral"))
        return fps_text

    def movecard_onhover(self, pos, rects):
        """Checks if the mouse hovers over a card rectangle
        Returns the index of this card"""

        for index in range(len(rects)):
            if rects[index].collidepoint(pos):

                rects[index] = rects[index].move(
                    0, - int(self.screen.get_height()/6))

        return rects

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
            cards_and_text[card] = font.render(card, True, "#f100ff")
        commonmemdict = {"rungame": True}

        print(id(commonmemdict))

        # init the game and start the gameloop thread
        table.startgame()
        eventobj = threading.Event()
        gamethread = Thread(target=table.gameloop,
                            args=(commonmemdict, eventobj))

        gamethread.start()

        # set values that need to be initialised before the loop
        self.screen = self.pygame.display.set_mode(
            self.menudimension)
        width, height = self.screen.get_width(), self.screen.get_height()
        rects = []
        clockfont = pygame.font.SysFont("Arial", 18)

        count = 0
        while True:

            self.screen.fill((60, 25, 60))
            events = pygame.event.get()
            pressed_keys = pygame.key.get_pressed()
            mousepos = pygame.mouse.get_pos()

            for event in events:
                if event.type == pygame.QUIT or pressed_keys[pygame.K_ESCAPE]:
                    eventobj.set()
                    commonmemdict["rungame"] = False
                    gamethread.join()
                    sys.exit()
                # check for button press
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_presses = pygame.mouse.get_pressed()
                    if mouse_presses[0]:
                        # check if the click was on a card
                        # if it was then tell the game thread which card and set the event object
                        for index, rect in enumerate(rects):
                            if rect.collidepoint(mousepos):
                                commonmemdict["index_playedcard"] = index
                                eventobj.set()

            # Recompute Rects for Player Cards

            hand = table.players[commonmemdict["curr_player_index"]].holding

            rects = []
            for index in range(len(hand)):
                rect_posh = int(width/len(hand))*index
                rect_post = int(height - (height/3))
                rect_width = int(width/len(hand))
                rect_height = int(height/3)
                rect = pygame.Rect(
                    (rect_posh, rect_post),
                    (rect_width, rect_height)
                )
                rects.append(rect)

            rects = self.movecard_onhover(mousepos, rects)

            # draw the cards in the Players Hand and draw rectangles around them
            hand = table.players[commonmemdict["curr_player_index"]].holding

            for index, rect in enumerate(rects):
                self.screen.blit(cards_and_text[str(hand[index])], rect)
                pygame.draw.rect(self.screen, "GREEN", rect, 2)

            # draw cards in the middle of the board
            self.screen.blit(
                cards_and_text[str(table.playedcards[-1])],
                (
                    int((width/2)
                        - cards_and_text[str(table.playedcards[-1])].get_width()/2),
                    int(height/2-height/10)
                )
            )

            # fps counter
            self.screen.blit(self.update_fps(self.clock, clockfont), (10, 0))

            # Render the Players number in the top right corner
            playernum_txt = clockfont.render(
                str(commonmemdict["curr_player_index"]), True, "#FFFFFF")
            self.screen.blit(
                playernum_txt, (width-playernum_txt.get_width(), 0))

            self.pygame.display.update()

            self.clock.tick(30)


if __name__ == "__main__":
    d = Draw()
    d.drawgame()
