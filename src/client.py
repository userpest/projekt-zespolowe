from threading import *
from socket import *
from utils import *
from player import *
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
		self.socket=CreateSocket()
		self.img=img
		self.imgc=imgc
		self.ch=ch
	def run(self):
        	Thread(target=Client.running,args=(self,)).start()
		self.invite()
	def send(self,addr,msg):
	        self.socket.sendto(msg,addr)
	def quit_(self):
        	self.not_end=False
		self.send_exit()
		self.socket.close()
		self.game.end()
	def running(self):
		print "a"
	        not_end=True
	        msg=""
	        size=0
	        begin=True
		last_id=0
		ct=0
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
	                        splited = data.split(' ',2)
				last_id = int(splited[0])
	                        size = int(splited[1])
	                        size = size - len(splited[2])
	                        if size != 0:
	                                begin = False
	                        msg = splited[1]
	                else:
				splited = data.split(' ',1)
				id_=int(splited[0])
				if id_!=last_id-1:
					#print id_, last_id
					ct=ct+1
					print ct
	                        size = size - len(splited[1])
	                        if size == 0:
	                                begin = True
	                        msg = msg + data
			print size
	                if begin:
	                        self.onMessage(msg,addr)
		if self.game != None:
			self.game.end()	
	def onMessage(self,data,addr):
		print data, addr
        	temp=json.loads(data)
	        if len(temp)==0:
			return
		if temp[0]=='K':
			self.id_=temp[3]
			self.game=Game(temp[1],temp[2],ch_img=self.ch,my_id=self.id)
			self.game.load(temp[4]) #loads starts game
			self.game.set_player_owner(self.id_,self.ch)
	        	for id_n in temp[5]:
		        	self.players.append(self.game.getObjectById(id_n))
	        elif temp[0]=='S':
			self.game.end()
			self.game=Game(temp[1])
			self.game.set_player_owner(self.id_,self.ch)
			self.players=[]
			for id_n in temp[2]:
				self.players.append(self.game.getObjectById(id_n))
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
			self.socket.sendto(chunk,self.addr)
	def chunks(self,s, n):
		splitted=[]
		for start in range(0,len(s),n):
			splitted.append( s[start:start+n] )
		return splitted
	def invite(self):
		self.send_invite(self.img,self.imgc)


client = Client(('127.0.0.1',16666),"hero.png","hero.png","crosshair.png")
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



