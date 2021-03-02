from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
import json
import threading

#class FriendsToolbar(GridLayout):
    #def __init__(self):
        #dm, direct transaction for now
       # self.root = GridLayout(cols=3)
       # self.send_money
        

class MoneyView(GridLayout):
    def __init__(self):
        self.root = GridLayout(cols=1)
        self.scroll = ScrollView(size_hint=(1, .7))
        self.friends_grid = GridLayout(cols=1)
        
        refresh_button = Button(text="refresh")
        refresh_button.bind(on_press=self.refresh_friends)

        self.root.add_widget(refresh_button) 
        self.fill_friends_grid()        
        self.scroll.add_widget(self.friends_grid)
        self.root.add_widget(self.scroll)

    #def fill_money_history(self):
        ##TODO:
    
    def refresh_grid(self, instance):
        self.fill_money_history()

class SendTransactionScreen(Screen):
    def __init__(self):
        self.root = Screen(name="NetworkScreen")
        self.grid = GridLayout(cols=3)

        toolbar = GridLayout(cols=3, size_hint_y=.3)

        money_view = GridLayout(rows=4)

        self.to_uname = TextInput()
        self.amount = TextInput() #replace later with uname or sig or someting idk
        
        self.uname = TextInput()
        self.grid.add_widget(Label(text="enter uname"))
        self.grid.add_widget(self.uname)

        self.amount = TextInput()
        self.grid.add_widget(Label(text="enter amoubt"))
        self.grid.add_widget(self.amount)
    
        submit_request = Button(text="send transactiion")
        submit_request.bind(on_press=self.send_transaction_press)
        self.grid.add_widget(submit_request)

        switch_page_curr = Button(text="To Current Block")
        switch_page_curr.bind(on_press=self.to_curr)

        toolbar.add_widget(switch_page_curr)
    
        self.root.add_widget(self.grid)

    def send_transaction_press(self, instance):
        #TODO:
            #fill in sig, uname
        app = App.get_running_app()
        message = json.dumps({
            "type":"Conn_Request",
            "node_tup":(app.host, int(app.port), app.uname, app.signature),
        }).encode("utf-8")

        if self.port.text != "":
            threading.Thread(target=app.send_message, args=(message, self.host.text, int(self.port.text))).start()
            app.nodes.append((self.host.text, int(self.port.text), "", ""))
        self.host.text = ""
        self.port.text = ""

    def to_curr(self, instance):
        app = App.get_running_app()
        app.sm.current = "ChainScreen"
