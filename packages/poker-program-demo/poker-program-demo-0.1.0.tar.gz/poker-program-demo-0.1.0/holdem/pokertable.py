class Table():
    def __init__(self, players_list, big_blind, small_blind, button):
        self.players_list = players_list
        self.big_blind = big_blind
        self.small_blind = small_blind
        self.button = button
 

    def add_players(self, player):
        self.players_list.append(player)
        
    def move_button(self):
        self.button += 1
        
    def retrieve_button(self):
        pass
