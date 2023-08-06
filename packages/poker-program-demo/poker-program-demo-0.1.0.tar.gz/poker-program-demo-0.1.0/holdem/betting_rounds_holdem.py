
import time

import organize_pots

class Ranks():
    suits_dict = {1: 'c', 2: 'd', 3: 'h', 4: 's'}
    ranks_dict = {1: '2', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: '10', 11: 'J', 12: 'Q', 13: 'K', 14: 'A'}



class Betting_Rounds():
#forced bet is like big blind, what everyone pays. after the flop, forced bet is 0, but there's still a minimum bet (usually the big blind, or 2x BB)
    @staticmethod
    def betting_round_preflop(players, forced_bet, minimum_bet, current_pots, big_blind):

        pots = current_pots

        big_blind_checked = False

        amount_of_players_remaining = len(players)

        pots = current_pots
        players_list = players
        print '\nstarting betting round!!!'
        current_bet = forced_bet
        raise_amount = 0
        required_raise = 0
        if minimum_bet > 0 and forced_bet == 0:
            required_raise = minimum_bet
        else:
            required_raise = 2 * forced_bet
         
        old_bet = 0

        while True:
            for index, player in enumerate(players):
                if player.chips == 0:
                    player.all_in = True

                owe = current_bet - player.current_bet
                if owe == 0 and player.checked == True:
                    continue

                if player.has_hand == False:
                    continue
                
                #user interaction: for each player's turn, give info
                print ('\nOn %s, %d chips' % (player.screen_name, player.chips))
                print ('Your cards are: %s%s, %s%s' % (Ranks().ranks_dict[player.cards[0].Rank], Ranks().suits_dict[player.cards[0].Suit], Ranks().ranks_dict[player.cards[1].Rank], Ranks().suits_dict[player.cards[1].Suit]))
                print 'Is all in? : %s' % player.all_in
                print 'Current bet: %s' % player.current_bet
                print 'Current investment: %s' % player.current_investment
                print 'Has hand? : %s' % player.has_hand
                print 'Checked? : %s' % player.checked
                print 'The current bet is %d' % current_bet
                print ('The current raise is: %d' % raise_amount)
                print ('The required raise is: %d' % required_raise)
                print 'Your current bet is %d' % player.current_bet
                print 'You owe: %d' % owe
                print 'You can bet up to: %d' % (player.current_bet + player.chips)
                print '\n'
                #give info about pots/sidepots during each player's turn
                pot_counter = 0
                for pot in pots:
                    print 'Pot %d:' % (pot_counter + 1)
                    print 'Pot size: %d' % pots[pot_counter]['pot']
                    print 'Bet to match for this pot: %d' % pots[pot_counter]['match']
                    print 'Any all in? %s' % pots[pot_counter]['any_all_in']
                    pot_counter += 1
 
                calling_all_in = False
                while True:
                    if current_bet > 0:
                        #if player cannot match the bet and has to choose all in vs. fold
                        if player.chips + player.current_bet <= current_bet:
                            action = raw_input("Do you want to call all in? y or n: ")
                            if action == 'y' or action == 'yes':
                                calling_all_in = True
                                break
                            elif action == 'n' or action == 'no':
                                player.has_hand = False
                                player.cards = []
                                player.current_bet = 0
                                break
                            else:
                                continue
                    break
                #check if BB already had their option in case a player raises and the BB later calls the raise, or it will cause an infinite loop
                went_through_big_blind_option_code = False
                if player.has_hand == True:
                    while True:
                        if calling_all_in == True:
                            player_bet = player.chips + player.current_bet
                            print 'ALL IN!'
                            pots = organize_pots.Organize_Pots().organize_pots(player_bet, player, pots, players_list)
                            break
                        if current_bet == big_blind and player.big_blind == True:
                            print 'big blind player current bet: %d' % player.current_bet
                            player_bet = raw_input("\nYou can bet an integer,\ncheck your big blind with 'c' or 'check',\nor fold if you just don\'t want to play: ")
                            went_through_big_blind_option_code = True
                            print 'player bet: %s' % player_bet
                            if player_bet == 'c' or player_bet == 'check':
                                player.checked = True
                                big_blind_checked = True
                                print ('\nYou decided to check your option\n')
                                break
                            test_bet = int(player_bet)
                            if test_bet == big_blind:
                                print 'your bet is equal to blinds, you check'
                                player.checked = True
                                big_blind_checked = True
                                break

                        if went_through_big_blind_option_code == False:
                            player_bet = raw_input("\nYou can bet an integer,\nsay 'f' or 'fold' to fold,\nor say 'c' or 'check' to check, if the current bet is 0: ")
                        if player_bet == 'f' or player_bet == 'fold':
                            player.has_hand = False
                            player.cards = []
                            player.current_bet = 0
                            print '\nYou decided to fold\n'
                            break
                        if current_bet == 0 and player_bet == 'c' or current_bet == 0 and player_bet == 'check':
                            print ('\nYou decided to check\n')
                            player.checked = True
                            break
                        try:
                            bet = int(player_bet)
                        except ValueError:
                            print ('Enter an integer.')
                            continue
                        #if bet > current_bet and not bet >= (current_bet + (2 * current_raise)):
                        if (player.chips + player.current_bet - bet) == 0:
                            print ('ALLLLLLLL INNNNNNNN!!!!!!!!!!')
                            if bet >= required_raise:
                                old_bet = current_bet
                                raise_amount = bet - old_bet
                                pots = organize_pots.Organize_Pots().organize_pots(bet, player, pots, players_list)
                                current_raise = (2 * (bet - current_bet) + current_bet)
                                required_raise = ((2 * raise_amount) + old_bet)
                                print 'required raise: %d' % required_raise
                                current_bet = bet
                                print('%s chips: %d' % (player.screen_name, player.chips))
                                break
                            elif bet < required_raise:
                                old_bet = current_bet
                                pots = organize_pots.Organize_Pots().organize_pots(bet, player, pots, players_list)
                                current_bet = bet
                                print('%s chips: %d' % (player.screen_name, player.chips))
                                break
                        elif bet > current_bet and not bet >= required_raise:
                            print ('If you\'d like to raise, enter a number at least twice the current bet.')
                            continue
                        elif current_bet > bet:
                            print ('That is smaller than the current bet. Stop cheating, you cheapskate!!!')
                            continue
                        elif bet > player.chips:
                            print ('You don\'t have enough chips to bet that much! Make a valid bet.')
                            continue
                        elif current_bet == 0 and bet == 0:
                            print ('\nYou decided to check\n')
                            player.checked = True
                            break
                        elif bet == current_bet:
                            pots = organize_pots.Organize_Pots().organize_pots(bet, player, pots, players_list)
                            print ('%s chips: %d' % (player.screen_name, player.chips))
                            break
                        else:
                            old_bet = current_bet
                            raise_amount = bet - old_bet
                            #current_raise = (2 * (bet - current_bet) + current_bet)
                            required_raise = ((2 * raise_amount) + old_bet)
                            pots = organize_pots.Organize_Pots().organize_pots(bet, player, pots, players_list)
                            print 'required raise: %d' % required_raise
                            current_bet = bet
                            print('%s chips: %d' % (player.screen_name, player.chips))
                            break
                print 'current bet: %d' % current_bet
                print "\nmade it to left_to_act code\n"
                #end the game with a winner
                left_to_act = 0
                players_with_hands = 0
                all_in_players = []
                remaining_players = []
                    
                for player in players:
                    if player.has_hand == True:
                        players_with_hands += 1
                        remaining_players.append(player)
                        if player.all_in == True:
                            all_in_players.append(player)
                            continue
                        if player.current_bet < current_bet:
                            left_to_act += 1
                        if current_bet == big_blind and player.current_bet == current_bet and player.big_blind == True and player.checked == False:
                            left_to_act += 1
                        if current_bet == 0:
                            if player.current_bet == 0:
                                if not player.checked:
                                    left_to_act += 1

                
                if players_with_hands == 1:
                    winner = []
                    for player in players:
                        if player.has_hand == True:
                            winner.append(player)
                    return ({'hand_over': True}, pots, winner)
                if players_with_hands == len(all_in_players):
                    return ({'hand_over': False}, pots, all_in_players, {'everybody_all_in': True})
                if left_to_act == 0:
                    print "\nround is over\n"
                    pot_counter = 0
                    print '\nEnding of "betting_round"...'
                    return ({'hand_over': False}, pots, remaining_players, {'everybody_all_in': False})






    #forced bet is like big blind, what everyone pays. after the flop, forced bet is 0, but there's still a minimum bet (usually the big blind, or 2x BB)
    @staticmethod
    def betting_round_postflop(players, forced_bet, minimum_bet, current_pots, big_blind, board):

        pots = current_pots

        amount_of_players_remaining = len(players)

        pots = current_pots
        players_list = players
        print '\nstarting betting round!!!'
        current_bet = forced_bet
        raise_amount = 0
        required_raise = 0
        if minimum_bet > 0 and forced_bet == 0:
            required_raise = minimum_bet
        else:
            required_raise = 2 * forced_bet
         
        old_bet = 0
                
        while True:       
            for index, player in enumerate(players):

                if player.chips == 0:
                    player.all_in = True

                owe = current_bet - player.current_bet
                if owe == 0 and player.checked == True:
                    continue

                if player.has_hand == False:
                    continue

                if player.all_in == True:
                    continue


                card_sub = ''
                count = 0
                for card in board:
                    card_sub += Ranks().ranks_dict[board[count].Rank]
                    card_sub += Ranks().suits_dict[board[count].Suit]
                    card_sub +=' '
                    count += 1
                print '\nBoard: %s' % card_sub


                print ('\nOn %s, %d chips' % (player.screen_name, player.chips))
                print ('Your cards are: %s%s, %s%s' % (Ranks().ranks_dict[player.cards[0].Rank], Ranks().suits_dict[player.cards[0].Suit], Ranks().ranks_dict[player.cards[1].Rank], Ranks().suits_dict[player.cards[1].Suit]))
                print 'Current bet: %s' % player.current_bet
                print 'Current investment: %s' % player.current_investment
                print 'The current bet is %d' % current_bet
                print ('The current raise is: %d' % raise_amount)
                print ('The required raise is: %d' % required_raise)
                print 'Your current bet is %d' % player.current_bet
                print 'You owe: %d' % owe
                print 'You can bet up to: %d' % (player.current_bet + player.chips)
                print '\n'
                pot_counter = 0
                for pot in pots:
                    print 'Pot %d:' % (pot_counter + 1)
                    print 'Pot size: %d' % pots[pot_counter]['pot']
                    print 'Bet to match for this pot: %d' % pots[pot_counter]['match']
                    print 'Any all in? %s' % pots[pot_counter]['any_all_in']
                    pot_counter += 1
 
                calling_all_in = False
                while True:
                    if current_bet > 0:
                        if player.chips + player.current_bet <= current_bet:
                            action = raw_input("Do you want to call all in? y or n: ")
                            if action == 'y' or action == 'yes':
                                calling_all_in = True
                                break
                            elif action == 'n' or action == 'no':
                                player.has_hand = False
                                player.cards = []
                                player.current_bet = 0
                                break
                            else:
                                continue
                    break
                
                went_through_big_blind_option_code = False
                if player.has_hand == True:
                    while True:
                        if calling_all_in == True:
                            player_bet = player.chips + player.current_bet
                            print 'ALLL INNN!!!!!!!!!!!!!'
                            pots = organize_pots.Organize_Pots().organize_pots(player_bet, player, pots, players_list)
                            break
                        player_bet = raw_input("\nYou can bet an integer,\nsay 'f' or 'fold' to fold,\nor say 'c' or 'check' to check, if the current bet is 0: ")
                        if player_bet == 'f' or player_bet == 'fold':
                            player.has_hand = False
                            player.cards = []
                            player.current_bet = 0
                            print 'You decided to fold'
                            break
                        if current_bet == 0 and player_bet == 'c' or current_bet == 0 and player_bet == 'check':
                            print ('\nYou decided to check\n')
                            player.checked = True
                            break
                        try:
                            bet = int(player_bet)
                        except ValueError:
                            print ('Enter an integer.')
                            continue
                        #if bet > current_bet and not bet >= (current_bet + (2 * current_raise)):
                        if (player.chips + player.current_bet - bet) == 0:
                            print ('ALLLLLLLL INNNNNNNN!!!!!!!!!!')
                            if bet >= required_raise:
                                old_bet = current_bet
                                raise_amount = bet - old_bet
                                pots = organize_pots.Organize_Pots().organize_pots(bet, player, pots, players_list)
                                current_raise = (2 * (bet - current_bet) + current_bet)
                                required_raise = ((2 * raise_amount) + old_bet)
                                print 'required raise: %d' % required_raise
                                current_bet = bet
                                print('%s chips: %d' % (player.screen_name, player.chips))
                                break
                            elif bet < required_raise:
                                old_bet = current_bet
                                pots = organize_pots.Organize_Pots().organize_pots(bet, player, pots, players_list)
                                current_bet = bet
                                print('%s chips: %d' % (player.screen_name, player.chips))
                                break
                        elif bet > current_bet and not bet >= required_raise:
                            print ('If you\'d like to raise, enter a number at least twice the current bet, or twice the current raise plus the previous bet.')
                            continue
                        elif current_bet > bet:
                            print ('That is smaller than the current bet. Stop cheating, you cheapskate!!!')
                            continue
                        elif bet > player.chips:
                            print ('You don\'t have enough chips to bet that much!')
                            continue
                        elif current_bet == 0 and bet == 0:
                            print ('\nYou decided to check\n')
                            player.checked = True
                            break
                        elif bet == current_bet:
                            pots = organize_pots.Organize_Pots().organize_pots(bet, player, pots, players_list)
                            print ('%s chips: %d' % (player.screen_name, player.chips))
                            break
                        else:
                            old_bet = current_bet
                            raise_amount = bet - old_bet
                            #current_raise = (2 * (bet - current_bet) + current_bet)
                            #current_raise is now obsolete in newer version as of december 2014. leave in for record
                            required_raise = ((2 * raise_amount) + old_bet)
                            pots = organize_pots.Organize_Pots().organize_pots(bet, player, pots, players_list)
                            print 'required raise: %d' % required_raise
                            current_bet = bet
                            print('%s chips: %d' % (player.screen_name, player.chips))
                            break

                
                print "\nmade it to left_to_act code postflop\n"
                #end the game with a winner
                left_to_act = 0
                players_with_hands = 0
                all_in_players = []
                remaining_players = []
                for player in players:
                    if player.has_hand == True:
                        players_with_hands += 1
                        remaining_players.append(player)
                        if player.all_in == True:
                            all_in_players.append(player)
                            continue
                        if player.current_bet < current_bet:
                            left_to_act += 1
                            continue
                        if current_bet == 0:
                            if player.current_bet == 0:
                                if not player.checked:
                                    left_to_act += 1
                #if only one player has cards, they won the hand
                if players_with_hands == 1:
                    winner = []
                    for player in players:
                        if player.has_hand == True:
                            winner.append(player)
                    return ({'hand_over': True}, pots, winner)
                #all players are all in or all players except 1 are all in, but the board has to be dealt and a winner determined then pots distributed- hence hand not over but everybody all in == True
                if len(all_in_players) >= (players_with_hands - 1) and left_to_act == 0:
                    return ({'hand_over': False}, pots, remaining_players, {'everybody_all_in': True})
                #players still have hands, not everyone is all in, and next round should be bet on
                if left_to_act == 0:
                    print "\nround is over\n"
                    pot_counter = 0
                    print '\nEnding of "betting_round"...'
                    return ({'hand_over': False}, pots, remaining_players, {'everybody_all_in': False})












