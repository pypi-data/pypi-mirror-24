import deck
import pokertable
import players
import dealer_holdem
import rules_holdem
import time

cody = players.Player('cody4321', 1500)
darren = players.Player('d_money', 1500)
table_players = [cody, darren]
newtable = pokertable.Table(table_players, 20, 10, 0)

players_list = newtable.players_list
button = 0
big_blind = 20
small_blind = 10

suits_dict = {1: 'c', 2: 'd', 3: 'h', 4: 's'}

ranks_dict = {1: '2', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: '10', 11: 'J', 12: 'Q', 13: 'K', 14: 'A'}

ranks_spaces = {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1, 10: 0, 11: 1, 12: 1, 13: 1, 14: 1}

newdeck = deck.Deck()
newdeck.shuffle()


def starter():
    newdeck = deck.Deck()
    newdeck.shuffle()



print ('"newdeck" has been generated and shuffled \n')


class Test():
    @staticmethod
    def determine_total_chipcount(players):
        total_chipcount = 0
        for player in players:
            total_chipcount += player.chips
        return total_chipcount


    @staticmethod
    #check that chips are the same as the game started, not higher or lower
    def ensure_chipcount(players, total_chipcount):
        actual_chipcount = 0
        for player in players:
            actual_chipcount += player.chips
        if not actual_chipcount == total_chipcount:
            print 'We are missing chips?!?!'
            raise AssertionError
        print '\nIn tests.py...Chipcount is clear\n'
        time.sleep(6)






    @staticmethod
    def viewdeck(deck):
        for index, card in enumerate(deck.cards_list):
        
            if len(str(index)) == 2:
                indexspaces = ''
            else:
                indexspaces = ' '
            s = ' '
            spaces = s * ranks_spaces[card.Rank]
            
            print ('Index %d: ' % index, '%s' % indexspaces, '%s%s' % (ranks_dict[card.Rank], spaces), suits_dict[card.Suit], '\n')
    
    
    @staticmethod
    def viewhand(hand):
        for index, card in enumerate(hand):
            print ('%s%s' % (card.Rank, suits_dict[card.Suit]))
            
            
    @staticmethod
    def deal_straight_flush(deck):
        myhand = []
        for index, card in enumerate(deck.cards_list):
            if card.Rank == 7 and card.Suit == 4:
                 myhand.append(deck.pick(index))
            if card.Rank == 9 and card.Suit == 4:
                 myhand.append(deck.pick(index))
            if card.Rank == 10 and card.Suit == 4:
                 myhand.append(deck.pick(index))
            if card.Rank == 11 and card.Suit == 4:
                 myhand.append(deck.pick(index))
            if card.Rank == 8 and card.Suit == 4:
                 myhand.append(deck.pick(index))
        print (myhand)
        return myhand
        
        
    @staticmethod
    def deal_boat(deck):
        myhand = []
        trips = 0
        index1 = 0
        while trips < 3:
            if deck.cards_list[index1].Rank == 7:
                myhand.append(deck.pick(index1))
                trips += 1
            index1 += 1

        pair = 0
        index2 = 0
        while pair < 2:
            if deck.cards_list[index2].Rank == 5:
                myhand.append(deck.pick(index2))
                pair += 1
            index2 += 1
        return myhand

    @staticmethod
    def deal_trips(deck):
        myhand = []
        trips = 0
        index1 = 0
        while trips < 3:
            if deck.cards_list[index1].Rank == 7:
                myhand.append(deck.pick(index1))
                trips += 1
            index1 += 1
        while count < 4:
            index = 49
            myhand.append(deck.pick(index))
            index -= 1
            count += 1
        return myhand
          
          
    @staticmethod
    def deal_twopair(deck):
        myhand = []
        pair1 = 0
        index1 = 0
        while pair1 < 2:
            if deck.cards_list[index1].Rank == 7:
                myhand.append(deck.pick(index1))
                pair1 += 1
            index1 += 1
        pair2 = 0
        index2 = 0
        while pair2 < 2:
            if deck.cards_list[index2].Rank == 5:
                myhand.append(deck.pick(index2))
                pair2 += 1
            index2 += 1
        index3 = 0
        while len(myhand) < 5:
            if deck.cards_list[index3].Rank == 9:
                myhand.append(deck.pick(index3))
            index3 += 1
        print (myhand)
        return myhand
            
    @staticmethod
    def deal_pair(deck):
        myhand = []
        pair1 = 0
        index1 = 0
        while pair1 < 2:
            if deck.cards_list[index1].Rank == 7:
                myhand.append(deck.pick(index1))
                pair1 += 1
            index1 += 1
        index2 = 0
        kicker1 = None
        while not kicker1:
            if deck.cards_list[index2].Rank == 9:
                myhand.append(deck.pick(index2))
                kicker1 = 1
            index2 += 1
        index3 = 0
        kicker2 = None
        while not kicker2:
            if deck.cards_list[index3].Rank == 4:
                myhand.append(deck.pick(index3))
                kicker2 = 1
            index3 += 1
        index4 = 0
        kicker3 = None
        while not kicker3:
            if deck.cards_list[index4].Rank == 12:
                myhand.append(deck.pick(index4))
                kicker3 = 1
            index4 += 1
        return myhand
        

    @staticmethod
    def test_awards(players, chips):
        for player in players:
            player.award(chips)
     

       
#view = Test().viewdeck(newdeck)

# straightflush_check works!!!
#myhandstr8flush = Test().deal_straight_flush(newdeck)
#print ('myhandstr8flush:')
#viewmyhand = Test().viewhand(myhandstr8flush)

#myhand2pair = Test().deal_twopair(newdeck)
#print ('myhand2pair:')
#viewmyhand = Test().viewhand(myhand2pair)

#myhandboat = Test().deal_boat(newdeck)
#print ('myhandboat:')
#viewmyhand = Test().viewhand(myhandboat)

#myhandpair = Test().deal_pair(newdeck)
#print ('myhandpair:')
#viewmyhand = Test().viewhand(myhandpair)

#Test().test_awards(players_list, 20)

#print (cody.chips)

#print (darren.chips)
# to view the deck:
# tests.Test().viewdeck(tests.newdeck)
