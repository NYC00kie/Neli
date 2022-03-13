"""docstring for draw."""
import sys
import random
from threading import Thread
import threading
import pygame
from logic import Table


def update_fps(clock, font):
    """updates the fps counter"""
    fps = str(int(clock.get_fps()))
    fps_text = font.render(fps, 1, pygame.Color("coral"))
    return fps_text


def checkcardclick(rects, commonmemdict, eventobj, mousepos):
    """check if the click was on a card
    if it was then tell the game thread which card and set the event object"""
    for index, rect in enumerate(rects):
        if rect.collidepoint(mousepos):
            commonmemdict["index_playedcard"] = index
            eventobj.set()


class Draw():
    """docstring for class Draw."""

    def __init__(self, playercount: int, npccount: int):
        pygame.init()
        self.pygame = pygame
        self.menudimension = (700, 600)
        self.table = Table(playercount=playercount, npccount=npccount)
        self.clock = pygame.time.Clock()
        self.clockfont = pygame.font.SysFont("Arial", 18)
        self.background = f"./Backgrounds/bg-{random.randint(1,5)}.jpg"
        self.deckindex = 0
        self.screen = self.pygame.display.set_mode(self.menudimension)
        self.cards_and_pic = self.generatecardimages()

    def generatecardimages(self):
        """generates the card images for display"""
        cards_and_pic = {}
        for card in self.table.deck.undrawncards:
            paf = f"./Deck{self.deckindex}/{card.color}-{card.value}-min.bmp"
            img = pygame.image.load(paf).convert_alpha()
            cards_and_pic[str(card)] = img

        return cards_and_pic

    def movecard_onhover(self, pos, rects):
        """Checks if the mouse hovers over a card rectangle
        Returns the index of this card"""

        for index, rect in enumerate(rects):
            if rect.collidepoint(pos):
                rects[index] = rects[index].move(
                    0, - int(self.screen.get_height() / 6))
        return rects

    def drawmenu(self):
        """draws the menu"""
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

    def drawgame(self):
        """method to draw the current state of the game"""
        #
        # Draw the current Card in the Middle of the screen
        # Draw the Players Cards in the Bottom of the Screen
        # Move the hovered over Card a bit up
        #

        # set screen
        self.screen = self.pygame.display.set_mode(
            self.menudimension)

        # set values that need to be initialised before the loop
        width, height = self.screen.get_width(), self.screen.get_height()
        rects = []

        background = self.background
        bgimg = pygame.transform.smoothscale(pygame.image.load(
            background).convert_alpha(), (width, height))

        # the curr_player_index gets overwritten directly in the gamethread but this might be needed for some systems
        commonmemdict = {"rungame": True, "curr_player_index": 0}

        # init the game and start the gameloop thread

        eventobj = threading.Event()
        gamethread = Thread(target=self.table.gameloop,
                            args=(commonmemdict, eventobj))

        gamethread.start()

        # generate the fonts, pictures etc. for displaying cards

        self.table.startgame()

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
                        checkcardclick(rects, commonmemdict,
                                       eventobj, mousepos)

            # Recompute Rects for Player Cards
            hand = self.table.players[commonmemdict["curr_player_index"]].holding

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

                transformed = pygame.transform.smoothscale(
                    self.cards_and_pic[str(hand[index])], (rect.w, rect.h))
                self.screen.blit(transformed, rect)
                pygame.draw.rect(self.screen, "GREEN", rect, 2)

            # draw cards in the middle of the board
            # for an aspect ratio of 309 to 436 the factor 0.708715596 is needed

            middlesize_rect = pygame.Rect(
                (int((width/2)-int(0.708715596 * int(height/5))/2),
                 int(height / 2-(height/5))),
                (int(0.708715596 * int(height/5)), int(height/5))
                )

            self.screen.blit(
                pygame.transform.smoothscale(self.cards_and_pic[str(
                    self.table.playedcards[-1])], (middlesize_rect.w, middlesize_rect.h)), middlesize_rect
            )

            # fps counter
            self.screen.blit(update_fps(self.clock, self.clockfont), (10, 0))

            # Render the Players number in the top right corner
            playernum_txt = self.clockfont.render(
                str(commonmemdict["curr_player_index"]), True, "#FFFFFF")

            self.screen.blit(
                playernum_txt, (width - playernum_txt.get_width(), 0))

            self.pygame.display.update()


if __name__ == "__main__":
    d = Draw(playercount=1, npccount=1)
    d.drawgame()
