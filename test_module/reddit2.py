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

import sys
from kivy.core.window import Window
import time
from components import BlockchainDisplay, CurrentBlockDisplay

from blockchain import Blockchain

class ChainScreen(Screen):
    def __init__(self):
        self.root = Screen(name="ChainScreen")
        #data is blockchain
        self.scroll = ScrollView(size_hint=(1, .6), size=(Window.width, Window.height))
        print("blockchain data")
        grid = GridLayout(cols=1)
        self.b = BlockchainDisplay()
        self.scroll.add_widget(self.b.root)
        grid.add_widget(self.scroll)

        #app = App.get_running_app()
        print("\n \n \n")
        print("\n")
        refresh_chain = Button(text="refresh chain", size_hint_y=.2)
        refresh_chain.bind(on_press=self.refresh_chain)
        
        grid.add_widget(refresh_chain)

        switch_page = Button(text="View Current Block", size_hint_y=.2)
        switch_page.bind(on_press=self.switch_page)
        grid.add_widget(switch_page)
        self.root.add_widget(grid)

    def switch_page(self, instance):
        app = App.get_running_app()
        #print(app.sm.current)
        app.sm.current = "CurrentBlockScreen"
        #clear widget
    def refresh_chain(self, instance):
        
        app = App.get_running_app()
        self.scroll.clear_widgets()
        self.b = BlockchainDisplay()
        self.scroll.add_widget(self.b.root)
               

class CurrentBlockScreen(Screen):
    def __init__(self):
        self.root = Screen(name="CurrentBlockScreen")
        self.grid = GridLayout(cols = 1)
        app = App.get_running_app()
        data = app.blockchain.chain[-1] 
        comments = app.blockchain.comments
        print(data," in CurrBlockScreen")
        #for i in data:
            #data is map of comments i think
        self.block_display = CurrentBlockDisplay().root
        self.grid.add_widget(self.block_display)
        self.grid.add_widget(Label(text="enter comment"))

        self.comment = TextInput()
        self.grid.add_widget(self.comment)
        submit_comment = Button(text="submit")
        submit_comment.bind(on_press=self.submit_comment)

        mine = Button(text="mine")
        mine.bind(on_press=self.mine)

        self.grid.add_widget(mine)
        self.grid.add_widget(submit_comment)

        switch_page = Button(text="Switch Page")
        switch_page.bind(on_press=self.switch_page)

        refresh_page = Button(text="Refresh Page")
        refresh_page.bind(on_press=self.reload_current_block)

        self.grid.add_widget(refresh_page)
        self.grid.add_widget(switch_page)
        self.root.add_widget(self.grid)

    def switch_page(self, instance):
        print("on page switch") 
        app = App.get_running_app()
        app.sm.current = "ChainScreen"

        #app.root.current="CurrenBlockScreen"
    def submit_comment(self, instace):

        app = App.get_running_app()
        app.blockchain.add_comment(self.comment.text, "Signature1", "General", "UserName1")
        #ask update screen
    
    def mine(self, instance):

        app = App.get_running_app()
        app.blockchain.mine("UserName1")
        #print(app.sm.current)

    def reload_current_block(self, instance):
        #app = App.get_running_app()
        #data = app.blockchain.chain[-1]
        self.grid.remove_widget(self.block_display)
        self.block_display = CurrentBlockDisplay().root
        self.grid.add_widget(self.block_display)

##refresh page within blockchain view probably ?
class PCApp(App):
    i = 0
    def build(self):
        self.sm = ScreenManager(transition=WipeTransition())
        self.port = sys.argv[1]
        
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
    
