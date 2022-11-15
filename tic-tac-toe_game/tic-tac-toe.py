# Tic Tac Toe

from assets import *

### Game logic ###
class GameLogic:
   def __init__(self):
      self.board = [
         [None, None, None],
         [None, None, None],
         [None, None, None]
      ]
      self.game_over = False
      self.current_player = True
      self.num_of_plays = 0
      self.current_grid = GRID
      self.p1_symbol = PLAYER_ONE_SYMBOL
      self.p2_symbol = PLAYER_TWO_SYMBOL

   def play_move(self):
      if self.num_of_plays < 9:
         print(GRID)
         play_input = input("Please type the number of the square you wish to play: ")

         while not self.validate_coor(play_input) and play_input != "r":
            print("Wrong input.")
            play_input = input("Please type the number of the square you wish to play: ")

         # Secret reset command
         if play_input == "r":
            self.reset_state()
            return

         self.update_board(play_input)
         self.update_grid(play_input)
         self.check_victory(play_input)

         if self.game_over:
            if self.current_player:
               player = f"Player 1 ({self.p1_symbol})"
            else:
               player = f"Player 2 ({self.p2_symbol})"
            print(f"{player} has won !")

         # Switching from one player to the other
         else:
            self.current_player = not self.current_player

      else:
         self.game_over = True
         print("Draw !")

      if self.game_over:
         reset_input = input("Type 'y' if you want to do another round: ")

         if reset_input == "y":
            self.reset_state()


   # Return True if the num given if valid, else False
   def validate_coor(self, num):
      if num in NUM_TO_COOR:
         row = NUM_TO_COOR[num][0]
         col = NUM_TO_COOR[num][1]

         if self.board[row][col] is None:
            return True

      return False


   # Update the state of the board
   def update_board(self, num):
      row = NUM_TO_COOR[num][0]
      col = NUM_TO_COOR[num][1]

      self.board[row][col] = self.current_player
      self.num_of_plays += 1


   # Update the grid with the player's symbol
   def update_grid(self, num):
      if self.current_player:
          symbol = self.p1_symbol
      else:
          symbol = self.p2_symbol

      self.current_grid = self.current_grid.replace(num, symbol)
      self.print_cleared_grid()


   # Print a version of the grid without the nums
   def print_cleared_grid(self):
      cleared_grid = self.current_grid
      for num in NUM_TO_COOR:
         cleared_grid = cleared_grid.replace(num, " ")

      print(cleared_grid)


   # Check the victory conditions, modify game_over to True if one player wins
   def check_victory(self, num):
      row = NUM_TO_COOR[num][0]
      col = NUM_TO_COOR[num][1]
      #print(f"Num : {num} // row : {row} // col : {col}")

      self.game_over = (
         self.board[row][0] == self.board[row][1] == self.board[row][2]) or (
         self.board[0][col] == self.board[1][col] == self.board[2][col]
      )

      # Handling diagonals
      exceptions = ["1", "3", "5", "7", "9"]
      if num in exceptions:
         if num == "1" or num == "5" or num == "9":
            self.game_over = self.game_over or (
               self.board[0][0] == self.board[1][1] == self.board[2][2]
            )
         if num == "3" or num == "5" or num == "7":
            self.game_over = self.game_over or (
               self.board[0][2] == self.board[1][1] == self.board[2][0]
            )
      

   # Reset the state of the game
   def reset_state(self):
      self.board = [[None for elem in self.board[0]] for row in self.board]
      self.current_grid = GRID
      self.game_over = False
      self.current_player = True
      self.num_of_plays = 0


### Execution ###
game = GameLogic()
while not game.game_over:
   game.play_move()