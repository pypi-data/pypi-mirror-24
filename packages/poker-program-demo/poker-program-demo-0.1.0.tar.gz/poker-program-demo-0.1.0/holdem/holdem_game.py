#!/usr/bin/env python

#minimum reraises and capping action with short all ins:
#http://poker.stackexchange.com/questions/158/minimum-re-raise-in-hold-em


# button rules in heads up:
#http://www.888poker.co.uk/how-to-play/heads-up-poker-rules

#dead blinds, including when going to heads up
#http://www.texasholdem-poker.com/dead-blinds



import sys
import deck
import pokertable
import players
import dealer_holdem
import rules_holdem
import betting_rounds_holdem
import tests

import time
import logging

from copy import deepcopy


cody = players.Player('cody4321', 1500)
darren = players.Player('d_money', 1500)
katelyn = players.Player('yuppitsme', 1500)
mike = players.Player('it\'s_massey\'s_world', 1500)
jon = players.Player('no_rules_2014', 1500)
derek = players.Player('dwreck', 1500)
table_players = [cody, darren, katelyn, mike, jon, derek]
newtable = pokertable.Table(table_players, 20, 10, 0)


#for player in table_players:
    #print (player.screen_name)


#active_players_list = newtable.players_list
#amount_of_players = len(players_list)
button = 0
button_bucket = 0
big_blind = 20
small_blind = 10




# to change button, constantly add 1 to button bucket, and % that beast by the amount of players at the table
# once the button rounds the table of 6 players, bucket has 6. next hand bucket has 7, 7%6 = 1, it returns to the start
# for us, seat 1 is actually seat 0


