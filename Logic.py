import random
import time


class Card():
    """docstring for Cards."""

    def __init__(self, val: str, color: str):
        """needs a cards value (0,1,2,3,4,5,6,7,8,9,SKIP,REVERSE,DRAW2,WILDCARD,WILDCARD4) and its color (RED,GREEN,BLUE,YELLOW,BLACK)"""
        super(Card, self).__init__()
        self.color = color
        self.value = val

    def __str__(self):
        return f"{self.color} {self.value}"


class Deck():
    """docstring for Deck."""

    def __init__(self, table, shuffled=True):
        super(Deck, self).__init__()

        self.shuffled = shuffled
        self.undrawncards = self.generatecards()
        self.playedcards = []
        self.table = table

    def generatecards(self):
        """Generates a cardset for a whole deck with 112 Cards in it.
        26 Red, 26 Green, 26 Blue, 26 Yellow
        With 0-9, Skip, Reverse and Draw2 twice per color.
        Wildcard and Wildcard draw 4 each four times
        """
        # generate cards which are not Black
        cards = []
        colors = ["RED", "GREEN", "BLUE", "YELLOW"]
        values = ["0", "1", "2", "3", "4", "5", "6",
                  "7", "8", "9", "SKIP", "DRAW2"]*2
        for colr in colors:
            for val in values:
                cards.append(Card(val=val, color=colr))

        # generate cards which are Black
        for colr in ["BLACK"]:
            for val in ["WILDCARD", "WILDCARD4"]*4:
                cards.append(Card(val=val, color=colr))

        if self.shuffled:
            random.shuffle(cards)

        return cards

    def drawcard(self):
        """Takes the last card from the deck"""

        # generates a new Deck of Cards once a Deck is Empty
        if len(self.undrawncards) <= 0:
            self.undrawncards = self.generatecards()

        drawncard = self.undrawncards.pop(-1)

        return drawncard


class Hand():
    """docstring for Hand."""

    def __init__(self, table, isplayer: bool):
        super(Hand, self).__init__()
        self.holding = []
        self.table = table
        self.deck = self.table.deck
        self.isplayer = isplayer

    def drawcard(self, amount: int = 1):
        """Draws a card from the deck and uses the draw function of the deck.
        draws the amount of cards that is given (default 1)"""
        for _ in range(amount):
            card = self.deck.drawcard()
            self.holding.append(card)

    def playcard(self, card):
        """Plays the given card"""

        self.table.playedcards.append(card)
        self.holding.pop(self.holding.index(card))


class Table():
    """docstring for Table."""

    def __init__(self, playercount: int = 2, npccount: int = 2, shuffled: bool = True):
        super(Table).__init__()
        self.deck = Deck(table=self, shuffled=shuffled)
        self.playedcards = self.deck.playedcards
        self.players = self.createPlayers(playercount, npccount)
        self.indexcurrplayer = 0

    def createPlayers(self, playercount: int, npccount: int):
        """Returns a list of Hand objects
        Creates Hands for the supplied amount of players and nonplayers"""
        hands = []
        for _ in range(playercount):
            hands.append(Hand(self, isplayer=True))
        for _ in range(npccount):
            hands.append(Hand(self, isplayer=False))
        return hands

    def startgame(self):
        """initialize the players cards and the top card to start the game"""
        for player in self.players:
            player.drawcard(amount=7)
        self.playedcards.append(self.deck.drawcard())

    def needdraw(self, player):
        """Check if the current Player can play a card
        Returns False if he can play a card"""

        for card in player.holding:

            # needed to check if the Person can Play a Card
            # checks if the color or value of the card is the same as the current card laying on the table
            # and if the color of the card laying on the table is not BLACK

            if (card.value == self.playedcards[-1].value or card.color == self.playedcards[-1].color) or self.playedcards[-1].color == "BLACK":
                return False
        return True

    def checkvalidityplacedcard(self, playcard):
        """Returns False if it wasn't valid
        Returns True if it was valid"""
        return True

    def blackcardfunctionality(self):
        """returns the color of the next Card"""
        pass

    def cardfunctionality(self, playedcard, commonmemdict):
        """Method checks if the Card Played was a Special Card and what effect it has"""
        # Check for "SKIP", "REVERSE", "DRAW2", "WILDCARD", "WILDCARD4"
        if playedcard.value == "SKIP":
            return
        elif playedcard.value == "REVERSE":
            return
        elif playedcard.value == "DRAW2":
            return
        elif playedcard.value == "WILDCARD":
            return
        elif playedcard.value == "WILDCARD4":
            # copy pure wildcard implementation

            # Draw 4 Cards
            nextplayerindex = self.indexcurrplayer % len(self.players)
            self.players[nextplayerindex].draw(amount=4)
            return

    def pcmove(self, event, commonmemdict):
        """Test if the Player can't do anything besides drawing
        If the player can only draw, then they autodraw
        ---
        If the player can play a card,
        then the Thread waits for the player to pick a card which is indicated by the eventobj flag beeing set to true
        the index of the played card is then shared via the common dictionary that the main and doughter thread share"""
        print(
            len(self.players[self.indexcurrplayer].holding), self.indexcurrplayer)
        if self.needdraw(self.players[self.indexcurrplayer]):
            self.players[self.indexcurrplayer].drawcard(1)
            self.indexcurrplayer += 1
            return 0

        # loop and wait until the main thread sets the event flag to true.
        # then leave the loop, clear the event flag and play the card, which the player chose
        while not event.is_set():
            event.wait(1)

        event.clear()
        playedcard = self.players[self.indexcurrplayer].holding[commonmemdict["index_playedcard"]]

        # check if the selected card is playable:
        # if its not then return the function without doing anything.
        # the loop will execute this function again and wait for a valid card
        if not self.checkvalidityplacedcard(playedcard):
            return
        self.cardfunctionality(playedcard)
        self.players[self.indexcurrplayer].playcard(playedcard)
        self.indexcurrplayer += 1

    def npcmove(self):
        pass

    def gameloop(self, commonmemdict, event):
        self.indexcurrplayer = 0
        commonmemdict["curr_player_index"] = self.indexcurrplayer

        # Gameloop and drawloop will be seperate.
        # They will only share a common dictionary, which is how they will communicate and share data

        while commonmemdict["rungame"] and not event.is_set():

            commonmemdict["curr_player_index"] = self.indexcurrplayer
            time.sleep(0.5)
            player = self.players[self.indexcurrplayer]

            if player.isplayer:
                self.pcmove(event=event, commonmemdict=commonmemdict)
            else:
                self.npcmove(event)

            self.indexcurrplayer = self.indexcurrplayer % len(self.players)


if __name__ == '__main__':
    d = Table(2, 0)
    d.startgame()
    d.gameloop({"rungame": True})
