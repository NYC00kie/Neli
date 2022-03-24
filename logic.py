"""
# Docstring für Logik.
"""
import random
import time


class Card():
    """
    # Docstring für Karten.
    """

    def __init__(self, val: str, color: str):
        """
        # Benötigt einen Kartenwert (0,1,2,3,4,5,6,7,8,9, überspringen, Draw2, Wildcard, Wildcard4) und seine Farbe (rot, grün, blau, gelb, schwarz)
        """
        self.color = color
        self.value = val

    def __str__(self):
        return f"{self.color} {self.value}"

    def __eq__(self, other) -> bool:
        return self.color == other.color and self.value == other.value


class Deck():
    """
    # Docstring für Deck.
    """

    def __init__(self, table, shuffled=True):

        self.shuffled = shuffled
        self.undrawncards = self.generatecards()
        self.playedcards = []
        self.table = table

    def generatecards(self):
        """
        # Erzeugt ein Kartenset für ein ganzes Deck mit 112 Karten darin.
        # 26 rot, 26 grün, 26 blau, 26 gelb
        # Mit 0-9, überspringen, rückwärts und draw2 zweimal pro Farbe.
        # Platzhalter- und Wildcard zeichnen 4 jeweils viermal
        """
        # Karten generieren, die nicht schwarz sind
        cards = []
        colors = ["RED", "GREEN", "BLUE", "YELLOW"]
        values = ["0", "1", "2", "3", "4", "5", "6",
                  "7", "8", "9", "SKIP", "DRAW2"] * 2
        for colr in colors:
            for val in values:
                cards.append(Card(val=val, color=colr))

        # Karten generieren, die schwarz sind
        for colr in ["BLACK"]:
            for val in ["WILDCARD", "WILDCARD4"] * 4:
                cards.append(Card(val=val, color=colr))

        if self.shuffled:
            random.shuffle(cards)

        return cards

    def drawcard(self):
        """
        # Nimmt die letzte Karte aus dem Deck
        """

        # erzeugt ein neues Kartenspiele, sobald ein Deck leer ist
        if len(self.undrawncards) <= 0:
            self.undrawncards = self.generatecards()

        drawncard = self.undrawncards.pop(-1)

        return drawncard


class Hand():
    """
    # Docstring für Hand.
    """

    def __init__(self, table, isplayer: bool):
        self.holding = []
        self.table = table
        self.deck = self.table.deck
        self.isplayer = isplayer
        self.saiduno = True

    def drawcard(self, amount: int = 1):
        """
        # Zeichnet eine Karte aus dem Deck und verwendet die Zeichnungsfunktion des Decks.
        # Zeichnet die Menge der angegebenen Karten (Standard 1)
        """
        self.saiduno = False
        self.table.commonmemdict["pressed_uno"] = False
        for _ in range(amount):
            card = self.deck.drawcard()
            self.holding.append(card)

    def playcard(self, card):
        """
        # Spielt die angegebene Karte
        """
        self.saiduno = self.table.commonmemdict["pressed_uno"]
        self.table.playedcards.append(card)
        self.holding.pop(self.holding.index(card))


