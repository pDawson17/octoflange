import sys
from screens.components import BlockchainDisplay
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.core.window import Window

class ChainScreen(Screen):
    def __init__(self):
        self.root = Screen(name="ChainScreen")
        #data is blockchain
        self.scroll = ScrollView(size_hint=(1, .6), size=(Window.width, Window.height))
        grid = GridLayout(cols=1)
        self.b = BlockchainDisplay()
        self.scroll.add_widget(self.b.root)
        grid.add_widget(self.scroll)

        #app = App.get_running_app()
        refresh_chain = Button(text="refresh chain", size_hint_y=.2)
        refresh_chain.bind(on_press=self.refresh_chain)

        grid.add_widget(refresh_chain)

        to_network = Button(text="To Netowrk View", size_hint_y=.2)
        to_network.bind(on_press=self.switch_to_network)

        switch_page = Button(text="View Current Block", size_hint_y=.2)

        switch_page.bind(on_press=self.switch_page)

        grid.add_widget(to_network)
        grid.add_widget(switch_page)
        self.root.add_widget(grid)

    def switch_to_network(self, instance):
        app = App.get_running_app()
        app.sm.current = "NetworkScreen"

    def switch_page(self, instance):
        app = App.get_running_app()
        app.sm.current = "CurrentBlockScreen"

    def refresh_chain(self, instance):

        app = App.get_running_app()
        self.scroll.clear_widgets()
        self.b = BlockchainDisplay()
        self.scroll.add_widget(self.b.root)

