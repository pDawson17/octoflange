from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
import json
import threading

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
