CARD_SUITS = {
    "H": "♥",  # heart
    "D": "♦",  # diamond
    "C": "♣",  # club
    "S": "♠"  # spade
}

CARDS = ["A", "2", "3", "4", "5", "6", "7",
         "8", "9", "10", "J", "Q", "K"]  # length 12

CARD_TEMPLATE = "[ ? ]"

### return a string of a card with a symbol given (string)
def display_card(symbol):
    return CARD_TEMPLATE.replace("?", DECK[symbol]["symbol"])


CLASSMENT_TEMPLATE = """:first_place: PLAYER_FIRST | FIRST_SCORE
:second_place: PLAYER_SECOND | SECOND_SCORE
:third_place: PLAYER_THIRD | THIRD_SCORE
:frowning2: PLAYER_LAST | LAST_SCORE"""

# initializing deck with both Jokers
DECK = {
    "JK1": {
        "value": 20,
        "symbol": ":black_joker:1"
    },
    "JK2": {
        "value": 20,
        "symbol": ":black_joker:2"
    }
}

# filling deck, final length 54
for i in range(len(CARDS)):
    value = i + 1
    for suit in CARD_SUITS:
        if CARDS[i] == "A":
            value = 14
        elif CARDS[i] == "2":
            value = 15

        deck_key = CARDS[i] + suit
        DECK[deck_key] = {
            "value": value,
            "symbol": CARDS[i] + CARD_SUITS[suit]
        }