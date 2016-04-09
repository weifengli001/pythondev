"""
CPSC-442X Python Programming
Assignment 3: Tic tac toe game using tkinter
Author: Weifeng Li
UBID: 0984558
Date: March 31, 2016
"""
from tkinter import *
import math
import sqlite3
from tkinter.messagebox import *

width = 500#width of the game window
height = 530#height of the game window
canvas_length = width - 50 #width of the canvas
canvas_height = height - 70#height of the canvas
cell_length = canvas_length / 3#cell length of each square
cell_num = 9#number of squares
dbfilepath = "tic_tac_toe.db"#name of the database

#global constants are declared here
WON = 'won'
DRAW = 'draw'
LOST = 'lost'
TIE = 'tie'
EMPTY = ' '

#Player class
class Player:

    def __init__(self, name, mark, id ): #init the Player class
        self.id = id
        self.Name = name #player name
        self.PlayingMark = mark #the mark used by a player that shown in the Deck
        self.Statistics = {WON: 0, DRAW: 0, LOST: 0} # a dictionary used to store the game result of the player
        self.id = id #to be replaced by database value


    def get_score(self): #return the total score
        won = self.Statistics[WON]
        draw = self.Statistics[DRAW]
        lost = self.Statistics[LOST]
        return won * 2 + draw - lost

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
    # modified 4/8/2016, adding a return value: positions tuple of win which will be used to draw the winner line.
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
                return self.Board[row[0]], row
        if EMPTY not in self.Board:
            return TIE, None
        return None, None

#data access class to access the database
class DAtaAccessLayer:

    def __init__(self, dbfile):
        self.conn = sqlite3.connect(dbfile)
        self.cursor = self.conn.cursor()

    def get_player_score(self, playerID):#function to get player score by playerid
        ret = {WON: 0, DRAW: 0, LOST: 0}
        self.cursor = self.cursor.execute("SELECT PlayerId, PlayerName,"
                                          " PlayingMark, Won, Drawn, Lost  from Player "
                                          " where PlayerId =?", (playerID,))
        data = self.cursor.fetchone()
        if data is None:
            return ret
        else:
            #return data[3], data[4], data[5]
            ret[WON] = data[3]
            ret[DRAW] = data[4]
            ret[LOST] = data[5]
            return ret

    def save_player_score(self, player): #save player score info to database when game is over.
        self.cursor.execute("select count(*) from Player where PlayerId=?", (player.id,))
        cnt = self.cursor.fetchone()
        if cnt == 0:#if player dosen't exist insert a new one.
            self.cursor.execute("insert into Player values(?, ?, ?,?,?,?)",
                                (player.id,player.Name,player.PlayingMark,
                                 player.Statistics[WON],player.Statistics[DRAW],player.Statistics[LOST] ))
        else:#player exists update the scores.
            self.cursor.execute("update Player set Won=?, Drawn=?, Lost=? where PlayerId=?",
                                (player.Statistics[WON],player.Statistics[DRAW],
                                 player.Statistics[LOST], player.id))
        self.conn.commit()

    def __del__(self):
        self.cursor.close()
        self.conn.close()


