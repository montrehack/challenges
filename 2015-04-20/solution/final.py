
# read the file and parse it
def parse_file():
    with open('pcap_export_bytes') as f:
    	lines = [x.strip('\n') for x in f.readlines()]
    k = 0
    for line in lines :
    	arr =  bytearray.fromhex(line)
    	i = 0
    	val = 0
    	for byte in arr:
    		if byte > 127:
                 val = int(byte)-256
    		else :
                 val = int(byte)

    		if i == 0:
    			#if click ( it's always either 0 or 1)
    			if(byte == 1):
    				clicks.add(k)
    #				print k
    		elif i == 1:
    			#add x point
    			x_ax.append(int(val))
    		elif i == 2:
    			#add y point
    			y_ax.append(int(val))

    		i = i+1
    	k = k+1


def get_key_row_1(x):
	if x < 200:
		return 'q'
	elif x < 250:
		return 'w'
	elif x < 300:
		return 'e'
	elif x < 400:
		return 'r'
	elif x < 500:
		return 't'
	elif x < 600:
		return 'y'
	elif x < 700:
		return 'u'
	elif x < 750:
		return 'i'
	elif x < 850:
		return 'o'
	else:
		return 'p'

def get_key_row_2(x):
	if x < 200:
		return 'a'
	elif x < 300:
		return 's'
	elif x < 400:
		return 'd'
	elif x < 500:
		return 'f'
	elif x < 550:
		return 'g'
	elif x < 600:
		return 'h'
	elif x < 700:
		return 'j'
	elif x < 800:
		return 'k'
	else:
		return 'l'

def get_key_row_3(x):
	if x < 250:
		return 'z'
	elif x < 300:
		return 'x'
	elif x < 400:
		return 'c'
	elif x < 500:
		return 'v'
	elif x < 600:
		return 'b'
	elif x < 700:
		return 'n'
	else:
		return 'm'

def get_key(x,y):
	if y < 50:
		return " "
	elif y < 150:
		return get_key_row_3(x)
	elif y < 250:
		return get_key_row_2(x)
	else:
		return get_key_row_1(x)


def main():

	x1=0
	y1=0

	x_click=0
	y_click=0
	# loop on all the points
	for l in range (0,len(x_ax)) :
		# if the user clicks here we draw a line from the last click to this click.
		if(l in clicks):
			x_click_2 = x1+x_ax[l]
			y_click_2 = y1+y_ax[l]
 			print get_key(x_click, -y_click),

			# to maintain the previous values of clicks
			x_click = x_click_2
			y_click = y_click_2

		#to calculate the next mouse movement
		x2 = x1 + x_ax[l]
		y2 = y1 + y_ax[l]

		# to maintain the previous values
		x1 = x2
		y1 = y2

x_ax = list()
y_ax = list()
clicks = set()

parse_file()
main()
