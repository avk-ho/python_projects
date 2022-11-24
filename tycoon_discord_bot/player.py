from assets import *

class Player:
    def __init__(self, name):
        self.name = name
        self.next_player = None
        self.prev_player = None
        self.hand = []
        self.has_finished = False  # necessary because hand not empty != finished
        self.status = "Commoner"  # Starting status, will change to
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


    ### display hand
    def display_hand(self, hidden=True):
        if hidden:
            player_hand = [CARD_TEMPLATE for card in self.hand]
        else:
            player_hand = [display_card(card) for card in self.hand]
            print(f"Hand: {self.hand}")
        print(f"{self.name}({self.score}) : {player_hand} ({len(player_hand)})")
