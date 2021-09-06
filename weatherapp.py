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
        try:
            key = store.get('settings')['apikey']
            units = '&units=metric'
            city = self.root.ids.city.text
            url = 'https://api.openweathermap.org/data/2.5/weather?q='
            self.resp = requests.get(url + city + '&appid=' + key + units).json()
            self.root.ids.city.text = ''
            return self.resp
            
        except:
            'Error'

    def results(self):
        if self.resp['cod'] == 200:
            self.root.ids.results.add_widget(
                    MDLabel(text=self.resp['name'], font_style='H3', pos_hint={"center_y": 0.8,"center_x": 0.6})
                )

            self.root.ids.results.add_widget(
                    MDLabel(text=str(self.resp['main']['temp']) + '°C', font_style='H4', pos_hint={"center_y": 0.65,"center_x": 0.6})
                )

            self.root.ids.results.add_widget(
                    AsyncImage(source="http://openweathermap.org/img/wn/" + self.resp['weather'][0]['icon'] + '@2x.png', pos_hint={"center_y": 0.67,"center_x": 0.7})
            )

            self.root.ids.results.add_widget(
                    MDLabel(text=str(self.resp['sys']['country']), pos_hint={"center_y": 0.75,"center_x": 0.6})
                )

            self.root.ids.results.add_widget(
                    MDLabel(text=self.resp['weather'][0]['description'], font_style='H5', pos_hint={"center_y": 0.6,"center_x": 0.6})
                )

            self.root.ids.results.add_widget(
                    Image(source="humidity.png" ,pos_hint={"center_y": 0.5,"center_x": 0.15}, size_hint_x=0.07, size_hint_y=0.07)
            )

            self.root.ids.results.add_widget(
                    MDLabel(text=str(self.resp['main']['humidity']) + '%', pos_hint={"center_y": 0.5,"center_x": 0.7})
                )

            self.root.ids.results.add_widget(
                    Image(source="wind.png" ,pos_hint={"center_y": 0.45,"center_x": 0.15}, size_hint_x=0.07, size_hint_y=0.07,)
            )

            self.root.ids.results.add_widget(
                    MDLabel(text=str(self.resp['wind']['speed']) + ' M/S', pos_hint={"center_y": 0.45,"center_x": 0.7})
                )
        else:
            self.root.ids.results.add_widget(
                    MDLabel(text=str(self.resp['cod']), font_style='H3', halign="center", pos_hint={"center_y": 0.5,"center_x": 0.5})
                )
            self.root.ids.results.add_widget(
                    MDLabel(text=str(self.resp['message']), size_hint_x=None, halign="center", width=280, pos_hint={"center_y": 0.4,"center_x": 0.5})
                )


class ContentNavigationDrawer(MDBoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()


WeatherApp().run()