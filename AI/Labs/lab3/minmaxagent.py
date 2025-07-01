import math
import random
from connect4 import Connect4

class MinMaxAgent:
    def __init__(self, my_token, depth=4):
        self.my_token = my_token
        self.opponent_token = 'o' if my_token == 'x' else 'x'
        self.depth = depth

    def decide(self, connect4):
        _, best_move = self.minmax(connect4, self.depth, True)
        return best_move

    def minmax(self, connect4, depth, maximizing_player):
        if depth == 0 or connect4.game_over:
            return self.evaluate(connect4), None

        possible_moves = connect4.possible_drops()
        best_move = None

        if maximizing_player:
            max_eval = -math.inf
            for move in possible_moves:
                new_connect4 = self.simulate_move(connect4, move, self.my_token)
                evaluation, _ = self.minmax(new_connect4, depth-1, False)
                if evaluation > max_eval:
                    max_eval = evaluation
                    best_move = move
            if best_move == 0:
                best_move = random.choice(connect4.possible_drops())
            return max_eval, best_move
        else:
            min_eval = math.inf
            for move in possible_moves:
                new_connect4 = self.simulate_move(connect4, move, self.opponent_token)
                evaluation, _ = self.minmax(new_connect4, depth-1, True)
                if evaluation < min_eval:
                    min_eval = evaluation
                    best_move = move
            if best_move == 0:
                best_move = random.choice(connect4.possible_drops())
            return min_eval, best_move

    def simulate_move(self, connect4, move, token):
        new_connect4 = Connect4(connect4.width, connect4.height)
        new_connect4.board = [row[:] for row in connect4.board]
        new_connect4.who_moves = connect4.who_moves
        new_connect4.game_over = connect4.game_over
        new_connect4.wins = connect4.wins
        
        new_connect4.drop_token(move)
        return new_connect4

    def evaluate(self, connect4):
        if connect4.wins == self.my_token:
            return 1000
        elif connect4.wins == self.opponent_token:
            return -1000
        else:
            return 0

    def heuristic(self, connect4):
        score = 0
        for four in connect4.iter_fours():
            score += self.evaluate_four(four)
        return score

    def evaluate_four(self, four):
        score = 0
        if four.count(self.my_token) == 3 and four.count('_') == 1:
            score += 100
        elif four.count(self.my_token) == 2 and four.count('_') == 2:
            score += 10
        elif four.count(self.opponent_token) == 3 and four.count('_') == 1:
            score -= 100
        elif four.count(self.opponent_token) == 2 and four.count('_') == 2:
            score -= 10
        return score