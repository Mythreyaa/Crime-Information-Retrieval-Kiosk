from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.core.text import LabelBase
from kivymd.uix.list import OneLineListItem
from kivy.animation import Animation
from kivymd.uix.button import MDIconButton
from kivy.properties import NumericProperty
from kivymd.uix.screen import MDScreen,Screen
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget 
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from asr import * 


Window.size = (350,580)

from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button

class DetailsPopup(Popup):
    def __init__(self, details_text, **kwargs):
        super().__init__(**kwargs)
        self.title = "Dish Details"  # Set the title of the popup
        self.size_hint = (None, None)  # Disable size_hint so you can set a fixed size
        self.size = (500, 800)  # Set the size of the popup

        cols = ["INCIDENT_NUMBER","OFFENSE_CODE","OFFENSE_DESCRIPTION","DISTRICT","REPORTING_AREA",
              "OCCURRED_ON_DATE","YEAR","MONTH","DAY_OF_WEEK","HOUR","STREET"]
        line = ""

        for i in range(len(cols)):
            line += cols[i] + "\n" + details_text[i] + "\n\n"
        
        self.details_text_input = TextInput(text=line, readonly=True, size_hint=(None, None),
                                                size=(self.width - 20, self.height - 50), multiline=True,
                                                padding=(10, 10))
        self.details_text_input.pos_hint = {"center_x": 0.5, "center_y": 0.6}
        self.add_widget(self.details_text_input)

class MyApp(MDApp,Widget):
    def build(self):
        # global screen_manager
        # screen_manager = Screen()
        
        # self.mainsc = Builder.load_file("main.kv") #Flavorphile screen
        # screen_manager.add_widget(self.mainsc)
        
        # self.homesc = Builder.load_file("home.kv") #voice input screen
        
        # self.ressc = Builder.load_file("res.kv") #output screen
        
        # return screen_manager

        self.screen_manager = ScreenManager()

        # Load the screens from .kv files
        self.mainsc = Builder.load_file("main.kv")
        self.homesc = Builder.load_file("home.kv")
        self.ressc = Builder.load_file("res.kv")

        # Add the screens to the ScreenManager
        self.screen_manager.add_widget(self.mainsc)
        self.screen_manager.current = "main"
        self.screen_manager.add_widget(self.homesc)
        self.screen_manager.add_widget(self.ressc)

        # Return the ScreenManager as the root widget
        return self.screen_manager
    
    def on_start(self):
        Clock.schedule_once(self.home,10)

    def home(self,*args):
        self.screen_manager.current = 'home'

    def on_voice_search(self):
        text = "You are searching for record with code..." + "\n\n" + voice_recognize().title()
        output_label = self.homesc.ids.output_label 
        output_label.text = text
        Clock.schedule_once(self.result,1)

    def result(self,*args):
        print("Result")
        res = invoke_recognize()
        self.ressc.ids.list_view.clear_widgets()
        for dish in res:
            #print("Dish:",dish)
            item = OneLineListItem(text=dish.split("||")[0])
            item.bind(on_release=lambda item, d=dish: self.on_item_click(d))
            self.ressc.ids.list_view.add_widget(item)

        self.screen_manager.current = "res"
    
    def on_item_click(self, instance):
        #print("INST:",instance)
        d_text = self.get_details_for_item(instance)  # Replace with your function to get details
        popup = DetailsPopup(details_text=d_text)
        popup.open()

    def get_details_for_item(self,text):
        return text.split("||")


if __name__ == "__main__":
    MyApp().run()
