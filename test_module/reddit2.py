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
from request_maker import Request_Maker
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
import threading
from server import Server
import sys
from kivy.app import runTouchApp
from kivy.uix.screenmanager import ScreenManager, Screen, WipeTransition
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from random import randint
from components import BlockchainDisplay

from kivy.core.window import Window
import time
from components import BlockchainDisplay, CurrentBlockDisplay

from blockchain import Blockchain

class ChainScreen(Screen):
    def __init__(self):
        self.root = Screen(name="ChainScreen")
        #data is blockchain
        scroll = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
        app = App.get_running_app()
        data = app.blockchain.chain
        print("blockchain data")
        grid = GridLayout(cols=1)
        b = BlockchainDisplay(data)
        scroll.add_widget(b.root)
        grid.add_widget(scroll)

        #app = App.get_running_app()
        print("\n \n \n")
        print("\n")
        refresh_chain = Button(text="get chain")
        refresh_chain.bind(on_press=self.refresh_comments)
        
        grid.add_widget(refresh_chain)

        switch_page = Button(text="View Current Block")
        switch_page.bind(on_press=self.switch_page)
        grid.add_widget(switch_page)
        self.root.add_widget(grid)

    def switch_page(self, instance):
        app = App.get_running_app()
        #print(app.sm.current)
        app.sm.current = "CurrentBlockScreen"
        #print("\n \n")
        #app.root.current="CurrenBlockScreen"

    def refresh_comments(self, instance):
        
        app = App.get_running_app()
        print("refreshing")
        #print(app.sm.current)
        #if data == 1:
         #   print('fail gettin data')
        #print(json.loads(data._content)['chain']) 

class CurrentBlockScreen(Screen):
    def __init__(self):
        self.root = Screen(name="CurrentBlockScreen")
        grid = GridLayout(cols = 1)
        app = App.get_running_app()
        data = app.blockchain.chain  
        comments = app.blockchain.comments
        print(data," in CurrBlockScreen")
        #for i in data:
            #data is map of comments i think
        grid.add_widget(CurrentBlockDisplay(data, comments).root)
        grid.add_widget(Label(text="enter comment"))

        self.comment = TextInput()
        grid.add_widget(self.comment)
        submit_comment = Button(text="submit")
        submit_comment.bind(on_press=self.submit_comment)

        mine = Button(text="mine")
        mine.bind(on_press=self.mine)

        grid.add_widget(mine)
        grid.add_widget(submit_comment)
        switch_page = Button(text="Switch Page")
        switch_page.bind(on_press=self.switch_page)
        grid.add_widget(switch_page)
        self.root.add_widget(grid)

    def switch_page(self, instance):
        print("on page switch") 
        app = App.get_running_app()
        app.sm.current = "ChainScreen"
        print("\n \n")

        #app.root.current="CurrenBlockScreen"
    def submit_comment(self, instace):
        app.blockchain.add_comment(self.comment.text, "Signature1", "General", "UserName1")
        #ask update screen
    
    def mine(self, instance):

        app = App.get_running_app()
        app.blockchain.mine("UserName1")
        #print(app.sm.current)
import sys
##refresh page within blockchain view probably ?
class PCApp(App):
    i = 0
    def build(self):
        self.sm = ScreenManager(transition=WipeTransition())
        self.port = sys.argv[1]
        if data == 1:
            print('fail gettin data')
        
        self.blockchain = Blockchain()
        comments_page = CurrentBlockScreen()
        blockchain_page = ChainScreen()
        
        self.sm.add_widget(blockchain_page.root)
        self.sm.add_widget(comments_page.root)


        return runTouchApp(self.sm)


def run_pc_app():
    PCApp().run()

#argv[1] = port
run_pc_app()
    