class Hand():

    #bets_to_match = []

    #pots = []

    suits_dict = {1: 'c', 2: 'd', 3: 'h', 4: 's'}
    ranks_dict = {1: '2', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: '10', 11: 'J', 12: 'Q', 13: 'K', 14: 'A'}


    @staticmethod
    def reset_round(players):
        for player in players:
            player.current_bet = 0
            player.checked = False
            #player.small_blind = False
            #player.big_blind = False


    @staticmethod
    def reset_hand(players):
        for player in players:
            player.current_bet = 0
            player.current_investment = 0
            player.starting_chips = player.chips
            player.checked = False
            player.has_hand = False
            player.all_in = False
            player.small_blind = False
            player.big_blind = False
            player.cards = []


    @staticmethod
    def start_hand(active_players, button, big_blind, small_blind, deck, one_big_blind):

        players = active_players
        number_of_players = len(players)
        #for player in players:
            #print 'in start_hand...player %s chips = %d' % (player.screen_name, player.chips)
        seat_order_of_players_list = []
        seats_list = []
        for player in players:
            seats_list.append(player.seat)
        seats_list.sort()
        for seat in seats_list:
            for player in players:
                if player.seat == seat:
                    seat_order_of_players_list.append(player)
                    break

        #screen_name_list = ''
        #for player in seat_order_of_players_list:
            #screen_name_list += player.screen_name
            #screen_name_list += ', '
        #print '\n'
        #print 'Seat order of players list: %s' % screen_name_list
        #print '\n'


        active_players_list = players

        dealer_holdem.Dealer().deal_player_hand(active_players_list, deck)

        for player in active_players_list:
            player.has_hand = True


        player_count = len(active_players_list)

        if player_count > 2:
            if one_big_blind == False:
                preflop_list = active_players_list[((button + 3) % player_count):] + active_players_list[0:((button + 3)% player_count)]
                postflop_list = active_players_list[((button + 1) % player_count):] + active_players_list[0:((button + 1) % player_count)]
            else:
                preflop_list = active_players_list[((button + 2) % player_count):] + active_players_list[0:((button + 2)% player_count)]
                postflop_list = active_players_list[((button + 1) % player_count):] + active_players_list[0:((button + 1) % player_count)]
        elif player_count == 2:
                preflop_list = active_players_list[button:]  #+ active_players_list[0:button]
                postflop_list = active_players_list[(button + 1)] + active_players_list[button]

        print '\nstarting hand, button = %d\n' % button

        screen_name_list = ''
        for player in active_players_list:
            screen_name_list += player.screen_name
            screen_name_list += ', '
        print '\n'
        print 'Active players list within "start_hand": %s' % screen_name_list
        print '\n'
        print 'The button within "start_hand": %d' % button
        print 'How many players? %d' % player_count

        small_blind_start = None

        if one_big_blind == False:
            if player_count > 2:
                small_blind_start = ((button + 1) % player_count)
                big_blind_start = ((button + 2) % player_count)
            elif player_count == 2:
                small_blind_start = button
                big_blind_start = (button + 1)
            elif player_count == 1:
                print 'Error, player count is 1 but game is still running!'
        elif one_big_blind == True:
            big_blind_start = (button + 1)

        #if small_blind_start:
            #print 'small blind start: %d' % small_blind_start
        #print 'big blind start: %d \n' % big_blind_start

        if one_big_blind == False:
            pots = Hand().handle_small_blind(small_blind, big_blind, active_players_list[((button + 1) % player_count)])
            print '\n'
            pots = Hand().handle_big_blind(small_blind, big_blind, active_players_list[((button + 2) % player_count)], pots)
        elif one_big_blind == True:
            pots = Hand().handle_single_big_blind(big_blind, active_players_list[((button + 1) % player_count)])

        print pots

        the_button = None
        for index, player in enumerate(active_players_list):
            if index == button:
                the_button = player
                break
        print '\n %s is the button' % the_button.screen_name

        return (preflop_list, pots, active_players_list, postflop_list)


    @staticmethod
    def handle_small_blind(small_blind, big_blind, player):

        print '%s is the small blind.' % player.screen_name
        print 'player\'s chips before handling small blind: %d' % player.chips

        player.small_blind = True

        if player.chips > small_blind:
            pots = [{'pot': small_blind, 'match': big_blind, 'any_all_in': False}]
            player.chips -= small_blind
            player.current_bet = small_blind
            player.current_investment += small_blind

        if player.chips == small_blind:
            pots = [{'pot': small_blind,'match': small_blind, 'any_all_in': True}]
            player.chips = 0
            player.current_bet = small_blind
            player.all_in = True
            player.current_investment += small_blind

        if player.chips < small_blind:
            pots = [{'pot': player.chips, 'match': player.chips, 'any_all_in': True}]
            player.current_bet = player.chips
            player.current_investment += player.chips
            player.chips = 0
            player.all_in = True

        print 'player\'s chips after handling small blind: %d' % player.chips
        return pots


    @staticmethod
    def handle_big_blind(small_blind, big_blind, player, pots):

    #NOT DONE!!!!
        player.big_blind = True

        print '%s is the big blind.' % player.screen_name
        print 'player\'s chips before handling big blind: %d' % player.chips
        if player.chips > big_blind:

            if pots[0]['any_all_in'] == True:
                pots[0]['pot'] = pots[0]['pot'] + pots[0]['match']
                side_pot_amount = (big_blind - pots[0]['match'])
                pots.insert(1, [{'pot': side_pot_amount,'match': big_blind, 'any_all_in': False}])
                player.chips -= big_blind
                player.current_bet = big_blind
                player.current_investment += big_blind

            elif pots[0]['any_all_in'] == False:
                pots[0]['pot'] += big_blind
                player.chips -= big_blind
                player.current_bet = big_blind
                player.current_investment += big_blind



        if player.chips == big_blind:
            if pots[0]['any_all_in'] == True:
                pots[0]['pot'] = pots[0]['pot'] + pots[0]['match']
                side_pot_amount = (big_blind - pots[0]['match'])
                pots.insert(1, [{'pot': side_pot_amount,'match': big_blind, 'any_all_in': True}])
                player.chips = 0
                player.current_bet = big_blind
                player.current_investment += big_blind
                player.all_in = True

            elif pots[0]['any_all_in'] == False:
                pots[0]['pot'] += big_blind
                pots[0]['any_all_in'] = True
                player.chips = 0
                player.current_bet = big_blind
                player.current_investment += big_blind
                player.all_in = True



        if player.chips < big_blind:
            if pots[0]['any_all_in'] == True:
                if player.chips < pots[0]['match']:
                    main_pot_amount = player.chips * 2
                    pots.insert(0, [{'pot': main_pot_amount,'match': player.chips, 'any_all_in': True}])
                    player.current_bet = player.chips
                    player.current_investment += player.chips
                    player.chips = 0
                    player.all_in = True
                elif player.chips == pots[0]['match']:
                    main_pot_amount = player.chips * 2
                    pots.insert(0, [{'pot': main_pot_amount,'match': player.chips, 'any_all_in': True}])
                    player.current_bet = player.chips
                    player.current_investment += player.chips
                    player.chips = 0
                    player.all_in = True
                elif player.chips > pots[0]['match']:
                    pots[0]['pot'] = pots[0]['match'] * 2
                    side_pot_amount = player.chips - pots[0]['match']
                    pots.insert(1, [{'pot': side_pot_amount,'match': player.chips, 'any_all_in': True}])
                    player.current_bet = player.chips
                    player.current_investment += player.chips
                    player.chips = 0
                    player.all_in = True

            elif pots[0]['any_all_in'] == False:
                if player.chips < small_blind:
                    main_pot_amount = (small_blind - player.chips) * 2
                    pots.insert(0, [{'pot': main_pot_amount,'match': player.chips, 'any_all_in': True}])
                    pots[1]['pot'] -= player.chips
                    player.current_bet = player.chips
                    player.current_investment += player.chips
                    player.chips = 0
                    player.all_in = True
                elif player.chips == small_blind:
                    main_pot_amount = small_blind * 2
                    pots[0]['pot'] = main_pot_amount
                    pots[0]['any_all_in'] = True
                    player.current_bet = player.chips
                    player.current_investment += player.chips
                    player.chips = 0
                    player.all_in = True
                elif player.chips > small_blind:
                    pots[0]['pot'] = small_blind * 2
                    pots[0]['any_all_in'] = True
                    side_pot_amount = player.chips - small_blind
                    pots.insert(1, [{'pot': side_pot_amount,'match': player.chips, 'any_all_in': True}])
                    player.current_bet = player.chips
                    player.current_investment += player.chips
                    player.chips = 0
                    player.all_in = True

        print 'player\'s chips after handling big blind: %d' % player.chips
        return pots


    @staticmethod
    def handle_single_big_blind(big_blind, player):

        print '%s is the big blind.' % player.screen_name
        print 'player\'s chips before handling big blind: %d' % player.chips

        player.big_blind = True

        if player.chips > big_blind:
            pots = [{'pot': big_blind, 'match': big_blind, 'any_all_in': False}]
            player.chips -= big_blind
            player.current_bet = big_blind
            player.current_investment += big_blind

        if player.chips == big_blind:
            pots = [{'pot': big_blind,'match': big_blind, 'any_all_in': True}]
            player.chips = 0
            player.current_bet = big_blind
            player.all_in = True
            player.current_investment += big_blind

        if player.chips < big_blind:
            pots = [{'pot': player.chips, 'match': player.chips, 'any_all_in': True}]
            player.current_bet = player.chips
            player.current_investment += player.chips
            player.chips = 0
            player.all_in = True

        print 'player\'s chips after handling big blind: %d' % player.chips
        return pots


    # dont worry about legal bets here; the betting round function screens out illegal bets
    # bet is player.current_bet
    # current_bet is the current bet at the table
    # list.insert(i, x) where i is the index to insert BEFORE



    @staticmethod
    def award_pot(remaining_players, pots):


        print 'Remaining players: %s' % remaining_players

        if len(remaining_players) == 1:
            winner = remaining_players[0]
            for pot in pots:
                winner.chips += pot['pot']
            return 1

        for pot in pots:
            eligible_players = []
            for player in remaining_players:
                if player.starting_chips >= pot['match']:
                    eligible_players.append(player)

            winners = rules_holdem.Holdem_rules().compare_hands(eligible_players)
            print 'winners: %s' % winners
            number_of_winners = len(winners)
            print 'number of winners: %d' % number_of_winners
            remainder = pot['pot'] % number_of_winners
            division_of_pot = (pot['pot'] - remainder) / number_of_winners
            for player in winners:
                player.chips += division_of_pot
            for number in range(remainder):
                winners[number].chips += 1
        return 1


    @staticmethod
    def run_hand(players, button, big_blind, small_blind, one_big_blind):
        #ignore bigblind for now. may want to split off a small method called init_hand to make the players lists for preflop, postflop, init the small
        # blind and bigblind bets

        newdeck = deck.Deck()

        Hand().reset_hand(players)

        start_hand = Hand().start_hand(players, button, big_blind, small_blind, newdeck, one_big_blind)

        preflop_list = start_hand[0]

        postflop_list = start_hand[3]

        pots = start_hand[1]

        active_players_list = start_hand[2]

        everybody_all_in = False

        was_one_big_blind = False

        if one_big_blind:
            was_one_big_blind = True


        print ('\nf to fold, c to call, and a number to raise. let\'s gamble, son!!!\n')

        for player in active_players_list:
            print ('%s: %s %s%s, %s%s' % (player.screen_name, player.chips, Hand().ranks_dict[player.cards[0].Rank], Hand().suits_dict[player.cards[0].Suit], Hand().ranks_dict[player.cards[1].Rank], Hand().suits_dict[player.cards[1].Suit]))

        print '\npreflop'

        #for player in active_players_list:
            #print '%s chips: %d' % (player.screen_name, player.chips)

        #PREFLOP
        screen_name_list = ''
        for player in preflop_list:
            screen_name_list += player.screen_name
            screen_name_list += ', '
        print '\n'
        print 'Preflop list within "run_hand" before dealing preflop: %s' % screen_name_list
        screen_name_list = ''
        for player in postflop_list:
            screen_name_list += player.screen_name
            screen_name_list += ', '
        print 'Postflop list within "run_hand" before dealing preflop: %s' % screen_name_list
        print '\n'

        #preflop = Hand().betting_round(preflop_list, big_blind, 0, pots, True, big_blind)
        preflop = betting_rounds_holdem.Betting_Rounds().betting_round_preflop(preflop_list, big_blind, 0, pots, big_blind)
        pots = preflop[1]
        #print preflop
        if preflop[0]['hand_over'] == True:
            print '\nhand_over == True\n'
            Hand().award_pot(preflop[2], pots)
            return (active_players_list, was_one_big_blind)
        else:
            print '\nflop\n'
            #FLOP
            print 'Dealing flop\n'
            flop_board = dealer_holdem.Dealer().deal_flop(newdeck)
            Hand().reset_round(active_players_list)

            if preflop[3]['everybody_all_in'] == True:
                everybody_all_in = True
            if everybody_all_in == True:
                flop = preflop
            else:
                flop = betting_rounds_holdem.Betting_Rounds().betting_round_postflop(postflop_list, 0, big_blind, pots, big_blind, flop_board)
            #print flop
            #print flop[1]
            pots = flop[1]
            print flop
            if flop[0]['hand_over'] == True:
                print 'hand_over == True'
                Hand().award_pot(flop[2], pots)
                return (active_players_list, was_one_big_blind)
            else:
                print '\nturn\n'
                #TURN
                print '\nDealing turn\n'
                turn_board = dealer_holdem.Dealer().deal_turn(newdeck, flop_board)

                if flop[3]['everybody_all_in'] == True:
                    everybody_all_in = True
                if everybody_all_in == True:
                    turn = flop

                else:
                    Hand().reset_round(active_players_list)
                    turn = betting_rounds_holdem.Betting_Rounds().betting_round_postflop(postflop_list, 0, big_blind, pots, big_blind, turn_board)
                pots = turn[1]
                if turn[0]['hand_over'] == True:
                    print 'hand_over == True'
                    Hand().award_pot(turn[2], pots)
                    return (active_players_list, was_one_big_blind)
                else:
                    print '\nriver\n'
                    #RIVER
                    print 'Dealing river\n\n'
                    final_board = dealer_holdem.Dealer().deal_river(newdeck, turn_board)
                    if turn[3]['everybody_all_in'] == True:
                        everybody_all_in = True
                    if everybody_all_in == True:
                        river = turn
                    else:
                        Hand().reset_round(active_players_list)
                        river = betting_rounds_holdem.Betting_Rounds().betting_round_postflop(postflop_list, 0, big_blind, pots, big_blind, final_board)
                    #print river[0]['hand_over']
                    #print river[1]
                    pots = river[1]
                    if river[0]['hand_over'] == True:
                        print 'hand_over == True'
                        Hand().award_pot(river[2], pots)
                        return (active_players_list, was_one_big_blind)
                    else:
                        remaining_players = []
                        for player in active_players_list:
                            if player.has_hand == True:
                                remaining_players.append(player)
                        for player in remaining_players:
                            for card in final_board:
                                player.cards.append(card)
                        print "right before awarding pot"
                        Hand().award_pot(remaining_players, pots)
                        return (active_players_list, was_one_big_blind)
                        #hands must be evaluated...need to finish writing "compare hands"

    @staticmethod
    def make_hand_dicts():
        pass


    @staticmethod
    def run_poker_game(players, big_blind, small_blind):

        total_chipcount = tests.Test().determine_total_chipcount(players)

        length = 2*len(players)

        raw_button = length

        first_hand = True

        for index, player in enumerate(players):
            player.seat = (index + 1)

        while True:
            players_with_chips = 0
            for player in players:
                if player.chips > 0:
                    players_with_chips += 1
            winner = []
            if players_with_chips == 1:
                for player in players:
                    if player.chips > 0:
                        print '\nThe winner is: %s!!!' % player.screen_name
                        print 'how many chip he got? %d' % player.chips
                        winner.append(player)
                time.sleep(3)
                print '\nThe winner is: %s!!!' % winner
                return (winner)


            if first_hand == True:
                HAND = list_of_players_from_last_hand = Hand().run_hand(players, 0, big_blind, small_blind, False)
            else:
                Hand().reset_round(players)
                HAND = Hand().run_hand(active_players_list, new_button, big_blind, small_blind, one_big_blind)
            first_hand = False

            tests.Test().ensure_chipcount(players, total_chipcount)

            list_of_players_from_last_hand = HAND[0]
            was_one_big_blind_previously = HAND[1]
            one_big_blind = False
            big_blind_busted = False
            length = len(list_of_players_from_last_hand)

            other_list = deepcopy(list_of_players_from_last_hand)

            previous_button = None
            for index, player in enumerate(list_of_players_from_last_hand):
                if player.big_blind == True:
                    previous_button = index
            new_blind_check_list = list_of_players_from_last_hand[(previous_button + 1):] + list_of_players_from_last_hand[0:(previous_button + 1)]

            new_big_blind_player = None
            while True:
                for player in new_blind_check_list:
                    if player.chips > 0:
                        new_big_blind_player = player
                        break
                break


            for index, player in enumerate(list_of_players_from_last_hand):
                if player.big_blind == True and player.chips == 0:
                    one_big_blind = True
                    break


            new_big_blind_player_screen_name = new_big_blind_player.screen_name
            new_button = 0
            active_players_list_screen_names = []
            for player in players:
                if player.chips > 0:
                    active_players_list_screen_names.append(player.screen_name)
            active_players_list = []
            for player in players:
                if player.chips > 0:
                    active_players_list.append(player)

            active_players_list_length = len(active_players_list)

            button_displacement = None

            if one_big_blind == True:
                button_displacement = 1
            else:
                button_displacement = 2

            index_for_new_big_blind = None

            for index, player in enumerate(active_players_list_screen_names):
                if player == new_big_blind_player_screen_name:
                    index_for_new_big_blind = index

            #print 'index for new big blind: %d' % index_for_new_big_blind
            #print 'button_displacement: %d' % button_displacement

            if index_for_new_big_blind == 0:
                if button_displacement == 1:
                    new_button = (active_players_list_length - 1)
                if button_displacement == 2:
                    new_button = (active_players_list_length - 2)
            if index_for_new_big_blind == 1:
                if button_displacement == 1:
                    new_button = (index_for_new_big_blind - 1)
                if button_displacement == 2:
                    new_button = (active_players_list_length - 1)
            if index_for_new_big_blind > 1:
                if button_displacement == 1:
                    new_button = (index_for_new_big_blind - 1)
                if button_displacement == 2:
                    new_button = (index_for_new_big_blind - 2)



            new_button_player = active_players_list[new_button]
            new_button_player_screen_name = new_button_player.screen_name

            print active_players_list_screen_names
            print active_players_list
            print '\n'
            print 'new button = %d\n' % new_button
            print 'new button player.screen name: %s' % active_players_list_screen_names[new_button]

        return 1



def run_poker_game(): 
    Hand().run_poker_game(table_players, 20, 10)




        #to run the test file
# python ~/Desktop/poker_site/game.py
