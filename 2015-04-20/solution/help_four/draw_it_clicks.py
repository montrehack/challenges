#import graphics(should be in the same directory) and time 
from graphics import *
import time

#max click to stop drawing after
max = 100
#min click to start drawing after
min = 0

# read the file
# file format each line 4 bytes
# 0005fd00
# 0007fe00
# 0006fe00

with open('pcap_export_bytes') as f:
	lines = [x.strip('\n') for x in f.readlines()]

# intialize Lists
x_ax = list()
y_ax = list()
clicks = set()

#the index of the event ( used to track at which position was there a click )
k = 0

####################################################
################### Parsing ########################
#parse and populate the lists 

for line in lines : 
	arr =  bytearray.fromhex(line)
	#byte counter 	       
	i = 0
	#signed value of byte
	val = 0
	for byte in arr:
		#if more than 127 means it's a negative signed byte (two's complement)
		if byte >  127:
                        val = int(byte)-256
                else :
                        val = int(byte)
		#should have used a switch lol 
		if i == 0:
			#if click ( it's always either 0 or 1)
			if(byte == 1):
				clicks.add(k)
				#print k (DEBUG PRINT IF NEEDED)
		elif i == 1:
			#add x point
			x_ax.append(int(val))
		elif i == 2:
			#add y point
			y_ax.append(int(val))

		i = i+1
	k = k+1

#DEBUG PRINTS IF NEEDED
#print len(clicks)
#print len(x_ax)
#print k
#raw_input()

####################################################
################### Drawing ########################
#draw all the mouse clicks

def main():
	win = GraphWin('NaughtyMouse', 10000, 10000) # give title and dimensions

	#values to start in the middle of the page / probably the final image is flipped upside down because when then Y value increase the point goes down
	#Actually it turns out that Y increases downwards and not upwards .. interesting !
	x1=500 
	y1=500

	x_click=500
	y_click=500

	#counters for clicks and all movements
	c_counter = 0
	all_counter =0


	# loop on all the points
	for l in range (0,len(x_ax)-1) : 
		all_counter = all_counter +1
		# if the user clicks here we draw a line from the last click to this click.
		if(l in clicks):
			c_counter = c_counter+1
			x_click_2 = x1+x_ax[l]
			y_click_2 = y1+y_ax[l]

			zoom = 1
 			message = Text(Point(x_click_2, y_click_2), str(c_counter))

			if  (min < c_counter < max) or (c_counter == 10) or (c_counter == 5) or (c_counter == 39) :
 				message.draw(win)

	                #This delay is to slow down the drawing
			#time.sleep(0.5)
			
			# to maintain the previous values of clicks
			x_click = x_click_2
			y_click = y_click_2
			
		##########################################

		#to calculate the next mouse movement
		x2 = x1 + x_ax[l]
		y2 = y1 + y_ax[l]

		# to maintain the previous values
		x1 = x2
		y1 = y2
		
		
	
	#DEBUG PRINTS IF NEEDED
	#print c_counter	
	#print all_counter
	
	# not important, ignore the following
	message = Text(Point(win.getWidth()/2, 20), 'Click anywhere to quit.')
	message.draw(win)
	win.getMouse()
	win.close()

main()
