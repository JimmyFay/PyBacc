from enum import Enum
import random

class Staves(Enum):
    circle=0
    triangle=1
    square=2
    zero=3
class Card:
    stave=None
    value=None
    def __init__(self,stave,value):
        self.stave=stave
        self.value=value
    def __repr__(self):
        return str(self.stave)+","+str(self.value)
class Deck:
    cards=None
    def __init__(self):
        self.cards=[]
        for s in range(3): #append all normal cards
            for v in range(1,11):
                self.cards.append(Card(s,v))
            for v in range(-10,0):
                self.cards.append(Card(s,v))
        self.cards.append(Card(3,0))
        self.cards.append(Card(3,0))
    def shuffle(self):
        random.shuffle(self.cards)
    def deal(self):
        return self.cards.pop()
    def length(self):
        return len(self.cards)
    def inspect(self):
        print("Deck: "+str(self.length())+" cards")
        for x in self.cards:
            print(str(x.stave)+","+str(x.value))
class DPile:
    cards=None
    def __init__(self):
        self.cards=[]
    def add(self,card):
        self.cards.append(card)
    def deal(self):
        return self.cards.pop()
    def inspect(self):
        print("Discard Pile:")
        for x in self.cards:
            print(str(x.stave)+","+str(x.value))
    def top(self):
        return str(self.cards[-1].stave)+","+str(self.cards[-1].value)
class Player:
    hand=None
    name=None
    total=None
    score=None
    title=None
    absTotal=None

    def __repr__(self):
        return "Player: Name= "+self.name+" Hand= "+str(self.hand)+" total= "+str(self.total)+" score= "+str(self.score)+" title= "+self.title

    def __init__(self,name):
        self.hand=[]
        self.name=name
        self.total=0
        self.score=0
        self.title="Nuhlrek"
        self.absTotal=0
    def update(self):
        self.total=0
        self.abstotal=0
        for x in self.hand:
            self.total+=x.value
            self.absTotal+=abs(x.value)
        self.handValue(self.total)
        
    def drop(self,cardInd):
        x=self.hand.pop(cardInd)
        self.update()
        return x
    def add(self,card):
        self.hand.append(card)
        self.update()
    def display(self):
        
        print(self.name+"\'s hand:")
        for x in self.hand:
            print(str(x.stave)+","+str(x.value))
        print("Total: "+str(self.total)+" Score: "+self.title+" ("+str(self.score)+")")
    def handValue(self,tot):
        cards=len(self.hand)
        vals=[]
        absvals=[]
        pairs=[]
        for x in self.hand:
            vals.append(x.value)
            absvals.append(abs(x.value))
        vals.sort()
        absvals.sort()
        if tot==0: #non nuhlrek
            if 0 in vals: #has a zero card
                if vals.count(0)==2:
                    self.score=14
                    self.title="Pure Sabacc"
                elif absvals.count(10)==4:
                    self.score=13
                    self.title="Full Sabacc"
                elif absvals.count(absvals[0])==4:
                    self.score=12
                    self.title="Fleet"
                elif cards==5 and absvals.count(absvals[1])==2 and absvals.count(absvals[-1])==2:
                    self.score=11
                    self.title="The Council"
                elif cards==3:
                    self.score=10
                    self.title="Happy Landing"
                else:
                    self.score=9
                    self.title="The Chosen One"
            else: #no zero card   
                if cards==5 and (vals.count(vals[0])==3 and vals.count(vals[-1])==2) or (vals.count(vals[0])==2 and vals.count(vals[-1])==3):
                    self.score=8
                    self.title="Rhylet" 
                elif absvals.count(absvals[0])==4 or absvals.count(absvals[-1])==4:
                    self.score=7
                    self.title="Squadron" 
                elif cards==5 and absvals[0]==1 and absvals[1]==2 and absvals[2]==3 and absvals[3]==4 and absvals[4]==10:
                    self.score=6
                    self.title="It's a Trap" 
                elif absvals[-1]-absvals[0]==3 and cards==4:
                    self.score=5
                    self.title="Straight Khyron" 
                else:
                    for v in absvals:
                        if absvals.count(v)==3:
                           self.score=4
                           self.title="Bantha's Wild"
                           return
                        elif absvals.count(v)==2:
                            if v not in pairs:
                                pairs.append(v)
                    if len(pairs)==2:
                        self.score=3
                        self.title="Rule of Two"
                    elif len(pairs)==1:
                        self.score=2
                        self.title="That's Your Sister"
                    else:
                        self.score=1
                        self.title="Sabacc"
        else: #not zero
            self.score=0
            self.title="Nuhlrek"
    
    def godHand(self,list):
        self.hand=list
        self.update()
    #WINNING HANDS:
    #pure sabacc: two zeroes --14-- 2 cards ##
    #full sabacc: 1 zero, 4 10s --13-- 5 cards ##
    #fleet: 1 zero with 4 of a kind (lower wins) --12-- 5 cards ##
    #The council: 1 zero with 2 pair (lowwer wins) --11-- 5 cards ## 
    #Happy Landing: 1 zero with 2 of a kind (lower wins) --10-- 3 cards ##
    #the chosen one: 1 zero --9-- 3+ cards ##
    #rhylet: 3 of a kind of (+/-) and 2 of a kind of the opposite polarity --8-- 5 cards ##
    #squadron: 4 of a kind --7-- 4 cards ##
    #it's a trap: 1-4(+/-) and a 10(-/+) --6-- 5 cards ##
    #straight khyron: run of 4 (lower wins) --5-- 4 cards ##
    #banthas wild: 3 of a kind (lower wins) --4-- 3+ cards ##
    #rule of two: 2 pairs (lower wins) --3-- 4+ cards ##
    #that's your sister: one pair (lower wins) --2-- 2+ cards ##
    #sabbac: zero, highest absolute value wins --1-- 2+ cards ##
    #nuhlrek: closest to zero wins (highest abs wins) --0-- 2+ cards ##