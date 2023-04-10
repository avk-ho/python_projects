import random
from assets import *

# Game is 3 rounds
# Each Round, players take Turns
# Each Turn, players make Plays (including passing)

# NOTE: implement a way to cancel a game in the making
# if there are not enough players registering within a time limit

class Gamelogic:
    
    def __init__(self) -> None:
        self.players = []
        self.revolution = False
        self.rounds = []



class Round:
    def __init__(self, player):
        self.starting_player = player
        self.turns = []
        self.players_status = {

        }
    
    def get_attributes(self):
        for attribute, value in self.__dict__.items():
            print(attribute, '=', value)


class Turn:
    def __init__(self, player):
        self.starting_player = player
        self.plays = []
        self.last_play = None
        self.ending_player = None


    def get_attributes(self):
        for attribute, value in self.__dict__.items():
            print(attribute, '=', value)


class Play:
    def __init__(self, player, value, nb_cards, cards_played):
        self.player = player
        self.value = value
        self.nb = nb_cards
        self.cards = cards_played


    def get_attributes(self):
        for attribute, value in self.__dict__.items():
            print(attribute, '=', value)