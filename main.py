from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import NumericProperty
from kivy.clock import Clock
from kivy.core.window import Window

class Gerenciador(ScreenManager):
    pass

class Inicio(Screen):

    def __init__(self, **kwargs):
        super(Inicio, self).__init__(**kwargs)
        Clock.schedule_once(self._do_setup)       

    def _do_setup(self, *args):
        self.verificacao()        
    
    def verificacao(self, *args):
        self.ids['pb'].value = 0
        self.progresso = 0
        Clock.schedule_interval(self.banco_de_dados, 0.5)
        Clock.schedule_interval(self.tela_menu, 0.5)

    def banco_de_dados(self, *args):
        self.progresso = self.progresso + 0.1

        if self.progresso > 1:
            Clock.unschedule(self.banco_de_dados)
        else:
            self.ids['pb'].value = self.progresso

    def tela_menu(self, *args):
        
        if self.ids['pb'].value >= 0.99:
            App.get_running_app().root.current = 'login'
            Clock.unschedule(self.tela_menu)

class Login(Screen):
    
    def __init__(self, **kwargs):
        super(Login, self).__init__(**kwargs)

    def on_pre_enter(self):
        Window.bind(on_keyboard=self.print_text)
        

    def print_text(self, window, key, *args):
        
        if key == 13:
            self.ids['txtSenha'].focus = True

        print('key: {}'.format(key))

        print('---args---')
        for arg in args:
            print('args: {}'.format(arg))

    def teste_usuario(self, *args):
        App.get_running_app().root.current = 'menu'

    def on_pre_leave(self, *args):
        for arg in args:
            print('args: {}'.format(arg))
        Window.unbind(on_keyboard=self.print_text)

class Menu(Screen):
    pass
        

    
class NVendas(App):
    
    def build(self):
        return Gerenciador()

NVendas().run()