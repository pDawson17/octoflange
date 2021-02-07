import json
import socket
import time
import threading
import hashlib
import pickle
import requests
from blockchain import Blockchain
from packet_creator import Packet_Creator


##TODO:
#  get request to sql to get list of items we need to check on !
    #then run that at the end of msg queue handler -> something that checks  
    #hist of items sent, confirmations recieved and not recieved, and proofs to
    #be checked`

#import message_sorter
#we're gonna just pass messages to that and have that handle everything else
class Server:
    def __init__(self, port, host=""):
        self.message_queue = [] #list of tuples: message, dest ip (str), dest port (int) 
        self.awaiting_conf = {} #format: message_hash : encoded message ready to be sent
        #need to check awaiting confirmation queue regularly
        if host == "":
            self.host= socket.gethostbyname(socket.gethostname())
        else:
            self.host = host
        self.port = port
        self.ph = Packet_Creator(self.host, self.port)
        print("here tho")
        self.lock = threading.Lock() 
        threading.Thread(target=self.run_server, args=(int(port), )).start()
        threading.Thread(target=self.handle_queue, args=()).start()
        threading.Thread(target=self.send_blockchain_update, args=()).start()

    def run_server(self, port):
        print("run server")
        response = "calculating"
        host = self.host
        port = self.port
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("server running on", port, host)
        s.bind((host, int(port)))
        s.listen()
        s.settimeout(None)
        while True:
            conn, addr = s.accept()
            threading.Thread(target=service_connection, args=(conn, response)).start()
        s.close()
        print("server closed. starting up again....")
        self.run_server(port)

    def send_blockchain_update(self):
        last_sent = time.time();
        print("in send_blockchain")
        while True:
            if time.time()-last_sent >= 30:
                packet = self.ph.create_blockchain_update_packet()
                self.lock.acquire()
                self.message_queue.append(packet)
                self.lock.release()
                last_sent = time.time()

    def service_connection(self, conn, response):
        data = conn.recv(1024)
        if not data:
            return
        conn.send(response)
        self.lock.acquire()
        self.message_queue.append(data)
        self.lock.release()


    def handle_queue(self):
        print("in handle_queue")
        while True:
            while self.message_queue:
                self.lock.acquire()
                cur = json.loads(self.message_queue.pop(0))
                print(cur, "SOEMTHING")
                if not cur or len(cur) < 1:
                    break
                ##FUNCTIONS TO HANDLE WHERE SHIT GO
                """
                TO WRITE:
                generate_packet here
                ####TYPES:
                #
                """
                #if cur[1] == "RANDOM":
                packet = self.ph.handle_message(cur[0])
                if packet:
                    self.send_message(cur[0], cur[1], cur[2])
                self.lock.release()
    
    def send_message(self, message, dest_ip, dest_port):
        """
           opens socket connection and sends message!
           ip -> string
           port -> int
        """
        host = socket.gethostbyname(socket.gethostname())
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.settimeout(5)
            s.connect((dest_ip, dest_port))
            s.send(message)
            data = s.recv(1024)
            s.close()
            return data.decode("utf-8")
        except socket.error as e:
            print("error", e)
            s.close()
            return -1

    #def send_message(self, message_packet):
        """
        sends encoded message packet to a node

        """
