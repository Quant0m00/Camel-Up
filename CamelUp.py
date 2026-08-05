from colorama import Fore, Back, Style, init
import copy
try:
    from Board import Board
except ModuleNotFoundError:
    print("Board.py is not found.")
    pass
try:
    from Player import Player
except ModuleNotFoundError:
    print("Player.py is not found.")
    pass
try:
    from AI import AI
except ModuleNotFoundError:
    print("AI.py is not found.")
    pass

class CamelUp:
    def __init__(self, camel_styles:dict[str, str], player_list:list[Player]):
        self.STYLES = camel_styles
        self.board = Board(self.STYLES)
        self.players = player_list
        self.ai = AI(self.board) #Comment this line in once AI is implemented
        pass

    def get_player_move(self, player:Player):
        print(f"{player.name}-", end =" ")
        choice = "not_an_option"
        while choice.lower() not in ["b", "r", "a"]:
            choice = input("(B)et or (R)oll or (A)dvice? ").lower()
        return choice

    def get_player_bet(self):
        available_tickets="Available bets: "
        for color in self.board.ticket_tents:
            tickets_left = self.board.ticket_tents[color]
            if len(tickets_left) > 0:
                top_ticket_value=tickets_left[0]
                available_tickets += f"({color})"+self.STYLES[color]+str(top_ticket_value)+Style.RESET_ALL+" "
            else:
                available_tickets += f"({color})"+self.STYLES[color]+"X"+Style.RESET_ALL+" "
        print(available_tickets)

        ticket_color = "not_an_option"
        while ticket_color.lower() not in self.STYLES.keys() or len(self.board.ticket_tents[ticket_color])<=0:
            ticket_color = input("Which betting ticket would you like to take?\n").lower()

        return ticket_color.lower()

    def play_leg(self):
        # You will need to modify this method (it is only partially completed)
        curr_player = 0
        while not self.board.is_leg_finished():
            player = self.players[curr_player]
            move = 'x'
            while move not in ['r', 'b']:
                move = self.get_player_move(player)
                match move:
                    case "r":
                        # TODO
                        die_roll = self.board.roll_die()
                        self.board.move_camel(die_roll)
                        player.update_money(1)
                        pass
                    case "b":
                        # TODO
                        color = self.get_player_bet()
                        bet = self.board.take_ticket(color)
                        player.add_bet(bet)
                        pass
                    case "a":
                        #print("AI is not implemented yet!") #Comment this line out once AI is implemented
                        print(self.ai) #Comment this line in once AI is implemented

            print(self)
            curr_player = (curr_player + 1) % 2

    def process_leg_payouts(self):
        """Process the payouts for the end of a leg, which includes determing first and second place camels
        and updating player money based on their bets. First place gets the value of their ticket, second place
        gets $1, and all other bets lose $1.

        Returns:
            tuple: a tuple of the form (first:str, second:str)
            where first is the color (letter) of the winning camel and second is the color (letter) of the second place camel
            ex. ("b","y")
        """
        ## YOUR CODE GOES HERE
        rankings = self.board.get_rankings()
        for player in self.players:
            for bet in player.bets:
                if bet[0] == rankings[0]:
                    player.update_money(bet[1])

                elif bet[0] == rankings[1]:
                    player.update_money(1)
                else: 
                    player.update_money(-1)
        return rankings
        
    
    

    
        pass

    def __str__(self):
        game_str = str(self.board)
        for player in self.players:
            game_str += str(player)+"\n"
        return game_str

if __name__ == "__main__":
    STYLES= {
            "r": Back.RED+Style.BRIGHT,
            "b": Back.BLUE+Style.BRIGHT,
            "g": Back.GREEN+Style.BRIGHT,
            "y": Back.YELLOW+Style.BRIGHT,
            "p": Back.MAGENTA
    }
    player1 = Player("Dave", STYLES)
    player2 = Player("Sasha", STYLES)
    game = CamelUp(STYLES, [player1, player2])
    print(game)
    game.play_leg()
    first, second = game.process_leg_payouts()

    print(f"{game.STYLES[first]}{first}{Style.RESET_ALL} comes in 1st🥇🥇🥇!")
    print(f"{game.STYLES[second]}{second}{Style.RESET_ALL} comes in 2nd🥈🥈🥈!")

    for player in game.players:
        print(f"{player.name} ended the leg with {player.money} coins.")
