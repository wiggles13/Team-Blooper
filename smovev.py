from kivy.uix.gridlayout import GridLayout
from kivy.app import App
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.config import Config
from kivy.core.text import LabelBase
import time as t
from kivy.uix.popup import Popup
from Main.py import main as Main
from Main.py import payment as cr

LabelBase.register(
    name="Luna2",
    fn_regular="fonts/LunaLuna-lRz5.ttf"
)

# Config.set('graphics', 'show_cursor', '0')
Config.set('graphics', 'width', '720')
Config.set('graphics', 'height', '1280')
Config.set('graphics', 'borderless', '1')
Config.set('graphics', 'resizable', '1')

class Menu(App):
    def IceCallback(self, instance, state):
        if state == 'down':
            self.iceval = instance.text
        else:
            self.iceval = "No Selection"
        self.icelabel.text = f"Value: {self.iceval}"
    
    def SizeCallback(self, instance, state):
        if state == 'down':
            self.sizeval = instance.text
        else:
            self.sizeval = "No Selection"
        self.sizelabel.text = f"Value: {self.sizeval}"
        
    def BobaCallback(self, instance, state):
        if state == 'down':
            self.bobaval = instance.text
        else:
            self.bobaval = "No Selection"
        self.bobalabel.text = f"Value: {self.bobaval}"  
        
    def bobaMake(self, instance, state):
        if state == 'down':
            answ = {
                0 : "Success!",
                1 : "Invalid currency detected!",
                2 : "No cup detected!"
                }
            
            if (self.iceval != "No Selection") * (self.bobaval != "No Selection") * (self.sizeval != "No Selection") != 0:
                exitButsm = Button(text="Please Insert Card", 
                                   font_name="Luna2",
                                   font_size="40sp") 
                popUp = Popup(title='Status', pos_hint={'center_x': 0.5, 'center_y': 0.5}, size_hint= (None, None), size=(500, 200), content=exitButsm)
                exitButsm.bind(on_release=popUp.dismiss)
                popUp.open()
                
                cardRead = cr()
                
                if cardRead == 1:
                    popUp.dismiss()
                    
                    exitButNP = Button(text="No Payment Recieved.", 
                                    font_name="Luna2",
                                    font_size="40sp") 
                    popUpNP = Popup(title='Status', pos_hint={'center_x': 0.5, 'center_y': 0.5}, size_hint= (None, None), size=(500, 200), content=exitButNP)
                    exitButNP.bind(on_release=popUpNP.dismiss)
                    popUpNP.open()
                
                if cardRead == 0:
                    popUp.dismiss()
                    
                    exitButMake = Button(text="Payment Recieved! Making Boba...", 
                                    font_name="Luna2",
                                    font_size="40sp") 
                    popUpMake = Popup(title='Status', pos_hint={'center_x': 0.5, 'center_y': 0.5}, size_hint= (None, None), size=(500, 200), content=exitButMake)
                    exitButMake.bind(on_release=popUpMake.dismiss)
                    popUpMake.open()
                    
                    response = Main.main(self.iceval, self.sizeval, self.bobaval)
                    
                    if response == 0:
                        popUpMake.dismiss()
                        exitBut2 = Button(text=answ[response], 
                                        font_name="Luna2",
                                        font_size="40sp") 
                        popUp2 = Popup(title='Status', pos_hint={'center_x': 0.5, 'center_y': 0.5}, size_hint= (None, None), size=(500, 200), content=exitBut2)
                        exitBut2.bind(on_release=popUp2.dismiss)
                    else:
                        popUpMake.dismiss()
                        exitButFail = Button(text=answ[response], 
                                        font_name="Luna2",
                                        font_size="40sp") 
                        popUpFail = Popup(title='Status', pos_hint={'center_x': 0.5, 'center_y': 0.5}, size_hint= (None, None), size=(500, 200), content=exitButFail)
                        exitButFail.bind(on_release=popUpFail.dismiss)
            else:
                choices = ["Ice Level", "Boba Type", "Size"]
                message = [choices[i] for i in [i for i, x in enumerate([self.iceval, self.bobaval, self.sizeval]) if x == "No Selection"]]
                
                exitButsm = Button(text=f"{str(message)[1:-1]} are not selected.",
                               font_name="Luna2",
                               font_size="20sp") 
                popUp = Popup(title='Status', pos_hint={'center_x': 0.5, 'center_y': 0.5}, size_hint= (None, None), size=(500, 200), content=exitButsm)
                exitButsm.bind(on_release=popUp.dismiss)
                
                popUp.open()

    def build(self):
        backgrounder = FloatLayout()

        # Background image
        background = Image(
            source='icons/moony.gif',
            allow_stretch=False,
            keep_ratio=True,
            anim_delay= 1 / 3)
        
        backgrounder.add_widget(background)
        
        layoutSize = GridLayout(rows=1, cols=3, size_hint=(None, None),
                                    padding=10, spacing=10, pos_hint={'center_x': 0.21, 'center_y': 0.57})
        
        self.iceval = "No Selection"
        self.icelabel = Label(text=f"Value: {self.iceval}", 
                              pos_hint={'center_x': 0.5, 'center_y': 0.8},
                              font_name="Luna2",
                              font_size="30sp")
        
        self.sizeval = "No Selection"
        self.sizelabel = Label(text=f"Value: {self.sizeval}", 
                               pos_hint={'center_x': 0.5, 'center_y': 0.62},
                               font_name="Luna2",
                               font_size="30sp")
        self.bobaval = "No Selection"
        self.bobalabel = Label(text=f"Value: {self.bobaval}", 
                               pos_hint={'center_x': 0.5, 'center_y': 0.44},
                               font_name="Luna2",
                               font_size="30sp")

        Icebtnlow = ToggleButton(text="Low Ice", 
                        background_normal='icons/noSelect.png',
                        background_down='icons/lowIce.png',
                        group = 'ice',
                        size_hint=(None, None),
                        size=(160, 160),
                        font_name="Luna2",
                        font_size="26sp",
                        pos_hint={'center_x': (275/720), 'center_y': 0.72})
        Icebtnlow.bind(state=self.IceCallback)
        
        Icebtnmed = ToggleButton(text="Normal Ice", 
                        background_normal='icons/noSelect.png',
                        background_down='icons/medIce.png',
                        group = 'ice',
                        size_hint=(None, None),
                        size=(160, 160),
                        font_name="Luna2",
                        font_size="20sp",
                        pos_hint={'center_x': (445/720), 'center_y': 0.72})
        Icebtnmed.bind(state=self.IceCallback)
        
        Icebtnhigh = ToggleButton(text="Many Ice", 
                        background_normal='icons/noSelect.png',
                        background_down='icons/highIce.png',
                        group = 'ice',
                        size_hint=(None, None),
                        size=(160, 160),
                        font_name="Luna2",
                        font_size="23sp",
                        pos_hint={'center_x': (615/720), 'center_y': 0.72})
        Icebtnhigh.bind(state=self.IceCallback)
        
        Icebtnno = ToggleButton(text="No Ice", 
                        background_normal='icons/noSelect.png',
                        background_down='icons/noIce.png',
                        group = 'ice',
                        size_hint=(None, None),
                        size=(160, 160),
                        font_name="Luna2",
                        font_size="27sp",
                        pos_hint={'center_x': (105/720), 'center_y': 0.72})
        Icebtnno.bind(state=self.IceCallback)
        
        btn4 = ToggleButton(text="Small", 
                        background_normal='icons/noSelect.png',
                        background_down='icons/pfp1smol.jpg',
                        group = 'size',
                        size_hint=(None, None),
                        size=(160, 160),
                        font_name="Luna2",
                        font_size="30sp")
        btn4.bind(state=self.SizeCallback)
        
        btn5 = ToggleButton(text="Medium", 
                        background_normal='icons/noSelect.png',
                        background_down='icons/pfp1smol.jpg',
                        group = 'size',
                        size_hint=(None, None),
                        size=(160, 160),
                        font_name="Luna2",
                        font_size="27sp")
        btn5.bind(state=self.SizeCallback)
        
        btn6 = ToggleButton(text="Large", 
                        background_normal='icons/noSelect.png',
                        background_down='icons/pfp1smol.jpg',
                        group = 'size',
                        size_hint=(None, None),
                        size=(160, 160),
                        font_name="Luna2",
                        font_size="30sp")
        btn6.bind(state=self.SizeCallback)
        
        bobabtnfew = ToggleButton(text="Few Boba", 
                        background_normal='icons/noSelect.png',
                        background_down='icons/bobaLow.png',
                        group = 'boba',
                        size_hint=(None, None),
                        size=(160, 160),
                        font_name="Luna2",
                        font_size="20sp",
                        pos_hint={'center_x': (275/720), 'center_y': 0.36})
        bobabtnfew.bind(state=self.BobaCallback)
        
        bobabtnno = ToggleButton(text="No Boba", 
                        background_normal='icons/noSelect.png',
                        background_down='icons/noBoba.png',
                        group = 'boba',
                        size_hint=(None, None),
                        size=(160, 160),
                        font_name="Luna2",
                        font_size="23sp",
                        pos_hint={'center_x': (105/720), 'center_y': 0.36})
        bobabtnno.bind(state=self.BobaCallback)
        
        bobabtnmed = ToggleButton(text="Medium Boba", 
                        background_normal='icons/noSelect.png',
                        background_down='icons/bobaMed.png',
                        group = 'boba',
                        size_hint=(None, None),
                        size=(160, 160),
                        font_name="Luna2",
                        font_size="17sp",
                        pos_hint={'center_x': (445/720), 'center_y': 0.36})
        bobabtnmed.bind(state=self.BobaCallback)
        
        bobabtnmany = ToggleButton(text="Many Boba", 
                        background_normal='icons/noSelect.png',
                        background_down='icons/bobaHigh.png',
                        group = 'boba',
                        size_hint=(None, None),
                        size=(160, 160),
                        font_name="Luna2",
                        font_size="20sp",
                        pos_hint={'center_x': (615/720), 'center_y': 0.36})
        bobabtnmany.bind(state=self.BobaCallback)
        
        for but in [Icebtnno, Icebtnlow, Icebtnmed, Icebtnhigh]:
            backgrounder.add_widget(but)
        
        for but in [btn4, btn5, btn6]:
            layoutSize.add_widget(but)
            
        for but in [bobabtnno, bobabtnfew, bobabtnmed, bobabtnmany]:
            backgrounder.add_widget(but)
        
        submitBut = Button(text="Make Boba!", size_hint=(None, None),
                           size=(256, 64), pos_hint={'center_x': 0.5, 'center_y': 0.26},
                           font_name="Luna2", font_size="20sp") 
        submitBut.bind(state=self.bobaMake)
        
        exitBut = Button(text="x", size_hint=(None, None),
                                        size=(24, 24), pos_hint={'center_x': 0.92, 'center_y': 0.97}) 
        exitBut.bind(on_release=lambda instance: App.get_running_app().stop())
        
        lockBut = Button(text="Selection Lock", size_hint=(None, None),
                         size=(160, 160), pos_hint={'center_x': 615/720, 'center_y': 0.225})
        
        backgrounder.add_widget(self.icelabel)
        backgrounder.add_widget(self.sizelabel)
        backgrounder.add_widget(layoutSize)
        backgrounder.add_widget(self.bobalabel)
        backgrounder.add_widget(submitBut)
        backgrounder.add_widget(exitBut)
        backgrounder.add_widget(lockBut)

        return backgrounder

if __name__ == "__main__":
    Menu().run()