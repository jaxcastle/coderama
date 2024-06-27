#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from random import shuffle
from colorama import Fore, Back, Style
from IPython.display import clear_output
import time
import os

BET_SIZE = 20
GAMEOVER = False

dict_rank = {  '2':2,
               '3':3,
               '4':4,
               '5':5,
               '6':6,
               '7':7,
               '8':8,
               '9':9,
               '10':10,
               'J':10,
               'Q':10,
               'K':10,
               'A':11}

dict_suit = {'spades':   ('♠',Fore.BLACK),
             'clubs':    ('♣',Fore.BLACK),
             'hearts':   ('♥',Fore.RED),
             'diamonds': ('♦',Fore.RED)}


# This class holds a single instance of a card
class Card:    
    def __init__(self, rank, suit):
        self.suit = suit
        self.rank = rank
        self.value = dict_rank[rank]
        self.str_card = '{: <2}'.format(self.rank) + dict_suit[self.suit][0] 
        
    def __str__(self):
        return Back.WHITE + dict_suit[self.suit][1] + "┌───┐\n│" + self.str_card + "│\n└───┘\n" + Style.RESET_ALL

    def str_top(self):
        return Back.WHITE + dict_suit[self.suit][1] + "┌───┐" + Style.RESET_ALL

    def str_mid(self):
        return Back.WHITE + dict_suit[self.suit][1] + "│" + self.str_card + "│" + Style.RESET_ALL

    def str_bot(self):
        return Back.WHITE + dict_suit[self.suit][1] + "└───┘" + Style.RESET_ALL


# This class holds a list with multiple instance of a card
class Deck:
    def __init__(self):
        self.cards = []

    def __len__(self):
        return len(self.cards) 
        
    def add_card(self, card):
        self.cards.append(card)

    def play_card(self):
        return self.cards.pop(0)

    def add_deck(self, deck):
        for card in deck.cards:
            self.cards.append(card)
    
    def shuffle_cards(self):
        shuffle(self.cards)

    def deal_cards(self, n=1):
        dealt_deck = Deck()
        for i in range(0,n):
            dealt_deck.cards.append(self.cards.pop(0))
        return dealt_deck

    def print_deck(self):
        top_row = ''
        mid_row = ''
        bot_row = ''
        for card in self.cards:
            top_row += card.str_top() + ' '
            mid_row += card.str_mid() + ' '
            bot_row += card.str_bot() + ' '
        print(top_row)
        print(mid_row)
        print(bot_row)

    def score(self):
        partial_score = 0
        for card in self.cards:
            partial_score += dict_rank[card.rank]
        for card in self.cards:
            if card.rank == 'A' and partial_score > 21:
                partial_score -= 10
        return partial_score

class Player:
    def __init__(self, name, chips):
        self.name = name
        self.chips = chips
        self.hand = Deck()
        self.card_played = Deck()

    def __str__(self):
        return f'{self.name} has {len(self.hand)} cards left!'

    def total_cards(self):
        return len(self.hand) + len(self.warstack) + len(self.card_played)

    def bust(self):
        return self.hand.score() > 21

    def win(self, bet = BET_SIZE):
        self.chips += bet

    def lose(self, bet = BET_SIZE):
        self.chips -= bet
        
# Moves a specified number of cards from deck_from to deck_to
def move_cards(deck_from, deck_to, n=1):
    deck_to.add_deck(deck_from.deal_cards(min(n,len(deck_from))))

# Clear Screen
def clear_screen():
    clear_output(wait=True)
    os.system('cls')

# Print Game
def print_game(player, dealer):
    clear_screen()
    print(f"{Back.WHITE + Fore.BLUE}{player.name.upper()} BALANCE = {player.chips}{Style.RESET_ALL}\n")
    print(f'Dealer has {dealer.hand.score()} points!')
    dealer.hand.print_deck()
    print('')
    print(f'Player has {player.hand.score()} points!')    
    player.hand.print_deck()
    print('')

def get_hit_or_stand(prompt):
    while True:
        user_input = input(prompt).strip().lower()
        if user_input in ['h', 's']:
            return user_input
        else:
            print("Invalid input. Please enter 'h' or 's'.")

def get_yes_or_no(prompt):
    while True:
        user_input = input(prompt).strip().lower()
        if user_input in ['y', 'n']:
            return user_input
        else:
            print("Invalid input. Please enter 'y' or 'n'.")
            
# MAIN LOGIC

main_deck = Deck()
for rank in dict_rank.keys():
    for suit in dict_suit.keys():
        main_deck.add_card(Card(rank,suit))


player = Player(input("Enter your name: "), 100)
dealer = Player("AI", 1000000)

while not GAMEOVER:
    shuffle(main_deck.cards)
    move_cards(main_deck, dealer.hand, 1)
    move_cards(main_deck, player.hand, 2)
    print_game(player, dealer)

    #PLAYER TURN
    player_input = ''
    while not (player.bust() or player_input == 's'):
        player_input = get_hit_or_stand("It's your turn! Would you like to Hit or Stand? (enter H or S): ")
        if player_input == 'h':
            move_cards(main_deck, player.hand,1)
            print_game(player, dealer)

    if player.bust():
        print('\nYOU BUSTED!!!\n')
    else:
        print_game(player, dealer)
        print("It's the dealers turn\n")
        time.sleep(1)
        while dealer.hand.score() < 17:
            time.sleep(1)
            print('Dealer hits!\n')
            time.sleep(1)
            move_cards(main_deck, dealer.hand, 1)
            print_game(player, dealer)

        if dealer.bust():
            print('DEALER BUSTED\n')
        else:
            print('Dealer stands.\n')
    
    time.sleep(1)

    if player.bust():
        print('YOU LOSE!')
        player.lose()
        dealer.win()
    elif dealer.bust():
        print('YOU WIN!')
        player.win()
        dealer.lose()
    elif player.hand.score() > dealer.hand.score():
        print('YOU WIN')
        player.win()
        dealer.lose()
    elif player.hand.score() < dealer.hand.score():
        print('YOU LOSE')
        player.lose()
        dealer.win()
    elif player.hand.score() == dealer.hand.score():
        print('TIE')
    else:
        print('hmmm, this is not supposed to happen!')

    time.sleep(3)
    print_game(player, dealer)
    
    move_cards(dealer.hand, main_deck, 52)
    move_cards(player.hand, main_deck, 52)

    time.sleep(1)
    if player.chips == 0:
        GAMEOVER = True
        print('\nYou lost all your money! :(')
        print('\n' + Back.WHITE + Fore.RED + "GAME OVER!" + Style.RESET_ALL)
        input()
    elif get_yes_or_no('\nWould you like to play again? (enter Y or N): ') == 'n':
        GAMEOVER = True
        print('\n' + Back.WHITE + Fore.RED + "GAME OVER!" + Style.RESET_ALL)
        input()


# In[ ]:




