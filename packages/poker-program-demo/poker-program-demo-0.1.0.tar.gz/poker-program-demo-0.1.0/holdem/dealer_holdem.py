import deck

class Dealer():

    suits_dict = {1: 'c', 2: 'd', 3: 'h', 4: 's'}
    ranks_dict = {1: '2', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: '10', 11: 'J', 12: 'Q', 13: 'K', 14: 'A'}

    
    @staticmethod
    def deal_player_hand(players, deck):
        deck.shuffle()
        print 'dealing hands'
        dealt = 0
        while dealt < 2:
            for player in players:
                player.cards.append(deck.draw())
            dealt += 1

    @staticmethod
    def deal_omaha_hand(players, deck):
        deck.shuffle()
        print 'dealing hands'
        dealt = 0
        while dealt < 4:
            for player in players:
                player.cards.append(deck.draw())
            dealt += 1
        for player in players:
            print player.cards


    @staticmethod
    def deal_flop(deck):
        board = []
        flopcards = 0
        while flopcards < 3:
            board.append(deck.draw())
            flopcards += 1
        return board
        
    @staticmethod
    def deal_turn(deck, board):
        board.append(deck.draw())
        return board

    @staticmethod
    def deal_river(deck, board):
        board.append(deck.draw())
        return board


    @staticmethod
    def combine_hand_with_board(board, players):
        pass
