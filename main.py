from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import NumericProperty, BooleanProperty
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.gridlayout import GridLayout
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.button import Button

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
       
    def teste_usuario(self, *args):
        App.get_running_app().root.current = 'menu'

    def on_pre_leave(self, *args):
        Window.unbind(on_keyboard=self.print_text)

class Menu(Screen):
    
    def __init__(self, **kwargs):
        super(Menu, self).__init__(**kwargs)

    def show_lista_clientes(self, **args):
        App.get_running_app().root.current = 'lista_cliente'

class SelectableRecycleGridLayout(FocusBehavior, LayoutSelectionBehavior, 
                                    RecycleGridLayout):
    pass

class Linha_cliente(GridLayout, RecycleDataViewBehavior, Button):

    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)
    _data_selected = None
    cols = 3

    def refresh_view_attrs(self, rv, index, data):

        self.index = index
        self.nome_text = data['cliente']['nome']
        self.telefone_text = data['cliente']['telefone']
        self.cidade_text = data['cliente']['cidade']

        return super().refresh_view_attrs(rv, index, data)
    
    def on_touch_down(self, touch):
        
        if super(Linha_cliente, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        
        self.selected = is_selected
        self._data_selected = rv.data[index]

        return True

    def detalhe_cliente(self, *args):
        pass
    

class Lista_cliente(Screen):
    pass
        

    
class NVendas(App):

    title= 'nVendas'
    
    def build(self):
        return Gerenciador()

NVendas().run()