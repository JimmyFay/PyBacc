from models import *
from engine import *
#players=2
#engine=GameEngine(players) #controlls num of players
lobby=Lobby()
p=[]
#print(lobby.state)
while lobby.state==GameState.LOBBY:
    comm=input()
    lobby.play(comm)
#print("between lobby")
engine=GameEngine(lobby.players)
run =True
while run:
    comm=input()
    engine.play(comm)