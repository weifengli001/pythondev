"""
CPSC-442X Python Programming
Assignment 2: Tic tac toe game
Author: Weifeng Li
UBID: 0984558
Date: March 3, 2016
"""

import os
import subprocess
import platform

#global constants are declared here
WON = 'won'
DRAW = 'draw'
LOST = 'lost'
TIE = 'tie'
EMPTY = ' '
FILENAME ='TicTacToe.txt' #game results are written to this file

#Player class
class Player:

    def __init__(self, name, mark): #init the Player class
        self.Name = name #player name
        self.PlayingMark = mark #the mark used by a player that shown in the Deck
        self.Statistics = {WON: 0, DRAW: 0, LOST: 0} # a dictionary used to store the game result of the player

    def get_score(self): #return the total score
        won = self.Statistics[WON]
        draw = self.Statistics[DRAW]
        lost = self.Statistics[LOST]
        return won * 2 + draw - lost

    def __str__(self): #print the detail information of a player
        return str('Player: ' + self.Name + ', Mark: '
                   + self.PlayingMark + ', Score: ' + str(self.get_score()))

    def __lt__(self, other): #compare two palyer by score
        return self.get_score() < other.get_score()

#Deck class
class Deck:

    def __init__(self): #init method
        self.Board = [] # a 3 * 3 board
        self.Player1Choices = [] # used to store each step of player1
        self.Player2Choices = [] #used to store each step of player2
        for i in range(9):
            self.Board.append(EMPTY)

    #to verify if somebody won or tie.
    #if one player won, return the player's mark
    # if tie return 'tie' else return None
    def winner(self):
        ways_to_win = (
             (0, 1, 2),
             (3, 4, 5),
             (6, 7, 8),
             (0, 3, 6),
             (1, 4, 7),
             (2, 5, 8),
             (0, 4, 8),
             (2, 4, 6)
        )
        for row in ways_to_win:
            if self.Board[row[0]] == self.Board[row[1]] == self.Board[row[2]] != EMPTY:
                return self.Board[row[0]]
        if EMPTY not in self.Board:
            return TIE
        return None

    def __str__(self): #used to print the game result to screen.
        myboard = '     |     |     \n' \
                   + '  {0}  |  {1}  |  {2}  \n' \
                   + '_____|_____|_____\n' \
                   + '     |     |     \n' \
                   + '  {3}  |  {4}  |  {5} \n' \
                   + '_____|_____|_____\n' \
                   + '     |     |    \n' \
                   + '  {6}  |  {7}  |  {8} \n' \
                   + '     |     |    \n'
        return str(myboard.format(*tuple(self.Board)))

#TicTacToe class
class TicTacToe:
    number = 0 #the # of game

    def __init__(self): #init function
        self.DeckList = [] #store all the deck in a game to this list
        self.Player1 = Player('X', 'X') #hard-code player1
        self.Player2 = Player('O', 'O') #hard-code player2

    def validate_user_input(self, val): #validate user input
        try:
            intVal = int(val)
        except ValueError:
            print('invalid move, move should be an integer')
            print('------------------------------------------')
            return False
        else:
            if(intVal < 0 or intVal > 8):
                print('Invalid move, move should be between 0 and 8')
                print('------------------------------------------')
                return False
            else:
                curdeck = self.get_cur_deck()
                if curdeck.Board[intVal] != EMPTY:
                    print('The cell at index {0} was already taken!'.format(val))
                    print('------------------------------------------')
                    return False
                else:
                    return True

    def is_game_over(self): #to verify if game over
        curdeck = self.get_cur_deck() #get current deck(the last one in DeckList)
        winner = curdeck.winner() #if somebody win or not
        if winner is None:
            return False
        else:
            if winner == TIE: #tie, record the result to players statistics
                print('Tie.')
                self.Player1.Statistics[DRAW] += 1
                self.Player2.Statistics[DRAW] += 1
            else:
                if self.Player1.PlayingMark == winner: #player1 won, record the result to players statistics
                    print('Player {0} won.'.format(self.Player1.Name))
                    self.Player1.Statistics[WON] += 1
                    self.Player2.Statistics[LOST] += 1
                else: #player2 won, record the result to players statistics
                    print('Player {0} won.'.format(self.Player2.Name))
                    self.Player1.Statistics[LOST] += 1
                    self.Player2.Statistics[WON] += 1
            print('Game over!')
            self.recordresult(self.DeckList, FILENAME) # write the result to the file.
            return True

    def recordresult(self, DeckList, file): #function used to write results to a file
        file = open(file, 'a')
        curdeck = self.get_cur_deck()
        #for deck in DeckList:
        file.write('Player1: {0} '.format(str(curdeck.Player1Choices)))
        file.write('Player2: {0}'.format(str(curdeck.Player2Choices)))
        file.write('\n')
        file.close()

    def get_user_input(self, player): #get user screen input
        inputval = input('Enter Player {0} move:'.format(player.Name))
        if self.validate_user_input(inputval): #validate input
            self.update_deck(int(inputval), player) #update deck
            #self.is_game_over()
            return True
        return False

    def update_deck(self, position, curplayer): #update deck
        curdeck = self.get_cur_deck()
        curdeck.Board[position] = curplayer.PlayingMark
        if curplayer.Name == 'X':
            curdeck.Player1Choices.append(position)
        else:
            curdeck.Player2Choices.append(position)

    def get_cur_deck(self): #get current deck, the last one of DeckList
        return self.DeckList[len(self.DeckList) - 1]

    def next_turn(self, turn): #return the next player who take the turn
        if turn == self.Player1:
            return self.Player2
        else:
            return self.Player1

    def start_game(self): #entrance of the game
        while True:
            self.number += 1
            print('Tic-Tac-Toe game number: ', self.number)
            deck = Deck()
            self.DeckList.append(deck)
            turn = self.Player1 # player1 first turn
            while True:
                if self.get_user_input(turn):
                    os.system('cls' if os.name == 'nt' else 'clear') #clear the screen
                    curdeck = self.get_cur_deck() #get current deck
                    print(curdeck)  #print current deck to screen
                    turn = self.next_turn(turn) #get next player
                if self.is_game_over(): #game over, print result to screen
                    print(self.Player1)
                    print(self.Player2)
                    request = self.ask_yes_no('Play agin?(Y/N)')
                    if request == 'n': #exit the game
                        exit(0)
                    else: #continue for another game
                        os.system('cls' if os.name == 'nt' else 'clear')
                        break;

    def ask_yes_no(self, question):
        """Ask a yes or no question."""
        response = None
        while response not in ("y", "n", 'Y', 'N'):
            response = input(question).lower()
        return response

if __name__ == "__main__":
    game = TicTacToe()
    game.start_game()


