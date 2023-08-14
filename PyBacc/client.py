import socket
import select
import pickle
import sys
#from _thread import *
import threading
import pygame
import json
from models import*
from engine import*



s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#server = "100.73.165.100"
#server="172.31.196.50"
port = 11306
server="2.tcp.ngrok.io"
#port=22189
addr = (server, port)

pygame.init()
w=1280
h=720
pygame.display.set_caption('Pybacc')
screen=pygame.display.set_mode((w,h))
clock=pygame.time.Clock()
SERVER_MSG=pygame.USEREVENT+1
data=[]
players=[]
lobbyNo=0

name=''
def connect():
    try:
        #print("Trying to connect")
        s.connect(addr)
        return s.recv(2048).decode()
    except:
        pass

def inputThread():
    while True:
        message=sys.stdin.readline()
        s.send(str.encode(message))
def socketThread():
    while True:
        try:
            #a=b'#*#'
            #m=b''
            #while a not in m:
                #m+=s.recv(2048*2)
            #print(sys.getsizeof(m))
            #message=pickle.loads(m)
            #if type(message)==str:
             #   message=message[:-3]
            size=s.recv(4)
            size2=int.from_bytes(size,'big')
            print("size is: "+str(size2))
            m=s.recv(2048*2)
            print("size of message is "+str(sys.getsizeof(m)))
            message=pickle.loads(m)
            pygame.event.post(pygame.event.Event(SERVER_MSG))
            data.append(message)
            print(message)
            #print(message)
            #m=pickle.loads(message)
        except BlockingIOError:
            pass
def send(socket,msg):
    m=pickle.dumps(msg)
    socket.send(m)
class TextInput(pygame.sprite.Sprite):
    def __init__(self,x,y,width=100,height=50,color=(10,10,10),bgcolor=(60,60,60),scolor=(90,90,90)):
        super().__init__()
        self.text_value=""
        self.isSelected=False
        self.color=color
        self.bgcolor=bgcolor
        self.scolor=scolor
        
        self.font=pygame.font.Font(None,20)
        self.text=self.font.render(self.text_value,True,self.color)
        self.bg=pygame.Rect(x,y,width,height)
    def update_text(self,new_text):
        temp=self.font.render(new_text,True,self.color)
        if temp.get_rect().width>=(self.bg.width-20): #text bigger than input box
            return
        self.text_value=new_text
        self.text=temp
    def render(self,display):
        self.pos=self.text.get_rect(center=(self.bg.x + self.bg.width/2,self.bg.y + self.bg.height/2))
        if self.isSelected:
            pygame.draw.rect(display,self.scolor,self.bg)
        else:
            pygame.draw.rect(display,self.bgcolor,self.bg)
        display.blit(self.text,self.pos)
    def update(self):
        pass
class Button(pygame.sprite.Sprite):
    def __init__(self,x,y,width,height,buttonText):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color="red"
        self.buttonSurface=pygame.Surface((self.width,self.height))
        self.buttonRect=pygame.Rect(self.x,self.y,self.width,self.height)
        self.buttonSurf=pygame.font.Font(None,20).render(buttonText,True,(10,10,10))
        self.buttonSurface.fill(self.color)
        self.buttonSurface.blit(self.buttonSurf,[self.buttonRect.width/2 - self.buttonSurf.get_rect().width/2,self.buttonRect.height/2 - self.buttonSurf.get_rect().height/2])
    def render(self,display):
        display.blit(self.buttonSurface,self.buttonRect)     
    def changeColor(self,display,color):
        self.buttonSurface.fill(color)
        self.color=color
        self.buttonSurface.blit(self.buttonSurf, [self.buttonRect.width/2-self.buttonSurf.get_rect().width/2,self.buttonRect.height/2-self.buttonSurf.get_rect().height/2])
        self.render(display)
    def changeText(self,display,text):
        self.buttonSurface.fill(self.color)
        self.buttonSurf=pygame.font.Font(None,20).render(text,True,(10,10,10))
        self.buttonSurface.blit(self.buttonSurf, [self.buttonRect.width/2-self.buttonSurf.get_rect().width/2,self.buttonRect.height/2-self.buttonSurf.get_rect().height/2])
        self.render(display)
