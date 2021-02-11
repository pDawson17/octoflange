
from screens.components import CurrentBlockDisplay
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.uix.textinput import TextInput

class CurrentBlockScreen(Screen):
    def __init__(self):
        self.root = Screen(name="CurrentBlockScreen")
        self.grid = GridLayout(cols = 1) #block content, then comment scrollview, then text input

        #for i in data:
            #data is map of comments i think
        mine = Button(text="mine")
        mine.bind(on_press=self.mine)


        switch_page = Button(text="Switch Page")
        switch_page.bind(on_press=self.switch_page)

        refresh_page = Button(text="Refresh Page", background_color="blue")
        refresh_page.bind(on_press=self.reload_current_block)

        toolbar = GridLayout(cols=3, size_hint_y=.3)
        toolbar.add_widget(refresh_page)

        toolbar.add_widget(switch_page)
        toolbar.add_widget(mine)

        self.root.add_widget(self.grid)

        self.block_display = CurrentBlockDisplay(-1).root

        self.block_display_container=GridLayout(cols=1) #just to make refresh stay in one spot
        self.block_display_container.add_widget(self.block_display)    

        self.grid.add_widget(self.block_display_container)

        self.grid.add_widget(toolbar)

    def switch_page(self, instance):
        app = App.get_running_app()
        app.sm.current = "ChainScreen"

    def mine(self, instance):

        app = App.get_running_app()
        app.blockchain.mine(app.uname)

    def reload_current_block(self, instance):
        #app = App.get_running_app()
        #data = app.blockchain.chain[-1]
        self.block_display_container.remove_widget(self.block_display)
        self.block_display = CurrentBlockDisplay(-1).root
        self.block_display_container.add_widget(self.block_display)

