from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.app import runTouchApp
from kivy.uix.label import Label
import json
from kivy.clock import Clock
import time
import pickle
import requests
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
import threading
import sys
from kivy.app import runTouchApp
from kivy.uix.screenmanager import ScreenManager, Screen, WipeTransition
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from random import randint
from components import BlockchainDisplay
import sys
from kivy.core.window import Window
import time
from components import BlockchainDisplay, CurrentBlockDisplay
from blockchain import Blockchain
import socket

class ChainScreen(Screen):
    def __init__(self):
        self.root = Screen(name="ChainScreen")
        #data is blockchain
        self.scroll = ScrollView(size_hint=(1, .6), size=(Window.width, Window.height))
        grid = GridLayout(cols=1)
        self.b = BlockchainDisplay()
        self.scroll.add_widget(self.b.root)
        grid.add_widget(self.scroll)

        #app = App.get_running_app()
        refresh_chain = Button(text="refresh chain", size_hint_y=.2)
        refresh_chain.bind(on_press=self.refresh_chain)
        
        grid.add_widget(refresh_chain)

        to_network = Button(text="To Netowrk View", size_hint_y=.2)
        to_network.bind(on_press=self.switch_to_network)

        switch_page = Button(text="View Current Block", size_hint_y=.2)

        switch_page.bind(on_press=self.switch_page)
      
        grid.add_widget(to_network)
        grid.add_widget(switch_page)
        self.root.add_widget(grid)

    def switch_to_network(self, instance):
        app = App.get_running_app()
        app.sm.current = "NetworkScreen"

    def switch_page(self, instance):
        app = App.get_running_app()
        app.sm.current = "CurrentBlockScreen"

    def refresh_chain(self, instance):
        
        app = App.get_running_app()
        self.scroll.clear_widgets()
        self.b = BlockchainDisplay()
        self.scroll.add_widget(self.b.root)
               
class CurrentBlockScreen(Screen):
    def __init__(self):
        self.root = Screen(name="CurrentBlockScreen")
        self.grid = GridLayout(cols = 1) #block content, then comment scrollview, then text input

        #for i in data:
            #data is map of comments i think
        mine = Button(text="mine")
        mine.bind(on_press=self.mine)


        switch_page = Button(text="Switch Page")
        switch_page.bind(on_press=self.switch_page)

        refresh_page = Button(text="Refresh Page")
        refresh_page.bind(on_press=self.reload_current_block)
        
        toolbar = GridLayout(cols=3, size_hint_y=.3)
        toolbar.add_widget(refresh_page)

        toolbar.add_widget(switch_page)
        toolbar.add_widget(mine)  
        
        self.grid.add_widget(toolbar)
        self.root.add_widget(self.grid)

        self.block_display = CurrentBlockDisplay(-1).root

        self.grid.add_widget(self.block_display)
        
    def switch_page(self, instance):
        app = App.get_running_app()
        app.sm.current = "ChainScreen"
 
    def mine(self, instance):

        app = App.get_running_app()
        app.blockchain.mine(app.uname)

    def reload_current_block(self, instance):
        #app = App.get_running_app()
        #data = app.blockchain.chain[-1]
        self.grid.remove_widget(self.block_display)
        self.block_display = CurrentBlockDisplay(-1).root
        self.grid.add_widget(self.block_display)
       
class NetworkScreen(Screen):
    def __init__(self):
        self.root = Screen(name="NetworkScreen")
        self.grid = GridLayout(cols=3)
        
        #TODO combine toolbars to on classe
        toolbar = GridLayout(cols=3, size_hint_y=.3)

        friends_view = GridLayout(rows=4)
        
        self.port = TextInput()
        self.host = TextInput() #replace later with uname or sig or someting idk          

        submit_request = Button(text="submit")
        submit_request.bind(on_press=self.submit_conn_request)
       
        #TODO: friend_list = ScrollView() 
        
        friends_view.add_widget(Label(text="enter port"))
        friends_view.add_widget(self.port)
        
        friends_view.add_widget(Label(text="enter host"))
        friends_view.add_widget(self.host)

        friends_view.add_widget(submit_request)

        switch_page_curr = Button(text="To Current Block")
        switch_page_curr.bind(on_press=self.to_curr)

        toolbar.add_widget(switch_page_curr)

        self.grid.add_widget(toolbar)
        self.grid.add_widget(friends_view)

        self.root.add_widget(self.grid) 

    def submit_conn_request(self, instance):
        #TODO:
            #fill in sig, uname
        app = App.get_running_app()
        message = json.dumps({
            "type":"Conn_Request",
            "node_tup":(app.host, int(app.port), app.uname,app.signature),
        }).encode("utf-8")
        
        if self.port.text != "":
            threading.Thread(target=app.send_message, args=(message, self.host.text, int(self.port.text))).start()
            app.nodes.append((self.host.text, int(self.port.text), "", ""))        
        self.host.text = ""
        self.port.text = "" 

    def to_curr(self, instance):
        app = App.get_running_app()
        app.sm.current = "ChainScreen"

##refresh page within blockchain view probably ?
class PCApp(App):

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
        self.message_recieved_queue.append(json.loads(data.decode("utf-8")))
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
        message = json.dumps({
            "type":"Blockchain_Update",
            "signature":self.signature, #i think we should sign the block ? then verification happens when we 
            "uname":self.uname,
            "chain":self.blockchain.chain,
            "comments":self.blockchain.comments
        }).encode("utf-8")
        for i in self.nodes:
            #shuold be node tuple
            self.send_message(message, i[0], i[1])     
 
    def build(self):
        self.sm = ScreenManager(transition=WipeTransition())

        self.port = sys.argv[1]
        self.host = socket.gethostbyname(socket.gethostname())
        self.nodes = []

        self.signature = ""
        self.uname = sys.argv[2]        

        self.message_recieved_queue = []
        self.message_recieved_lock = threading.Lock()

        #self.sql_lock = threading.Lock()

        self.blockchain = Blockchain()
        comments_page = CurrentBlockScreen()
        blockchain_page = ChainScreen()
        network_page = NetworkScreen()
        
        self.sm.add_widget(blockchain_page.root)
        self.sm.add_widget(comments_page.root)
        self.sm.add_widget(network_page.root)

        Clock.schedule_interval(self.send_blockchain_update, 7)
        Clock.schedule_interval(self.read_message_queue, 10)

        threading.Thread(target=self.run_server, args=()).start()        

        return runTouchApp(self.sm)

def run_pc_app():
    PCApp().run()

#argv[1] = port
run_pc_app()
    
