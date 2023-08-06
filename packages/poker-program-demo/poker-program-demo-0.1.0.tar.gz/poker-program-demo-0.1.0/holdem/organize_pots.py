class Organize_Pots():
    @staticmethod
    def organize_pots(bet, current_player, table_pots, players_at_table):

        pots = table_pots

        pot_counter = 0
        #print '\nBeginning "organize_pot"...'
        #print '\nthe bet: %d' % bet
        #print '\nthe current player: %s' % current_player.screen_name
        #for pot in pots:
        #    print 'Pot %d:' % (pot_counter + 1)
        #    print 'Pot size: %d' % pots[pot_counter]['pot']
         #   print 'Bet to match for this pot: %d' % pots[pot_counter]['match']
         #   print 'Any all in? %s' % pots[pot_counter]['any_all_in']
         #   pot_counter += 1

        bets_to_match = []
        for pot in pots:
            bets_to_match.append(pot['match'])

        highest_pot = len(pots) - 1

        different_bet = True


        bet_increase = bet - current_player.current_bet
        print 'Bet increase: %d' % bet_increase

        new_current_investment = bet_increase + current_player.current_investment 
        print 'New current investment: %d' % new_current_investment

        current_player.current_investment += bet_increase
        print 'current player\'s investment: %d' % current_player.current_investment

        current_player.current_bet = bet
        print 'Current player\'s new current bet: %d' % current_player.current_bet

        current_player.chips -= bet_increase
        print 'player chips before testing for all in: %d' % current_player.chips
        if current_player.chips == 0:
            current_player.all_in = True

        for index, pot in enumerate(pots):
            if new_current_investment == pots[index]['match']:
                different_bet = False

        #determine if we need to insert a new pot
        if different_bet == True:
            if new_current_investment > pots[highest_pot]['match']:
                if pots[highest_pot]['any_all_in'] == False:
                    pots[highest_pot]['match'] = new_current_investment
                    if current_player.all_in == True:
                        pots[highest_pot]['any_all_in'] = True                        
                elif pots[highest_pot]['any_all_in'] == True:
                    pots.append({'pot': 0, 'match': new_current_investment, 'any_all_in': False})
                    if current_player.all_in == True:
                        #the new highest pot is this one
                        pots[highest_pot + 1]['any_all_in'] = True
            elif new_current_investment < pots[highest_pot]['match']:
                for index, pot in enumerate(pots):
                    print 'index: %d, pot: %s' % (index, pot)
                    if new_current_investment < pots[index]['match']:
                        pots.insert((index), {'pot': 0, 'match': new_current_investment, 'any_all_in': True})
                        break

        #reorganize/correct the chip total for pots
        for index, pot in enumerate(pots): 
            pots[index]['pot'] = 0
            pot_total = 0
            for player in players_at_table:
                if index == 0:
                    if player.current_investment >= pots[index]['match']:
                        pot_total += pots[index]['match']
                    elif player.current_investment < pots[index]['match']:
                        pot_total += player.current_investment
                elif index > 0:
                    if player.current_investment <= pots[index - 1]['match']:
                        continue
                    elif player.current_investment > pots[index - 1]['match']:
                        if player.current_investment >= pots[index]['match']:
                            pot_total += pots[index]['match'] - pots[index -1]['match']
                        elif player.current_investment < pots[index]['match']:
                            pot_total += player.current_investment - pots[index -1]['match']
            pots[index]['pot'] = pot_total
            

        print 'Ending "organize_pot"...'
        pot_counter = 0
        for pot in pots:
            print 'Pot %d:' % (pot_counter + 1)
            print 'Pot size: %d' % pots[pot_counter]['pot']
            print 'Bet to match for this pot: %d' % pots[pot_counter]['match']
            print 'Any all in? %s' % pots[pot_counter]['any_all_in']
            pot_counter += 1
        return (pots)

