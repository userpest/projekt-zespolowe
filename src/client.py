from threading import *
from socket import *
from utils import *
from player import *
from game_ import *
import json
import select

class Client:
	players={}
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
		self.lock_messages=Lock()
		self.messages = []
	def run(self):
		try:
			self.socket.connect(self.addr)
		except Exception as ex:
			print "Error. Unable connect to server (", ex, ")"
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
	            except Exception as ex:
			print 'stoped reciving messages'
	                return ex
	            if do_read:
			try:
		                data=self.socket.recv(buffsize)
			except Exception as ex:
				print 'exception during recv', ex
				continue
	                if begin:
				if data == '':
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
	                        self.msgRecived(msg)
				#onMessage(msg)
		print 'stoped reciving messages'
	def msgRecived(self,data):
		temp=json.loads(data)
		if len(temp) == 0:
			return
		if temp[0] == 'K': #after reciving game
			self.id_=temp[3]
			self.game = Game(temp[1],temp[2],Client.ExecuteMessages,self,False,ch_img=self.ch,my_id=self.id_)
			self.game.load(temp[4])
			self.game.set_player_owner(self.id_,self.ch)
			self.player = self.game.getPlayer(self.id_)
			# weapon bux fix?
			camera.registerObjects(self.player.attached)
			#
			for id_n in temp[5]:
				self.players[id_n]=self.game.getPlayer(id_n)
			self.send(json.dumps(['J']))	# send joined
		elif temp[0] == 'Q':
			print 'Exit'
			self.not_end = False
			self.socket.close()
			self.game.end()
			print 'Exit done'
		else:
			self.lock_messages.acquire(True)
			self.messages.append(temp)
			self.lock_messages.release()
	def ExecuteMessages(self,ecb):
		if len(self.messages) == 0:
			return False
		self.lock_messages.acquire(True)
		message = self.messages.pop(0)
		to_return = self.onMessage(message)
		if to_return:
			ecb.processEvents()
			move = self.player.getMoves()
			self.send_move(self.player.getMoves())
		self.lock_messages.release()
		return to_return
	def onMessage(self,temp):
		#print data
	        """
			elif temp[0]=='S':
			self.game.end()
			self.game=Game(temp[1])
			self.game.set_player_owner(self.id_,self.ch)
			self.players=[]
			for id_n in temp[2]:
				self.players.append(self.game.getPlayer(id_n))
		"""
		if temp[0]=='N':	
			player=Player(temp[1],temp[2],temp[3],temp[4],temp[5],temp[6])
			self.players[temp[6]]=player
			self.game.join_player(player)
		elif temp[0]=='P':
			for pair in temp[1]:
				#if pair[0] != self.id_:
				if True:
					self.players[pair[0]].setMoves(pair[1])
					#for p in self.players:
					#	if p.id_ == pair[0]:
					#		p.setMoves(pair[1])
					#		break

			return True
		elif temp[0]=='E':
			player = self.players[temp[1]]
			del self.players[temp[1]]
			self.game.remove_player(player)
			#i=0
			#
			#while i<len(self.players):
			#	if self.players[i].obj_id==temp[1]:
			#		player = self.players.pop(i)
			#		self.game.remove_player(player)		
			#		i=i+1
		elif temp[0]=='Q':
			self.not_end = False
			self.game.end()	
		return False
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


client = Client(('127.0.0.1',16667),"hero.png","hero.png","crosshair.png")
client.run()

import time
time.sleep(20)
client.quit_()
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