class Label(pygame.sprite.Sprite):
    def __init__(self,x,y,width=100,height=50,tColor=(10,10,10)):
        super().__init__()
        self.text_value=""
        self.tColor=tColor
        self.font=pygame.font.Font(None,20)
        self.text=self.font.render(self.text_value,True,self.tColor)
        self.bg=pygame.Rect(x,y,width,height)
    def update_text(self,new_text):
        temp=self.font.render(new_text,True,self.tColor)
        self.text_value=new_text
        self.text=temp
    def render(self,display):
        self.pos=self.text.get_rect(center=(self.bg.x + self.bg.width/2,self.bg.y + self.bg.height/2))
        #pygame.draw.rect(display,None,self.bg)
        display.blit(self.text,self.pos)
    def update(self):
        pass
def nameScreen():
    global name
    run=True
    screen.fill("purple")
    all=pygame.sprite.Group()
    inputBox=(TextInput(x=100,y=100,width=200))
    all.add(inputBox)
    #code for text
    text=pygame.font.Font(None,20).render("Enter Username here",True,(10,10,10))
    tRect=text.get_rect()
    tRect.center=(inputBox.bg.centerx,inputBox.bg.centery-(inputBox.bg.height//2+tRect.height//2))
    screen.blit(text,tRect)
    #button text
    button=Button(inputBox.bg.centerx+inputBox.bg.width//2,inputBox.bg.centery-inputBox.bg.height//2,50,50,"Enter")
    screen.blit(button.buttonSurface,button.buttonRect)
    while run:
        #events/or inputs
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type==pygame.MOUSEBUTTONDOWN:
                if inputBox.bg.collidepoint(event.pos):
                   inputBox.isSelected=True
                if button.buttonRect.collidepoint(event.pos):
                    run=False
                    name=inputBox.text_value
                    print("Sending: "+name)
                    s.send(str.encode(name))
                    break
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_BACKSPACE:
                    inputBox.update_text(inputBox.text_value[:-1])
                if event.key == pygame.K_RETURN:
                    run=False
                    name=inputBox.text_value
                    print("Sending: "+name)
                    s.send(str.encode(name))
                    break
            if event.type==pygame.TEXTINPUT:
                inputBox.update_text(inputBox.text_value+event.text)
        #logic upddate

        #graphics update
        inputBox.update()
        inputBox.render(screen)
        pygame.display.flip()
        clock.tick(60)
def selLobbyScreen():
    global lobbyNo
    run=True
    screen.fill("grey")
    text=pygame.font.Font(None,20).render("LOBBY SELECT SCREEN",True,(10,10,10))
    tRect=text.get_rect()
    tRect.center=(w//2,h//2)
    screen.blit(text,tRect)
    label=(Label(x=500,y=500))
    lobbies=pygame.sprite.Group()
    wait=False
    count=0
    #label.update_text("")
    while run:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type==pygame.MOUSEBUTTONDOWN:
                if button.buttonRect.collidepoint(event.pos):
                    run=False
                    print("sending: "+"New")
                    s.send(str.encode("New"))
                    players.append(Player(name))
                    lobbyNo=count+1
                    break
                for a in lobbies:
                    if a.bg.collidepoint(event.pos):
                        print("sending: "+str(count))
                        s.send(str.encode(str(count)))
                        run=False
                        num=a.text_value.split(':',1)
                        num=num[0].split(' ',1)
                        lobbyNo=int(num[1])
                        break
            if event.type==SERVER_MSG:
                #screen.fill("green")
                print('about to pop')
                d=data.pop(0)
                print(d)
                if type(d)==int: #default new lobby
                    label.update_text("No one here! Starting your new lobby...")
                    label.render(screen)
                    run=False
                    wait=True
                    players.append(Player(name))
                    if d!=0:
                        count+=1
                        lobbyNo=count
                    break
                else:
                    label.update_text("Available Lobbies:")
                    label.render(screen)
                    times=1
                    count=int(d.pop(0))
                    for x in d:
                        z=(Label(x=500,y=500+(50*times)))
                        z.update_text(x)
                        z.render(screen)
                        lobbies.add(z)
                        times+=1
                    button=Button(500,500+(50*times),75,50,"New Lobby")
                    screen.blit(button.buttonSurface,button.buttonRect)
        pygame.display.flip()
        clock.tick(60)
    if wait:
        pygame.time.wait(4000)
def lobScreen():
    global lobbyNo
    global name
    global players
    run=True
    alls=(pygame.sprite.Group())
    screen.fill("green")
    title=(Label(x=500,y=70))
    alls.add(title)
    #title.render(screen)
    title.update_text("LOBBY "+str(lobbyNo)+": "+str(len(players))+" online.")
    nextButton=Button(w//2,600,50,50,"Start")
    #screen.blit(nextButton.buttonSurface,nextButton.buttonRect)
    nextButton.render(screen)
    alls.add(nextButton)
    playerNameList=(pygame.sprite.Group())
    #code for list of active players in lobby
    count=0
    for x in players:
        y=Label(x=500,y=100+(count*50))
        if x.name==name:
            #print("name is "+name)
            y.update_text(x.name+" (You)")
        else:
            y.update_text(x.name)
        y.render(screen)
        playerNameList.add(y)
        #alls.add(y)
        count+=1
    while run:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type==pygame.MOUSEBUTTONDOWN: #start game
                if nextButton.buttonRect.collidepoint(event.pos):
                    run=False
                    s.send(str.encode("Start"))
                    break
            if event.type==SERVER_MSG:
                print('about to pop')
                d=data.pop(0)
                print(d)
                if type(d)==list: #just joined a pre-existing lobby
                    title.update_text("LOBBY: "+str(lobbyNo)+" "+str(len(d))+" online.")
                    #title.render(screen)
                    for z in d: 
                        players.append(Player(z))
                        y=Label(x=500,y=100+(count*50))
                        if z==name:
                            y.update_text(z+" (You)")
                        else:
                            y.update_text(z)
                        y.render(screen)
                        count+=1
                        playerNameList.add(y)
                        #alls.add(y)
                elif d=="Starting": #everyone else in the lobbys cue to start
                    s.send(str.encode("Starting"))
                    run=False
                    break
                elif d.split(' ',1)[0]=='Removed': #removing player
                    Lname=d.split(' ',1)[1]
                    print(Lname+" left") 
                    for x in players: #remove old player
                        if x.name==Lname:
                            players.remove(x)
                            break
                    c=0
                    for x in playerNameList:
                        if x.text_value==Lname:
                            playerNameList.remove(x)
                            count=count-1
                            break
                        c+=1
                    for x in playerNameList:
                        if c>0:
                            c+=-1
                        else:
                            x.bg.y+=-50
                    title.update_text("LOBBY "+str(lobbyNo)+": "+str(len(players))+" online.")
                else:
                    print("Someone new joined")
                    #print(d.split(' ',1))
                    players.append(Player(d))
                    y=Label(x=500,y=100+(count*50))
                    if d==name:
                        y.update_text(d+" (You)")
                    else:
                        y.update_text(d)
                    y.render(screen)
                    count+=1
                    playerNameList.add(y)
                    #alls.add(y)
                    title.update_text("LOBBY "+str(lobbyNo)+": "+str(len(players))+" online.")
        screen.fill("green")
        title.update()
        for b in alls:
            b.render(screen)
        for b in playerNameList:
            b.render(screen)
        #title.render(screen)
        pygame.display.flip()
        clock.tick(60)
def gameScreen():
    #bg=pygame.image.load("pics/gametable.jpg")
    global lobbyNo
    global name
    global players
    run=True
    myTurn=False
    cardClicked=False
    selectedCard=None
    discClicked=False
    deckClicked=False
    action=False
    turn=0
    bTurn=0
    selfDex=0
    count=0
    round=1
    d1=0
    d2=0
    deck=None
    discard=None
    positions=[]
    playerCards=[]
    otherCards=[]
    dice=[d1,d2]
    pos=[[w//2,h-70],[w//2,70],[w//2-500,h//2],[w//2+500,h//2],[w//2-250,h//4],[w//2+250,h//4],[w//2-250,h//4*3],[w//2+250,h//4*3]]
    for x in players:
        if x.name==name: #found self
            selfDex=count
            break
        else: #not self
            count+=1
    screen.fill("blue")
    turnB=Button(w-100,h-100,50,50,"Next")
    turnB.render(screen)
    turnIndicator=Label(x=10,y=10)
    roundIndicator=Label(x=w//2,y=10)
    diceIndicator=Label(w//2,h//2+50)
    diceIndicator.update_text("Dice are: "+str(d1)+","+str(d2))
    scoreIndicator=Label(pos[0][0]+10,pos[0][1]+15)
    totalIndicator=Label(pos[0][0]+10,pos[0][1]-15)
    titleIndicator=Label(pos[0][0]+10,pos[0][1])
    deckB=Button(w//2+20,h//2,50,50,"Deck")
    discardB=Button(w//2-70,h//2,50,50,"Discard")
    deckB.render(screen)
    discardB.render(screen)
    selfB=Button(pos[0][0],pos[0][1],50,50,"You")
    positions.append([selfB,selfDex])
    def updateIndicators():
        scoreIndicator.update_text("Score: "+str(players[selfDex].score))
        totalIndicator.update_text("Total: "+str(players[selfDex].total))
        titleIndicator.update_text(str(players[selfDex].title))
        scoreIndicator.bg.x=pos[0][0]+10+scoreIndicator.text.get_width()//2
        totalIndicator.bg.x=pos[0][0]+10+totalIndicator.text.get_width()//2
        titleIndicator.bg.x=pos[0][0]+10+titleIndicator.text.get_width()//2
        diceIndicator.update_text("Dice are: "+str(d1)+","+str(d2))
    def packager(com):
        message=[]
        message.append(com)
        message.append(players)
        message.append(deck)
        message.append(discard)
        dice=[d1,d2]
        message.append(dice)
        return(message)
    if selfDex==0: #you are the original creator of lobby
        turnIndicator.update_text("It is YOUR turn!")
        turnB.changeColor(screen,"green")
        myTurn=True
        deck=Deck()
        deck.shuffle()
        discard=DPile()
        discard.add(deck.deal())
        #deal out cards to the players and send out list of players
        for x in players:
            for a in range(2):
                x.add(deck.deal())
            x.update()
            print(x)
        updateIndicators()
        discardB.changeText(screen,discard.top())
        print("sending init")
        message=packager("INIT")
        #m=pickle.dumps(message)
        #print("Size of data is: "+str(sys.getsizeof(message)))
        #print("Pickle Size of data is: "+str(sys.getsizeof(m)))
        #m=pickle.dumps(message)
#        #s.send(m)
        send(s,message)
        match len(players):
            case 2:
                p2=Button(pos[1][0],pos[1][1],50,50,players[1].name)
                positions.append([p2,1])
            case 3:
                p2=Button(pos[4][0],pos[4][1],50,50,players[1].name)
                p3=Button(pos[5][0],pos[5][1],50,50,players[2].name)
                positions.append([p2,1])
                positions.append([p3,2])
            case 4:
                p2=Button(pos[2][0],pos[2][1],50,50,players[1].name)
                p3=Button(pos[1][0],pos[1][1],50,50,players[2].name)
                p4=Button(pos[3][0],pos[3][1],50,50,players[3].name)
                positions.append([p2,1])
                positions.append([p3,2])
                positions.append([p4,3])
            case 5:
                p2=Button(pos[6][0],pos[6][1],50,50,players[1].name)
                p3=Button(pos[4][0],pos[4][1],50,50,players[2].name)
                p4=Button(pos[5][0],pos[5][1],50,50,players[3].name)
                p5=Button(pos[7][0],pos[7][1],50,50,players[4].name)
                positions.append([p2,1])
                positions.append([p3,2])
                positions.append([p4,3])
                positions.append([p5,4])
            case 6:
                p2=Button(pos[6][0],pos[6][1],50,50,players[1].name)
                p3=Button(pos[4][0],pos[4][1],50,50,players[2].name)
                p4=Button(pos[1][0],pos[1][1],50,50,players[3].name)
                p5=Button(pos[5][0],pos[5][1],50,50,players[4].name)
                p6=Button(pos[7][0],pos[7][1],50,50,players[5].name)
                positions.append([p2,1])
                positions.append([p3,2])
                positions.append([p4,3])
                positions.append([p5,4])
                positions.append([p6,5])
            case 7:
                p2=Button(pos[6][0],pos[6][1],50,50,players[1].name)
                p3=Button(pos[2][0],pos[2][1],50,50,players[2].name)
                p4=Button(pos[4][0],pos[4][1],50,50,players[3].name)
                p5=Button(pos[5][0],pos[5][1],50,50,players[4].name)
                p6=Button(pos[3][0],pos[3][1],50,50,players[5].name)
                p7=Button(pos[7][0],pos[7][1],50,50,players[6].name)
                positions.append([p2,1])
                positions.append([p3,2])
                positions.append([p4,3])
                positions.append([p5,4])
                positions.append([p6,5])
                positions.append([p7,6])
            case 8:
                p2=Button(pos[6][0],pos[6][1],50,50,players[1].name)
                p3=Button(pos[2][0],pos[2][1],50,50,players[2].name)
                p4=Button(pos[4][0],pos[4][1],50,50,players[3].name)
                p5=Button(pos[1][0],pos[1][1],50,50,players[4].name)
                p6=Button(pos[5][0],pos[5][1],50,50,players[5].name)
                p7=Button(pos[3][0],pos[3][1],50,50,players[6].name)
                p8=Button(pos[7][0],pos[7][1],50,50,players[7].name)
                positions.append([p2,1])
                positions.append([p3,2])
                positions.append([p4,3])
                positions.append([p5,4])
                positions.append([p6,5])
                positions.append([p7,6])
                positions.append([p8,7])
            case _:
                print("invalid or One players")
    else:#not the OG of lobby
        turnIndicator.update_text("It is "+players[0].name+"\'s turn!")
        backupPlayers=[]
        #backupPlayers.append(players[selfDex])
        y=selfDex
        for x in players[selfDex:]:
            backupPlayers.append([x,y])
            y+=1
        y=0
        for x in players[:selfDex]:
            backupPlayers.append([x,y])
            y+=1
        #backupPlayers=players[selfDex:]+players[:selfDex]
        for x in backupPlayers:
            print(x[0].name)
        match len(players):
            case 2:
                p2=Button(pos[1][0],pos[1][1],50,50,backupPlayers[1][0].name)
                positions.append([p2,backupPlayers[1][1]])
            case 3:
                p2=Button(pos[4][0],pos[4][1],50,50,backupPlayers[1][0].name)
                p3=Button(pos[5][0],pos[5][1],50,50,backupPlayers[2][0].name)
                positions.append([p2,backupPlayers[1][1]])
                positions.append([p3,backupPlayers[2][1]])
            case 4:
                p2=Button(pos[2][0],pos[2][1],50,50,backupPlayers[1][0].name)
                p3=Button(pos[1][0],pos[1][1],50,50,backupPlayers[2][0].name)
                p4=Button(pos[3][0],pos[3][1],50,50,backupPlayers[3][0].name)
                positions.append([p2,backupPlayers[1][1]])
                positions.append([p3,backupPlayers[2][1]])
                positions.append([p4,backupPlayers[3][1]])
            case 5:
                p2=Button(pos[6][0],pos[6][1],50,50,backupPlayers[1][0].name)
                p3=Button(pos[4][0],pos[4][1],50,50,backupPlayers[2][0].name)
                p4=Button(pos[5][0],pos[5][1],50,50,backupPlayers[3][0].name)
                p5=Button(pos[7][0],pos[7][1],50,50,backupPlayers[4][0].name)
                positions.append([p2,backupPlayers[1][1]])
                positions.append([p3,backupPlayers[2][1]])
                positions.append([p4,backupPlayers[3][1]])
                positions.append([p5,backupPlayers[4][1]])
            case 6:
                p2=Button(pos[6][0],pos[6][1],50,50,backupPlayers[1][0].name)
                p3=Button(pos[4][0],pos[4][1],50,50,backupPlayers[2][0].name)
                p4=Button(pos[1][0],pos[1][1],50,50,backupPlayers[3][0].name)
                p5=Button(pos[5][0],pos[5][1],50,50,backupPlayers[4][0].name)
                p6=Button(pos[7][0],pos[7][1],50,50,backupPlayers[5][0].name)
                positions.append([p2,backupPlayers[1][1]])
                positions.append([p3,backupPlayers[2][1]])
                positions.append([p4,backupPlayers[3][1]])
                positions.append([p5,backupPlayers[4][1]])
                positions.append([p6,backupPlayers[5][1]])
            case 7:
                p2=Button(pos[6][0],pos[6][1],50,50,backupPlayers[1][0].name)
                p3=Button(pos[2][0],pos[2][1],50,50,backupPlayers[2][0].name)
                p4=Button(pos[4][0],pos[4][1],50,50,backupPlayers[3][0].name)
                p5=Button(pos[5][0],pos[5][1],50,50,backupPlayers[4][0].name)
                p6=Button(pos[3][0],pos[3][1],50,50,backupPlayers[5][0].name)
                p7=Button(pos[7][0],pos[7][1],50,50,backupPlayers[6][0].name)
                positions.append([p2,backupPlayers[1][1]])
                positions.append([p3,backupPlayers[2][1]])
                positions.append([p4,backupPlayers[3][1]])
                positions.append([p5,backupPlayers[4][1]])
                positions.append([p6,backupPlayers[5][1]])
                positions.append([p7,backupPlayers[6][1]])
            case 8:
                p2=Button(pos[6][0],pos[6][1],50,50,backupPlayers[1][0].name)
                p3=Button(pos[2][0],pos[2][1],50,50,backupPlayers[2][0].name)
                p4=Button(pos[4][0],pos[4][1],50,50,backupPlayers[3][0].name)
                p5=Button(pos[1][0],pos[1][1],50,50,backupPlayers[4][0].name)
                p6=Button(pos[5][0],pos[5][1],50,50,backupPlayers[5][0].name)
                p7=Button(pos[3][0],pos[3][1],50,50,backupPlayers[6][0].name)
                p8=Button(pos[7][0],pos[7][1],50,50,backupPlayers[7][0].name)
                positions.append([p2,backupPlayers[1][1]])
                positions.append([p3,backupPlayers[2][1]])
                positions.append([p4,backupPlayers[3][1]])
                positions.append([p5,backupPlayers[4][1]])
                positions.append([p6,backupPlayers[5][1]])
                positions.append([p7,backupPlayers[6][1]])
                positions.append([p8,backupPlayers[7][1]])
            case _:
                print("invalid players")    
        for y in backupPlayers: #finds OG player and makes them yellow
            if y[0].name==players[0].name:
                break
            else: bTurn+=1
    diceIndicator.render(screen)
    turnIndicator.render(screen)
    scoreIndicator.render(screen)
    titleIndicator.render(screen)
    totalIndicator.render(screen)
    for x in positions: #renders players
        x[0].render(screen)
        if x[1]!=selfDex:
            cCount=0
            for y in players[x[1]].hand: #puts in all the right cards to othercards
                card=Button(x[0].x-((15*len(players[x[1]].hand))/2)+(35*cCount),x[0].y+60,30,50,"Back")
                cCount+=1
                otherCards.append(card)
    #render player cards
    def drawCards():
        cards=[]
        print(cardClicked)
        print(selectedCard)
        cCount=0
        for x in players[selfDex].hand:
            card=Button(pos[0][0]-((15*len(players[selfDex].hand))/2)+(35*cCount),pos[0][1]-60,30,50,str(x.stave)+","+str(x.value))
            cCount+=1
            cards.append(card)
        if selectedCard!=None:
            cards[selectedCard].changeColor(screen,"yellow")
        return(cards)
    playerCards=drawCards()
    for x in playerCards:
        x.render(screen)
    for x in otherCards:
        x.render(screen)
    while round<6:
        screen.fill("blue")
        #screen.blit(bg,(0,0))
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type==SERVER_MSG:
                print('about to pop')
                d=data.pop(0)
                print(d)
                if d[0]=="Next": #update turn
                    count=0
                    for x in d[1]:
                        players[count]=x
                        count+=1
                    deck=d[2]
                    discard=d[3]
                    d1=d[4][0]
                    d2=d[4][1]
                    diceIndicator.update_text("Dice are: "+str(d1)+","+str(d2))
                    discardB.changeText(screen,discard.top())
                    otherCards=[]
                    for x in positions: #renders players
                        if x[1]!=selfDex:
                            cCount=0
                            for y in players[x[1]].hand: #puts in all the right cards to othercards
                                card=Button(x[0].x-((15*len(players[x[1]].hand))/2)+(35*cCount),x[0].y+60,30,50,"Back")
                                cCount+=1
                                otherCards.append(card)
                    if turn==(len(players)-1):#loop it around
                        turn=0
                        round+=1
                    else:
                        turn+=1
                    if bTurn==(len(players)-1):
                        bTurn=0
                    else:
                        bTurn+=1
                    if turn==selfDex: #its now your turn
                        turnB.changeColor(screen,"green")
                        selfB.changeColor(screen,"yellow")
                        positions[-1][0].changeColor(screen,"red")
                        myTurn=True
                        action=False
                        for x in playerCards:
                            x.render(screen)
                    else: #someone elses turn, undo last turns yellow and make current turn yellow
                        print("turning "+str(bTurn)+" yello")
                        positions[bTurn][0].changeColor(screen,"yellow")
                        if bTurn==0:
                            positions[-1][0].changeColor(screen,"red")
                        else:
                            positions[bTurn-1][0].changeColor(screen,"red")
                elif d[0]=='INIT': #got the signal to init the game variables
                    print("Game initialized")
                    count=0
                    for x in d[1]:
                        players[count]=x
                        count+=1
                    deck=d[2]
                    discard=d[3]
                    discardB.changeText(screen,discard.top())
                    print("making "+str(bTurn)+" yelo")
                    positions[bTurn][0].changeColor(screen,"yellow")
                    for x in positions: #renders other players cards
                        if x[1]!=selfDex:
                            cCount=0
                            for y in players[x[1]].hand:
                                card=Button(x[0].x-((15*len(players[x[1]].hand))/2)+(35*cCount),x[0].y+60,30,50,"Back")
                                cCount+=1
                                otherCards.append(card)
                    cCount=0
                    playerCards=drawCards()
                    updateIndicators()
            if event.type==pygame.MOUSEBUTTONDOWN:
                cardClicked=False
                if turnB.buttonRect.collidepoint(event.pos) and myTurn: #turn button clicked
                    myTurn=False
                    turnB.changeColor(screen,"red")
                    selfB.changeColor(screen,"red")
                    if turn==(len(players)-1):#loop it around
                        turn=0
                        round+=1
                        d1=random.randint(1,6)
                        d2=random.randint(1,6)
                        diceIndicator.update_text("Dice are: "+str(d1)+","+str(d2))
                        if d1==d2: #put the cards back
                            for x in players:
                                count=0
                                for y in x.hand:
                                    discard.add(y)
                                    count+=1
                                x.hand=[]
                                while count>0:
                                    x.add(deck.deal())
                                    count+=-1
                            players[selfDex].update()
                            playerCards=drawCards()
                            discardB.changeText(screen,discard.top())
                            updateIndicators()
                    else:
                        turn+=1
                    if len(players)!=1:
                        bTurn+=1
                    print("turning "+str(bTurn)+" yello")
                    positions[bTurn][0].changeColor(screen,"yellow")
                    print("sending: Next")
                    #s.send(str.encode("Next"))
                    message=packager("Next")
                    #print("Size of data is: "+str(sys.getsizeof(message)))
                    #print("Pickle Size of data is: "+str(sys.getsizeof(pickle.dumps(message))))
                    #m=json.dumps(message)
#                    #s.send(m)
                    send(s,message)
                    if turn==selfDex: #this is literally just for single player games
                        turnB.changeColor(screen,"green")
                        selfB.changeColor(screen,"yellow")
                        myTurn=True
                        action=False
                        #round+=1
                y=0
                if action==False: #player did not previously make amove
                    for x in playerCards: #see if a card was clicked
                        if x.buttonRect.collidepoint(event.pos) and myTurn:
                            cardClicked=True
                            selectedCard=y
                            if discClicked: #snipe
                                print("sniped") 
                                temp=discard.deal()
                                discard.add(players[selfDex].drop(selectedCard))
                                players[selfDex].add(temp)
                                discClicked=False
                                discardB.changeColor(screen,"red")
                                cardClicked=False
                                selectedCard=None
                                discardB.changeText(screen,discard.top())
                                action=True
                            elif deckClicked: #swap
                                discard.add(players[selfDex].drop(selectedCard))
                                players[selfDex].add(deck.deal())
                                selectedCard=None
                                discardB.changeText(screen,discard.top())
                                deckClicked=False
                                deckB.changeColor(screen,"red")
                                action=True
                            players[selfDex].update()
                            playerCards=drawCards()
                            updateIndicators()
                            break
                        y+=1             
                    if cardClicked==False: #card not clicked see if its anything else
                        if discardB.buttonRect.collidepoint(event.pos) and myTurn: #discard clicked
                            if deckClicked:
                                deckB.changeColor(screen,"red")
                                deckClicked=False  
                            if selectedCard!=None:#swap with selected card
                                temp=discard.deal()
                                discard.add(players[selfDex].drop(selectedCard))
                                players[selfDex].add(temp)
                                selectedCard=None
                                cardClicked=False
                                players[selfDex].update()
                                playerCards=drawCards()
                                discardB.changeText(screen,discard.top())
                                updateIndicators()
                                action=True
                            else:#no selected card to swap with
                                discardB.changeColor(screen,"yellow")
                                discClicked=True  
                        elif deckB.buttonRect.collidepoint(event.pos) and myTurn: #deck clicked
                            if discClicked:
                                discardB.changeColor(screen,"red")
                                discClicked=False  
                            if deckClicked==True: #gained card
                                players[selfDex].add(deck.deal())
                                playerCards=drawCards()
                                updateIndicators()
                                deckClicked=False
                                deckB.changeColor(screen,"red")
                                action=True
                            elif selectedCard!=None: #swap card
                                discard.add(players[selfDex].drop(selectedCard))
                                players[selfDex].add(deck.deal())
                                selectedCard=None
                                playerCards=drawCards()
                                discardB.changeText(screen,discard.top())
                                updateIndicators()
                                action=True
                            else:
                                deckB.changeColor(screen,"yellow")
                                deckClicked=True
                        #deselecting
                        #no cards were clicked, deselct old card
                        else:
                            if selectedCard!=None:
                                selectedCard=None
                                playerCards=drawCards()
                            if discClicked:
                                discClicked=False
                                discardB.changeColor(screen,"red")
                            if deckClicked:
                                deckClicked=False
                                deckB.changeColor(screen,"red")    
            #update the graphics
        if myTurn:
            turnIndicator.update_text("It is YOUR turn!")
            selfB.changeColor(screen,"yellow")
        else:
            turnIndicator.update_text("It is "+players[turn].name+"\'s turn!")
        turnIndicator.render(screen)
        roundIndicator.update_text("ROUND: "+str(round))
        roundIndicator.render(screen)
        scoreIndicator.render(screen)
        titleIndicator.render(screen)
        totalIndicator.render(screen)
        diceIndicator.render(screen)
        turnB.render(screen)
        deckB.render(screen)
        discardB.render(screen)
        for x in positions:
            x[0].render(screen)
        for x in playerCards:
            x.render(screen)
        for x in otherCards:
            x.render(screen)
        pygame.display.flip()
        clock.tick(60)
def endScreen():
    global lobbyNo
    global name
    global players
    run=True
    win=0
    for x in range(1,len(players)):
        if players[win].score==players[x].score:
            if players[win].absTotal<players[x].absTotal:
                win=x
        elif players[win].score<players[x].score:
            win=x
    winnerBanner=Label(w//2,h//2)
    winnerBanner.update_text("WINNER IS: "+players[win].name)
    while run:
        screen.fill("yellow")
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                raise SystemExit
        winnerBanner.render(screen)
        pygame.display.flip()
        clock.tick(60)
def connectScreen():
    global server
    global port
    global addr
    run=True
    hostSelect=False
    portSelect=False
    hostInput=(TextInput(x=100,y=100,width=250))
    portInput=(TextInput(x=100,y=200,width=250))
    hTip=(Label(100,70))
    pTip=(Label(100,170))
    hTip.update_text("Enter server here.")
    pTip.update_text("Enter port here.")
    hB=(Button(w//2,h//2,50,50,"Submit"))
    
    while run:
        screen.fill("sky blue")
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type==pygame.MOUSEBUTTONDOWN:
                if hostInput.bg.collidepoint(event.pos):
                   hostSelect=True
                   portSelect=False
                elif portInput.bg.collidepoint(event.pos):
                   portSelect=True
                   hostSelect=False
                else:
                    hostSelect=False
                    portSelect=False
                    if hB.buttonRect.collidepoint(event.pos):
                        server=hostInput.text_value
                        port=portInput.text_value
                        addr=(server,int(port))
                        run=False       
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_BACKSPACE:
                    if hostSelect:
                        hostInput.update_text(hostInput.text_value[:-1])
                    elif portSelect:
                        portInput.update_text(portInput.text_value[:-1])
            if event.type==pygame.TEXTINPUT:
                if hostSelect:
                    hostInput.update_text(hostInput.text_value+event.text)
                elif portSelect:
                    portInput.update_text(portInput.text_value+event.text)
        hostInput.update()
        hostInput.render(screen)
        portInput.update()
        portInput.render(screen)
        hTip.render(screen)
        pTip.render(screen)
        hB.render(screen)
        pygame.display.flip()
        clock.tick(60)
def main():
    #connectScreen()
    print(addr)
    if connect()!=None:
        s.setblocking(0)
        x=threading.Thread(target=inputThread,daemon=True)
        x.start()
        y=threading.Thread(target=socketThread,daemon=True)
        y.start()
        nameScreen()
        selLobbyScreen()
        lobScreen()
        gameScreen()
        endScreen()
        x.join()
        y.join()
    else:
        print("connect failed")
main() 
s.close()