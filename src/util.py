from math import copysign,floor

def apply_bounds(minimal, maximal, value):
	value = min ( value,maximal)
	value = max (minimal,value)
	return value

#TODO: implement bresenham

def calc_line( (x0, y0), (x1, y1)):
	x = x1-x0
	y = y1-y0
	s_x = int(copysign(1,x))
	s_y = int(copysign(1,y))
	x = abs(x)
	y = abs(y)

	errx=0
	erry=0
	if y == 0:
		stepy=0
		stepx = x
	elif x ==0:
		stepx =0 
		stepy = y
	elif x > y:
		stepx = int(floor(x/y))
		errx = abs(x/y - stepx )
		stepy = 1	
	else :
		stepy = int(floor(abs(y/x)))
		erry =abs(y/x - stepy)
		stepx = 1	

	cumerrx = 0 
	cumerry = 0 
	cx = x0
	cy = y0
	while x > 0 or y > 0:
		for i in range(0,stepx):
			x-=1
			cx+=s_x
			yield (cx,cy)
		for i in range(0,stepy):
			y-=1
			cy+=s_y
			yield (cx,cy)
		cumerrx+=errx
		cumerry+=erry

		if cumerrx > 1:
			a += int(math.floor(cumerrx))
			cumerrx -= a
			x-=a
			cx+=a*s_x

		if cumerrx > 1:
			a += int(math.floor(cumerry))
			y-=a
			cumerry -= a
			cx+=a*s_y
