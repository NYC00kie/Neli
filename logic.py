"""
# docstring for logic.
"""
import random
import time


class Card():
    """
    # docstring for Cards.
    """

    def __init__(self, val: str, color: str):
        """
        # needs a cards value (0,1,2,3,4,5,6,7,8,9,SKIP,DRAW2,WILDCARD,WILDCARD4) and its color (RED,GREEN,BLUE,YELLOW,BLACK)
        """
        self.color = color
        self.value = val

    def __str__(self):
        return f"{self.color} {self.value}"

    def __eq__(self, other) -> bool:
        return self.color == other.color and self.value == other.value


class Deck():
    """
    # docstring for Deck.
    """

    def __init__(self, table, shuffled=True):

        self.shuffled = shuffled
        self.undrawncards = self.generatecards()
        self.playedcards = []
        self.table = table

    def generatecards(self):
        """
        # Generates a cardset for a whole deck with 112 Cards in it.
        # 26 Red, 26 Green, 26 Blue, 26 Yellow
        # With 0-9, Skip, Reverse and Draw2 twice per color.
        # Wildcard and Wildcard draw 4 each four times
        """
        # generate cards which are not Black
        cards = []
        colors = ["RED", "GREEN", "BLUE", "YELLOW"]
        values = ["0", "1", "2", "3", "4", "5", "6",
                  "7", "8", "9", "SKIP", "DRAW2"] * 2
        for colr in colors:
            for val in values:
                cards.append(Card(val=val, color=colr))

        # generate cards which are Black
        for colr in ["BLACK"]:
            for val in ["WILDCARD", "WILDCARD4"] * 4:
                cards.append(Card(val=val, color=colr))

        if self.shuffled:
            random.shuffle(cards)

        return cards

    def drawcard(self):
        """
        #Takes the last card from the deck
        """

        # generates a new Deck of Cards once a Deck is Empty
        if len(self.undrawncards) <= 0:
            self.undrawncards = self.generatecards()

        drawncard = self.undrawncards.pop(-1)

        return drawncard


class Hand():
    """
    #docstring for Hand.
    """

    def __init__(self, table, isplayer: bool):
        self.holding = []
        self.table = table
        self.deck = self.table.deck
        self.isplayer = isplayer
        self.saiduno = True

    def drawcard(self, amount: int = 1):
        """
        #Draws a card from the deck and uses the draw function of the deck.
        #draws the amount of cards that is given (default 1)
        """

        for _ in range(amount):
            card = self.deck.drawcard()
            self.holding.append(card)

    def playcard(self, card):
        """
        #Plays the given card
        """

        self.table.playedcards.append(card)
        self.holding.pop(self.holding.index(card))


