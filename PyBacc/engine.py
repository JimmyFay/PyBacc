from enum import Enum
from models import *

class GameState(Enum):
    PLAYING=0
    ENDED=1
    LOBBY=2
class Lobby:
    players=None
    state=None
    def __init__(self):
        self.players=[]
        self.state=GameState.LOBBY
        print("Enter names to add players. When ready type \"Start\" to begin, or \"Rules\" for the rules.")
    def play(self,input):
        match input:
            case "Start":
                print("Starting")
                self.state=GameState.PLAYING
            case "Rules":
                print("...Didn't make those yet")
            case _:
                self.players.append(Player(input))
                print(input+" joined!")
class GameEngine: #everything that happens while in play state, lobby/end menu will be different classes
    deck=None
    dPile=None
    players=None
    numPlayers=None
    state=None
    currentPlayer=None
    result=None
    turns=None
    d1=None
    d2=None
    win=None

    def __init__(self,plist: list):
        self.deck=Deck()
        self.deck.shuffle()
        self.dPile=DPile()
        self.numPlayers=len(plist)
        self.players=plist
        self.turns=1
        self.win=0
        d1=0
        d2=0
        x=0
        while x<self.numPlayers:
            self.players.append(Player("Player "+(str)(x+1)))
            x+=1
        self.gDeal()
        self.currentPlayer=self.players[0]
        self.state=GameState.PLAYING
        print("Round "+str(self.turns))
        print("it is now "+str(self.currentPlayer.name)+"\'s turn.")
        print("Top card on discard pile is "+self.dPile.top())
        self.currentPlayer.display()
    def gDeal(self):
        self.dPile.add(self.deck.deal())
        for i in self.players:
            for a in range(2):
                i.add(self.deck.deal())
    def nextPlayer(self):
        x=self.players.index(self.currentPlayer)+1
        if x>(self.numPlayers-1): #end of round
            self.roll()
            self.currentPlayer=self.players[0]
            self.turns+=1
            if self.turns>5:
                print("GAME OVER")
                self.winner()
                self.state=GameState.ENDED
                return
        else:
            self.currentPlayer=self.players[x]
        print("Round "+str(self.turns))
        print("It is now "+str(self.currentPlayer.name)+"\'s turn.")
        print("Top card on discard pile is "+self.dPile.top())
        self.currentPlayer.display()
    def roll(self):
        self.d1=random.randint(1,6)
        self.d2=random.randint(1,6)
        print("Rolled a "+str(self.d1)+" and a "+str(self.d2))
        if self.d1==self.d2:
            print("Doubles! Everyone's junked.")
            self.junkAll()
        else:
            print("Everyone's safe... for now.")
    def junkAll(self):
        for x in self.players:
            count=0
            for y in x.hand:
                self.dPile.add(y)
                count+=1
            x.hand=[]
            while count>0:
                x.add(self.deck.deal())
                count+=-1
    def winner(self):
        for x in range(1,len(self.players)):
            if self.players[self.win].score==self.players[x].score:
                if self.players[self.win].absTotal<self.players[x].absTotal:
                    self.win=x
            elif self.players[self.win].score<self.players[x].score:
                self.win=x
        print("Winner is: "+self.players[self.win].name+"!")
    def swap(self,ind): #swap card from deck
        self.dPile.add(self.currentPlayer.drop(ind))
        self.currentPlayer.add(self.deck.deal())
        print(str(self.currentPlayer.name)+" Swapped from the deck.")
    def snipe(self,ind): #swap card from discard pile
        temp=self.dPile.deal()
        self.dPile.add(self.currentPlayer.drop(ind))
        self.currentPlayer.add(temp)
        print(str(self.currentPlayer.name)+" Sniped from the discard pile.")
    def gain(self): #pickup card
        self.currentPlayer.add(self.deck.deal())
        print(str(self.currentPlayer.name)+" Gains a card.")
    def hold(self): #do nothing
        print(str(self.currentPlayer.name)+" Holds.")
    
    def play(self,input): #all possible inputs from gameplay essentially
        list=input.split()
        comm=''
        index=0
        if list[-1].isnumeric(): #command has index
            index=int(list.pop())
            #print(index)          
        for x in list:
            comm=comm+x+' '
        comm=comm.strip()
        if self.state==GameState.ENDED:
            return
        match comm:
            case "show":
                self.currentPlayer.display()
            case "test":
                print("testing")
            case "inspect deck":
                self.deck.inspect()
            case "inspect discard":
                self.dPile.inspect()
            case "turn":
                self.nextPlayer()
            case "swap":
                self.swap(index)
                self.nextPlayer()
            case "snipe":
                print(index)
                self.snipe(index)
                self.nextPlayer()
            case "gain":
                self.gain()
                self.nextPlayer()
            case "hold":
                self.hold()
                self.nextPlayer()
            case "god":
                xlist=[Card(0,6),Card(0,-6),Card(1,5),Card(1,-2),Card(1,-3)]
                self.currentPlayer.godHand(xlist)
                self.nextPlayer()
            case _:
                print("default, command was:"+comm)
                return
        ##all player actions here: swap (swap card from deck), snipe (swap card from discard), gain (pickup card), hold (do nothing), fold (not implemented for now)




