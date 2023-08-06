#4 = spades
#3 = hearts
#2 = diamonds
#1 = clubs

import random, time


class Suit():
 Clubs, Diamonds, Hearts, Spades = range(1,5)
 
 
class Card():
 Suit = None
 Rank = None
 
 def __init__(self, suit, rank):
  self.Suit = suit
  self.Rank = rank

# deck adds 52 cards per instance to the actual deck class-
# newdeck = Deck() 52
# newdeck2 = Deck() 104 and so on

#nvm bug fixed by removing cards_list from class level and hiding it in init

class Deck():
    def __init__(self):
        self.cards_list = []
        for i in range(2,15):
            new_card = Card(Suit.Spades, i)
            self.cards_list.append(new_card)
            new_card = Card(Suit.Hearts, i)
            self.cards_list.append(new_card)
            new_card = Card(Suit.Diamonds, i)
            self.cards_list.append(new_card)
            new_card = Card(Suit.Clubs, i)
            self.cards_list.append(new_card)

        self.deck_length = len(self.cards_list)

    #debug only
    def debugdeck(self):
        for index, card in enumerate(self.cards_list):
            print (self.cards_list[index].Suit)
            print (self.cards_list[index].Rank)
        
    def _swap(self, i, j):
        temp = self.cards_list[i]
        self.cards_list[i] = self.cards_list[j]
        self.cards_list[j] = temp


    def shuffle(self):
        print 'shufflin!'
        start_time = time.clock()
        shuffles = 0
        while shuffles < 50:
            for i in range(0, 52):
                j = self.get_random()
                self._swap(i, j)
            shuffles +=1
        end_time = (time.clock() - start_time)
        print "%f seconds" % end_time


    def get_random(self):
        return int((random.SystemRandom(random.seed()).random())*51)

    #draws a card off the 'top' of the deck (the end of the list of cards)
    def draw(self):
        return self.cards_list.pop()

    #draw a certain card
    def select(self, a):
        return self.cards_list.pop(a)
        
    #this method picks a card, but doesn't actually remove it from the deck
    def pick(self, a):
        return self.cards_list[a]
        
  

  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
