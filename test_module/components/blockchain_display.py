from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
import time
import json

class BlockView(GridLayout): #probably change to floatlayout eventually

    def __init__(self, data):
        self.root = GridLayout(cols=2, size_hint_y=.7)
        self.data = data
        if self.data == None:
            print("no data entered to blockview")
            self.root.add_widget(Label(text="error getting data"))
        
        print("in blockview", self.data)
        #loop thru & add all comments for now
        comments = self.data['comments']
        for i in comments:
            print("in comments", comments, i)
            self.root.add_widget(Label(text=comments[i], font_size=10))
        if len(comments) == 0:
            self.root.add_widget(Label(text="no comments", font_size=10))
        button = Button(text="view block", font_size=10)
        self.root.add_widget(button)
        button.bind(on_press=self.button_press)

    def button_press(self, instance):
        print("NAVIGATE TO CLOSER BLOCKVIEW", self.data)

class BlockchainDisplay(GridLayout): #replace w/ screen later

    def __init__(self, data):
        self.data = data
        if self.data == None:
            print("no data entered to blockchain display")
        #print("data is in bc display", data)
        
        self.root = GridLayout(cols=1, spacing=1, size_hint_y = 2)
        self.root.bind(minimum_height=self.root.setter('height'))
        for i in self.data:
            b = BlockView(i)
            self.root.add_widget(Label(text="ok"))
            self.root.add_widget(b.root) #b.root