class Table():
    """
    #docstring for Table.
    """

    def __init__(self, playercount: int = 2, npccount: int = 2, shuffled: bool = True):
        self.deck = Deck(table=self, shuffled=shuffled)
        self.playedcards = self.deck.playedcards
        self.players = self.createplayers(playercount, npccount)
        self.indexcurrplayer = 0

    def createplayers(self, playercount: int, npccount: int) -> list:
        """
        #Returns a list of Hand objects
        #Creates Hands for the supplied amount of players and nonplayers
        """
        hands = []
        for _ in range(playercount):
            hands.append(Hand(self, isplayer=True))
        for _ in range(npccount):
            hands.append(Hand(self, isplayer=False))
        return hands

    def startgame(self) -> None:
        """
        #initialize the players cards and the top card to start the game
        """
        for player in self.players:
            player.drawcard(amount=7)

        # draw until the card is not black
        topcard = Card("WILDCARD", "BLACK")
        topcard = self.deck.drawcard()
        while topcard.color == "BLACK":
            print(topcard)
            topcard = self.deck.drawcard()
        self.playedcards.append(topcard)

    def needdraw(self, player) -> bool:
        """
        #Check if the current Player can play a card
        #Returns False if he can play a card
        """
        total_playable_cards = 0

        for card in player.holding:

            # needed to check if the Person can Play a Card
            # checks if the color or value of the card is the same as the current card laying on the table
            # and if the color of the card laying on the table is not BLACK

            black = (self.playedcards[-1].color
                     == "BLACK" or card.color == "BLACK") and total_playable_cards > 0

            same_partial_card = (
                card.value == self.playedcards[-1].value or card.color == self.playedcards[-1].color)

            if same_partial_card or black:
                total_playable_cards += 1

        if total_playable_cards == 0:
            return True
        else:
            return False

    def checkvalidityplacedcard(self, playedcard) -> bool:
        """
        #Returns False if it wasn't valid
        #Returns True if it was valid
        """
        latestcard = self.playedcards[-1]
        if playedcard.value == latestcard.value or playedcard.color == latestcard.color or (playedcard.color == "BLACK" and latestcard.value != "EMPTY"):
            return True
        else:
            return False

    def blackcardfunctionality(self, commonmemdict, event, chosen_color) -> None:
        """
        #returns None
        """
        if chosen_color == "":
            commonmemdict["display_wildcard_screen"] = True
            while not event.is_set():
                event.wait(1)

            event.clear()

            chosen_color = commonmemdict["chosen_color"]

        self.playedcards[-1] = Card("EMPTY", chosen_color)
        print(self.playedcards[-1])

    def cardfunctionality(self, playedcard, commonmemdict, event, chosencolor) -> None:
        """
        #Method checks if the Card Played was a Special Card and what effect it has
        """
        # Check for "SKIP", "REVERSE", "DRAW2", "WILDCARD", "WILDCARD4"
        if playedcard.value == "SKIP":
            self.indexcurrplayer = (self.indexcurrplayer+1) % len(self.players)
            return
        elif playedcard.value == "DRAW2":
            nextplayerindex = (self.indexcurrplayer+1) % len(self.players)
            self.players[nextplayerindex].drawcard(amount=2)
            return
        elif playedcard.value == "WILDCARD":
            self.blackcardfunctionality(
                commonmemdict=commonmemdict, event=event, chosen_color=chosencolor)

            return
        elif playedcard.value == "WILDCARD4":
            # copy pure wildcard implementation
            self.blackcardfunctionality(
                commonmemdict, event, chosen_color=chosencolor)
            # Draw 4 Cards
            print(self.indexcurrplayer, self.indexcurrplayer
                  + 1, (self.indexcurrplayer+1) % len(self.players))
            nextplayerindex = (self.indexcurrplayer+1) % len(self.players)
            self.players[nextplayerindex].drawcard(amount=4)
            return

    def pcmove(self, event, commonmemdict) -> None:
        """
        #Test if the Player can't do anything besides drawing
        #If the player can only draw, then they autodraw
        ---
        #If the player can play a card,
        #then the Thread waits for the player to pick a card which is indicated by the eventobj flag beeing set to true
        #the index of the played card is then shared via the common dictionary that the main and doughter thread share
        """
        print(
            len(self.players[self.indexcurrplayer].holding), self.indexcurrplayer)
        if self.needdraw(self.players[self.indexcurrplayer]):
            self.players[self.indexcurrplayer].drawcard(1)
            return

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
            self.indexcurrplayer = (self.indexcurrplayer-1) % len(self.players)
            return

        self.players[self.indexcurrplayer].playcard(playedcard)
        self.cardfunctionality(playedcard, commonmemdict, event, "")

    def calc_chosen_color(self):
        playerscards = self.players[self.indexcurrplayer].holding
        colors = ["RED", "GREEN", "BLUE", "YELLOW"]
        picked_color = colors[random.randint(0, 3)]
        return picked_color

    def npcmove(self, commonmemdict) -> None:
        """
        #tests if the npc needs to draw a card.
        #then it checks all valid cards it can play and chooses one at random and plays it
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
        print(chosencolor)
        chosencard = random.choice(validcards)

        self.players[self.indexcurrplayer].playcard(chosencard)
        self.cardfunctionality(chosencard, commonmemdict,
                               None, chosencolor=chosencolor)

    def checkwin(self) -> bool:
        """
        #checks wether the current player has won the game
        #returns True if the current Player has no cards and said uno
        #returns False if the current Player has more then 0 cards
        """
        if len(self.players[self.indexcurrplayer].holding) > 0:

            return False
        else:
            # didn't say Uno
            if not self.players[self.indexcurrplayer].saiduno:
                self.players[self.indexcurrplayer].drawcard(2)
                return False
            # said Uno
            else:
                return True

    def gameloop(self, commonmemdict, event) -> None:
        """
        #Function for the main gameloop
        #It gets called by the main thread
        """
        self.indexcurrplayer = 0
        commonmemdict["curr_player_index"] = self.indexcurrplayer
        self.players[self.indexcurrplayer].holding = sorted(
            self.players[self.indexcurrplayer].holding, key=lambda card: card.color)
        # Gameloop and Drawloop will be seperate.
        # They will only share a common dictionary, which is how they will communicate and share data

        while commonmemdict["rungame"] and not event.is_set():
            commonmemdict["curr_player_index"] = self.indexcurrplayer

            player = self.players[self.indexcurrplayer]

            player.holding = sorted(
                player.holding, key=lambda card: card.color, reverse=True)

            print([card.color for card in player.holding])

            if player.isplayer:
                self.pcmove(event=event, commonmemdict=commonmemdict)
                time.sleep(0.5)
            else:
                self.npcmove(commonmemdict=commonmemdict)

            if self.checkwin():
                commonmemdict["rungame"] = False
                break

            self.indexcurrplayer += 1

            self.indexcurrplayer = self.indexcurrplayer % len(self.players)

            print(str(self.playedcards[-1]))
