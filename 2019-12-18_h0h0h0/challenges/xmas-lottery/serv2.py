import socket
import threading
import random
import sys

class ThreadedServer(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def listen(self):
        self.sock.listen(5)
        while True:
            client, address = self.sock.accept()
            client.settimeout(60)
            threading.Thread(target = self.listenToClient,args = (client,address)).start()
#            print(client,address)

    def listenToClient(self, client, address):
        size = 1024
        d = list(range(100))
        self.welcome(client)
        while True:
            try:
                data = client.recv(size)
                if len(d) < 5:
                    client.send(b'No more powerball left. Try later!\n')
                    client.close()
                if data:
                    comb = []
                    for i in range(5):
                        n = random.choice(d)
                        comb.append(n)
                        d.remove(n)
                    response = self.check_input(data,sorted(comb))
                    d = list(set(d)-set(comb))
                    client.send(response)
                    if b'Congrats' in response:
                        client.close()
                else:
                    raise error('Client disconnected')
            except:
                client.close()
                return False

    def welcome(self, client):
        client.send(b'''
         __  __             _            _                _    
        |  \/  | ___  _ __ | |_ _ __ ___| |__   __ _  ___| | __
        | |\/| |/ _ \| '_ \| __| '__/ _ \ '_ \ / _` |/ __| |/ /
        | |  | | (_) | | | | |_| | |  __/ | | | (_| | (__|   < 
        |_|  |_|\___/|_| |_|\__|_|  \___|_| |_|\__,_|\___|_|\_\
                                                               
        __  __                      _          _   _                  
        \ \/ /_ __ ___   __ _ ___  | |    ___ | |_| |_ ___ _ __ _   _ 
         \  /| '_ ` _ \ / _` / __| | |   / _ \| __| __/ _ \ '__| | | |
         /  \| | | | | | (_| \__ \ | |__| (_) | |_| ||  __/ |  | |_| |
        /_/\_\_| |_| |_|\__,_|___/ |_____\___/ \__|\__\___|_|   \__, |
                                                                |___/ 
        Entre a combination of 5 numbers to win a prize!!
        Format: 01-23-45-78-89 (Increasing order) 
''')

    def check_input(self, data, comb):
        ans = False
        try:
#            print(type(data),'data:',data)
            d = sorted(map(int,data.split(b'-')))
#            print(d)
            ans = d == comb
        except:
#            print('error')
            ans = False

        if ans:
            msg = "Congrats!! Here's the promised flag: FLAG-RBr1Ryen75o1aZ6NZriap6VopLBZTx3C"
        else:
            msg = "Try again! It was "+'-'.join([str(i).rjust(2,'0') for i in comb])+"\n"
#        print(msg)
        return msg.encode()

if __name__ == "__main__":
    try:
        port = int(sys.argv[1])
    except:
        port = 5000
    ThreadedServer('', port).listen()

























