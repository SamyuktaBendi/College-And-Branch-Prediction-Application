from kivy.app import App
from kivy.properties import StringProperty
from kivy.lang import Builder
from kivy.uix.recycleview import RecycleView
#import dfgui
import xlrd
import pandas as pd
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout

from kivy.uix.label import Label
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.button import Button
from kivy.properties import BooleanProperty, ListProperty, ObjectProperty
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.core.window import Window
# Create both screens. Please note the root.manager.current: this is how
# you can control the ScreenManager from kv. Each screen has by default a
# property manager that gives you the instance of the ScreenManager used.
Builder.load_string("""
<LoginScreen>:
    BoxLayout:
        id: login_layout
        orientation: 'vertical'
        padding: [10,50,10,50]
        spacing: 50

        Label:
            text: 'Welcome'
            font_size: 32

        BoxLayout:
            orientation: 'vertical'

            Label:
                text: 'Login'
                font_size: 18
                halign: 'left'
                text_size: root.width-20, 20

            TextInput:
                id: login
                multiline:False
                font_size: 16

        BoxLayout:
            orientation: 'vertical'
            Label:
                text: 'Password'
                halign: 'left'
                font_size: 18
                text_size: root.width-20, 20

            TextInput:
                id: password
                multiline:False
                password:True
                font_size: 28

        Button:
            text: 'Login'
            font_size: 24

            on_press: root.manager.current = 'connected'

        Button:
            text: "Don't have an account? Sign Up"
            font_size: 24
            on_press: root.manager.current = 'signup'

<SignupScreen>:
    BoxLayout:
        id: signup_layout
        orientation: 'vertical'
        padding: [5,30,5,30]
        spacing: 30

        Label:
            text: 'Signing Up'
            font_size: 32

        BoxLayout:
            orientation: 'vertical'

            Label:
                text: 'First Name'
                font_size: 18
                halign: 'left'
                text_size: root.width-30, 30

            TextInput:
                id: firstname
                multiline:False
                font_size: 16
        BoxLayout:
            orientation: 'vertical'

            Label:
                text: 'Last Name'
                font_size: 18
                halign: 'left'
                text_size: root.width-20, 20

            TextInput:
                id: lastname
                multiline:False
                font_size: 16
        BoxLayout:
            orientation: 'vertical'

            Label:
                text: 'Email ID'
                font_size: 18
                halign: 'left'
                text_size: root.width-20, 20

            TextInput:
                id: emailid
                multiline:False
                font_size: 16
        
        BoxLayout:
            orientation: 'vertical'
            Label:
                text: 'Password'
                halign: 'left'
                font_size: 16
                text_size: root.width-20, 20

            TextInput:
                id: password
                multiline:False
                password:True
                font_size: 28

        Button:
            text: 'Finish Sign Up and Login'
            font_size: 24

            on_press: root.manager.current = 'login'

<ConnectedScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: [50,250,50,250]
        
        spacing: 30
        Label: 
            text: 'Choose Your Exam'
            font_size: 32
        Button:
            text: 'JEE Advanced'
            on_press: root.manager.current= 'jadv'
        Button:
            text: 'Back to Login'
            on_press: root.manager.current = 'login'
            
<JEEAdvancedScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: [10,50,10,50]
        spacing: 50

        Label:
            text: 'Enter Your Details'
            font_size: 32
        
        BoxLayout:
            orientation: 'vertical'

            Label:
                text: 'Category i.e. GEN, OBC, SC, ST'
                font_size: 18
                halign: 'left'
                text_size: root.width-20, 20

            TextInput:
                id: cat
                multiline:False
                font_size: 16

        BoxLayout:
            orientation: 'vertical'
            Label:
                text: 'Rank'
                halign: 'left'
                font_size: 18
                text_size: root.width-20, 20

            TextInput:
                id: rank
                multiline:False
                font_size: 16
        Button:
            text: 'Get Prediction'
            on_press: root.manager.current = 'predict'
                
        Button:
            text: 'Back to Login'
            on_press: root.manager.current = 'login'
            
<SelectableButton>:
    # Draw a background to indicate selection
    canvas.before:
        #Color:
        #    rgba: (0, 0.517, 0.705, 1) if self.selected else (0, 0.517, 0.705, 1)
        Rectangle:
            pos: self.pos
            size: self.size
    background_color: [1, 0, 0, 1]  if self.selected else [1, 1, 1, 1]  # dark red else dark grey
    #on_release: app.root.delete_row(self)

<Predict>:
    column_headings: column_headings
    orientation: "vertical"

    Label:
        canvas.before:
            Color:
                rgba: (0, 0, 1, .5)     # 50% translucent blue
            Rectangle:
                pos: self.pos
                size: self.size
        text: 'Click on any row to delete'
        size_hint: 1, 0.1

    GridLayout:
        canvas.after:
            Color:
                rgba: (1, 0.2, 0, .5)     # 50% translucent orange red
            Rectangle:
                pos: self.pos
                size: self.size

        id: column_headings
        size_hint: 1, None
        size_hint_y: None
        height: 25
        cols: 3

    BoxLayout:
        canvas.before:
            Color:
                rgba: (.0, 0.9, .1, .3)
            Rectangle:
                pos: self.pos
                size: self.size

        RecycleView:
            viewclass: 'SelectableButton'
            data: root.rv_data
            SelectableRecycleGridLayout:
                cols: 2
                key_selection: 'selectable'
                default_size: None, dp(26)
                default_size_hint: 1, None
                size_hint_y: None
                height: self.minimum_height
                multiselect: True
                touch_multiselect: True
                
       
""")
class SelectableRecycleGridLayout(FocusBehavior, LayoutSelectionBehavior,
                                  RecycleGridLayout):
    ''' Adds selection and focus behaviour to the view. '''

