# https://www.programmingexpert.io/projects/blackjack-card-game

import random

class Blackjack():
    SUITS = ["♦", "♥", "♣", "♠"]
    VALUES = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K"]
    DECK = []

    for value in VALUES:
        for suit in SUITS:
            DECK.append(value + suit)

    def __init__(self):
        self.deck = Blackjack.DECK
        self.player_money = 500
        self.player_hand = []
        self.dealer_hand = []
        self.current_bet = 0
        self.game_over = False


    def play(self):
        start_game = input(f"You are starting with ${self.player_money}. Would you like to play a hand (y/n)? ")

        if start_game != "y":
            print(f"You stopped with ${self.player_money}.")
            self.game_over = True
        else:
            self.bet()
            self.deal_hands()

            player_value = self.calculate_hand_value(of="player")
            # print(player_value)
            stay = False
            round_over = False
            natural = player_value == 21
            while not stay and not round_over and not natural:
                hit_or_stay = input("Would you like to hit or stay? ")

                if hit_or_stay == "stay":
                    stay = True

                elif hit_or_stay == "hit":
                    self.deal_card(to="player")
                    player_value = self.calculate_hand_value(of="player")
                    # print(player_value)

                    natural = player_value == 21
                    round_over = player_value > 21

                else:
                    print("That is not a valid option.")
                
            # player's hand value over 21
            if round_over:
                print(f"Your hand value is over 21 and you lose ${self.current_bet} :(")

            # dealer's turn
            else:
                print(f"The dealer has: ", end="")
                print(*self.dealer_hand, sep=", ")

                dealer_value = self.calculate_hand_value(of="dealer")
                while dealer_value < 17:
                    self.deal_card(to="dealer")
                    dealer_value = self.calculate_hand_value(of="dealer")

                # player wins
                if dealer_value > 21 or dealer_value < player_value:
                    if natural:
                        prize = self.current_bet * 1.5
                        self.player_money += prize
                        print(f"Blackjack! You win ${prize} :)")
                    else:
                        self.player_money += self.current_bet
                        print(f"You win ${self.current_bet} !")
                    
                    self.player_money += self.current_bet

                # tie
                elif dealer_value == player_value:
                    self.player_money += self.current_bet
                    print("You tie. Your bet has been returned.")
                
                # player loses
                else:
                    print(f"The dealer wins, you lose ${self.current_bet} :(")
                
            self.reset()


    # sets the current bet value after receiving a valid input
    def bet(self):
        valid_bet = False
        while not valid_bet:
            bet = input("Place your bet: ")
            
            try:
                bet = float(bet)
                valid_bet = True
            except:
                print("Invalid bet. Minimum bet is $1.")
        
            if valid_bet:
                if bet > self.player_money:
                    valid_bet = False
                    print("You do not have sufficient funds.")

        self.current_bet = bet
        self.player_money -= bet


    # deals initial hands to the player and dealer
    def deal_hands(self):
        random.shuffle(self.deck)
        self.player_hand.append(self.deck.pop())
        self.player_hand.append(self.deck.pop())
        print("You are dealt: ",end="")
        print(*self.player_hand, sep=", ")

        self.dealer_hand.append(self.deck.pop())
        self.dealer_hand.append(self.deck.pop())
        print(f"The dealer is dealt: {self.dealer_hand[0]}, ??")


    # takes either "player" or "dealer", deals them a card from the deck
    def deal_card(self, to):
        card = self.deck.pop()
        if to == "player":
            print(f"You are dealt: {card}")
            self.player_hand.append(card)
            print("You now have: ", end="")
            print(*self.player_hand, sep=", ")

        elif to == "dealer":
            print(f"The dealer hits and is dealt: {card}")
            self.dealer_hand.append(card)
            print("The dealer has: ", end="")
            print(*self.dealer_hand, sep=", ")


    # takes either "player" or "dealer", returns the value of their hand
    def calculate_hand_value(self, of):
        if of == "player":
            hand = self.player_hand
        elif of == "dealer":
            hand = self.dealer_hand

        value = 0
        num_of_A = 0
        for card in hand:
            card_value = card[0]

            if card_value.isdigit():
                value += int(card_value)
            else: 
                if card_value != "A":
                    value += 10
                else:
                    num_of_A += 1
        
        while num_of_A > 0:
            temp_value = value + 11
            
            if temp_value > 21:
                value += 1
            else:
                value += 11
            
            num_of_A -= 1
                        
        return value


    # resets player's bet, both hands, and puts the card back into the deck
    # sets game_over to True if the player runs out of money
    def reset(self):
        self.current_bet = 0

        self.deck.extend(self.player_hand)
        self.deck.extend(self.dealer_hand)

        self.player_hand = []
        self.dealer_hand = []

        if self.player_money <= 0:
            self.game_over = True
            print(
                "You've ran out of money. Please restart this program to try again. Goodbye.")


blackjack_game = Blackjack()

while not blackjack_game.game_over:
    blackjack_game.play()