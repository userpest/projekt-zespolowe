from threading import *
from socket import *
from utils import *
from game_ import *
from player import *
from ThreadSafeArray import *
import select
import time
import json

respawn_angle=0
respawn_x=0
respawn_y=0

class User:
	def __init__(self,socket):
		self.socket = socket
		self.up = False
	def setup(self, id_, player):
		self.id_ = id_
		self.player = player
		self.up = True
	def setup_obj(self,obj):
		self.id_ = obj[0]
		self.player = obj[1]
		self.up = True

class Server:
    game=None
    port=None
    socket=None
    new_id=0
    lock=None
    def __init__(self,port,map_name,scrw,scrh):
	self.players = ThreadSafeArray()
        self.game=Game(scrw,scrh,Server.executeFrap,self,True) #
	self.scrw=scrw
	self.scrh=scrh
	self.game.create(map_name)
        self.port=port
	self.socket=CreateSocketTcp()
	self.socket.settimeout(10)
        self.socket.bind(('127.0.0.1',self.port))
	#
	self.socket.listen(10)
	#
        self.lock=Lock()
	self.lock_messages = Lock()
	self.messages = ['P',[]]
	self.w84join_response = 0
    def run(self):
	self.game.start()
	self.not_end = True
        Thread(target=Server.listening,args=(self,)).start()
    def listening(self):
	while self.not_end:
		try:
			print 'listen for new client'
			sock,addr = self.socket.accept()
			if sock == None:
				continue
			print 'new client', addr
			user=User(sock)
			self.players.add(user)
			Thread(target=Server.running,args=(self,user)).start()
		except Exception as ex:
   			print 'exception',ex
	print 'stoped listening'
    def running(self, user):
	print 'begin reading msgs from new client'
	msg=""
	size=0
	begin=True
        while self.not_end:
            do_read=False
            try:
                r, _, _ = select.select([user.socket], [], [],timeout)
                do_read = bool(r)
            except Exception as ex:
		print 'stoped reciving messages from client'
                return ex
            if do_read:
		try:
	                data=user.socket.recv(buffsize)
		except Exception as ex:
			print 'exception during recv', ex
			continue
		if begin:
			if len(data) == 0:
				continue
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
		        self.onMessage(msg,user)
	print 'stoped reciving messages from client'
    def a(self):
        self.lock.acquire(True)
    def r(self):
        self.lock.release()

    def onMessage(self,data,user):
	temp=json.loads(data)
        if len(temp)==0:
            return
        if temp[0]=='I':
            self.a()
            self.invite(temp,user)
            self.r()
        elif temp[0]=='S':
            self.a()
            self.sync(temp,user)
            self.r()
        elif temp[0]=='E':
            self.a()
            self.exit_(temp,user)
            self.r()
        elif temp[0]=='P':
            self.a()
            #self.send_to_all(temp,user)
	    self.createPack(temp,user)
            self.r()
	elif temp[0]=='J':
	    self.w84join_response = self.w84join_response - 1
        else:
            return
    def executeFrap(self,ecb):
	if self.w84join_response > 0: #should be counter (connection timeout)
		return False
	else:
		self.sendPackage(ecb)
		return True
    def createPack(self,temp,user):
	self.lock_messages.acquire(True)
	self.messages[1].append(temp[1:])
	self.lock_messages.release()
   
    def invite(self,temp,user):
	self.w84join_response = self.w84join_response + 1
	msg_a=['N',respawn_x,respawn_y,respawn_angle,temp[1],temp[2],self.new_id]
        msg=json.dumps(msg_a)	
        for pl in self.players.get_list():
		if pl.up:
		        self.send(pl,msg)
	player=Player(respawn_x,respawn_y,respawn_angle,temp[1],temp[2],self.new_id)
	self.players.action_method(User.setup_obj,user,(self.new_id,player)) #threadsafe setup a player
        self.game.join_player(user.player)
	msg_a=['K',self.scrw,self.scrh,self.new_id,self.game.serialize(),self.get_players()]
        msg=json.dumps(msg_a)        
	self.send(user,msg)
        self.new_id=self.new_id+1
    def sync(self,temp,user):
        self.send(user,json.dumps(['S',self.game.serialize(),self.get_players()]))

    def exit_(self,temp,user):
        u = self.players.pop(user)
	if u.up:
		self.game.remove_player(user.player)
		try:
			u.socket.close()
		except:
			pass
		id_ = u.id_
	        msg=json.dumps(['E',id_])
        	for pl in self.players.get_list():
	            self.send(pl,msg)
		print 'player', id_, 'quit game'
    def send_to_all(self,temp,user):            
        for pl in self.players.get_list():
            self.send(pl,temp)
            if pl.id_==temp[1]:                
                pl.player.setMoves(temp[2])
    def sendPackage(self,ecb):
	self.lock_messages.acquire(True)
	#if len(self.messages[1]) == 0:
	#	self.lock_messages.release()
	#	return
	ecb.processEvents()
	for pair in self.messages[1]:
		for pl in self.players.get_list():
			if pl.id_ == pair[0]:
				pl.player.setMoves(pair[1])
				break
	msg = json.dumps(self.messages)
	self.messages[1] = []
	self.lock_messages.release()
        for pl in self.players.get_list():
		self.send(pl,msg)

    def get_players(self):
        players=[]		
        for pl in self.players.get_list():
	    if pl.up:
	        players.append(pl.id_)
        return players
                    
    def send(self,user,msg):
	#if len(msg)<1000:
		#print user.id_,msg
	msg=str(len(msg))+" "+msg
	chunks=self.chunks(msg,1024)
	for chunk in chunks:
		try:
			user.socket.send(chunk)
		except Exception as ex:
			print 'Exception', ex, 'during sending'
    def quit_full(self):
	for pl in self.players.get_list():
	    try:
		self.send(pl,json.dumps(['Q']))
	        pl.socket.close()
	    except Exception as ex:
		print ex, 'during quit'
	self.not_end = False
	self.socket.close()
	print 'listen socket closed'
	self.game.end()
    def quit_(self):
        self.not_end=False


    def chunks(self,s, n):
	splited=[]
	for start in range(0, len(s), n):
		splited.append(s[start:start+n])
	return splited

server=Server(16667,"map.png",800,600)
server.run()
print("Running")
time.sleep(60)
server.quit_full()
    