class Table():
    """
    # Docstring für Tabelle.
    """

    def __init__(self, playercount: int = 2, npccount: int = 2, shuffled: bool = True):
        self.deck = Deck(table=self, shuffled=shuffled)
        self.playedcards = self.deck.playedcards
        self.players = self.createplayers(playercount, npccount)
        self.indexcurrplayer = 0

    def createplayers(self, playercount: int, npccount: int) -> list:
        """
        # Gibt eine Liste von Handobjekten zurück
        # Erzeugt Hände für den mitgelieferten Betrag der Spieler und Nichtspieler
        """
        hands = []
        for _ in range(playercount):
            hands.append(Hand(self, isplayer=True))
        for _ in range(npccount):
            hands.append(Hand(self, isplayer=False))
        return hands

    def startgame(self) -> None:
        """
        # Initialisieren Sie die Spielerkarten und die oberste Karte, um das Spiel zu starten
        """
        for player in self.players:
            player.drawcard(amount=7)

        # Zeichnen, bis die Karte nicht schwarz ist
        topcard = self.deck.drawcard()
        while topcard.color == "BLACK":
            topcard = self.deck.drawcard()
        self.playedcards.append(topcard)

    def needdraw(self, player) -> bool:
        """
        # Prüfen Sie, ob der aktuelle Spieler eine Karte abspielen kann
        # Gibt false zurück, wenn er eine Karte spielen kann
        """
        total_playable_cards = 0

        for card in player.holding:

            if self.checkvalidityplacedcard(card):
                total_playable_cards += 1

        return total_playable_cards == 0

    def checkvalidityplacedcard(self, playedcard) -> bool:
        """
        # Gibt false zurück, wenn es kein gültiger Schritt wäre
        # Gibt true zurück, wenn es gültig gilt
        """
        latestcard = self.playedcards[-1]

        # Prüfen Sie, ob Farben oder Werte übereinstimmen oder wenn die gespielte Karte schwarz ist und die neueste gespielte Karte nicht von einem Platzhalter ist
        if playedcard.value == latestcard.value or playedcard.color == latestcard.color or (playedcard.color == "BLACK" and latestcard.value != "EMPTY"):
            return True

        return False

    def blackcardfunctionality(self, commonmemdict, event, chosen_color) -> None:
        """
        # Gibt keine zurück
        # Ersetzt die Wildcard mit einer leeren Karte der gewählten Farbe
        """
        # Eine Farbe kann der Funktion geliefert werden
        # Dies erfolgt nur von NPCs
        if chosen_color == "":
            commonmemdict["display_wildcard_screen"] = True
            # warte auf Eingabe des Benutzers
            while not event.is_set():
                event.wait(1)

            event.clear()

            chosen_color = commonmemdict["chosen_color"]

        self.playedcards[-1] = Card("EMPTY", chosen_color)

    def cardfunctionality(self, playedcard, commonmemdict, event, chosencolor) -> None:
        """
        # Methode prüft, ob die gespielte Karte eine spezielle Karte war und welche Auswirkungen er hat
        """
        # Prüfen Sie auf "Skip", "umgekehrt", "draw2", "wildcard", "wildcard4"
        if playedcard.value == "SKIP":
            # Zum nächsten Spieler springen
            # Dies funktioniert, weil wieder in der MainLoop der Index des aktuellen Spielers erneut von einem inkrementiert wird
            self.indexcurrplayer = (self.indexcurrplayer+1) % len(self.players)

        elif playedcard.value == "DRAW2":
            # Macht den nächsten Spieler 2 Karten, indem Sie die Zeichnungsfunktion auf sie aufrufen
            nextplayerindex = (self.indexcurrplayer+1) % len(self.players)
            self.players[nextplayerindex].drawcard(amount=2)

        elif playedcard.value == "WILDCARD":
            # Rufen Sie die Blackcardfunctionalitätsfunktion an
            self.blackcardfunctionality(
                commonmemdict=commonmemdict, event=event, chosen_color=chosencolor)

        elif playedcard.value == "WILDCARD4":
            # Pure Wildcard-Implementierung kopieren
            self.blackcardfunctionality(
                commonmemdict, event, chosen_color=chosencolor)

            # Macht den nächsten Spieler 4 Karten, indem Sie die Zeichnungsfunktion anrufen
            nextplayerindex = (self.indexcurrplayer+1) % len(self.players)
            self.players[nextplayerindex].drawcard(amount=4)

    def pcmove(self, event, commonmemdict) -> None:
        """
        # Testen Sie, wenn der Spieler nicht neben der Zeichnung nichts tun kann
        # Wenn der Spieler nur zeichnen kann, dann autodraw
        ---
        # Wenn der Spieler eine Karte spielen kann,
        # Dann wartet der Thread auf den Player, um eine Karte auszuwählen, die von der EVENTOBJ-Fahnenbeeide angezeigt wird, die auf TRUE eingestellt ist
        # Der Index der abgespielten Karte wird dann über das allgemeine Wörterbuch geteilt, das der Haupt- und Temperfaden-Anteil
        """
        print(
            len(self.players[self.indexcurrplayer].holding), self.indexcurrplayer)
        if self.needdraw(self.players[self.indexcurrplayer]):
            self.players[self.indexcurrplayer].drawcard(1)
            return

        # Schleife und warten, bis der Hauptthread das Ereignis-Flag auf true setzt.
        # Dann verlassen Sie die Schleife, löschen Sie das Ereignis-Flag und spiele die Karte, die der Spieler entschieden hat
        while not event.is_set():
            event.wait(1)

        event.clear()
        playedcard = self.players[self.indexcurrplayer].holding[commonmemdict["index_playedcard"]]

        # Prüfen Sie, ob die ausgewählte Karte spielbar ist:
        # Wenn es nicht dann die Funktion zurückgibt, ohne etwas zu tun.
        # Die Schleife führt diese Funktion wieder aus, und warten Sie auf eine gültige Karte
        if not self.checkvalidityplacedcard(playedcard):
            self.indexcurrplayer = (self.indexcurrplayer-1) % len(self.players)
            return

        self.players[self.indexcurrplayer].playcard(playedcard)
        self.cardfunctionality(playedcard, commonmemdict, event, "")

    def calc_chosen_color(self):
        """
        # Berechnet die Farbe die Auswahl für den n
        """

        colors = ["RED", "GREEN", "BLUE", "YELLOW"]
        picked_color = colors[random.randint(0, 3)]
        return picked_color

    def npcmove(self, commonmemdict) -> None:
        """
        # Tests, wenn der NPC eine Karte zeichnen muss.
        # Dann prüft es alle gültigen Karten, die sie spielen können, und wählen Sie einen zufälligen und spielt sie
        """
        print(
            len(self.players[self.indexcurrplayer].holding), self.indexcurrplayer)
        if self.needdraw(self.players[self.indexcurrplayer]):
            self.players[self.indexcurrplayer].drawcard(1)

            return

        validcards = []
        for card in self.players[self.indexcurrplayer].holding:
            if self.checkvalidityplacedcard(card):
                validcards.append(card)

        chosencolor = self.calc_chosen_color()

        chosencard = random.choice(validcards)

        self.players[self.indexcurrplayer].playcard(chosencard)
        self.cardfunctionality(chosencard, commonmemdict,
                               None, chosencolor=chosencolor)

    def checkwin(self, commonmemdict) -> bool:
        """
        # prüft, ob der aktuelle Spieler das Spiel gewonnen hat
        # Gibt true zurück, wenn der aktuelle Spieler keine Karten hat und UNO gesagt hat
        # Gibt false zurück, wenn der aktuelle Spieler mehr als 0 Karten hat
        """
        commonmemdict["display_uno"] = False
        if len(self.players[self.indexcurrplayer].holding) > 0:

            return False
        else:
            # habe nicht uno gesagt
            if not self.players[self.indexcurrplayer].saiduno:
                self.players[self.indexcurrplayer].drawcard(2)
                commonmemdict["display_uno"] = False
                return False
            # sagte Uno.
            else:
                return True

    def gameloop(self, commonmemdict, event) -> None:
        """
        # Funktion für den wichtigsten Gameloop
        # Es wird vom Hauptfaden aufgerufen
        """
        self.indexcurrplayer = 0
        self.commonmemdict = commonmemdict
        commonmemdict["curr_player_index"] = self.indexcurrplayer
        self.players[self.indexcurrplayer].holding = sorted(
            self.players[self.indexcurrplayer].holding, key=lambda card: card.color)
        # Gameloop und Drawoop werden getrennt sein.
        # Sie teilen nur ein allgemeines Wörterbuch, mit dem sie Daten kommunizieren und teilen

        while commonmemdict["rungame"] and not event.is_set():
            commonmemdict["curr_player_index"] = self.indexcurrplayer

            player = self.players[self.indexcurrplayer]

            player.holding = sorted(
                player.holding, key=lambda card: card.color, reverse=True)

            if len(player.holding) < 2:
                commonmemdict["display_uno"] = True

            if player.isplayer:
                self.pcmove(event=event, commonmemdict=commonmemdict)
                time.sleep(0.5)
            else:
                self.npcmove(commonmemdict=commonmemdict)

            if self.checkwin(commonmemdict):
                commonmemdict["rungame"] = False
                break

            self.indexcurrplayer += 1

            self.indexcurrplayer = self.indexcurrplayer % len(self.players)

