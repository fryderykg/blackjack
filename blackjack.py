# Mini-project #6 - Blackjack
try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")

# initialize global variables
in_play = False
outcome = ""
win = ""
score = 0
player_hand = []
dealer_hand = []
deck = []

# globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 10, 'Q': 10, 'K': 10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print("Invalid card: ", suit, rank)

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank),
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)


# define hand class
class Hand:
    def __init__(self):     # create Hand object
        self.hand_list = []

    def __str__(self):    # return a string representation of a hand
        str_hand = ""
        for i in range(len(self.hand_list)):
            str_hand += str(self.hand_list[i]) + " "
        return "Hand contains: " + str_hand

    def add_card(self, card):    # add a card object to a hand
        self.hand_list.append(card)

    def get_value(self):    # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        value, ace = 0, False
        for card in self.hand_list:
            value += VALUES[card.get_rank()]
            if RANKS[0] == card.get_rank():
                ace = True
        if ace and value + 10 <= 21:
            return value + 10
        else:
            return value

    def draw(self, canvas, pos):    # draw a hand on the canvas, use the draw method for cards
        pass


# define deck class
class Deck:
    def __init__(self):                 # create a Deck object
        self.deck = []
        for i in SUITS:
            for j in RANKS:
                self.deck.append(Card(i, j))

    def shuffle(self):                  # shuffle the deck
        random.shuffle(self.deck)       # use random.shuffle()

    def deal_card(self):
        return self.deck.pop()  	    # deal a card object from the deck

    def __str__(self):                  # return a string representing the deck
        str_deck = ""
        for i in range(len(self.deck)):
            str_deck += str(self.deck[i]) + " "
        return "Deck contains: " + str_deck


# event handlers for buttons
def deal():
    global outcome, in_play, player_hand, dealer_hand, deck, win
    outcome = "Hit or Stand?"
    win = ""
    deck = Deck()
    deck.shuffle()
    player_hand = Hand()
    dealer_hand = Hand()

    for i in range(2):
        player_hand.add_card(deck.deal_card())
        dealer_hand.add_card(deck.deal_card())

    in_play = True


def hit():
    global player_hand, deck, in_play, outcome, score, win
    if player_hand.get_value() <= 21 and in_play:
        player_hand.add_card(deck.deal_card())
        if player_hand.get_value() > 21:
            in_play = False
            outcome = "New deal?"
            win = "You busted!"
            score -= 1

    # if the hand is in play, hit the player
    # if busted, assign a message to outcome, update in_play and score


def stand():
    global in_play, dealer_hand, player_hand, deck, outcome, score, win

    if in_play:
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(deck.deal_card())

        if 21 >= dealer_hand.get_value() >= player_hand.get_value():
            win = "You lose!"
            outcome = "New deal?"
            score -= 1
        else:
            win = "You win!"
            outcome = "New deal?"
            score += 1

    in_play = False
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    # assign a message to outcome, update in_play and score


# draw handler
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    a, b = 80, 80
    for card in player_hand.hand_list:
        card.draw(canvas, [a, 400])
        a += 80
    for card in dealer_hand.hand_list:
        card.draw(canvas, [b, 180])
        b += 80
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [116, 228], CARD_BACK_SIZE)

    canvas.draw_text("Dealer", (80, 150), 35, "Black", "serif")
    canvas.draw_text("Player", (80, 370), 35, "Black", "serif")
    canvas.draw_text(outcome, (220, 370), 35, "Black", "serif")
    canvas.draw_text(win, (220, 130), 35, "Red", "serif")
    canvas.draw_text("Score: " + str(score), (400, 150), 35, "Black", "serif")
    canvas.draw_text(str(player_hand.get_value()), (450, 370), 35, "Black", "serif")
    canvas.draw_text("B  l  a  c  k  J  a  c  k", (100, 50), 45, "DarkBlue", "serif")


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

# create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()
