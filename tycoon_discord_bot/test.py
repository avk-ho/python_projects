from main import *

## sorted add card test
p1 = Player("P1")
rand_deck = [key for key in DECK]
random.shuffle(rand_deck)
print(rand_deck)
while len(rand_deck) > 0:
    new_card = rand_deck.pop()
    p1.add_card_to_hand(new_card)

# print(P1.hand)
# print(len(P1.hand))

## play_cards test
# p1 = Player("P1")
# p1.hand = [""]
game = Gamelogic()
game.last_play = [4, 3, ["4H", "4C", "4S"]]
game.current_turn_player = p1

# game.revolution = True
game.last_play = [20, 1, ["JK1"]]
game.last_play = [9, 3, ["9H", "9C", "9S"]]

game.play_cards()
print(p1.hand)
# 5c jk1 9h
# jk1 jk2 5h
# 5c 5s 5d