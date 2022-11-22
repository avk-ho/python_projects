import random
from assets import *

# Game is 3 Rounds
# Each Round, players take Turns
# Each Turn, players make Plays (including passing)

class Gamelogic:
    def __init__(self):
        self.revolution = False
        self.players = []
        self.current_turn_player = None
        self.current_card_stack = []
        self.card_template = CARD_TEMPLATE
        self.last_players_status = {
            # players' status at the end of the previous round
            "Tycoon": None,
            "Rich": None,
            "Poor": None,
            "Beggar": None
        }
        self.classment = CLASSMENT_TEMPLATE
        self.all_rounds = []
        self.round = 1

    ### add a player to the list of players, then start a game if there are 4 players
    def register_player(self, player):
        # TO DO: manage registration through discord command
        if len(self.players) < 4:
            self.players.append(player)

        self.start_game()
    

    ### if there are 4 players, determines players' turns then start a round
    def start_game(self):
        # not yet enough players
        if len(self.players) < 4:
            return
        
        # setting turns, only at the start
        if self.round == 1:
            first_player = random.choice(self.players)
            players_list = [player for player in self.players
                            if player != first_player]
            self.current_turn_player = first_player

            current_player = first_player
            next_player = None
            while current_player.next_player is None and len(players_list) > 0:
                next_player = random.choice(players_list)
                players_list.remove(next_player)
                current_player.next_player, next_player.prev_player = next_player, current_player

                current_player = next_player

            current_player.next_player, self.current_turn_player.prev_player = self.current_turn_player, current_player

        # start rounds, stop after round 3
        while self.round < 4:
            self.start_round()


    ### start a round, end when 3 players finish
    def start_round(self):
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

        # card trading for round 2 & 3
        if self.round > 1:
            self.current_turn_player = self.last_players_status["Beggar"]
            self.redistribute_cards()

        # round start
        round = Round(player=self.current_turn_player, num=self.round)

        end_round = False
        while not end_round:
            turn = self.start_turn(round)
            round.turns.append(turn)

            # check if 3 players have finished
            remaining_players = 0
            last_status = ""
            for status in round.players_status:
                if round.players_status[status] is None:
                    remaining_players += 1
                    last_status = status

            if remaining_players == 1:
                end_round = True
        
        # round ending, attributing last remaining status
        round.players_status[last_status] = self.current_turn_player

        self.last_players_status = round.players_status
        self.all_rounds.append(round)
        self.round += 1

        # distributing score (desc order)
        # and resetting state of players (hand and has_finished)
        score = 30
        for status in self.last_players_status:
            player = self.last_players_status[status]
            player.hand = []
            player.has_finished = False
            player.score += score

            score -= 10

        # display ranking
        self.display_classment()


    # TO DO: Discord implementation
    ### manage a full turn
    def start_turn(self, round):
        turn = Turn(player=self.current_turn_player)

        end_turn = False
        while not end_turn:
            # all players passed
            if turn.last_play.player is not None \
            and turn.last_play.player == self.current_turn_player:
                end_turn = True
                continue

            # TO DO:
            # direct to self.current_turn_player through discord
            current_play = self.play_cards(turn=turn)

            # passed
            if current_play.value is None:
                self.current_turn_player = self.current_turn_player.next_player
                continue

            # revolution / counter revolution
            if current_play.nb == 4:
                self.revolution = not self.revolution

                if self.revolution:
                    print("Revolution ! All cards' strength is reversed (excluding Jokers).")
                else:
                    print("Counter revolution ! All cards' strength is back to normal.")

            # 8 turn stop
            if current_play.value == 8:
                end_turn = True

            # joker 3S counter
            if (turn.last_play.cards[0] == "JK1" or turn.last_play.cards[0]) == "JK2" \
            and turn.last_play.nb == 1 \
            and current_play.cards[0] == "3S":
                end_turn = True

            # player empties hand
            if turn.has_emptied_hand():
                current_play.player.has_finished = True

                for status in round.players_status:
                    if status is None:
                        round.players_status[status] = current_play.player
                        current_play.player.status = status

                        # bankruptcy case
                        if self.round > 1 and status == "Tycoon" \
                        and self.last_players_status[status] != current_play.player:
                            round.players_status["Beggar"] = self.last_players_status[status]
                            self.last_players_status[status].status = "Beggar"
                            self.last_players_status[status].has_finished = True
                            
                            # TO DO:
                            # send Bankruptcy message through discord

                        break

                # check if 3 players have finished (status already distributed)
                # if so, finish turn early
                remaining_players = 0
                for status in round.players_status:
                    if round.players_status[status] is None:
                        remaining_players += 1
                
                if remaining_players == 1:
                    end_turn = True

            
            turn.plays.append(current_play)
            turn.last_play = current_play

            self.current_turn_player = self.current_turn_player.next_player
            # finding the next player
            while self.current_turn_player.has_finished:
                self.current_turn_player = self.current_turn_player.next_player

        turn.ending_player = turn.last_play.player

        return turn


    # TO DO: discord implementation
    ### ask for a player input, check if valid 
    ### then return a new valid Play object
    def play_cards(self, turn):
        valid_play = False

        while not valid_play:
            # TO DO: DIRECT TO self.current_turn_player
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
            if turn.last_play is not None \
            and len(input_cards) != turn.last_play.nb:
                print(
                    f"Incorrect number of cards played. {len(input_cards)} instead of {turn.last_play.nb]}.")
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

            if turn.last_play is not None:
                # comparing with last play's value
                if self.revolution:
                    valid_play = play_value < turn.last_play.value
                else:
                    valid_play = play_value > turn.last_play.value

                # joker 3S counter
                if turn.last_play.nb == 1 \
                and (turn.last_play.value == 0 or turn.last_play.value == 20) \
                and input_cards[0] == "3S":
                    valid_play = True

                ### TO DO: ADD CARD DISPLAY
                # cards too "weak"
                if not valid_play:
                    print(
                        f"Invalid card value played. Last card(s) played: {turn.last_play.cards}")
        
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
        
        # TO DELETE
        play.get_attributes()
        return play


    ### display hands of players (cards hidden) MAY BE USELESS
    def display_players_hands(self):
        for player in self.players:
            player_hand = [CARD_TEMPLATE for card in player.hand]
            print(
                f"{player.name}({player.score}) : {player_hand} ({len(player_hand)})")


    # TO DO: discord implementation
    ### depending on players' status at start of round 2 and 3, exchange cards
    def redistribute_cards(self):
        for player in self.players:
            if player.status == "Tycoon":
                tycoon = player
            if player.status == "Rich":
                rich = player
            if player.status == "Poor":
                poor = player
            if player.status == "Beggar":
                beggar = player

        # TO DO: implement choice through discord
        # should be async
        beggar_trade = [beggar.hand.pop() for i in range(2)]
        poor_trade = poor.hand.pop()

        # tycoon
        valid_trade_tycoon = False
        while not valid_trade_tycoon:
            tycoon_trade_input = input(f"Please choose 2 cards to give (example: 3H 5D):\n")
            tycoon_trade_cards = tycoon_trade_input.upper().split()

            own_cards = True
            for card in tycoon_trade_cards:
                if card not in tycoon.hand:
                    own_cards = False
                    break
            
            if own_cards:
                valid_trade_tycoon = True
            else:
                print("Selection invalid.")

        for card in tycoon_trade_cards:
            tycoon.hand.remove(card)

        # rich
        valid_trade_rich = False
        while not valid_trade_rich:
            rich_trade_input = input(
                f"Please choose 1 card to give (example: 4D):\n")
            rich_trade_card = rich_trade_input.upper()
            if rich_trade_card in rich.hand:
                valid_trade_rich = True
            else:
                print("Selected card invalid.")

        rich.hand.remove(rich_trade_card)

        ## trading
        # TO DO: wait for both trade to be valid before going through the trade
        if valid_trade_tycoon and valid_trade_rich:
            for card in beggar_trade:
                tycoon.add_card_to_hand(card)
            
            for card in tycoon_trade_cards:
                beggar.add_card_to_hand(card)

            rich.add_card_to_hand(poor_trade)

            poor.add_card_to_hand(rich_trade_card)


    ### return a list of players in ascending scores
    def get_player_ranking(self):
        # recursive in-place sorting function
        def get_player_ranking_helper(player, ranking):
            if len(ranking) == 0:
                ranking.append(player)

            else:
                top_ranking = ranking.pop()
                if player.score >= top_ranking.score:
                    ranking.append(top_ranking)
                    ranking.append(player)

                else:
                    get_player_ranking_helper(player, ranking)
                    ranking.append(top_ranking)

        ranking = []

        for player in self.players:
            get_player_ranking_helper(player, ranking)

        return ranking


    ### display up to date classment
    def display_classment(self):
        current_classment = self.classment
        ranking = self.get_player_ranking()

        while len(ranking) > 0:
            player = ranking.pop()

            if len(ranking) == 3:
                current_classment = current_classment.replace(
                    "PLAYER_FIRST", player.name)
                current_classment = current_classment.replace(
                    "FIRST_SCORE", player.score)

            elif len(ranking) == 2:
                current_classment = current_classment.replace(
                    "PLAYER_SECOND", player.name)
                current_classment = current_classment.replace(
                    "SECOND_SCORE", player.score)

            elif len(ranking) == 1:
                current_classment = current_classment.replace(
                    "PLAYER_THIRD", player.name)
                current_classment = current_classment.replace(
                    "THIRD_SCORE", player.score)

            elif len(ranking) == 0:
                current_classment = current_classment.replace(
                    "PLAYER_LAST", player.name)
                current_classment = current_classment.replace(
                    "LAST_SCORE", player.score)

        print(current_classment)


# Used in Gamelogic
class Round():
    def __init__(self, player, num):
        self.starting_player = player
        self.number = num
        self.turns = []
        self.players_status = {
            # players' status at the end of this round
            "Tycoon": None,
            "Rich": None,
            "Poor": None,
            "Beggar": None
        }

    def get_attributes(self):
        for attribute, value in self.__dict__.items():
            print(attribute, '=', value)


class Turn():
    def __init__(self, player):
        self.starting_player = player
        self.plays = []
        self.last_play = None
        self.ending_player = None

    def get_attributes(self):
        for attribute, value in self.__dict__.items():
            print(attribute, '=', value)

    # return True after a play if the player has emptied their hand
    # else False
    def has_emptied_hand(self):
        player = self.last_play.player

        return len(player.hand) == 0


class Play():
    def __init__(self, player, value, nb_cards, cards_played):
        self.player = player
        self.value = value
        self.nb = nb_cards
        self.cards = cards_played

    def get_attributes(self):
        for attribute, value in self.__dict__.items():
            print(attribute, '=', value)


###
class Player:
    def __init__(self, name):
        self.name = name
        self.next_player = None
        self.prev_player = None
        self.hand = []
        self.has_finished = False # necessary because hand not empty != finished
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
