from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
#need request maker for refresh
import sys
from kivy.app import App
sys.path.append("../")

class Comment(GridLayout):
    def __init__(self, data):
        self.data = data
        print(self.data)
        self.root = GridLayout(cols=3)
        upvote = Button(text="upvote")
        upvote.bind(on_press=self.upvote)
        self.root.add_widget(upvote)

    def upvote(self, instance):
        print("UPVOTE",self.data)

        app = App.get_running_app()
        #app.blockchain.like_comment()

class CurrentBlockDisplay(GridLayout):
    def __init__(self, block, comments):
        self.block = block
        self.comments = comments
        app = App.get_running_app()
        print(app.port)
        self.root = GridLayout(rows=3, spacing=10, size_hint_x=.5, size_hint_y=2)
        for i in self.comments:
            self.root.add_widget(Comment(i).root)
        self.root.add_widget(Label(text=str(app.port)))
