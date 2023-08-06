import deck

class Card_Dict():
    suits_dict = {1: 'c', 2: 'd', 3: 'h', 4: 's'}
    ranks_dict = {1: '2', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: '10', 11: 'J', 12: 'Q', 13: 'K', 14: 'A'}

class Hand_Ranks():
    High_card, Pair, Two_pair, Trips, Straight, Flush, Boat, Quads, Straight_flush = range(1, 10)
    hand_ranks_dict = {1: 'high card', 2: 'pair', 3: 'two pair', 4: 'trips', 5: 'straight', 6: 'flush', 7: 'boat', 8: 'quads', 9: 'straight flush'}


class Holdem_rules():
    @staticmethod
    def check_consecutive(a, b):
        if a == (b - 1):
            return True
        else:
            return False
    #breaking off the inner for loop into a function. will return false if not consecutive. will need to use list splicing to tear off the last 5 items, middle 5 items, or first 5 items...
    #h = (hand_length - 5) cuz we count backwards from h to 0
    @staticmethod
    def straight_check(hand):
        this_hand = []
        for index, card in enumerate(hand):
            this_hand.append(hand[index].Rank)
        this_hand.sort()
        is_straight = False
        hand_length = len(hand)
        consecutive = 0
        h = (hand_length - 5)
        i = 0
        for j in range(h, -1, -1):
            consecutive = 0
            for i in range(0, 4):
                if Holdem_rules().check_consecutive(this_hand[i + j], this_hand[i + j + 1]) == True:
                    consecutive += 1
            if consecutive == 4:
                return (this_hand[j + 4])
                # since straights are always consecutive, no need for kickers
        return False

    #h = (hand_length - 5 + 1) cuz h ends the range)
    @staticmethod
    def flush_check(hand):
        suit_list = []
        for card in hand:
            suit_list.append(card.Suit)
        hand_length = len(hand)
        h = (hand_length - 5 + 1)
        for j in range(0, h):
            suitcount = suit_list.count(suit_list[j])
            if suitcount >= 5:
                flushlist = []
                for index, card in enumerate(hand):
                    if card.Suit == suit_list[j]:
                        flushlist.append(hand[index].Rank)
                flushcount = len(flushlist)
                flushlist.sort()
                flush_high_card = flushlist[flushcount - 1]
                flush_kickers = flushlist[0:(flushcount - 1)]
                suit = suit_list[j]
                return (flush_high_card, flush_kickers, {'suit': suit})
        return False

    #h = (hand_length - 5 + 2) because quads only needs to check 4 at a time, up to the 4th spot
    @staticmethod
    def quads_check(hand):
        hand_length = len(hand)
        h = (hand_length - 5 + 2)
        for i in range(0, h):
            if hand.count(hand[i].Rank) == 4:
                quads = hand[i].Rank
                kickers = []
                for card in hand:
                    if card.Rank != quads:
                        kickers.append(card.Rank)
                kickers.sort
                kicker = []
                kicker.append(kickers[hand_length - 5])
                return (hand[i], kicker)
        return False

    @staticmethod
    def straightflush_check(hand):
        if Holdem_rules().straight_check(hand):
            if Holdem_rules().flush_check(hand):
                flushlist = []
                flushsuit = Holdem_rules().flush_check(hand)[2]['suit']
                for index, card in enumerate(hand):
                    if card.Suit == flushsuit:
                        flushlist.append(hand[index])
                checked_straightflush = Holdem_rules().straight_check(flushlist)
                if checked_straightflush:
                    return (checked_straightflush, {'suit': flushsuit})
                else:
                    return False
                #flushcount = len(suit_list)
                #flushcount.sort()
                

    @staticmethod
    def royalflush_check(hand):
        results = Holdem_rules().straightflush_check(hand)
        if results[0] == 14:
            return (results[1])
        else:
            False
            
    @staticmethod
    def boat_check(hand):
        hand_length = len(hand)
        h = (hand_length - 5 + 3)
        this_hand = []
        for index, card in enumerate(hand):
            this_hand.append(hand[index].Rank)
        for i in range(0, h):
            if this_hand.count(this_hand[i]) == 3:
                trips = this_hand[i]
                for i in range(0, h+1):
                    if this_hand[i] != trips:
                        if this_hand.count(this_hand[i]) == 2:
                            pair = this_hand[i]
                            return (trips, pair)                
        return False
        
    @staticmethod
    def trips_check(hand):
        hand_length = len(hand)
        h = (hand_length - 5 + 3)
        this_hand = []
        for index, card in enumerate(hand):
            this_hand.append(hand[index].Rank)
        for i in range(0, h):
            if this_hand.count(this_hand[i]) == 3:
                kickers = []
                kicker_starter = []
                for card in this_hand:
                    kicker_starter.append(card)
                count = 0
                while count > 4:
                    try:
                        kicker_starter.remove(this_hand[i])
                        count += 1
                    except ValueError:
                        break
                kicker_starter.sort()
                length = len(kicker_starter)
                kickers.append(kicker_starter[length - 1])
                kickers.append(kicker_starter[length - 2])
                kickers.sort()
                return (this_hand[i], kickers)
        
    @staticmethod
    def twopair_check(hand):
        hand_length = len(hand)
        h = (hand_length - 5 + 4)
        this_hand = []
        for index, card in enumerate(hand):
            this_hand.append(hand[index].Rank)
        for i in range(0, h):
            if this_hand.count(this_hand[i]) == 2:
                pair1 = this_hand[i]
                for i in range(0, h):
                    if this_hand[i] != pair1:
                        if this_hand.count(this_hand[i]) == 2:
                            pair2 = this_hand[i]
                            if pair1 > pair2:
                                highest_pair = pair1
                                lowest_pair = pair2
                            else:
                                highest_pair = pair2
                                lowest_pair = pair1
                            kicker = []
                            for card in this_hand:
                                if card != pair1 and card != pair2:
                                    kicker.append(card)
                            kicker.sort()
                            length = len(kicker)
                            kicker.append(length - 1)
                            return (highest_pair, lowest_pair, kicker)                
        return False
        
        
    @staticmethod
    #need 3 kickers
    def pair_check(hand):
        hand_length = len(hand)
        h = (hand_length - 5 + 4)
        this_hand = []
        for index, card in enumerate(hand):
            this_hand.append(hand[index].Rank)
        for i in range(0, h):
            if this_hand.count(this_hand[i]) == 2:
                pair = this_hand[i]
                kickers_start = []
                for index, rank in enumerate(this_hand):
                    if rank != pair:
                        kickers_start.append(this_hand[index])
                kickers_start.sort()
                kickers = []
                kickers.append(kickers_start[hand_length - 3])
                kickers.append(kickers_start[hand_length - 4])
                kickers.append(kickers_start[hand_length - 5])
                kickers.sort()
                #print 'pair: %d, kickers: %s' % (pair, kickers)
                return (pair, kickers)
                
    @staticmethod
    def highcard_check(hand):
        hand_length = len(hand)
        high_card = (hand_length - 1)
        this_hand = []
        for index, card in enumerate(hand):
            this_hand.append(hand[index].Rank)
        this_hand.sort()
        start = (hand_length - 5)
        end = (hand_length - 1)
        kickers = this_hand[start:end]
        return (high_card, kickers)
        
                
    @staticmethod
    def evaluate_hand(player):

        hand = player.cards

        flush = Holdem_rules().flush_check(hand)
        if flush:
            straightflush = Holdem_rules().straightflush_check(hand)
            if straightflush:
                print "\n%s has a straight flush!" % player.screen_name
                return (9, straightflush[0], straightflush[1])

        quads = Holdem_rules().quads_check(hand)
        if quads:
            print "\n%s has quads!" % player.screen_name
            return (8, quads[0], quads[1])

        boat = Holdem_rules().boat_check(hand)
        if boat:
            print "\n%s has a boat!" % player.screen_name
            return (7, boat[0], boat[1])

        flush = Holdem_rules().flush_check(hand)
        if flush:
            print "\n%s has a flush!" % player.screen_name
            return (6, flush[0], flush[1], flush[2])

        straight = Holdem_rules().straight_check(hand)
        if straight:
            print "\n%s has a straight!" % player.screen_name
            return (5, straight)

        trips = Holdem_rules().trips_check(hand)
        if trips:
            print "\n%s has trips!" % player.screen_name
            return (4, trips[0], trips[1])

        twopair = Holdem_rules().twopair_check(hand)
        if twopair:
            print "\n%s has two pair!" % player.screen_name
            return (3, twopair[0], twopair[1], twopair[2])

        pair = Holdem_rules().pair_check(hand)
        if pair:
            print "\n%s has a pair!" % player.screen_name
            return (2, pair[0], pair[1])

        highcard = Holdem_rules().highcard_check(hand)
        print "\n%s has a highcard!" % player.screen_name
        return (1, highcard[0], highcard[1])            

    @staticmethod
    def make_hand_dict(player):
        return {'screen_name': player.screen_name, 'hand': player.cards}

    @staticmethod
    def make_hands_list(players):
        hands_list = []
        for player in players:
            hand_dict = Holdem_rules().make_hand_dict(player)
            hands_list.append(hand_dict)
        return hands_list


    #compare hands between multiple playesr
    @staticmethod
    def compare_hands(players):
        for player in players:
            player.hand_rank = Holdem_rules().evaluate_hand(player)
        hand_ranks = []
        for player in players:
            hand_ranks.append(player.hand_rank[0])
        hand_ranks.sort()
        handcount = len(hand_ranks)
        end = (handcount - 1)
        high_hand = hand_ranks[end]
        print '\nhigh hand: %s\n' % Hand_Ranks().hand_ranks_dict[high_hand]
        contenders = []
        winners = []
        for player in players:
            if player.hand_rank[0] == high_hand:
                contenders.append(player)
        if len(contenders) == 1:
            winners.append(contenders[0])
            return winners
        else:
        #else, if there are more than 1 person with same type of hand but we dont know who won
            #check high card
            if high_hand == 1:
                end_of_list = len(contenders) - 1
                remaining_ranks = []
                leading_rank = None
                for player in contenders:
                    remaining_ranks.append(player.hand_rank[1])
                remaining_ranks.sort()
                leading_rank = remaining_ranks[end_of_list]
                contenders_2 = []
                for player in contenders:
                    if player.hand_rank[1] == leading_rank:
                        contenders_2.append(player)
                if contenders_2 == 1:
                    winners.append(contenders_2[0])
                    return winners
                else:
                #if the highcard ties evaluate highest kicker
                    end_of_list = len(contenders_2) - 1
                    remaining_ranks = []
                    leading_rank = None
                    for player in contenders_2:
                        remaining_ranks.append(player.hand_rank[2][3])
                    remaining_ranks.sort()
                    leading_rank = remaining_ranks[end_of_list]
                    contenders_3 = []
                    for player in contenders_2:
                        if player.hand_rank[2][3] == leading_rank:
                            contenders_3.append(player)
                    if contenders_3 == 1:
                        winners.append(contenders_3[0])
                        return winners
                    else:
                    #if the highest kicker ties evaluate second highest kicker
                        end_of_list = len(contenders_3) - 1
                        remaining_ranks = []
                        leading_rank = None
                        for player in contenders_3:
                            remaining_ranks.append(player.hand_rank[2][2])
                        remaining_ranks.sort()
                        leading_rank = remaining_ranks[end_of_list]
                        contenders_4 = []
                        for player in contenders_3:
                            if player.hand_rank[2][2] == leading_rank:
                                contenders_4.append(player)
                        if contenders_4 == 1:
                            winners.append(contenders_4[0])
                            return winners
                        else:
                        #if the second highest kicker ties evaluate third highest kicker
                            end_of_list = len(contenders_4) - 1
                            remaining_ranks = []
                            leading_rank = None
                            for player in contenders_4:
                                remaining_ranks.append(player.hand_rank[2][1])
                            remaining_ranks.sort()
                            leading_rank = remaining_ranks[end_of_list]
                            contenders_5 = []
                            for player in contenders_5:
                                if player.hand_rank[2][1] == leading_rank:
                                    contenders_5.append(player)
                            if contenders_5 == 1:
                                winners.append(contenders_5[0])
                                return winners
                            else:
                            #if the third highest kicker ties evaluate lowest kicker
                                end_of_list = len(contenders_5) - 1
                                remaining_ranks = []
                                leading_rank = None
                                for player in contenders_5:
                                    remaining_ranks.append(player.hand_rank[2][0])
                                remaining_ranks.sort()
                                leading_rank = remaining_ranks[end_of_list]
                                contenders_6 = []
                                for player in contenders_6:
                                    if player.hand_rank[2][0] == leading_rank:
                                        contenders_6.append(player)
                                winners = contenders_6
                                return winners


            #check a pair
            elif high_hand == 2:
                end_of_list = len(contenders) - 1
                remaining_ranks = []
                leading_rank = None
                for player in contenders:
                    remaining_ranks.append(player.hand_rank[1])
                remaining_ranks.sort()
                leading_rank = remaining_ranks[end_of_list]
                contenders_2 = []
                for player in contenders:
                    if player.hand_rank[1] == leading_rank:
                        contenders_2.append(player)
                if len(contenders_2) == 1:
                    winners = contenders_2
                    return winners
                else:
                #if the pair ties evaluate highest kicker
                    end_of_list = len(contenders_2) - 1
                    remaining_ranks = []
                    leading_rank = None
                    for player in contenders_2:
                        remaining_ranks.append(player.hand_rank[2][2])
                    remaining_ranks.sort()
                    leading_rank = remaining_ranks[end_of_list]
                    contenders_3 = []
                    for player in contenders_2:
                        if player.hand_rank[2][2] == leading_rank:
                            contenders_3.append(player)
                    if contenders_3 == 1:
                        winners.append(contenders_3[0])
                        return winners
                    else:
                    #if the highest kicker ties evaluate middle kicker
                        end_of_list = len(contenders_3) - 1
                        remaining_ranks = []
                        leading_rank = None
                        for player in contenders_3:
                            remaining_ranks.append(player.hand_rank[2][1])
                        remaining_ranks.sort()
                        leading_rank = remaining_ranks[end_of_list]
                        contenders_4 = []
                        for player in contenders_3:
                            if player.hand_rank[2][1] == leading_rank:
                                contenders_4.append(player)
                        if contenders_4 == 1:
                            winners.append(contenders_4[0])
                            return winners
                        else:
                        #if the second highest kicker ties evaluate lowest kicker
                            end_of_list = len(contenders_4) - 1
                            remaining_ranks = []
                            leading_rank = None
                            for player in contenders_4:
                                remaining_ranks.append(player.hand_rank[2][0])
                            remaining_ranks.sort()
                            leading_rank = remaining_ranks[end_of_list]
                            contenders_5 = []
                            for player in contenders_5:
                                if player.hand_rank[2][0] == leading_rank:
                                    contenders_5.append(player)
                            winners = contenders_5
                            return winners

            
            #check 2 pair
            elif high_hand == 3:
                end_of_list = len(contenders) - 1
                remaining_ranks = []
                leading_rank = None
                for player in contenders:
                    remaining_ranks.append(player.hand_rank[1])
                remaining_ranks.sort()
                leading_rank = remaining_ranks[end_of_list]
                contenders_2 = []
                for player in contenders:
                    if player.hand_rank[1] == leading_rank:
                        contenders_2.append(player)
                if contenders_2 == 1:
                    winners.append(contenders_2[0])
                    return winners
                else:
                #if the higher pair ties evaluate lower pair
                    end_of_list = len(contenders_2) - 1
                    remaining_ranks = []
                    leading_rank = None
                    for player in contenders_2:
                        remaining_ranks.append(player.hand_rank[2])
                    remaining_ranks.sort()
                    leading_rank = remaining_ranks[end_of_list]
                    contenders_3 = []
                    for player in contenders_2:
                        if player.hand_rank[2] == leading_rank:
                            contenders_3.append(player)
                    if contenders_3 == 1:
                        winners.append(contenders_3[0])
                        return winners
                    else:
                    #if both pairs tie evaluate the kicker
                        end_of_list = len(contenders_3) - 1
                        remaining_ranks = []
                        leading_rank = None
                        for player in contenders_3:
                            remaining_ranks.append(player.hand_rank[3])
                        remaining_ranks.sort()
                        leading_rank = remaining_ranks[end_of_list]
                        contenders_4 = []
                        for player in contenders_3:
                            if player.hand_rank[3] == leading_rank:
                                contenders_4.append(player)
                        winners = contenders_4
                        return winners
                

            #check trips
            elif high_hand == 4:
                end_of_list = len(contenders) - 1
                remaining_ranks = []
                leading_rank = None
                for player in contenders:
                    remaining_ranks.append(player.hand_rank[1])
                remaining_ranks.sort()
                leading_rank = remaining_ranks[end_of_list]
                contenders_2 = []
                for player in contenders:
                    if player.hand_rank[1] == leading_rank:
                        contenders_2.append(player)
                if contenders_2 == 1:
                    winners.append(contenders_2[0])
                    return winners
                else:
                #if the trips ties evaluate higher kicker
                    end_of_list = len(contenders_2) - 1
                    remaining_ranks = []
                    leading_rank = None
                    for player in contenders_2:
                        remaining_ranks.append(player.hand_rank[2][1])
                    remaining_ranks.sort()
                    leading_rank = remaining_ranks[end_of_list]
                    contenders_3 = []
                    for player in contenders_2:
                        if player.hand_rank[2][1] == leading_rank:
                            contenders_3.append(player)
                    if contenders_3 == 1:
                        winners.append(contenders_3[0])
                        return winners
                    else:
                    #if the higher kicker ties evaluate lower kicker
                        end_of_list = len(contenders_3) - 1
                        remaining_ranks = []
                        leading_rank = None
                        for player in contenders_3:
                            remaining_ranks.append(player.hand_rank[2][0])
                        remaining_ranks.sort()
                        leading_rank = remaining_ranks[end_of_list]
                        contenders_4 = []
                        for player in contenders_3:
                            if player.hand_rank[2][0] == leading_rank:
                                contenders_4.append(player)
                        winners = contenders_4
                        return winners


            #check straights
            elif high_hand == 5:
                end_of_list = len(contenders) - 1
                remaining_ranks = []
                leading_rank = None
                for player in contenders:
                    remaining_ranks.append(player.hand_rank[1])
                remaining_ranks.sort()
                leading_rank = remaining_ranks[end_of_list]
                contenders_2 = []
                for player in contenders:
                    if player.hand_rank[1] == leading_rank:
                        contenders_2.append(player)
                winners = contenders_2
                return winners


            #check flush
            if high_hand == 6:
                end_of_list = len(contenders) - 1
                remaining_suits = []
                leading_suit = None
                for player in contenders:
                    remaining_ranks.append(player.hand_rank[3]['suit'])
                remaining_suits.sort()
                leading_suit = remaining_suits(end_of_list)
                suit_contenders = []
                for player in contenders:
                    if player.hand_rank[3]['suit'] == leading_suit:
                        suit_contenders.append(player)
                if suit_contenders == 1:
                    winners.append(suit_contenders[0])
                    return winners
                else:
                    #if the suit ties check highcard of flush
                    end_of_list = len(suit_contenders) - 1
                    remaining_ranks = []
                    leading_rank = None
                    for player in suit_contenders:
                        remaining_ranks.append(player.hand_rank[1])
                    remaining_ranks.sort()
                    leading_rank = remaining_ranks[end_of_list]
                    contenders_2 = []
                    for player in suit_contenders:
                        if player.hand_rank[1] == leading_rank:
                            contenders_2.append(player)
                    if contenders_2 == 1:
                        winners.append(contenders_2[0])
                        return winners
                    else:
                        #if the flush ties evaluate highest kicker
                        end_of_list = len(contenders_2) - 1
                        remaining_ranks = []
                        leading_rank = None
                        for player in contenders_2:
                            remaining_ranks.append(player.hand_rank[2][3])
                        remaining_ranks.sort()
                        leading_rank = remaining_ranks[end_of_list]
                        contenders_3 = []
                        for player in contenders_2:
                            if player.hand_rank[2][3] == leading_rank:
                                contenders_3.append(player)
                        if contenders_3 == 1:
                            winners.append(contenders_3[0])
                            return winners
                        else:
                            #if the highest kicker ties evaluate second highest kicker
                            end_of_list = len(contenders_3) - 1
                            remaining_ranks = []
                            leading_rank = None
                            for player in contenders_3:
                                remaining_ranks.append(player.hand_rank[2][2])
                            remaining_ranks.sort()
                            leading_rank = remaining_ranks[end_of_list]
                            contenders_4 = []
                            for player in contenders_3:
                                if player.hand_rank[2][2] == leading_rank:
                                    contenders_4.append(player)
                            if contenders_4 == 1:
                                winners.append(contenders_4[0])
                                return winners
                            else:
                                #if the second highest kicker ties evaluate third highest kicker
                                end_of_list = len(contenders_4) - 1
                                remaining_ranks = []
                                leading_rank = None
                                for player in contenders_4:
                                    remaining_ranks.append(player.hand_rank[2][1])
                                remaining_ranks.sort()
                                leading_rank = remaining_ranks[end_of_list]
                                contenders_5 = []
                                for player in contenders_5:
                                    if player.hand_rank[2][1] == leading_rank:
                                        contenders_5.append(player)
                                if contenders_5 == 1:
                                    winners.append(contenders_5[0])
                                    return winners
                                else:
                                #if the third highest kicker ties evaluate lowest kicker
                                    end_of_list = len(contenders_5) - 1
                                    remaining_ranks = []
                                    leading_rank = None
                                    for player in contenders_5:
                                        remaining_ranks.append(player.hand_rank[2][0])
                                    remaining_ranks.sort()
                                    leading_rank = remaining_ranks[end_of_list]
                                    contenders_6 = []
                                    for player in contenders_6:
                                        if player.hand_rank[2][0] == leading_rank:
                                            contenders_6.append(player)
                                    winners = contenders_6
                                    return winners


            #check boat
            elif high_hand == 7:
                end_of_list = len(contenders) - 1
                remaining_ranks = []
                leading_rank = None
                for player in contenders:
                    remaining_ranks.append(player.hand_rank[1])
                remaining_ranks.sort()
                leading_rank = remaining_ranks[end_of_list]
                contenders_2 = []
                for player in contenders:
                    if player.hand_rank[1] == leading_rank:
                        contenders_2.append(player)
                if contenders_2 == 1:
                    winners.append(contenders_2[0])
                    return winners
                else:
                #if the trips ties evaluate the pair
                    end_of_list = len(contenders_2) - 1
                    remaining_ranks = []
                    leading_rank = None
                    for player in contenders_2:
                        remaining_ranks.append(player.hand_rank[2])
                    remaining_ranks.sort()
                    leading_rank = remaining_ranks[end_of_list]
                    contenders_3 = []
                    for player in contenders_2:
                        if player.hand_rank[2] == leading_rank:
                            contenders_3.append(player)
                    winners = contenders_3
                    return winners


            #check quads
            elif high_hand == 8:
                end_of_list = len(contenders) - 1
                remaining_ranks = []
                leading_rank = None
                for player in contenders:
                    remaining_ranks.append(player.hand_rank[1])
                remaining_ranks.sort()
                leading_rank = remaining_ranks[end_of_list]
                contenders_2 = []
                for player in contenders:
                    if player.hand_rank[1] == leading_rank:
                        contenders_2.append(player)
                if contenders_2 == 1:
                    winners.append(contenders_2[0])
                    return winners
                else:
                #if the quads ties evaluate the kicker
                    end_of_list = len(contenders_2) - 1
                    remaining_ranks = []
                    leading_rank = None
                    for player in contenders_2:
                        remaining_ranks.append(player.hand_rank[2])
                    remaining_ranks.sort()
                    leading_rank = remaining_ranks[end_of_list]
                    contenders_3 = []
                    for player in contenders_2:
                        if player.hand_rank[2] == leading_rank:
                            contenders_3.append(player)
                    winners = contenders_3
                    return winners



            #check straightflush
            if high_hand == 9:
                end_of_list = len(contenders) - 1
                remaining_suits = []
                leading_suit = None
                for player in contenders:
                    remaining_ranks.append(player.hand_rank[2]['suit'])
                remaining_suits.sort()
                leading_suit = remaining_suits(end_of_list)
                suit_contenders = []
                for player in contenders:
                    if player.hand_rank[2]['suit'] == leading_suit:
                        suit_contenders.append(hand)
                if suit_contenders == 1:
                    winners.append(suit_contenders[0])
                    return winners
                else:
                    #if the suit ties check highcard of straightflush
                    end_of_list = len(suit_contenders) - 1
                    remaining_ranks = []
                    leading_rank = None
                    for player in suit_contenders:
                        remaining_ranks.append(player.hand_rank[1])
                    remaining_ranks.sort()
                    leading_rank = remaining_ranks[end_of_list]
                    contenders_2 = []
                    for player in suit_contenders:
                        if player.hand_rank[1] == leading_rank:
                            contenders_2.append(player)
                    winners = contenders_2
                    return winners


















