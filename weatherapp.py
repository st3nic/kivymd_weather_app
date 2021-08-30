from kivy.core.window import Window
from kivy.properties import ObjectProperty, StringProperty
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import IconLeftWidget, OneLineListItem, OneLineIconListItem, TwoLineListItem
from kivy.storage.jsonstore import JsonStore
from kivy.uix.image import Image, AsyncImage
import requests

store = JsonStore('settings.json')

Window.size = 320,600

class WeatherApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark" 

    def save_settings(self):
        key = self.root.ids.apikey.text
        store.put('settings', apikey=key)

    def get_settings(self):
        key = store.get('settings')['apikey']
        return key

    def get_weather(self):
        key = store.get('settings')['apikey']
        units = '&units=metric'
        city = self.root.ids.city.text
        url = 'https://api.openweathermap.org/data/2.5/weather?q='
        self.resp = requests.get(url + city + '&appid=' + key + units).json()
        self.root.ids.city.text = ''
        return self.resp

    def results(self):
        print(self.resp)
        self.root.ids.results.add_widget(
                MDLabel(text=self.resp['name'], pos_hint={"center_y": 0.8,"center_x": 0.5})
            )

        self.root.ids.results.add_widget(
                MDLabel(text=str(self.resp['main']['temp']) + '°C',pos_hint={"center_y": 0.6,"center_x": 0.5})
            )

        self.root.ids.results.add_widget(
                AsyncImage(source="http://openweathermap.org/img/wn/" + self.resp['weather'][0]['icon'] + '@2x.png')
        )

        
class ContentNavigationDrawer(MDBoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()


WeatherApp().run()