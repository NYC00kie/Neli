"""
# docstring für unentschieden.
"""
import sys
import random
import time
from threading import Thread
import threading
import copy
import pygame
from logic import Table
from logic import Card
from button import Button
from Menü.Mainmenu import Mainmenu


def update_fps(clock, font):
    """
    # aktualisiert den FPS-Zähler
    """
    fps = str(int(clock.get_fps()))
    fps_text = font.render(fps, 1, pygame.Color("coral"))
    return fps_text


def checkcardclick(rects, commonmemdict, eventobj, mousepos):
    """
    # Prüfen Sie, ob der Klick auf einer Karte war
    # Wenn es dann dem Spiel Thread mitgeteilt hätte, welche Karte und das Ereignisobjekt einstellen
    """
    for index, rect in enumerate(rects):
        if rect.collidepoint(mousepos):
            commonmemdict["index_playedcard"] = index
            eventobj.set()


class Draw():
    """
    # docstring für den Klassenzug.
    """

    def __init__(self, playercount: int, npccount: int):
        pygame.init()
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
        print(self.bg_average_color, self.inverted_bgavgcolor)

    def generatecardimages(self):
        """
        # Erzeugt die Kartenbilder für die Anzeige
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
        # Prüft, ob die Maus über ein Kartenrechteck schwebt
        # Gibt den Index dieser Karte zurück
        """

        for index, rect in enumerate(rects):
            if rect.collidepoint(pos):
                rects[index] = rects[index].move(
                    0, - int(self.screen.get_height() / 6))
        return rects

    def drawmenu(self):
        """
        # Zeichnet das Menü an
        # noch nicht implementiert, weil mir der Code nicht gegeben wurde
        """
        self.screen = self.pygame.display.set_mode(self.menudimension)

        musicobject = pygame.mixer.Sound("./Music/Sound_Startseite.mp3")
        musicobject.set_volume(0.1)
        musicobject.play(-1)

        callback, partner, background, Mode = Mainmenu(
            self.drawgame, self.screen)

        playercount = 1
        if partner:
            playercount = 2

        if Mode:
            self.deckindex = 1

        self.backgroundimg = background.convert()

        self.Table = Table(playercount=playercount, npccount=1)
        self.cards_and_pic = self.generatecardimages()

        musicobject.stop()
        callback()

    def display_Wildcardchoose(self, commonmemdict, eventobj) -> None:
        """
        # Gibt keine zurück
        # Zeigt einen Ausschreibungsbildschirm für die Wildcard-Karte an
        # A 2 x 2 Farbmuster wird mit den Farben angezeigt, die den Kartenfarben entsprechen
        """

        # Die Kartenfarbe wird durch die Durchschnittsfarbe bestimmt
        # der Karte mit dem Wert von 1 und den entsprechenden Farben
        # Was von Pygame gezogen wird, sind

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
        # Eine Farbe muss ausgewählt werden, um diese Schleife zu verlassen und das Spiel zu beenden
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
        # Methode, um den aktuellen Status des Spiels zu zeichnen
        """

        # Zeichnen Sie die aktuelle Karte in der Mitte des Bildschirms
        # Zeichnen Sie die Spielerkarten in der Unterseite des Bildschirms
        # Bewegen Sie die schwebende Überkarte ein bisschen auf

        # Musik setzen
        musicobject = pygame.mixer.Sound("./Music/Spielsound_Neli.mp3")
        musicobject.set_volume(0.1)
        musicobject.play(-1)

        # Bildschirm einstellen
        self.screen = self.pygame.display.set_mode(
            self.menudimension)

        # Stellen Sie Werte ein, die vor der Schleife initialisiert werden müssen
        width, height = self.screen.get_width(), self.screen.get_height()
        rects = []

        bgimg = pygame.transform.smoothscale(
            self.backgroundimg, (width, height))

        # Der Curr_Player_Index wird direkt in der Gamethread überschrieben, aber dies ist möglicherweise für einige Systeme erforderlich
        commonmemdict = {"rungame": True, "curr_player_index": 0}
        hand = copy.deepcopy(
            self.table.players[commonmemdict["curr_player_index"]].holding)

        # Zieh das Spiel an und starte den Gameloop-Thread

        uno_btn = Button("Neli", (width/2, 0), 32,
                         commonmemdict, bg="# 777777 ", Feedback =" gedrückt ")

        eventobj = threading.Event()
        gamethread = Thread(target=self.table.gameloop,
                            args=(commonmemdict, eventobj))

        gamethread.start()

        self.table.startgame()

        commonmemdict["display_wildcard_screen"] = False

        while commonmemdict["rungame"]:

            self.screen.blit(bgimg, (0, 0))
            events = pygame.event.get()
            pressed_keys = pygame.key.get_pressed()
            mousepos = pygame.mouse.get_pos()

            self.clock.tick(90)

            for event in events:
                if event.type == pygame.QUIT or pressed_keys[pygame.K_ESCAPE]:
                    # müssen das Spiel richtig schließen
                    commonmemdict["index_playedcard"] = 0
                    eventobj.set()
                    commonmemdict["rungame"] = False
                    gamethread.join()
                    sys.exit()
                # Überprüfen Sie die Taste, drücken Sie
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_presses = pygame.mouse.get_pressed()
                    if mouse_presses[0]:
                        checkcardclick(rects, commonmemdict,
                                       eventobj, mousepos)
                uno_btn.click(event)

            # Zerlegen Sie die Funktionen für Spielerkarten
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

            # Zeichne die Karten in die Hand des Spielers und zeichne Rechtecke um sie herum

            for index, rect in enumerate(rects):

                transformed = pygame.transform.smoothscale(
                    self.cards_and_pic[str(hand[index])],
                    (rect.w, rect.h)
                )
                self.screen.blit(transformed, rect)
                pygame.draw.rect(self.screen, "GREEN", rect, 2)

            # Karten in der Mitte des Brettes zeichnen
            # Für ein Seitenverhältnis von 309 bis 436 ist der Faktor 0,708715596 erforderlich

            middlesize_rect = pygame.Rect(
                (int((width/2)-int(0.708715596 * int(height/5))/2),
                 int(height / 2-(height/5))),
                (int(0.708715596 * int(height/5)), int(height/5))
                )

            self.screen.blit(
                pygame.transform.smoothscale(
                    self.cards_and_pic[str(self.table.playedcards[-1])], (middlesize_rect.w, middlesize_rect.h)), middlesize_rect
            )

            # FPS-Zähler
            self.screen.blit(update_fps(self.clock, self.clockfont), (10, 0))

            # Rendern Sie die Spielernummer in der oberen rechten Ecke

            playernum_txt = self.clockfont.render(
                f"Player {str(commonmemdict['curr_player_index'])}", True, self.inverted_bgavgcolor)

            self.screen.blit(
                playernum_txt, (width - playernum_txt.get_width(), 0))

            # Anzeige der UNO-Taste, falls erforderlich
            if commonmemdict['display_uno']:
                uno_btn.show(self.screen)

            self.pygame.display.update()

            # Zeigen Sie den Platzhalterbildschirm für die Auswahl einer Farbe an
            if commonmemdict["display_wildcard_screen"]:
                self.display_Wildcardchoose(commonmemdict, eventobj)

        # Bildschirm
        self.screen.fill((60, 25, 60))
        end_font = pygame.font.SysFont("Arial", 18)
        end_text = end_font.render("Ende", 1, pygame.Color("coral"))
        self.screen.blit(end_text, (width/2, height/2))
        self.pygame.display.update()
        time.sleep(3)


if __name__ == "__main__":
    d = Draw(playercount=1, npccount=1)
    d.drawgame()

