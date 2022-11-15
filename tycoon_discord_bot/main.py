import random
from assets import *

# initializing deck with both Jokers
deck = {
    "JK1": {
        "value": 0,
        "symbol": "JK"
    },
    "JK2": {
        "value": 0,
        "symbol": "JK"
    }
}

# filling deck
for i in range(len(CARDS)):
    value = i + 1
    for symbol in CARD_SYMBOLS:
        if CARDS[i] == "A":
            value = 14
        elif CARDS[i] == "2":
            value = 15
        
        deck_key = CARDS[i] + symbol
        deck[deck_key] = {
            "value": value,
            "symbol": CARDS[i] + CARD_SYMBOLS[symbol]
        }

# Test
# x = 0
# for card in deck:
#     x += 1
#     print(f"{card} : {deck[card]['value']} / {deck[card]['symbol']}")
# print(x)

class Gamelogic:
    def __init__(self, deck):
        self.revolution = False
        self.players = []
        self.current_turn_player = None
        self.current_card_stack = []
        self.deck = deck
        self.card_template = CARD_TEMPLATE
        self.classment_template = CLASSMENT_TEMPLATE

    
    def start_game(self):
        # not yet enough players
        if len(self.players) < 4:
            return
        
        # distributing cards
        for card in self.deck:
            card_distributed = False

            while not card_distributed:
                # pick a random player
                player = random.choice(self.players)
                
                # checking if player hand is full
                if len(player.hand) < 14:
                    player.hand.append(card)
                    card_distributed = True

        # setting turns
        first_player = random.choice(self.players)
        players_list = [player for player in self.players if player != first_player]
        self.current_turn_player = first_player
        
        current_player = first_player
        next_player = None
        while current_player.next_player is None and len(players_list) > 0:
            next_player = random.choice(players_list)
            players_list.remove(next_player)
            current_player.next_player, next_player.prev_player = next_player, current_player

            current_player = next_player

        current_player.next_player, self.current_turn_player.prev_player = self.current_turn_player, current_player
        # test
        # i = 0
        # while i < 4:
        #     i += 1
        #     print(self.current_turn_player.name)
        #     self.current_turn_player = self.current_turn_player.next_player


    # display hands of players (cards hidden) MAY BE USELESS
    def display_players_hands(self):
        for player in self.players:
            player_hand = [CARD_TEMPLATE for card in player.hand]
            print(f"{player.name}({player.score}) : {player_hand} ({len(player_hand)})")

    # manage a full turn TBC
    def turn_gameplay(self):
        end_turn = False
        
        while not end_turn:
            pass

    # TBC
    def play_cards(self):
        pass

    # add a player to the list of players
    def register_player(self, player):
        self.players.append(player)

        self.start_game()



class Player:
    def __init__(self, name):
        self.name = name
        self.next_player = None
        self.prev_player = None
        self.hand = []
        self.status = "Commoner" # Starting status, will change to 
        #"Tycoon" > "Rich" > "Poor" > "Beggar"
        self.score = 0