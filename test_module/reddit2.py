from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
import json
from kivy.clock import Clock
import pickle
import requests
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
import threading
import sys
from kivy.app import runTouchApp
from kivy.uix.screenmanager import ScreenManager, Screen, WipeTransition
from random import randint
import sys
from kivy.core.window import Window
import time
#from components import BlockchainDisplay, CurrentBlockDisplay
from blockchain import Blockchain
import socket
import random
from screens import *              
from ecdsa import SigningKey, NIST384p
from sql import sql_handler
      
##refresh page within blockchain view probably ?
class PCApp(App):

####
# server functionalities
####
    def run_server(self):
         
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.host, int(self.port)))
        s.listen()
        s.settimeout(None)
        print("server on host ", self.host, " and port ", self.port) 
        response = b"message received"
        while True:
            conn, addr = s.accept()
            threading.Thread(target=self.service_connection, args=(conn, response)).start()
        s.close()
        print("server closed. trying again....")
        self.run_server() 

    def service_connection(self, conn, response):
        
        data = conn.recv(1024)
        if not data:
            return
        conn.send(response)
        self.message_recieved_lock.acquire()    
        print("adding data to revienved que", data)    
        self.message_recieved_queue.append(pickle.loads(data.decode("utf-8")))
        self.message_recieved_lock.release()        
        
    def send_message(self, message, dest_ip, dest_port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        s.settimeout(5)
        try:
            s.connect((dest_ip, dest_port))
            s.send(message)
            data=s.recv(1024)
            s.close()
            return data.decode("utf-8")
        except socket.error as e:
            print("error", e)
            s.close()
            return -1
    
    def read_message_queue(self, dt):
        self.message_recieved_lock.acquire()
        while self.message_recieved_queue:
            message = self.message_recieved_queue.pop()
            print("MQ", message)
            if message["type"] == "Conn_Request":
                self.nodes.append(message["node_tup"])
            elif message["type"] == "Blockchain_Update":
                print("IN BC UPDATEE> ", message)
                self.blockchain.collect_chain(message["chain"], message["comments"])
        self.message_recieved_lock.release()

    def send_blockchain_update(self, dt):
        vk_string = self.verifying_key.to_string()
        message = pickle.dumps({
            "type":"Blockchain_Update",
            "verifying_key":vk_string, #i think we should sign the block ? then verification happens when we 
            "uname":self.uname,
            "chain":self.blockchain.chain,
            "comments":self.blockchain.comments
        })
        for i in self.nodes:
            #shuold be node tuple
            self.send_message(message, i[0], i[1])     
###
# storage funcs
###

    def save_app(self):
        self.sql_lock.acquire()
        #save nodes and blockchain
        for i in self.nodes:
            self.storage_man.insert_node(i)
        
        #save blockchain
        self.storage_man.replace_chain(self.blockchain.chainn)
    
        self.sql_lock.release()

    def load_app(self):
        #return nodes, blockchain
        self.sql_lock.acquire()
        saved_chain = self.storage_man.get_chain()
        #TODO:
            #or call replace_chain or somehtibg ?
        self.blockchain.chain = saved_chain

        saved_nodes = self.storage_man.get_nodes()
        self.nodes = saved_nodes
        self.sql_lock.release()    

    def build(self):
        self.sm = ScreenManager(transition=WipeTransition())

        self.port = sys.argv[1]
        self.host = socket.gethostbyname(socket.gethostname())
        self.nodes = []
        
        #TODO:
            #Check if SK is in db/localstorage
        self.private_key = SigningKey.generate(curve=NIST384p) #change so that this is ONLY accessed inside the sql handler and the signature is passed up
        self.verifying_key = self.private_key.verifying_key   
    

        #self.load_app()
        
        self.uname = sys.argv[2]        

        self.message_recieved_queue = []
        self.message_recieved_lock = threading.Lock()

        self.storage_man = sql_handler()

        self.sql_lock = threading.Lock()
        
        self.pc_addr = "" #TODO generate this
        #TODO:
            #figure out way for users to send each other crypto and stay anon -> link unames to accounts 1 way ?        
        self.blockchain = Blockchain()
        
        #TODO:
            #make more blockchains
            #One that hosts peer contracts like so:

                #pc addr of contract giver and lister
                #each block mined the contract giver sends out a salt. contractors respond w/ data hashed. at end of cycle everyone who responded w/ matching hashes gets paid. result recorded in blockchain. 
                #could also try to record access records.  
                #at beginning of every mining if less than certain # respond, reallocate and record on bc whoever responds 
        
        comments_page = CurrentBlockScreen()
        blockchain_page = ChainScreen()
        network_page = NetworkScreen()
        
        self.sm.add_widget(blockchain_page.root)
        self.sm.add_widget(comments_page.root)
        self.sm.add_widget(network_page.root)

        Clock.schedule_interval(self.send_blockchain_update, 7)
        Clock.schedule_interval(self.read_message_queue, 10)
        #Clock.schedule_interval(self.save_app(), 10)
        threading.Thread(target=self.run_server, args=()).start()        

        return runTouchApp(self.sm)

def run_pc_app():
    PCApp().run()

#argv[1] = port
run_pc_app()
    
