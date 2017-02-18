#Riley Kunkel
#2143 OOP
#Program 1- War 
#2-17-17


# -*- coding: utf-8 -*-
import os
import random
import time

#Source: http://codereview.stackexchange.com/questions/82103/ascii-fication-of-playing-cards

CARD = """\
┌───────┐
│{}     │
│       │
│   {}  │
│       │
│     {}│
└───────┘
""".format('{trank:^2}', '{suit: <2}', '{brank:^2}')

TEN = """\
┌───────┐
│{}    │
│       │
│   {}  │
│       │
│    {}│
└───────┘
""".format('{trank:^3}', '{suit: <2}', '{brank:^3}')

FACECARD = """\
┌───────┐
│{}│
│       │
│   {}  │
│       │
│{}│
└───────┘
""".format('{trank:<7}', '{suit: <2}', '{brank:>7}')

HIDDEN_CARD = """\
┌───────┐
│░░░░░░░│
│░░░░░░░│
│░░░░░░░│
│░░░░░░░│
│░░░░░░░│
└───────┘
"""

class Card(object):
    
    def __init__(self, suit, rank):
        """
        :param suit: The face of the card, e.g. Spade or Diamond
        :param rank: The value of the card, e.g 3 or King
        """

        self.ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King","Ace"]



        self.card_values = {
            '2': 2,
            '3': 3,
            '4': 4,
            '5': 5,
            '6': 6,
            '7': 7,
            '8': 8,
            '9': 9,
            '10': 10,
            'Jack': 11,
            'Queen': 12,
            'King': 13,
            'Ace': 14  
        }

        self.str_values = {
            '2': CARD,
            '3': CARD,
            '4': CARD,
            '5': CARD,
            '6': CARD,
            '7': CARD,
            '8': CARD,
            '9': CARD,
            '10': TEN,
            'Jack': FACECARD,
            'Queen': FACECARD,
            'King': FACECARD,
            'Ace': FACECARD,  # value of the ace is high until it needs to be low
        }

        self.suits = ['Spades','Hearts','Diamonds','Clubs']

        self.symbols = {
            'Spades':   '♠',
            'Diamonds': '♦',
            'Hearts':   '♥',
            'Clubs':    '♣',
        }


        if type(suit) is int:
            self.suit = self.suits[suit]
        else:
            self.suit = suit.capitalize()
        self.rank = str(rank)
        self.symbol = self.symbols[self.suit]
        self.points = self.card_values[str(rank)]
        self.ascii = self.__str__()
    

    def __str__(self):
        symbol = self.symbols[self.suit]
        trank = self.rank+symbol
        brank = symbol+self.rank
        return self.str_values[self.rank].format(trank=trank, suit=symbol,brank=brank)
           
    def __cmp__(self,other):
        return self.points < other.points 
   
    # Python3 wasn't liking the __cmp__ to sort the cards, so 
    # documentation told me to use the __lt__ (less than) 
    # method.
    def __lt__(self,other):
        return self.__cmp__(other)

"""
@Class Deck 
@Description:
    This class represents a deck of cards. 
@Methods:
    pop_cards() - removes a card from top of deck
    add_card(card) - adds a card to bottom of deck
    shuffle() - shuffles deck
    sort() - sorts the deck based on value, not suit (could probaly be improved based on need)
"""       
class Deck(object):
    def __init__(self):
        #assume top of deck = 0th element
        self.cards = []
        for suit in range(4):
            for rank in ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King","Ace"]:
                self.cards.append(Card(suit,rank))
                
    def __str__(self):
        res = []
        for card in self.cards:
            res.append(str(card))
        return "".join(res)
    
    def pop_card(self):
        return self.cards.pop(0)
        
    def add_card(self,card):
        self.cards.append(card)
        
    def shuffle(self):
        random.shuffle(self.cards)
    
    def sort(self):
        self.cards = sorted(self.cards)

class Hand(list):
    def __init__(self, cards=None):
        """Initialize the class"""
        super().__init__()
        if (cards is not None):
            self._list = list(cards)
        else:
            self._list = []
    
    def __str__(self):
        return self.join_lines()

    def join_lines(self):
        """
        Stack strings horizontally.
        This doesn't keep lines aligned unless the preceding lines have the same length.
        :param strings: Strings to stack
        :return: String consisting of the horizontally stacked input
        """
        liness = [card.ascii.splitlines() for card in self._list]
        return '\n'.join(''.join(lines) for lines in zip(*liness))
        
    def add(self,card):
        self._list.append(card)
        
    def sort(self):
        self._list = sorted(self._list)
        
    def __getitem__(self,key):
        return self._list[key]
    
    def shuff(self):
        random.shuffle(self._list)
   
    

#Prints Hands To Screen
def Step1(ac):
    k = 1
    j = 1
    print("Computer" , len(H1._list))
    while (k <= ac):
        if k%2 == 0:
            print(HIDDEN_CARD)
        else:
            print(H1[-k])
        k = k+1
    time.sleep(1)
    print("Player" , len(H2._list))
    while (j <= ac):
        if j%2 == 0:
            print(HIDDEN_CARD)
        else:
            print(H2[-j])
        j = j+1
    Step2(ac)

#Determine Win Lose Or War 
def Step2(ac):
    h1p = 0
    h2p = 0
    x = 1
    y = 1
    h1p = H1[-ac].points
    h2p = H2[-ac].points
    time.sleep(2)
    if h1p < h2p: #if Player Wins
        for x in range(ac):
            H2.add(H1[-x])
            H1._list.remove(H1[-x])
        print("Player wins the hand!")
        H1.shuff()
        H2.shuff()
        time.sleep(.5)
        os.system('clear')  # For Linux/OS X
        Step1(1)

    elif h2p < h1p: #if Computer Wins
        for y in range(ac):
            H1.add(H2[-y])
            H2._list.remove(H2[-y])
        print("Computer wins the hand!")
        H1.shuff()
        H2.shuff()
        time.sleep(.5)
        os.system('clear')  # For Linux/OS X
        Step1(1)

    else: #Tie
        print("We have a Tie!")
        print("Time for War")
        time.sleep(.5)
        Step1(ac + 2)
        

#Create and shuffle deck
D = Deck()
D.shuffle()

#Create Hand1  
H1 = Hand()

#Create Hand2
H2 = Hand()

#Add 26 Cards to Each Players Deck
for i in range(26):
    H1.add(D.pop_card())
    H2.add(D.pop_card())
       
ac = 1
#CALLS
Step1(ac)









