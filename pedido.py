from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.properties import BooleanProperty
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.clock import Clock


class Lista_pedido(Screen):
    
    def __init__(self, **kwargs):
        super(Lista_pedido, self).__init__(**kwargs)
        Clock.schedule_once(self._setup, 0)

    def _setup(self, *args):
        p1 = {'pedido':
                {
                    'cliente':'Marcelo Paes Rocha Nunes',
                    'numero':'102345',
                    'data_criacao':'01/08/2019 - 17:00',
                    'data_envio': '02/08/2019 - 10:00',
                    'valor': 'R$ 2.500,00',
                    'situacao': 'enviado'                
                }
        }

        self.ids['recycle_pedido'].data.append(p1)

    def show_menu(self, *args):
        App.get_running_app().root.current = 'menu'
        


class PedidoRecycleGridLayout(FocusBehavior, LayoutSelectionBehavior,
                        RecycleGridLayout):
    pass

class Linha_pedido(GridLayout, RecycleDataViewBehavior, Button):

    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)
    _data_selected = None
    cols = 1

    def refresh_view_attrs(self, rv, index, data):

        self.index = index

        self.cliente_text = data['pedido']['cliente']
        self.num_pedido_text = data['pedido']['numero']
        self.data_criacao_text = data['pedido']['data_criacao']
        self.data_envio_text = data['pedido']['data_envio']
        self.valor_text = data['pedido']['valor']
        self.situacao_text = data['pedido']['situacao']


        return super(Linha_pedido, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):

        if super(Linha_pedido, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):

        self.selected = is_selected
        self._data_selected = rv.data[index]

        return True


class Detalhe_pedido(Screen):

    def __init__(self, **kwargs):
        super(Detalhe_pedido, self).__init__(**kwargs)

class Selecao_cliente(Screen):

    def __init__(self, **kwargs):
        super(Selecao_cliente, self).__init__(**kwargs)

        
