from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
#need request maker for refresh
import sys
from kivy.app import App
sys.path.append("../")

class Comment(GridLayout):
    def __init__(self, data):
        self.data = data
        print("in comment,", self.data)
        self.root = GridLayout(cols=3)

        self.text_label = Label(text=self.data["comment"], font_size=35)

        self.root.add_widget(self.text_label)        

        upvote = Button(text="upvote")
        upvote.bind(on_press=self.upvote)
        self.root.add_widget(upvote)

    def upvote(self, instance):
        print("UPVOTE",self.data)

        app = App.get_running_app()
        app.blockchain.update_likes(self.data["comment"], self.data["signature"], self.data["likes"], "Signature1", 1)
        #app.blockchain.like_comment()

class CurrentBlockDisplay(GridLayout):
    def __init__(self):
        
        app = App.get_running_app()
        self.block = app.blockchain.chain[-1]
        self.comments = app.blockchain.comments
        self.grid = GridLayout(rows=3, spacing=10, size_hint_x=.5, size_hint_y=2)
        for i in self.comments:

            self.grid.add_widget(Comment(self.comments[i]).root)
        self.root = ScrollView(size_hint=(1,.4), do_scroll_y=False)
        self.root.add_widget(self.grid)
