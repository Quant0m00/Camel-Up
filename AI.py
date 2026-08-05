from colorama import Fore, Back, Style, init
from copy import deepcopy
from itertools import permutations, product
import math
from Pyramid import Pyramid 
try:
    from Board import Board
except ModuleNotFoundError:
    print("Board.py is not found.")
    pass

class AI:
    def __init__(self, board:Board):
        self.STYLES = board.STYLES
        self.board = board #reference to actual game board... updates as game is played
        pass

    def run_experimental_analysis(self, trials:int) -> dict[str, tuple[float, float]]:
        '''Conducts an experimental analysis (ie. a random simulation) of the probability that each camel
            will win either 1st or 2nd place in this leg of the race. The experimental analysis counts
            1st/2nd place finishes by counting outcomes from randomly shaking the pyramid over a given
            number of trials.

           General Steps:
                1) Save current gamestate using deepcopy
                2) Shake the pyramid and move camels enough times to finish the leg
                2) Count a 1st/2nd place finish for each camel
                3) Reset gamestate and repeat steps #1 - #2 trials number of times
                3) Calculate the probability that each camel will come in 1st or 2nd based on the total
                   number of 1st/2nd finishes out of the total number of trials

           Args
              trials (int): The number of random simulations to conduct

           Returns:
              dict[str, tuple[float, float]] - A dictionary representing the probabilities that a camel will
                                               come in first or second place according to an experimental analysis
                {
                    'r':(0.5, 0.2),
                    'b':(0.1, 0.04),
                    ...
                }
        '''
        ## YOUR CODE GOES HERE
        tally_wins_dictionary = {
            "r": [0,0],            
            "b": [0,0],
            "g": [0,0],
            "p": [0,0],
            "y": [0,0],
        }
        tally_probability = {

        }
        for games in range(trials):
            gamestate_copy =deepcopy(self.board)
            for i in range(len(gamestate_copy.pyramid.remaining_dice)):
                trial_rolls = gamestate_copy.roll_die()
                gamestate_copy.move_camel(trial_rolls)
            
            trial_rankings = gamestate_copy.get_rankings()
            tally_wins_dictionary[trial_rankings[0]][0]+= 1
            tally_wins_dictionary[trial_rankings[1]][1] += 1
        for i in tally_wins_dictionary.keys():
            tally_probability[i] = (tally_wins_dictionary[i][0]/trials, tally_wins_dictionary[i][1]/trials)
        return tally_probability
    









        
        pass

    def get_ticket_EV(self, ticket_value:int, prob_first:float, prob_second:float)->float:
        '''Caclulates the Expected Value of a ticket

            Args:
                ticket_value (int): The value of a betting ticket if a camel comes in first place for a leg
                prob_first (float): The probability (0.0 - 1.0) that a camel will come in first place
                prob_second (float): The probability (0.0 - 1.0) that a camel will come in second place

            Return:
                float: The expected value of the ticket
        '''

        ## YOUR CODE GOES HERE
        ev = (ticket_value * prob_first) + (1 * prob_second) + ((1- (prob_first+prob_second))* -1)
        return ev
        pass

    def __str__(self) -> str:
        exper = self.run_experimental_analysis(10000)

        stats_str=" Experimental\n"
        analysis = [(self.STYLES[c]+c+Style.RESET_ALL, exper[c][0], exper[c][1])  for c in exper ]
        stats_str+="   1st   2nd\n"
        for row in analysis:
            stats_str+="{: >1} {: >5.2f} {: >5.2f}".format(*row)+"\n"

        advice_str="Available bets: "
        best_ev = -10
        best_camel = "x"
        for color in self.board.ticket_tents:
            tickets_left = self.board.ticket_tents[color]
            if len(tickets_left) > 0:
                top_ticket_value=tickets_left[0]
                ev = self.get_ticket_EV(top_ticket_value, exper[color][0], exper[color][1])
                if ev>best_ev:
                    best_ev=ev
                    best_camel=color
                advice_str += f"({color})"+self.STYLES[color]+str(top_ticket_value)+Style.RESET_ALL+f" EV:{ev:.2f} "
            else:
                advice_str += f"({color})"+self.STYLES[color]+"X"+Style.RESET_ALL+" "

        advice_str += "\nAI Advice: "
        if best_ev>1:
            advice_str+=f"  Bet on {self.STYLES[best_camel]+best_camel+Style.RESET_ALL} with an expected value of {best_ev:.2f}\n"
        else:
            advice_str+="  No camel has an EV > 1. You should roll instead of bet.\n"

        return stats_str + advice_str

if __name__ == "__main__":
    STYLES= {
            "r": Back.RED+Style.BRIGHT,
            "b": Back.BLUE+Style.BRIGHT,
            "g": Back.GREEN+Style.BRIGHT,
            "y": Back.YELLOW+Style.BRIGHT,
            "p": Back.MAGENTA
    }
    game_board = Board(STYLES)
    ai = AI(game_board)
    print(game_board)
    for _ in range(3):
        rolled_die=game_board.roll_die()
        game_board.move_camel(rolled_die)
    print(game_board)
    print(ai)
    print(game_board) #game state hasn't changed
