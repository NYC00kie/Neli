"""
#docstring for draw.
"""
import sys
import random
import time
from threading import Thread
import threading
import copy
import pygame
import pygame_widgets
from pygame_widgets.slider import Slider
from logic import Table
from logic import Card
from button import Button
from button import Buetton


def update_fps(clock, font):
    """
    #updates the fps counter
    """
    fps = str(int(clock.get_fps()))
    fps_text = font.render(fps, 1, pygame.Color("coral"))
    return fps_text


def checkcardclick(rects, commonmemdict, eventobj, mousepos):
    """
    #check if the click was on a card
    #if it was then tell the game thread which card and set the event object
    """
    for index, rect in enumerate(rects):
        if rect.collidepoint(mousepos):
            commonmemdict["index_playedcard"] = index
            eventobj.set()


class Draw():
    """
    #docstring for class Draw.
    """

    def __init__(self, playercount: int, npccount: int):
        pygame.init()
        self.musicobject = None
        self.pygame = pygame
        self.menudimension = (700, 600)
        self.table = Table(playercount=playercount, npccount=npccount)
        self.clock = pygame.time.Clock()
        self.clockfont = pygame.font.SysFont("Arial", 18)
        self.playernumfont = pygame.font.SysFont("Arial", 25)
        self.deckindex = 0
        self.screen = self.pygame.display.set_mode(self.menudimension)
        self.background = f"./Backgrounds/bg-{random.randint(1,5)}.jpg"
        self.backgroundimg = pygame.image.load(self.background).convert()
        self.cards_and_pic = self.generatecardimages()
        self.bg_average_color = pygame.transform.average_color(
            self.backgroundimg)
        self.inverted_bgavgcolor = [
            255-self.bg_average_color[i] for i in range(0, 3)
            ]
        width = self.menudimension[0]
        height = self.menudimension[1]
        self.slider = Slider(self.screen, int(width/2-(0.5*width*1/4)), int(height/2+50*(2+1)),
                             width*1/4, 20, min=0, max=0.6, step=0.01, initial=0.1)
        print(self.bg_average_color, self.inverted_bgavgcolor)

    def generatecardimages(self):
        """
        #generates the card images for display
        """
        cards_and_pic = {}
        drawy_cards = [Card("EMPTY", "BLUE"), Card("EMPTY", "GREEN"), Card(
            "EMPTY", "RED"), Card("EMPTY", "YELLOW")]
        drawy_cards += self.table.deck.undrawncards
        for card in drawy_cards:
            paf = f"./Deck{self.deckindex}/{card.color}-{card.value}-min.bmp"
            img = pygame.image.load(paf).convert_alpha()
            cards_and_pic[str(card)] = img

        print(cards_and_pic)
        return cards_and_pic

    def movecard_onhover(self, pos, rects):
        """
        #Checks if the mouse hovers over a card rectangle
        #Returns the index of this card
        """

        for index, rect in enumerate(rects):
            if rect.collidepoint(pos):
                rects[index] = rects[index].move(
                    0, - int(self.screen.get_height() / 6))
        return rects

    def setFalse(self, x):
        global loop
        loop = False

    def drawsettings(self):

        global loop, slider
        loop = True
        width = self.menudimension[0]
        height = self.menudimension[1]
        btns = [
            Buetton(text="Return", pos=(width/2, height/2), font=35,
                    assignedfunc=lambda: self.setFalse(loop))

        ]

        while loop:
            self.clock.tick(90)
            events = pygame.event.get()
            pressed_keys = pygame.key.get_pressed()
            for event in events:
                if event.type == pygame.QUIT or pressed_keys[pygame.K_ESCAPE]:
                    sys.exit()
                for btn in btns:
                    btn.click(event, pygame)
            self.screen.blit(pygame.transform.scale(
                self.backgroundimg, self.menudimension), (0, 0))

            for btn in btns:
                btn.hover(self.screen)
            for btn in btns:
                btn.show(self.screen)

            self.musicobject.set_volume(self.slider.getValue())

            pygame_widgets.update(events)
            pygame.display.update()

    def drawmenu(self):
        """
        #draws the menu
        """
        self.screen = self.pygame.display.set_mode(self.menudimension)

        self.musicobject = pygame.mixer.Sound("./Music/Sound_Startseite.mp3")
        self.musicobject.set_volume(0.1)
        self.musicobject.play(-1)
        playercount = 1
        self.deckindex = 0
        self.Table = Table(playercount=playercount, npccount=1)
        self.cards_and_pic = self.generatecardimages()
        btns = [
            Buetton(text="Single Player", pos=(self.menudimension[0]/2, (self.menudimension[1]/4)+0),
                    font=35, assignedfunc=self.drawgame, feedback="Single Player"),
            Buetton(text="Multiplayer", pos=(self.menudimension[0]/2, (self.menudimension[1]/4)+50),
                    font=35, assignedfunc=self.drawsettings, feedback="Multiplayer"),
            Buetton(text="Settings", pos=(self.menudimension[0]/2, (self.menudimension[1]/4)+100),
                    font=35, assignedfunc=self.drawsettings, feedback="Settings")
        ]

        while True:
            events = pygame.event.get()
            self.clock.tick(90)
            pressed_keys = pygame.key.get_pressed()
            for event in events:
                if event.type == pygame.QUIT or pressed_keys[pygame.K_ESCAPE]:
                    sys.exit()
                for btn in btns:
                    btn.click(event, pygame)
            self.screen.blit(pygame.transform.scale(
                self.backgroundimg, self.menudimension), (0, 0))

            for btn in btns:
                btn.hover(self.screen)
            for btn in btns:
                btn.show(self.screen)

            pygame.display.update()

    def display_Wildcardchoose(self, commonmemdict, eventobj) -> None:
        """
        #Returns None
        #displays a chosing screen for the wildcard card
        #A 2 by 2 Pattern of colors will be displayed with the colors equal to the Cards colors
        """

        # the Cards color gets determined by taking the average color
        # of the Card with value of 1 and the corresponding colors
        # what gets drawn by pygame are

        width, height = self.screen.get_width(), self.screen.get_height()

        Yellow = {
            "name": "YELLOW",
            "color": pygame.transform.average_color(self.cards_and_pic["YELLOW 1"]),
            "rect": pygame.Rect(0, 0, width/2, height/2)}

        Green = {
            "name": "GREEN",
            "color": pygame.transform.average_color(self.cards_and_pic["GREEN 1"]),
            "rect": pygame.Rect(width/2, 0, width/2, height/2)
            }

        Red = {
            "name": "RED",
            "color": pygame.transform.average_color(self.cards_and_pic["RED 1"]),
            "rect": pygame.Rect(0, height/2, width/2, height/2)
            }

        Blue = {
            "name": "BLUE",
            "color": pygame.transform.average_color(self.cards_and_pic["BLUE 1"]),
            "rect": pygame.Rect(width/2, height/2, width/2, height/2)
            }

        pygame.draw.rect(self.screen, Yellow["color"], Yellow["rect"])
        pygame.draw.rect(self.screen, Green["color"], Green["rect"])
        pygame.draw.rect(self.screen, Red["color"], Red["rect"])
        pygame.draw.rect(self.screen, Blue["color"], Blue["rect"])

        self.pygame.display.update()
        # a color need to be chosen to leave this loop and to end the game
        loop = True
        while loop:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_presses = pygame.mouse.get_pressed()
                    if mouse_presses[0]:
                        mousepos = pygame.mouse.get_pos()
                        for color in [Blue, Red, Green, Yellow]:
                            if color["rect"].collidepoint(mousepos):
                                chosen_color = color["name"]
                                loop = False
                                break

        commonmemdict["chosen_color"] = chosen_color
        commonmemdict["display_wildcard_screen"] = False
        eventobj.set()

    def drawgame(self):
        """
        #method to draw the current state of the game
        """

        # Draw the current Card in the Middle of the screen
        # Draw the Players Cards in the Bottom of the Screen
        # Move the hovered over Card a bit up

        # set music
        self.musicobject.stop()
        self.musicobject = pygame.mixer.Sound("./Music/Spielsound_Neli.mp3")
        self.musicobject.set_volume(0.1)
        self.musicobject.play(-1)

        # set screen
        self.screen = self.pygame.display.set_mode(
            self.menudimension)

        # set values that need to be initialised before the loop
        width, height = self.screen.get_width(), self.screen.get_height()
        rects = []

        bgimg = pygame.transform.smoothscale(
            self.backgroundimg, (width, height))

        # the curr_player_index gets overwritten directly in the gamethread but this might be needed for some systems
        commonmemdict = {"rungame": True, "curr_player_index": 0,
                         "display_wildcard_screen": False, "display_uno": False}
        hand = copy.deepcopy(
            self.table.players[commonmemdict["curr_player_index"]].holding)

        # init the game and start the gameloop thread

        uno_btn = Button("Neli", (width/2, 0), 32,
                         commonmemdict, bg="#777777", feedback="pressed")

        eventobj = threading.Event()
        gamethread = Thread(target=self.table.gameloop,
                            args=(commonmemdict, eventobj))

        gamethread.start()

        self.table.startgame(commonmemdict)

        commonmemdict["display_wildcard_screen"] = False

        while commonmemdict["rungame"]:

            self.screen.blit(bgimg, (0, 0))
            events = pygame.event.get()
            pressed_keys = pygame.key.get_pressed()
            mousepos = pygame.mouse.get_pos()

            self.clock.tick(90)

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
                uno_btn.click(event)

            # Recompute Rects for Player Cards
            hand = copy.deepcopy(
                self.table.players[commonmemdict["curr_player_index"]].holding)

            rects = []
            for index in range(len(hand)):
                rect_posh = int(width / len(hand)) * index
                rect_post = int(height - (height / 3))
                if len(hand) >= 4:
                    rect_width = int(width / len(hand))
                else:
                    rect_width = int(width / 4)
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
                    self.cards_and_pic[str(hand[index])],
                    (rect.w, rect.h)
                )
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
                pygame.transform.smoothscale(
                    self.cards_and_pic[str(self.table.playedcards[-1])], (middlesize_rect.w, middlesize_rect.h)), middlesize_rect
            )

            # fps counter
            self.screen.blit(update_fps(self.clock, self.clockfont), (10, 0))

            # Render the Players number in the top right corner

            playernum_txt = self.clockfont.render(
                f"Player {str(commonmemdict['curr_player_index'])}", True, self.inverted_bgavgcolor)

            self.screen.blit(
                playernum_txt, (width - playernum_txt.get_width(), 0))

            # display Uno Button if necessary
            if commonmemdict['display_uno']:
                uno_btn.show(self.screen)

            self.pygame.display.update()

            # display the wildcard screen for choosing a color
            if commonmemdict["display_wildcard_screen"]:
                self.display_Wildcardchoose(commonmemdict, eventobj)

        # Ending Screen
        self.screen.fill((60, 25, 60))
        end_font = pygame.font.SysFont("Arial", 18)
        end_text = end_font.render("Ende", 1, pygame.Color("coral"))
        self.screen.blit(end_text, (width/2, height/2))
        self.pygame.display.update()
        time.sleep(3)


if __name__ == "__main__":
    d = Draw(playercount=1, npccount=1)
    d.drawgame()