#TicTacToe class
class TicTacToe:
    number = 0 #the # of game

    def __init__(self): #init function
        self.DeckList = [] #store all the deck in a game to this list
        self.data_access = DAtaAccessLayer(dbfilepath)# Data access object
        self.Player1 = Player('O', 'O', 1) #hard-code player1
        self.Player1.Statistics = self.data_access.get_player_score(self.Player1.id)
        self.Player2 = Player('X', 'X', 2) #hard-code player2
        self.Player2.Statistics = self.data_access.get_player_score(self.Player2.id)
        self.root = Tk()
        self.root.geometry(str(width)+"x"+str(height))
        self.frm = Frame(self.root)#using a frame holding all the wadgits.
        self.gamecnt = 0# game count
        self.gameCanvas = Canvas(self.frm, bg = "grey", height = canvas_height, width = canvas_length)
        self.gameCanvas.grid(row = 1, column = 0, columnspan = 3)# using grid
        """
            score information using 3 lables: player1_lb1, gamenum_lb, player2_lb1
        """
        self.player1_lb1 = Label(self.frm, text = "Player1"+ "\n" + str(self.Player1.get_score()))
        self.gamenum_lb = Label(self.frm, text ='Game counter'+ "\n" + str(self.gamecnt))
        self.player2_lb1 = Label(self.frm, text = "Player2" + "\n" + str(self.Player2.get_score()))
        self.player1_lb1.grid(row=0, column = 0)
        self.gamenum_lb.grid(row=0, column = 1)
        self.player2_lb1.grid(row=0, column = 2)

        #status label to show the game status
        self.status_lb = Label(self.frm, text="Game start")
        self.status_lb.grid(row = 2, column = 0, columnspan = 3)

        self.gameCanvas.bind("<Button>", self.mouseClick)#binding the canvas with click event
        self.frm.pack()
        self.start_game()

        self.root.mainloop()

    def mouseClick(self,event): #catch the click event,convert the coordinate to position index(0 -8)
        x = event.x
        y = event.y
        index =  math.floor(x / cell_length) + math.floor(math.sqrt(cell_num)) * math.floor(y / cell_length)
        #coordStr = str( (x,y, index) )
        #print(coordStr)
        self.play(index)

    #play game, most important game logic here.
    def play(self, index):
         if self.validate_user_input(index): #validate input, passed
            self.status_lb.config(fg='black')#change back status label font color to black
            self.status_lb['text'] = 'Player {0} selected cell {1}'.format(self.turn.Name, index)
            self.update_deck(int(index), self.turn) #update deck
            curdeck = self.get_cur_deck() #get current deck
            self.drawMark(index, self.turn)#draw the Deck
            self.turn = self.next_turn(self.turn) #get next player
            state, msg = self.is_game_over()
            if state == True: #game over
                self.data_access.save_player_score(self.Player1)
                self.data_access.save_player_score(self.Player2)
                result = askyesno(title='Game over', message=msg)
                if result:
                    self.start_game()#start a new game.
                else:
                    exit(0)
         else:#validate input, not passed
             self.status_lb.config(fg='red')#change status label font color to red
             self.status_lb['text'] = 'The cell at index {0} was already taken!'.format(index)


    def drawMark(self, index, player):#draw player marks to canvers player1(X), plaer2(O)
        x = index % 3 * cell_length + cell_length / 2
        y = math.floor(index / 3) * cell_length + cell_length / 2
        r = math.sqrt(cell_length * cell_length * 2) / 4

        p1 = (index % 3 * cell_length + cell_length / 4,
              math.floor(index / 3) * cell_length + cell_length / 4)
        p2 = (index % 3 * cell_length + 3 * cell_length / 4,
              math.floor(index / 3) * cell_length + cell_length / 4)
        p3 = (index % 3 * cell_length + 3 * cell_length / 4,
              math.floor(index / 3) * cell_length + 3 * cell_length / 4)
        p4 = (index % 3 * cell_length + cell_length / 4,
              math.floor(index / 3) * cell_length + 3 * cell_length / 4)
        if player.id == 2:
            self.gameCanvas.create_line([p1[0], p1[1], p3[0], p3[1]],  fill='black', width=4 )
            self.gameCanvas.create_line([p2[0], p2[1], p4[0], p4[1]],  fill='black', width=4 )
        elif player.id == 1:
            self.gameCanvas.create_oval(x - r, y-r,
                                    x + r, y+r, width=4, outline ="black" )

    #function that is used for the drawing of winner line.
    #(x1, y1): the most left-up center
    #(x2, y2): the most right-down cneter
    #using these 2 point we can draw the winner line when any player win the game.
    def drawWin(self, indexes):
        x1 = indexes[0] % 3 * cell_length + cell_length / 2
        y1 = math.floor(indexes[0] / 3) * cell_length + cell_length / 2

        x2 = indexes[2] % 3 * cell_length + cell_length / 2
        y2 = math.floor(indexes[2] / 3) * cell_length + cell_length / 2

        self.gameCanvas.create_line(x1, y1, x2, y2, fill="red", width=4)

    #validate if a position has already been taken by the other player.
    def validate_user_input(self, val): #validate user input
        curdeck = self.get_cur_deck()
        if curdeck.Board[int(val)] != EMPTY:
            print('The cell at index {0} was already taken!'.format(val))
            print('------------------------------------------')
            return False
        else:
            return True

    def is_game_over(self): #to verify if game over
        curdeck = self.get_cur_deck() #get current deck(the last one in DeckList)

        winner, indexes = curdeck.winner() #if somebody win or not, return the marker of winner and positions.
        message = ''#this will be shown in the opened dialog when the game is over.
        if winner is None:
            return False, message
        else:
            if winner == TIE: #tie, record the result to players statistics
                print('Tie.')
                message = 'Tie, start new game?'
                self.Player1.Statistics[DRAW] += 1
                self.Player2.Statistics[DRAW] += 1
            else:
                if self.Player1.PlayingMark == winner: #player1 won, record the result to players statistics
                    print('Player {0} won.'.format(self.Player1.Name))
                    message = 'Player {0} won, start new game?'.format(self.Player1.Name)
                    self.Player1.Statistics[WON] += 1
                    self.Player2.Statistics[LOST] += 1
                else: #player2 won, record the result to players statistics
                    print('Player {0} won.'.format(self.Player2.Name))
                    message = 'Player {0} won, start new game?'.format(self.Player2.Name)
                    self.Player1.Statistics[LOST] += 1
                    self.Player2.Statistics[WON] += 1
                self.drawWin(indexes)#when one player win the game winner line is drawn.
            print('Game over!')
            #self.recordresult(self.DeckList, FILENAME) # write the result to the file.
            return True, message

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
        self.gameCanvas.delete(ALL)
        self.gamecnt += 1
        print('Tic-Tac-Toe game number: ', self.gamecnt)
        deck = Deck()
        self.DeckList.append(deck)
        self.turn = self.Player1 # player1 first turn
        t = [[cell_length, 0, cell_length, canvas_height],
            [cell_length * 2, 0, cell_length * 2, canvas_height],
            [0, cell_length, canvas_length, cell_length],
            [0, cell_length * 2, canvas_length, cell_length * 2]]
        for x in t: # draw the deck line, seperate the deck into several cells.
            self.gameCanvas.create_line(x, fill='blue', width=4 )
        self.player1_lb1['text'] = "Player1"+ "\n" + str(self.Player1.get_score())
        self.gamenum_lb['text'] = 'Game counter'+ "\n" + str(self.gamecnt)
        self.player2_lb1['text'] = "Player2"+ "\n" + str(self.Player2.get_score())


if __name__ == "__main__":
    game = TicTacToe()


