import pygame
import sys
import random
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
        self.bg = f"./Backgrounds/bg-{random.randint(1,5)}.jpg"
        self.deckindex = 0

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
                    0, - int(self.screen.get_height() / 6))

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

        # set screen
        self.screen = self.pygame.display.set_mode(
            self.menudimension)

        # set values that need to be initialised before the loop
        count = 0
        width, height = self.screen.get_width(), self.screen.get_height()
        rects = []
        clockfont = pygame.font.SysFont("Arial", 18)

        background = self.bg
        bgimg = pygame.transform.smoothscale(pygame.image.load(
            background).convert_alpha(), (width, height))

        # creating the Table object and creating a dictionarie with each card and a text for it
        table = Table(playercount=1, npccount=1)

        # the curr_player_index gets overwritten directly in the gamethread but this might be needed for some systems
        commonmemdict = {"rungame": True, "curr_player_index": 0}

        print(id(commonmemdict))

        # init the game and start the gameloop thread

        eventobj = threading.Event()
        gamethread = Thread(target=table.gameloop,
                            args=(commonmemdict, eventobj))

        gamethread.start()

        # generate the fonts, pictures etc. for displaying cards

        font = pygame.font.SysFont("dejavusans", 12)
        cards_and_text = {}
        cards_and_pic = {}
        for card in [x for x in table.deck.undrawncards]:
            paf = f"./Deck{self.deckindex}/{card.color}-{card.value}-min.bmp"
            img = pygame.image.load(paf).convert_alpha()
            cards_and_pic[str(card)] = img
            cards_and_text[str(card)] = font.render(str(card), True, "#f100ff")

        table.startgame()

        while True:

            self.screen.blit(bgimg, (0, 0))
            events = pygame.event.get()
            pressed_keys = pygame.key.get_pressed()
            mousepos = pygame.mouse.get_pos()

            for event in events:
                if event.type == pygame.QUIT or pressed_keys[pygame.K_ESCAPE]:
                    # need to correctly close the game
                    commonmemdict["index_playedcard"] = 0
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

            # clock tick needed here else it crashes because the length of the hand ist not equal to the length of rects
            self.clock.tick(15)

            rects = []
            for index in range(len(hand)):
                rect_posh = int(width / len(hand)) * index
                rect_post = int(height - (height / 3))
                rect_width = int(width / len(hand))
                rect_height = int(height / 3)
                rect = pygame.Rect(
                    (rect_posh, rect_post),
                    (rect_width, rect_height)
                )
                rects.append(rect)

            rects = self.movecard_onhover(mousepos, rects)

            # draw the cards in the Players Hand and draw rectangles around them

            for index, rect in enumerate(rects):

                key = str(hand[index])
                if cards_and_pic[key]:
                    transformed = pygame.transform.smoothscale(
                        cards_and_pic[str(hand[index])], (rect.w, rect.h))
                    self.screen.blit(transformed, rect)
                else:
                    self.screen.blit(cards_and_text[str(hand[index])], rect)
                pygame.draw.rect(self.screen, "GREEN", rect, 2)

            # draw cards in the middle of the board
            height_rect = int(height/5)
            # for an aspect ratio of 309 to 436 the factor 0.708715596 is needed
            width_rect = int(0.708715596 * height_rect)
            middlesize_rect = pygame.Rect(
                (int((width/2)-width_rect/2), int(height / 2-(height/5))),
                (width_rect, height_rect)
                )
            self.screen.blit(
                pygame.transform.smoothscale(cards_and_pic[str(
                    table.playedcards[-1])], (middlesize_rect.w, middlesize_rect.h)), middlesize_rect
            )

            # fps counter
            self.screen.blit(self.update_fps(self.clock, clockfont), (10, 0))

            # Render the Players number in the top right corner
            playernum_txt = clockfont.render(
                str(commonmemdict["curr_player_index"]), True, "#FFFFFF")
            self.screen.blit(
                playernum_txt, (width - playernum_txt.get_width(), 0))

            self.pygame.display.update()


if __name__ == "__main__":
    d = Draw()
    d.drawgame()
