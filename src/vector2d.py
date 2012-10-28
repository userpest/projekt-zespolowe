#!/usr/bin/python
import math
class Vector2D:

	#gief overloading
	def __init__(self,lenght=0, angle=0,x=0,y=0):

		if lenght == 0 and angle == 0:
			self.x=x
			self.y=y
		else:
			self.x = math.cos(angle)*lenght
			self.y = math.sin(angle)*lenght


	def setByAngle(self,lenght, angle):
		self.x = math.cos(angle)*lenght
		self.y = math.sin(angle)*lenght

	def setByCoords(self,x,y):
		self.x=x
		self.y=y

	def __add__(self,other):
		return Vector2D(x=self.x+other.x,y=self.y+other.y)

	def __sub__(self,other):
		return Vector2D(x=self.x-other.x,y=self.y-other.y)

	def __mul__(self,other):
		return Vector2D(x=self.x*other,y=self.y*other)

	def __div__(self,other):
		return Vector2D(x=self.x/other, y=self.y/other)

	def __iadd__(self,other):
		self.x+=other.x
		self.y+=other.y
		return self

	def __isub__(self,other):
		self.x-=other.x
		self.y-=other.y
		return self

	def __imul__(self,other):
		self.x*=other
		self.y*=other
		return self

	def __idiv__(self,other):
		self.x/=other
		self.y/=other
		return self

	def getlen(self):
		return math.sqrt(self.x*self.x+self.y*self.y)

	def get_angle(self):
		return math.atan2(self.x,self.y)

	def __str__(self):
		s = "Vector2D, x:%d y:%d"%(self.x,self.y)
		return s
	def dot(self,v):
		return self.x*v.x + self.y*v.y

	#not sure if works
	def dotAngle(self,v):
		ablen = self.getlen()*v.getlen()
		dotprodtuct = self.dot(v)
		angle = math.acos(dotprodtuct/ablen)
		return math.acos(angle)
