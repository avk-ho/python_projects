import random
from assets import *

# Test
# x = 0
# for card in DECK:
#     x += 1
#     print(f"{card} : {DECK[card]['value']} / {DECK[card]['symbol']}")
# print(x)

class Gamelogic:
    def __init__(self):
        self.revolution = False
        self.players = []
        self.current_turn_player = None
        self.current_card_stack = []
        self.last_play = [] # [play_value, nb_cards, [cards_played], last_play_player]
        self.card_template = CARD_TEMPLATE
        self.classment_template = CLASSMENT_TEMPLATE

    
    def start_game(self):
        # not yet enough players
        if len(self.players) < 4:
            return
        
        # distributing cards
        for card in DECK:
            card_distributed = False

            while not card_distributed:
                # pick a random player
                player = random.choice(self.players)
                
                # checking if player hand is full
                if len(player.hand) < 14:
                    player.add_card_to_hand(card)
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


    # manage a full turn
    def turn_gameplay(self):
        end_turn = False
        
        while not end_turn:
            # directed to self.current_turn_player
            current_play = self.play_cards()

            # passed
            if current_play[0] is None:
                pass
                ### TO DO


    # ask for a player input, check if valid 
    # then return a new valid play [play_value, nb_cards, [cards_played]]
    def play_cards(self):
        valid_play = False

        while not valid_play:
            play_input = input(
                "Please input the card(s) you want to play (example: 4S 4C JK1): \n")
            play_input = play_input.upper()
            input_cards = play_input.split()


            ## checking if the cards selected are valid
            # pass
            if len(input_cards) == 1 and input_cards[0] == "PASS":
                valid_play = True
                play_value = None
                continue

            # more than 4 cards played
            if len(input_cards) > 4:
                print("Too many card played. Only up to 4 cards can be played at once.")
                continue

            # incorrect number of cards played
            if len(input_cards) != self.last_play[1]:
                print(
                    f"Incorrect number of cards played. {len(input_cards)} instead of {self.last_play[1]}.")
                continue


            own_cards = True # cards played are in hand
            valid_values = True # cards are all of 1 set (or jokers)
            has_joker = False # cards played contains at least 1 joker
            play_value = 0

            for card in input_cards:
                # card not in hand
                if card not in self.current_turn_player.hand:
                    own_cards = False
                    print(f"Invalid input: {card}")
                    break

                if card == "JK1" or card == "JK2":
                    has_joker = True
                    continue
                
                # all cards have the same value (ignoring Jokers)
                if play_value == 0:
                    play_value = DECK[card]["value"]
                elif play_value != DECK[card]["value"]:
                    print(f"Incompatible cards played. {play_value} card with a {DECK[card]['value']} card.")
                    valid_values = False
                    break
                
            if not own_cards or not valid_values:
                continue

            # cards are only jokers
            if has_joker and play_value == 0 and not self.revolution:
                play_value = 20

            # comparing with last play's value
            if self.revolution:
                valid_play = play_value < self.last_play[0]
            else:
                valid_play = play_value > self.last_play[0]

            # joker 3S counter
            if self.last_play[1] == 1 \
            and (self.last_play[0] == 0 or self.last_play[0] == 20) \
            and input_cards[0] == "3S":
                valid_play = True

            ### TO DO: ADD CARD DISPLAY
            # cards too "weak"
            if not valid_play:
                print(
                    f"Invalid card value played. Last card(s) played: {self.last_play[2]}")
        
        play = Play(
            player=self.current_turn_player,
            value=play_value,
            nb_cards=len(input_cards),
            cards_played=[card for card in input_cards]
        )

        # removing the cards played from the player's hand
        if play.value is not None:
            while len(input_cards) > 0:
                card = input_cards.pop()
                self.current_turn_player.hand.remove(card)

        
        play.get_attributes()
        return play


    # add a player to the list of players
    def register_player(self, player):
        self.players.append(player)

        self.start_game()


# Used in Gamelogic
class Play():
    def __init__(self, player, value, nb_cards, cards_played):
        self.player = player
        self.value = value
        self.nb = nb_cards
        self.cards = cards_played

    def get_attributes(self):
        for attribute, value in self.__dict__.items():
            print(attribute, '=', value)


class Player:
    def __init__(self, name):
        self.name = name
        self.next_player = None
        self.prev_player = None
        self.hand = []
        self.status = "Commoner" # Starting status, will change to 
        #"Tycoon" > "Rich" > "Poor" > "Beggar"
        self.score = 0


    # add a card (key of DECK) to own hand in a sorted fashion
    def add_card_to_hand(self, card):
        # empty hand
        if len(self.hand) == 0:
            self.hand.append(card)
            return
        
        card_inserted = False
        for i in range(len(self.hand)):
            current_card = DECK[self.hand[i]]
            new_card = DECK[card]

            if new_card["value"] < current_card["value"]:
                self.hand.insert(i, card)
                card_inserted = True

            # sorting by suits H < D < C < S 
            elif new_card["value"] == current_card["value"]:
                new_card_suit = list(DECK[card]["symbol"]).pop()
                current_card_suit = list(DECK[self.hand[i]]["symbol"]).pop()

                if new_card_suit == CARD_SUITS["H"] or \
                current_card_suit == CARD_SUITS["S"] or \
                new_card_suit == CARD_SUITS["D"] and current_card_suit == CARD_SUITS["C"]:
                    self.hand.insert(i, card)
                    card_inserted = True

            if card_inserted:
                break

        if not card_inserted:
            self.hand.append(card)
