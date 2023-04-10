from assets import *

class Player:
    def __init__(self, discord_user):
        self.discord_user = discord_user
        self.next_player = None
        self.prev_player = None
        self.hand = []
        self.round_finished = False
        self.status = "Commoner"
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

            elif new_card["value"] == current_card["value"]:
                # second joker
                if new_card["value"] == 20:
                    if new_card["symbol"][len(new_card["symbol"])-1] == "1":
                        self.hand.insert(i, card)
                        card_inserted = True
                
                # sorting by suits H < D < C < S
                else:
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


    # TO DO: DISCORD IMPLEMENTATION
    # display hand
    def display_hand(self, hidden=True):
        if hidden:
            player_hand = [CARD_TEMPLATE for card in self.hand]
        else:
            player_hand = [display_card(card) for card in self.hand]
        # TO DO: TO REPLACE WITH DISCORD MESSAGE
        print(f"{self.discord_user}({self.score}) : {player_hand} ({len(player_hand)})")


    def get_attributes(self):
        for attribute, value in self.__dict__.items():
            print(attribute, '=', value)
