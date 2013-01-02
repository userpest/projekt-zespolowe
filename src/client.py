from threading import *
from socket import *
from utils import *
from player import *
from game_ import *
import json
import select

class Client:
	players=[]
	game=None
	addr=None
	socket=None
	id_=0
	player=None
	
	def __init__(self,addr,img,imgc,ch):		
		self.addr=addr
		self.socket=CreateSocketTcp()
		self.img=img
		self.imgc=imgc
		self.ch=ch
	def run(self):
		try:
			self.socket.connect(self.addr)
		except:
			print "Error. Unable to connect to server"
			return 1
        	Thread(target=Client.running,args=(self,)).start()
		self.invite()
	def send(self,addr,msg):
	        self.socket.send(msg)
	def quit_(self):
        	self.not_end=False
		self.send_exit()
		try:
			self.socket.close()
		except:
			pass
		self.game.end()
	def running(self):
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
	                data=self.socket.recv(buffsize)
			#print data
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
				if len(msg) < 1000:
					print msg
	                        self.onMessage(msg)
		if self.game != None:
			self.game.end()	
	def onMessage(self,data):
		#print data
        	temp=json.loads(data)
	        if len(temp)==0:
			return
		if temp[0]=='K':
			self.id_=temp[3]
			self.game=Game(temp[1],temp[2],ch_img=self.ch,my_id=self.id_)
			self.game.load(temp[4]) #loads starts game
			self.game.set_player_owner(self.id_,self.ch)
	        	for id_n in temp[5]:
		        	self.players.append(self.game.getPlayer(id_n))
	        elif temp[0]=='S':
			self.game.end()
			self.game=Game(temp[1])
			self.game.set_player_owner(self.id_,self.ch)
			self.players=[]
			for id_n in temp[2]:
				self.players.append(self.game.getPlayer(id_n))
		elif temp[0]=='N':	
			player=Player(temp[1],temp[2],temp[3],temp[4],temp[5],temp[6])
			self.players.append(player)
			self.game.join_player(player)
		elif temp[0]=='P':
			if temp[1]==self.id_:
				return
			for p in self.players:
				if p.id_ == temp[1]:
					p.setMoves(temp[2])
					break
		elif temp[0]=='E':
			i=0
			while i<len(self.players):
				if self.players[i].obj_id==temp[1]:
					player = self.players.pop(i)
					self.game.remove_player(player)		
					i=i+1
		elif temp[0]=='Q':
			self.not_end = False
			self.game.end()	
	def send_invite(self,img_name,collsion_map_name):
		self.send(json.dumps(['I',img_name,collsion_map_name]))
	def send_sync(self):
		self.send(json.dumps(['S']))
	def send_exit(self):
		self.send(json.dumps(['E',self.id_]))
	def send_move(self,move):
		self.send(json.dumps(['P',self.id_,move]))
	def send(self,msg):
		msg=str(len(msg))+" "+msg
		for chunk in self.chunks(msg,1024):
			self.socket.send(chunk)
	def chunks(self,s, n):
		splitted=[]
		for start in range(0,len(s),n):
			splitted.append( s[start:start+n] )
		return splitted
	def invite(self):
		self.send_invite(self.img,self.imgc)


client = Client(('127.0.0.1',16662),"hero.png","hero.png","crosshair.png")
client.run()

import time
time.sleep(20)
#client=Client(('127.0.0.1',16666))
#client.run()
#print("Running")
#time.sleep(5)
#client.send_invite()
#time.sleep(5)
#client.send_move('a')
#time.sleep(5)
#client.send_exit()
#client.quit_()



