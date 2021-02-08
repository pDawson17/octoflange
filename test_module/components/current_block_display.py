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
        self.root = GridLayout(cols=3)

        self.text_label = Label(text=self.data["comment"], font_size=35)

        self.root.add_widget(self.text_label)        

        upvote = Button(text="upvote")
        upvote.bind(on_press=self.upvote)
        self.root.add_widget(upvote)

    def upvote(self, instance):

        app = App.get_running_app()
        app.blockchain.update_likes(self.data["comment"], self.data["signature"], self.data["likes"], "Signature1", 1)
        #app.blockchain.like_comment()

class CurrentBlockDisplay(GridLayout):
    def __init__(self, index):
        
        app = App.get_running_app()
        self.block = app.blockchain.chain[index]
        self.comments = app.blockchain.comments
        self.grid = GridLayout(rows=1, spacing=10, size_hint_x=6, size_hint_y=1)
        for i in self.comments:

            self.grid.add_widget(Comment(self.comments[i]).root)
        self.scroll = ScrollView(size_hint=(1,.8), do_scroll_y=False)
        self.scroll.add_widget(self.grid)
        
        self.root = GridLayout(rows=2)
        self.root.add_widget(self.scroll)

        self.comments_bar = GridLayout(cols=2, size_hint_y=.4)
        if index == -1:
            self.comment = TextInput()
            submit_button = Button(text="submit comment", size_hint_x=.3)
            submit_button.bind(on_press=self.submit_comment)        


            self.comments_bar.add_widget(self.comment)
            self.comments_bar.add_widget(submit_button)
            self.root.add_widget(self.comments_bar)

    def submit_comment(self, instance):
        app = App.get_running_app()
        app.blockchain.add_comment(self.comment.text, ("Signature1"+str(app.port)), ("General"), ("User1"+str(app.port)))
        self.comment.text = ""
