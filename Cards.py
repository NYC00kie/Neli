import random


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
                  "7", "8", "9", "SKIP", "REVERSE", "DRAW2"]*2
        for colr in colors:
            for val in values:
                cards.append(Card(val=val, color=colr))

        # generate cards which are Black
        for col in ["BLACK"]:
            for val in ["WILDCARD", "WILDCARD4"]*4:
                cards.append(Card(val=val, color=col))

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

    def __init__(self, table):
        super(Hand, self).__init__()
        self.holding = []
        self.table = table
        self.deck = self.table.deck

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

    def __init__(self, Playercount: int = 4):
        super(Table).__init__()
        self.deck = Deck(table=self)
        self.playedcards = self.deck.playedcards
        self.players = self.createPlayers(Playercount)

    def createPlayers(self, count: int):
        """Returns a list of Hand objects
        Creates Hands for the supplied amount of players"""

        hands = []
        for _ in range(count):
            hands.append(Hand(self))
        return hands

    def startgame(self):
        """initialize the players cards and the top card to start the game"""
        for player in self.players:
            player.drawcard(amount=7)
        self.playedcards.append(self.deck.drawcard())


if __name__ == '__main__':
    d = Table()
    print(len(d.deck.undrawncards))
    d.startgame()
    print(len(d.deck.undrawncards))
    print(dir(d))
    print(d.players)
    for player in d.players:
        print([str(x) for x in player.holding])
        print(len(player.holding))
