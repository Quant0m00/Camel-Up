from colorama import Fore, Back, Style, init

class Player:
    def __init__(self, name:str, camel_styles: dict[str, str]):
        self.money = 3
        self.bets = []
        self.name = name
        self.STYLES = camel_styles
        ## YOUR CODE GOES HERE

    def update_money(self, amount:int):
        """Update the player's money by the given amount
        Args:
            amount (int): the amount to update the player's money by
        """
        ## YOUR CODE GOES HERE
        self.money = self.money + amount
        pass

    def add_bet(self, ticket:tuple[str, int]):
        """Add a betting ticket to the player's bets
        Args:
            ticket (tuple): a tuple of the form (camel_color:str, value:int)
            Ex. ('g', 5)
        """
        ## YOUR CODE GOES HERE
        self.bets.append(ticket)
        pass

    def reset_leg(self):
        """Reset the player's bets at the end of a leg"""
        self.bets = []
        pass

    def __str__(self):
        player_string=f"\n{self.name} has {self.money} coins."
        if len(self.bets)>0:
            bets_string = " ".join([self.STYLES[bet[0]]+str(bet[1])+Style.RESET_ALL for bet in self.bets])
            player_string += f" Betting Tickets: {bets_string}"
        return player_string

if __name__ == "__main__":
    STYLES= {
            "r": Back.RED+Style.BRIGHT,
            "b": Back.BLUE+Style.BRIGHT,
            "g": Back.GREEN+Style.BRIGHT,
            "y": Back.YELLOW+Style.BRIGHT,
            "p": Back.MAGENTA
    }
    player = Player("Dave", STYLES)
    player.add_bet(('y', 5))
    player.add_bet(('b', 3))
    player.update_money(-1)
    print(player)
