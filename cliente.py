from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import NumericProperty, BooleanProperty
from kivy.clock import Clock
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.gridlayout import GridLayout
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.button import Button
from kivy.properties import ObjectProperty, StringProperty

class ClienteRecycleGridLayout(FocusBehavior, LayoutSelectionBehavior, 
                                    RecycleGridLayout):
    pass

class Linha_cliente(GridLayout, RecycleDataViewBehavior, Button):

    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)
    _data_selected = None
    cols = 1

    def refresh_view_attrs(self, rv, index, data):

        self.index = index
        self.nome_text = data['nome']['text']
        self.fantasia_text = data['fantasia']['text']
        self.codigo_text = data['codigo']['text']
        

        return super(Linha_cliente, self).refresh_view_attrs(rv, index, data)
    
    def on_touch_down(self, touch):

        if super(Linha_cliente, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)
    

    def apply_selection(self, rv, index, is_selected):
        
        self.selected = is_selected
        self._data_selected = rv.data[index]

        return True

    def on_press(self, *args):
        App.get_running_app().root.get_screen('detalhe_cliente').cliente = self._data_selected
        App.get_running_app().root.current = 'detalhe_cliente'

    def detalhe_cliente(self, *args):
        pass
    

class Lista_cliente(Screen):
    
    def __init__(self, **kwargs):
        super(Lista_cliente, self).__init__(**kwargs)
        Clock.schedule_once(self._setup, 0)
    
    def _setup(self, *args):
        p1 = {'nome':{'text':'Marcelo Paes Rocha Nunes'}, 'codigo':{'text':'10101'}, 'fantasia':{'text':'Nome fantasia'}}
        p2 = {'nome':{'text':'Marcio Rocha Nunes'}, 'codigo':{'text':'10102'}, 'fantasia':{'text':'Nome fantasia'}}
        self.ids['recycle'].data.append(p1)
        self.ids['recycle'].data.append(p2)

class Detalhe_cliente(Screen):

    cliente = ObjectProperty(None)
    nome = StringProperty('')
    fantasia = StringProperty('')
    codigo = StringProperty('')
    
    def __init__(self, **kwargs):
        super(Detalhe_cliente, self).__init__(**kwargs)

    def on_cliente(self, *args):
        self.nome = self.cliente['nome']['text']
        self.fantasia = self.cliente['fantasia']['text']
        self.codigo = self.cliente['fantasia']['text']
