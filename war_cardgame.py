#!/usr/bin/env python
# coding: utf-8

# In[260]:


from random import shuffle
from colorama import Fore, Back, Style
from IPython.display import clear_output
import time
import os

WAR_COUNT = 3
WAIT_TIME = 0
WAIT_TIME_WAR = 3
WAIT_INPUT = True

dict_rank = {'2':2,
               '3':3,
               '4':4,
               '5':5,
               '6':6,
               '7':7,
               '8':8,
               '9':9,
               '10':10,
               'J':11,
               'Q':12,
               'K':13,
               'A':14}

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
        
    def __str__(self):
        str_card =  '{: <2}'.format(self.rank) + dict_suit[self.suit][0] 
        return Back.WHITE + dict_suit[self.suit][1] + "┌───┐\n│" + str_card + "│\n└───┘\n" + Style.RESET_ALL

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

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = Deck()
        self.warstack = Deck()
        self.card_played = Deck()

    def __str__(self):
        return f'{self.name} has {len(self.hand)} cards left!'

    def total_cards(self):
        return len(self.hand) + len(self.warstack) + len(self.card_played)
        
# Moves a specified number of cards from deck_from to deck_to
def move_cards(deck_from, deck_to, n=1):
    deck_to.add_deck(deck_from.deal_cards(min(n,len(deck_from))))


# MAIN GAME LOGIC

main_deck = Deck()
for suit in dict_suit.keys():
    for rank in dict_rank.keys():
        main_deck.add_card(Card(rank, suit)) 

main_deck.shuffle_cards()

player1 = Player("Jaques")
player2 = Player("Magda")

while len(main_deck) > 0:
    move_cards(main_deck, player1.hand, 1)
    move_cards(main_deck, player2.hand, 1)

GAMEOVER = False

while not GAMEOVER:
    
    SPECIAL_ROUND = len(player1.warstack) + len(player2.warstack) > 0
    
    if SPECIAL_ROUND:
        print(f'SPECIAL ROUND! THIS TURN IS WORTH {2+ len(player1.warstack) + len(player2.warstack)} CARDS!!!\n')
    else:
        print('\n')
    
    print(f'{str(player1)} {player1.name} played:')
    move_cards(player1.hand, player1.card_played,1)
    p1_card = player1.card_played.cards[0]
    print(p1_card)
    
    print(f'{str(player2)} {player2.name} played:')
    move_cards(player2.hand, player2.card_played,1)
    p2_card = player2.card_played.cards[0]
    print(p2_card)
    
    
    if p1_card.value > p2_card.value:
        print(f'{player1.name} won the round!\n\n')
        move_cards(player1.card_played, player1.hand)
        move_cards(player2.card_played, player1.hand)
        move_cards(player1.warstack, player1.hand, len(player1.warstack))
        move_cards(player2.warstack, player1.hand, len(player2.warstack))
        
    elif p1_card.value < p2_card.value:
        print(f'{player2.name} won the round!\n\n')
        move_cards(player1.card_played, player2.hand)
        move_cards(player2.card_played, player2.hand)
        move_cards(player1.warstack, player2.hand, len(player1.warstack))
        move_cards(player2.warstack, player2.hand, len(player2.warstack))
        
    elif p1_card.value == p2_card.value:
        print(f"TIE! IT'S A WAR! {WAR_COUNT} CARDS MOVED TO THE STACK!\n\n")
        move_cards(player1.card_played, player1.warstack)
        move_cards(player2.card_played, player2.warstack)
        move_cards(player1.hand, player1.warstack, min(WAR_COUNT,len(player1.hand)))
        move_cards(player2.hand, player2.warstack, min(WAR_COUNT,len(player2.hand)))
        time.sleep(WAIT_TIME_WAR)
    
    else:
        print('This is not supposed to happen')

    if len(player1.hand) == 0:
        GAMEOVER = True
        print(f'{player2.name.upper()} WON THE GAME, CONGRATULATIONS!!!')
        time.sleep(10)
        input()
        
    elif len(player2.hand) == 0:
        GAMEOVER = True
        print(f'{player1.name.upper()} WON THE GAME, CONGRATULATIONS!!!')
        time.sleep(10)
        input()

    else:
        if WAIT_INPUT:
            input()
        if SPECIAL_ROUND:
            time.sleep(WAIT_TIME_WAR)
        else:
            time.sleep(WAIT_TIME)
            
        clear_output(wait=True)
        os.system('cls')



# TEST STUFF HERE



# In[ ]:




