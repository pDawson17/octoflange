from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
import sys
from kivy.app import App
sys.path.append("../")
import time

class Comment(GridLayout):
    def __init__(self, data):
        self.data = data #FIELDS: comment, likes, dislikes, uname, timestamp, topic, signature
        self.root = GridLayout(rows=2, size_hint_x=.25)
        print("IN COMMENT", data)
        self.text_label = Label(text=self.data["comment"], font_size=35)
   
        self.info = GridLayout(cols=6) 

        self.info.add_widget(Label(text="commenters name"))
        self.info.add_widget(Label(text=self.data["uname"]))

        self.info.add_widget(Label(text="timestamp"))
        self.info.add_widget(Label(text=str(self.data["timestamp"])))

        self.info.add_widget(Label(text="likes"))
        self.info.add_widget(Label(text=str(len(self.data["likes"]))))

        self.info.add_widget(Label(text="dislikes"))
        self.info.add_widget(Label(text=str(len(self.data["dislikes"]))))

        upvote = Button(text="upvote")
        upvote.bind(on_press=self.upvote)
        self.info.add_widget(upvote)
 
        downvote = Button(text="downvote")
        downvote.bind(on_press=self.downvote)
        self.info.add_widget(downvote)
      
        self.root.add_widget(self.text_label)        

        self.root.add_widget(self.info)

    def upvote(self, instance):

        app = App.get_running_app()
        app.blockchain.update_likes(self.data["comment"], self.data["signature"], {app.signature: 1})
        #app.blockchain.like_comment()
 
    def downvote(self, instance):

        app = App.get_running_app()
        app.blockchain.update_dislikes(self.data["comment"], self.data["signature"], {app.signature: 1})
        #app.blockchain.like_comment()


class CurrentBlockDisplay(GridLayout):
    def __init__(self, index):
        
        app = App.get_running_app()
        self.block = app.blockchain.chain[index]
        self.comments = app.blockchain.comments
        #so we want N commments to take up the page, size_hint_x will be: lencomments/num per page
        size_x = max(len(self.comments)/4, 1) #but never less than 1
        self.grid = GridLayout(rows=1, spacing=10, size_hint_x=size_x, size_hint_y=1)
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
        app.blockchain.add_comment(self.comment.text, app.signature, "General", app.uname)
        self.comment.text = ""
