# AUTOGENERATED! DO NOT EDIT! File to edit: dev/01_ai.ipynb (unless otherwise specified).

__all__ = ['RandomAgent', 'BasicAgent', 'win_rates', 'swoggle_to_state_vector', 'action_from_number']

# Cell
from .core import *
import random
class RandomAgent:
    """ Given a swoggle board on which it is a player, make a random valid move """

    def __init__(self, player):
        self.player = player

    def move(self, board, dice_roll):

        # If in jail, try to escape
        if self.player in board.jail:
            board.move(self.player, (0, 0), (0, 0), dice_roll, False, False)
            return 'escape'

        # Get start_loc
        start_loc = (9, 9)
        for row in board.board:
            for cell in row:
                if cell.player == self.player:
                    start_loc = (cell.y, cell.x)
        if start_loc == (9, 9):
            return None

        # Make a random move within reach
        move = ()
        count = 0
        while True:
            count += 1
            end_x = random.choice(range(8))
            end_y = random.choice(range(8))
            drone = random.choice([True, False])
            powerjump = random.choice([True, False])
            valid = board.is_valid_move(self.player, start_loc, (end_x, end_y), dice_roll, drone=drone, powerjump=powerjump)
            move = ()
            if valid:
                move = ((self.player, start_loc, (end_x, end_y), dice_roll, drone, powerjump))
#                 print(f'{self.player} took {count} tries to guess a random move')
                break
        board.move(*move)
        return move


# Cell
class BasicAgent:
    """ Given a swoggle board on which it is a player, make a sensible move """

    def __init__(self, player):
        self.player = player

    def move(self, board, dice_roll):

        # If in jail, try to escape
        if self.player in board.jail:
            board.move(self.player, (0, 0), (0, 0), dice_roll, False, False)
            return 'escape'

        # Get start_loc
        start_loc = (9, 9)
        for row in board.board:
            for cell in row:
                if cell.player == self.player:
                    start_loc = (cell.y, cell.x)
        if start_loc == (9, 9):
            return None


        # If bases in range, take them

        for row in board.board:
            for cell in row:
                if cell.player == None and cell.base != None and cell.base != self.player: # Normal move
                    move = (self.player, start_loc, (cell.x, cell.y), dice_roll, False, False)
                    if board.is_valid_move(*move):
                        board.move(*move)
                        return (move)

                if cell.base != None and cell.base != self.player: # Drone attack
                    move = (self.player, start_loc, (cell.x, cell.y), dice_roll, True, False)
                    if board.is_valid_move(*move):
                        board.move(*move)
                        return (move)

        # If on base and player in range, take or powerjump them
        if board.board[start_loc[0]][start_loc[1]].base == self.player:
            for row in board.board:
                for cell in row:
                    if cell.player != None and cell.player != self.player:
                        # try normal move
                        move = (self.player, start_loc, (cell.x, cell.y), dice_roll, False, False)
                        if board.is_valid_move(*move):
                            board.move(*move)
                            return (move)
                        # Try powerjump
                        move = (self.player, start_loc, (cell.x, cell.y), dice_roll, False, True)
                        if board.is_valid_move(*move):
                            board.move(*move)
                            return (move)

        # If players in range and takeable, take them
        for row in board.board:
            for cell in row:
                if cell.player != None and cell.player != self.player:
                    # Normal take
                    move = (self.player, start_loc, (cell.x, cell.y), dice_roll, False, False)
                    if board.is_valid_move(*move):
                        board.move(*move)
                        return (move)
                    # Drone take
                    move = (self.player, start_loc, (cell.x, cell.y), dice_roll, True, False)
                    if board.is_valid_move(*move):
                        board.move(*move)
                        return (move)

        # TODO: If player close to your base and base reacheable, go back to base

        # Else move randomly

        # Make a random move within reach
        move = ()
        count = 0
        while True:
            count += 1
            end_x = random.choice(range(8))
            end_y = random.choice(range(8))
            drone = random.choice([True, False])
            powerjump = random.choice([True, False])
            valid = board.is_valid_move(self.player, start_loc, (end_x, end_y), dice_roll, drone=drone, powerjump=powerjump)
            move = ()
            if valid:
                move = ((self.player, start_loc, (end_x, end_y), dice_roll, drone, powerjump))
#                 print(f'{self.player} took {count} tries to guess a random move')
                break
        board.move(*move)
        return move

# Cell
from IPython.display import clear_output

def win_rates(n, agents):
    wins = {}
    for i in range(n):
        rounds = 0
        sr = Swoggle(agents, verbose=False)
        while True:
            sr.move_agents()
            rounds += 1
            players = []
            for row in sr.board.board:
                for cell in row:
                    if cell.player != None:
                        players.append(cell.player)
            if len(players) <= 1:
                clear_output(wait=True)
                print("Winner:", players, rounds)
                if len(players) == 1:
                    if players[0] in wins:
                        wins[players[0]] += 1
                    else:
                        wins[players[0]] = 1
                break
    return wins




# Cell
import numpy as np
def swoggle_to_state_vector(sr, player, dice_roll):
    board = sr.board
    spa = board.jail
    # The player locations (192 = 3*8*8)
    players = np.concatenate([np.array([c.player == p for c in np.array(sr.board.board).flatten()]).astype(int) for p in range(1, 5) if p != player])
    # The base locations of the other players (192 = 3*8*8)
    bases = np.concatenate([np.array([c.base == p for c in np.array(sr.board.board).flatten()]).astype(int) for p in range(1, 5) if p != player])
    # The drones (64 = 8*8)
    drones = np.array([c.drone for c in np.array(sr.board.board).flatten()]).astype(int)
    # Player location and base (64 each)
    player_loc = np.array([c.player == player for c in np.array(sr.board.board).flatten()]).astype(int)
    base = np.array([c.base == player for c in np.array(sr.board.board).flatten()]).astype(int)
    # dice (6)
    dice = np.array([int(i==dice_roll) for i in range(1, 7)])
    # Spa (3)
    prisoners = np.array([p in spa for p in range(1, 5) if p != player]).astype(int)

    return np.concatenate([players, bases, player_loc, base, drones, dice, prisoners])

# Cell
def action_from_number(move, player, sw, dice_roll):
    """ Takes the output of the network, samples from the probs, does the move if possible, returns move_type,  the move itself and the move number"""
    board = sw.board
    move_number = move * 1

    # Start by getting player's current loc
    start_loc = (9, 9)
    for row in board.board:
        for cell in row:
            if cell.player == player:
                start_loc = (cell.y, cell.x)
    if start_loc == (9, 9): # Player
        action = (player, (9, 9),(9, 9), dice_roll, False, False)
        return 'dead', action, 0


    drone, pj = False, False
    move_type = ''
    if move//64 == 0: # Normal Move
        move_type = 'normal'
    elif move//64 == 1:
        move -= 64
        pj=True
        move_type = 'powerjump'
    else:
        move -= 128
        drone = True
        move_type = 'drone'

    x = move//8
    y = move%8
    action = (player, start_loc, (x, y), dice_roll, drone, pj)
    return move_type, action, move_number