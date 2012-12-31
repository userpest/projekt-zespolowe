from threading import *
from socket import *
from utils import *
from game_ import *
from player import *
import select
import time
import json

respawn_angle=0
respawn_x=0
respawn_y=0

class User:
    id_=0
    player=None
    addr=(None,None)
    def __init__(self,id_,player,addr):
            self.id_=id_
            self.player=player
            self.addr=addr


class Server:
    players=[]
    game=None
    port=None
    socket=None
    new_id=0
    lock=None
    def __init__(self,port,map_name,scrw,scrh):
        self.game=Game(scrw,scrh) #
	self.scrw=scrw
	self.scrh=scrh
	self.game.create(map_name)
        self.port=port
        self.socket=CreateSocket()
        self.socket.bind(('127.0.0.1',self.port))
        self.lock=Lock()
    def run(self):
        Thread(target=Server.running,args=(self,)).start()
            
    def running(self):
	self.game.start()
        not_end=True
	msg=""
	size=0
	begin=True
        while not_end:
            do_read=False
            try:
                r, _, _ = select.select([self.socket], [], [],timeout)
                do_read = bool(r)
            except error as ex:
                return ex
            if do_read:
                data,addr=self.socket.recvfrom(buffsize)
		if begin:
			splited = data.split(' ',1)	
			size = int(splited[0])
			size = size - len(splited[1])
			if size != 0:
				begin = False
			msg = splited[1]
		else:
			size = size - len(data)
			if size == 0:
				begin = True
			msg = msg + data
		if begin:
	                self.onMessage(msg,addr)
	self.game.end()
    def a(self):
        self.lock.acquire(True)
    def r(self):
        self.lock.release()

    def onMessage(self,data,addr):
	print data,addr
	temp=json.loads(data)
        if len(temp)==0:
            return
        if temp[0]=='I':
            self.a()
            self.invite(temp,addr)
            self.r()
        elif temp[0]=='S':
            self.a()
            self.sync(temp,addr)
            self.r()
        elif temp[0]=='E':
            self.a()
            self.exit_(temp,addr)
            self.r()
        elif temp[0]=='P':
            self.a()
            self.send_to_all(temp,addr)
            self.r()
        else:
            return
    def invite(self,temp,addr):
	msg_a=['N',respawn_x,respawn_y,respawn_angle,temp[1],temp[2],self.new_id]
        msg=json.dumps(msg_a)	
        for pl in self.players:
                self.send(pl.addr,msg)
        user=User(self.new_id,Player(respawn_x,respawn_y,respawn_angle,temp[1],temp[2],self.new_id),addr)
        self.players.append(user)
        self.game.join_player(user.player)
	msg_a=['K',self.scrw,self.scrh,self.new_id,self.game.serialize(),self.get_players()]
        msg=json.dumps(msg_a)        
	self.send(addr,msg)
        self.new_id=self.new_id+1
    def sync(self,temp,addr):
        self.send(addr,json.dumps(['S',self.game.serialize(),self.get_players()]))
    def exit_(self,temp,addr):
        i=0
        id_=-1
        while i<len(self.players):
            if players[i].addr==addr:
                id_=players[i].id_
		user = players.pop(i)
		self.game.remove_player(user.player)
                break
            i=i+1
        msg=json.dumps(['E',id_])
        for pl in self.players:
            self.send(pl.addr,msg)
    def send_to_all(self,temp,addr):            
        for pl in self.players:
            self.send(pl.addr,temp)
            if pl.id_==temp[1]:                
                pl.player.setMoves(temp[2])
       
                
    def get_players(self):
        players=[]		
        for pl in self.players:
            players.append(pl.id_)
        return players
                    
    def send(self,addr,msg):
	msg=str(len(msg))+" "+msg
	print "to send: ", len(msg)
	chunks=self.chunks(msg,1024)
	print len(chunks), len(chunks)*1024
	i=len(chunks)
	for chunk in chunks:
		f=open('q.txt','a')
		f.write("sending "+ str(i) + " chunk")
		#print "sending ",i ,"chunk"
		i=i-1
		self.socket.sendto(str(i)+' '+chunk,addr)
	f.close()
    def quit_full(self):
	for pl in self.players:
	    self.send(pl.addr,'Q')
	self.socket.close()
	self.not_end=False
	self.game.end()
    def quit_(self):
        self.not_end=False


    def chunks(self,s, n):
	splited=[]
	for start in range(0, len(s), n):
		splited.append(s[start:start+n])
	return splited

server=Server(16666,"map.png",800,600)
server.run()
print("Running")
time.sleep(60)
server.quit_full()
    
