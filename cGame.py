


import chess
import chess.pgn
import time
import random
import datetime
from typing import Callable
from typing import List


GAME_TIME = 30
DELAY = 0.5
MAX_MOVES = 150

def chessGame (white: Callable[[chess.Board, float], chess.Move], black: Callable[[chess.Board, float], chess.Move], board: chess.Board) -> (chess.pgn.Game, chess.Outcome):
    
    """ Takes in functions representing black and white players and plays a chess game between the two given a starting board. Returns gamke object (history of the game) as well as outcome object given by chess library """
    
    timeWhite = GAME_TIME
    timeBlack = GAME_TIME
    
    game = chess.pgn.Game() 
    game.headers["White"] = white.__name__ 
    game.headers["Black"] = black.__name__
    game.headers["Event"] = "Chess Coding Competition"
    game.headers["Site"] = ""
    date_time = datetime.datetime.now()
    game.headers["Date"] = date_time.strftime("%m/%d/%Y")
    game.setup(board)    
    node = game
    
    for _ in range(MAX_MOVES):
        
        #White move
        startTime = time.perf_counter() 
        move = white(board, timeWhite) #creates white's move
        endTime = time.perf_counter()
        
        if endTime - startTime > timeWhite + 0.5: #timing system selects a random move if time is exceeded
            timeWhite = 0
            move = random.choice(list(board.legal_moves)) 
        else: 
            timeWhite -= endTime - startTime
            
        try: #catches incorrect moves 
            board.push(move)
            node = node.add_variation(move)
        except:
            print("supplied move either not legal or incorrectly formatted")
            board.push(random.choice(list(board.legal_moves)))
            node = node.add_variation(move)
        
        if board.outcome():
            break
            
        #black move               
        startTime = time.perf_counter() 
        move = black(board, timeBlack) #creates blacks's move
        endTime = time.perf_counter()
        
        if endTime - startTime > timeBlack + 0.5: #timing system selects a random move if time is exceeded
            timeBlack = 0
            move = random.choice(list(board.legal_moves)) 
        else: 
            timeBlack -= endTime - startTime
            
        try: #catches incorrect moves 
            board.push(move)
            node = node.add_variation(move)
        except:
            print("supplied move either not legal or incorrectly formatted")
            board.push(random.choice(list(board.legal_moves)))
            node = node.add_variation(move)
                               
        if board.outcome():
            break
   
    if board.outcome():
        return game, board.outcome()
    else:
        return game, chess.Board("8/8/3k4/8/8/8/5K2/8 w - - 0 1").outcome() #will return a drawn outcome if the max moves are exceeded

def chessMatch (bot1: Callable[[chess.Board, float], chess.Move], bot2: Callable[[chess.Board, float], chess.Move], boardPositions: List[str]) -> (int, int, int, List[chess.pgn.Game]):
    
    """ Takes in two bots names as strings as well as a list of positions as a FEN string. OUtputs the result between those two bots playing every given position as both white and black. Returns bot1 wins, bot2wins, and draws each as integers as well as returns a list game objects for every game played. """
    
    games = [[],[]]
    
    bot1Score = 0
    draws = 0
    bot2Score = 0
    
    round_ = 1
    
    for position in boardPositions:
        
        board = chess.Board(position)
        game, outcome = chessGame(bot1,bot2,board) #bot1 playing as white
        result = outcome.winner
        
        game.headers["Round"] =  round_
        round_ += 1
        games[0].append(game)
        if result: 
            bot1Score +=1 
        elif result == None:
            draws += 1
        else:
            bot2Score += 1
        
        board = chess.Board(position)
        game, outcome = chessGame(bot2,bot1,board) #bot2 playing as white
        result = outcome.winner
        
        game.headers["Round"] =  round_
        round_ += 1        
        games[1].append(game)
        if result: 
            bot2Score +=1 
        elif result == None:
            draws += 1
        else:
            bot1Score += 1
            
    return bot1Score, draws, bot2Score, games

def downloadGame (game: chess.pgn.Game, filename: str):
    
    """ takes in a game object as well as a filename as a string and downloads the game object as a pgn file to the given filename"""
    
    with open(filename, "w") as pgn_file:
        pgn_file.write(str(game))