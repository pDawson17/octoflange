from kivy.uix.widget import Widget
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
import time
import json

class BlockView(GridLayout): #probably change to floatlayout eventually

    def __init__(self, data):
        self.root = GridLayout(cols=3, size_hint_y=.7)
        self.data = data
        self.index = data['index']
        if self.data == None:
            print("no data entered to blockview")
            self.root.add_widget(Label(text="error getting data"))
        
        comment_grid = GridLayout(rows=1)
        comments = self.data['comments']
        for i in comments:
            comment_grid.add_widget(Label(text=comments[i]['comment'], font_size=10))
        if len(comments) == 0:
            self.root.add_widget(Label(text="no comments", font_size=10))
        
        self.root.add_widget(comment_grid)

        button = Button(text="view block", font_size=10)
        button.bind(on_press=self.button_press)

        self.root.add_widget(button)

    def button_press(self, instance):
        print("NAVIGATE TO CLOSER BLOCKVIEW", self.data)
        #now either a popup for each one or navigate
        #to a third screen that ill set up to look at a specific one
class BlockchainDisplay(GridLayout): #replace w/ screen later

    def __init__(self):
        app = App.get_running_app()
        self.data = app.blockchain.chain
        if self.data == None:
            print("no data entered to blockchain display")
        
        self.root = GridLayout(cols=1, spacing=1, size_hint_y = 2)
        self.root.bind(minimum_height=self.root.setter('height'))
        for i in self.data:
            b = BlockView(i)
            self.root.add_widget(b.root) #b.root

