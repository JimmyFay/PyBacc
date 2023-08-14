import socket
from _thread import *
import sys
import pickle
import json
from pyngrok import ngrok
#server="100.73.165.100"
port=5555
clients=[]
lobbies=[]
names=[]
startedLobbies=[]
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server=socket.gethostbyname(socket.gethostname())
print(server)
#host="159.203.126.35"
def send(conn,msg):
    print("Sending "+str(msg))
    x=pickle.dumps(msg)
    b=sys.getsizeof(x)
    print("Pickled size is "+str(b))
    print(x)
    y=b.to_bytes(4,'big')
    a=conn.send(y+x)
        #x=x[a:]
        #print("looped")
    
    print(x[a:])
    print("sent "+str(a)+" bytes.")

try:
    s.bind(('',port))
except socket.error as e:
    str(e)
s.listen()    
print("waiting for connection")

def threaded_client(conn,addr):
    lob=0
    conn.send(str.encode("Connected."))
    reply = "Welcome: "
    #reply=str(clients[clients.index(conn.raddr)])+": "
    try: #get username here
        name = conn.recv(2048)
        name=name.decode("utf-8").strip()
        reply+=name

        if not name:
            print("Disconnected")
            remove(conn,lob)
        else:
            print(addr[0]+": "+reply)
            #print("Sending : ", reply)
        #conn.send(pickle.dumps(reply))
      #  broadcast(pickle.dumps(reply),conn) #change this from broadcast
    except:
        print("brokey")
    try: #get lobby
        if len(lobbies)<1: #No one in a lobby yet 
            #message="No lobbies have been made yet. Starting yours.\nLobby: 0"
            lobbies.append([])
            names.append([])
            lobbies[0].append(conn)
            names[0].append(name)
            lob=0
            send(conn,lob)
            #conn.send(pickle.dumps(lob)+pickle.dumps('#*#'))
        elif len(lobbies)==len(startedLobbies):#no started lobbies
            lobbies.append([])
            names.append([])
            lobbies[-1].append(conn)
            names[-1].append(name)
            lob=(len(lobbies)-1)
            send(conn,lob)
            #conn.send(pickle.dumps(lob)+pickle.dumps('#*#'))
        else:
            message=[]
            message.append((len(lobbies)-1))
            x=0
            while x<len(lobbies):
                if x not in startedLobbies:
                    message.append("Lobby "+str(x)+": "+str(len(lobbies[x]))+" online.")
                x+=1
            #print("about to send")
            send(conn,message)
            #conn.send(pickle.dumps(message)+pickle.dumps('#*#'))
            #print("after send")
            message=conn.recv(2048) #clients reply
            message=message.decode("utf-8").strip()
            if message=="New":
                lob=len(lobbies)
                lobbies.append([])
                names.append([])
                lobbies[lob].append(conn)
                names[lob].append(name)
            else:
                lob=int(message)
                lobbies[lob].append(conn)
                names[lob].append(name)
                message=names[lob]
                send(conn,message)
                #conn.send(pickle.dumps(message)+pickle.dumps('#*#'))
            #message="Joining lobby: "+str(lob)
            message=name
            #x=json.dumps(message)
            broadcast(message,conn,lob)
            #broadcast(pickle.dumps(message)+pickle.dumps('#*#'),conn,lob)       
    except socket.error as e:
        print(e)
    #need a loop to process lobby activities thats waiting for a Start symbol  
    lobScreen=True
    gameScreen=False
    while lobScreen: #lobby loop
        try:
            reply=name+": "
            data = conn.recv(2048)
            message= data.decode("utf-8").strip()
            if not data:
                print("Disconnected")
                remove(conn,lob,name)
                break
            elif message=="Start": #this is the og lobby starter
                print("Lobby starting")
                #x=json.dumps("Starting")
                broadcast("Starting",conn,lob)
                #broadcast(pickle.dumps("Starting"+'#*#'),conn,lob)
                gameScreen=True
                lobScreen=False
                startedLobbies.append(lob)
                break
            elif message=="Starting":
                gameScreen=True
                lobScreen=False
                break
            else:
                print("Lobby "+str(lob)+": "+addr[0]+": "+reply)
                #print("Sending : ", reply)
                #x=json.dumps(reply)
                broadcast(reply,conn,lob)
                #broadcast(pickle.dumps(reply+'#*#'),conn,lob)
        except socket.error as e:
            print(e)
            break
    while gameScreen:#go thru a basic turn for the lobby
        try:
            #data = conn.recv(2048)
            #message= data.decode("utf-8").strip()
            #data=pickle.loads(conn.recv(2048*2))
            data=pickle.loads(conn.recv(2048*2))
            print(data)
            print("Size of data is: "+str(sys.getsizeof(data)))
            print("Size of pickeld data is: "+str(sys.getsizeof(pickle.dumps(data))))
            if not data:
                print("Disconnected")
                remove(conn,lob,name)
                break
            elif data[0]=="Next":#client just finished turn, tell other clients and update the game variables
                #x=json.dumps(data)
                broadcast(data,conn,lob)
                #broadcast(pickle.dumps(data)+pickle.dumps('#*#'),conn,lob)
            elif data[0]=='INIT':
                print("Initializing game")
                #x=json.dumps(data)
                broadcast(data,conn,lob)
                #broadcast(pickle.dumps(data)+pickle.dumps('#*#'),conn,lob)
        except (socket.error,EOFError) as e:
            print(e)
            break

    print("Lost connection")
    remove(conn,lob,name)
    conn.close()
def broadcast(message,connection,l):
    for x in lobbies[l]:
        if x!=connection:
            try:
                send(x,message)
            except:
                x.close()
                #remove(x,l)
def remove(connection,l,name):
    if connection in clients:
        clients.remove(connection)
        if connection in lobbies[l]:
            lobbies[l].remove(connection)
            names[l].remove(name)
            broadcast(("Removed "+name),connection,l)
            if len(lobbies[l])<1: #Was the last in lobby
                lobbies.pop(l)
                names.pop(l)
                startedLobbies.remove(l)
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    clients.append(conn)
    start_new_thread(threaded_client, (conn,addr))
conn.close()
server.close()