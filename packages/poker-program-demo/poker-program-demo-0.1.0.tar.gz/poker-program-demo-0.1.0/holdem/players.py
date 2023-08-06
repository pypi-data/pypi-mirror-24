
class Player():
    def __init__(self, screen_name, chips):
        self.screen_name = screen_name
        self.starting_chips = int(chips)
        self.chips = int(chips)
        self.cards = []
        self.current_investment = 0
        self.current_bet = 0
        self.has_hand = False
        self.all_in = False
        self.checked = False
        self.small_blind = False
        self.big_blind = False
        self.hand_rank = None
        self.seat = None
        self.omaha_high_hand = None

    def deduct(self, chips):
        self.chips -= chips
        
    def award(self, chips):
        self.chips += chips
    

