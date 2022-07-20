import os.path
import os
from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty
from kivymd.uix.navigationdrawer import MDNavigationLayout
from kivymd.app import MDApp
from kivymd.theming import ThemableBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import OneLineIconListItem, MDList, TwoLineIconListItem, IconLeftWidget, OneLineListItem, TwoLineListItem
from kivymd.uix.dialog import MDDialog
from kivy.properties import ObjectProperty
from kivymd.uix.button import MDFlatButton
from kivymd.uix.screen import MDScreen
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.datatables import MDDataTable
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
import firebase_admin
from kivymd.icon_definitions import md_icons
from kivy.uix.image import Image
from kivy.atlas import Atlas
from kivymd.uix.list import IRightBodyTouch, OneLineAvatarIconListItem
from firebase_admin import credentials, auth, db, storage
import json

# glogal variebles
employee_name = " "
class RegistrationWindow(MDScreen):

    def sing_up(self):

        password = self.ids["passw"].text
        email = self.ids["email"].text
        name = self.ids["name"].text

        close_btn = MDFlatButton(text="Close", on_release=self.close_dialog)

        if email == "" or password == "" or name == "":
            self.dialog = MDDialog(title="Error", text="No email, password or name entered",
                              buttons=[close_btn])
            self.dialog.open()
        else:
            if (str(email).find("@") != -1) == False:
                self.dialog = MDDialog(title="Error", text="Incorrect email",
                                       buttons=[close_btn])
                self.dialog.open()
            else:
                firebase_admin.auth.create_user(email=email, password=password, display_name=name)
                ref = db.reference("/Users")
                ref.set({
                    name:
                    {
                        u'password': password
                    }
                })
                self.manager.current = "Second"
    def close_dialog(self, obj):
        self.dialog.dismiss()


class SecondWindow(MDScreen):
    def get_data(self):
        ref = db.reference(f"/Users/Sergey/")
        item = ref.get()
        ref = db.reference(f"/Users/Sergey/employees/value")
        num = ref.order_by_key().get()
        item = str(item)
        item = item.replace("'", '"')
        obj = json.loads(item)
        # for i in range(num):
        print(obj['employees']['0']['first_name'])

    def start(self):
        self.data_tables.open()

    def go_back(self):
        self.manager.current = "Registration"

    class ContentNavigationDrawer(BoxLayout):

        screen_manager = ObjectProperty()
        nav_drawer = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.create_list)

    def create_list(self, *args):
        ref = db.reference(f"/Users/Sergey/")
        item = ref.get()
        item = str(item).replace("'", '"')
        obj = json.loads(item)
        for i in range(len(obj['employees']) - 1):
            self.ids.card_view.add_widget(OneLineListItem(
                text=obj["employees"][f"{i}"]["first_name"] + " " + obj["employees"][f"{i}"]["nick_name"],
                secondary_text="asdfgsdfg",
                on_press=self.mycallback)
            )
    def mycallback(self, instance):
        global employee_name
        employee_name = instance.text
        print(employee_name)
        self.manager.current = "EmployeeCard"
        self.manager.transition.direction = "left"

    def close_dialog(self, obj):
        self.dialog.dismiss()

class EmployeeCard(MDScreen):
    source_photo = StringProperty('unrecognize.jpg')
    name_of_employee = StringProperty('text')
    happy = StringProperty("happy")
    sad = StringProperty("sad")
    neutral = StringProperty("neutral")
    angry = StringProperty("angry")
    surprise = StringProperty("surprise")
    fear = StringProperty("fear")
    disgust = StringProperty("disgust")

    def on_enter(self, *args):
        def on_enter(interval):
            self.name_of_employee = employee_name
            if not os.path.exists(f'{employee_name}.jpg'):
                self.source_photo = f'unrecognize.jpg'
            else:
                self.source_photo = f'{employee_name}.jpg'
            ref = db.reference(f"/Users/Sergey/")
            item = ref.get()
            item = str(item).replace("'", '"')
            obj = json.loads(item)
            name = employee_name.split(' ')
            print(obj)
            for i in range(len(obj['employees']) - 1):
                print(i)
                if obj['employees'][f'{i}']['first_name'] == name[0] and obj['employees'][f'{i}']['nick_name'] == name[1]:
                    self.happy = str(obj['employees'][f'{i}']['happy'])
                    self.sad = str(obj['employees'][f'{i}']['sad'])
                    self.neutral = str(obj['employees'][f'{i}']['neutral'])
                    self.angry = str(obj['employees'][f'{i}']['angry'])
                    self.surprise = str(obj['employees'][f'{i}']['surprise'])
                    self.fear = str(obj['employees'][f'{i}']['fear'])
                    self.disgust = str(obj['employees'][f'{i}']['disgust'])

        Clock.schedule_once(on_enter)

class SingInWindow(MDScreen):
    # sing in function
    def sing_in(self):

        email = self.ids['email_sing_in'].text
        password = self.ids['passw_sing_in'].text

        close_btn = MDFlatButton(text="Close", on_release=self.close_dialog)

        if email == "" or password == "":
            self.dialog = MDDialog(title="Error", text="No email or password entered",
                              buttons=[close_btn])
            self.dialog.open()
        else:
            if (str(email).find("@") != -1) == False:
                self.dialog = MDDialog(title="Error", text="Incorrect email",
                                       buttons=[close_btn])
                self.dialog.open()
            else:
                name = firebase_admin.auth.get_user_by_email(email)
                name_db = name.display_name


                ref = db.reference(f"/Users/{name_db}/password")
                password2 = ref.order_by_key().get()
                print(password2)

                if password == password2:
                    self.manager.current = "Second"
                else:
                    self.dialog = MDDialog(title="Error", text="Wrong password",
                                           buttons=[close_btn])
                    self.dialog.open()

    # function for make close button in dialog window
    def close_dialog(self, obj):
        self.dialog.dismiss()

# class for make multiscreen app
class WindowManager(ScreenManager):
    pass


# run app
class MyMainApp(MDApp):
    def build(self):
        cred = credentials.Certificate("serviceAccountKey.json")
        firebase_admin.initialize_app(cred, {
	        'databaseURL':"https://emotion-recognition-v1-default-rtdb.europe-west1.firebasedatabase.app/",
            'databaseAuthVariableOverride': {
                'uid': 'my-service-worker'
            },
            'storageBucket': 'emotion-recognition-v1.appspot.com'
	    })

        self.theme_cls.primary_palette = "BlueGray"
        return Builder.load_file('main.kv')

if __name__ == '__main__':
    MyMainApp().run()