class SelectableButton(RecycleDataViewBehavior, Button):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableButton, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableButton, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected

# Declare both screens
class LoginScreen(Screen):
    pass
class SignupScreen(Screen):
    pass
class ConnectedScreen(Screen):
    pass
class JEEAdvancedScreen(Screen):
    pass

class Predict(Screen,BoxLayout):
    category = StringProperty(None)
    rank1 = StringProperty(None)
    items_list = ObjectProperty(None)
    column_headings = ObjectProperty(None)
    rv_data = ListProperty([])

    def __init__(self, **kwargs):
        super(Predict, self).__init__(**kwargs)
        self.predictor()

    def predictor(self):
        # fl2 = pd.read_excel("DataGen.xlsx")

        category = "GEN"
        if category == "GEN":
            fl = pd.read_excel(r"C:\Users\Sahithi Ravipati\Desktop\PD Lab\DataGEN.xlsx", encoding='latin-1')
        elif category == "OBC":
            fl = pd.read_excel(r"C:\Users\Sahithi Ravipati\Desktop\PD Lab\DataGEN.xlsx", encoding='latin-1')
        elif category == "SC":
            fl = pd.read_excel(r"C:\Users\Sahithi Ravipati\Desktop\PD Lab\DataSC.xlsx", encoding='latin-1')
        elif category == "ST":
            fl = pd.read_excel(r"C:\Users\Sahithi Ravipati\Desktop\PD Lab\DataST.xlsx", encoding='latin-1')
        # fl.head()

        # In[2]:

        #rank=int(input())
        rank = 8000

        # ## Updating Probabilities

        # In[3]:

        fl["prob2017"] = 0
        fl["prob2016"] = 0
        fl["prob2015"] = 0
        fl["prob2014"] = 0
        fl["prob2013"] = 0
        fl["prob2012"] = 0
        fl["prob2011"] = 0

        # In[4]:

        fl.loc[fl["2017CR"] > rank, "prob2017"] = 0.4
        fl.loc[fl["2016CR"] > rank, "prob2016"] = 0.25
        fl.loc[fl["2015CR"] > rank, "prob2015"] = 0.2
        fl.loc[fl["2014CR"] > rank, "prob2014"] = 0.075
        fl.loc[fl["2013CR"] > rank, "prob2013"] = 0.025
        fl.loc[fl["2012CR"] > rank, "prob2012"] = 0.025
        fl.loc[fl["2011CR"] > rank, "prob2011"] = 0.025
        # fl.head()

        # ## Finding Cumulative probability

        # In[5]:

        fl["fprob"] = fl["prob2017"] + fl["prob2016"] + fl["prob2015"] + fl["prob2014"] + fl["prob2013"] + fl[
            "prob2012"] + fl["prob2011"]

        # In[6]:

        # ## Extracting based on threshold probability

        # In[7]:

        fl1 = fl[fl["fprob"] > 0.6]

        # In[8]:

        fl2 = fl1.iloc[:, 1:3]

        # Extract and create column headings
        for heading in fl2.columns:
            self.column_headings.add_widget(Label(text=heading))

        # Extract and create rows
        data = []
        for row in fl2.itertuples():
            for i in range(1, len(row)):
                data.append([row[i], row[0]])
        self.rv_data = [{'text': str(x[0]), 'Index': str(x[1]), 'selectable': True} for x in data]

    def delete_row(self, instance):
        # TODO
        print("delete_row:")
        print("Button: text={0}, index={1}".format(instance.text, instance.index))
        print(self.rv_data[instance.index])
        print("Pandas: Index={}".format(self.rv_data[instance.index]['Index']))


# Create the screen manager
sm = ScreenManager()
bm= BoxLayout()
sm.add_widget(LoginScreen(name='login'))
sm.add_widget(SignupScreen(name='signup'))
sm.add_widget(ConnectedScreen(name='connected'))
sm.add_widget(JEEAdvancedScreen(name='jadv'))
sm.add_widget(Predict(name='predict'))

class TestApp(App):

    def build(self):
        return sm
    def get_application_config(self):
            if(not self.username):
                return super(TestApp, self).get_application_config()

            conf_directory = self.user_data_dir + '/' + self.username

            if(not os.path.exists(conf_directory)):
                os.makedirs(conf_directory)

            return super(TestApp, self).get_application_config(
                '%s/config.cfg' % (conf_directory)
            )

if __name__ == '__main__':
    TestApp().run()
