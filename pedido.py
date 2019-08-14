from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.properties import BooleanProperty, ObjectProperty
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
        p2 = {'pedido':
                {
                    'cliente':'Rafael Gomes',
                    'numero':'112255',
                    'data_criacao':'13/08/2019 - 17:00',
                    'data_envio': '',
                    'valor': 'R$ 1.245,00',
                    'situacao': 'orçamento'                
                }
        }

        self.ids['recycle_pedido'].data.append(p1)
        self.ids['recycle_pedido'].data.append(p2)

    def show_menu(self, *args):
        App.get_running_app().root.current = 'menu'
        


class PedidoClienteRecycleGridLayout(FocusBehavior, LayoutSelectionBehavior,
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

        if self.situacao_text == 'enviado':
            self.disabled = True

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


class Linha_pedido_cliente(GridLayout, RecycleDataViewBehavior, Button):

    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)
    _data_selected = None
    cols = 1

    def refresh_view_attrs(self, rv, index, data):

        self.index = index
        self.codigo_text = data['cliente']['codigo']
        self.nome_text = data['cliente']['nome']
        self.fantasia_text = data['cliente']['fantasia']

        return super(Linha_pedido_cliente, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):

        if super(Linha_pedido_cliente, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):

        self.selected = is_selected
        self._data_selected = rv.data[index]

        return True

    def on_press(self):
        App.get_running_app().root.get_screen('selecao_forma_pagto').cliente = self._data_selected
        App.get_running_app().root.current = 'selecao_forma_pagto'
        

class Detalhe_pedido(Screen):

    def __init__(self, **kwargs):
        super(Detalhe_pedido, self).__init__(**kwargs)

class Selecao_cliente(Screen):

    def __init__(self, **kwargs):
        super(Selecao_cliente, self).__init__(**kwargs)
        Clock.schedule_once(self._setup, 0)

    def _setup(self, *args):
        c1 = {
            'cliente': {
                'nome': 'Marcelo Paes Rocha Nunes',
                'codigo': '10111',
                'fantasia': 'Empresa Fantasia',
                'filial': 'Filial 1'
            }
        }

        c2 = {
            'cliente':{
                'nome': 'Rafael Gomes',
                'codigo': '12345',
                'fantasia': 'Empresa Gomes Fantasia',
                'filial': 'Filial 2'
            }
        }

        data = self.ids['recycle_pedido_cliente'].data

        data.append(c1)
        data.append(c2)

    def voltar_menu(self):
        App.get_running_app().root.current = 'menu'

class Selecao_forma_pagto(Screen):

    cliente = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super(Selecao_forma_pagto, self).__init__(**kwargs)

    def on_cliente(self, *args):
        print('cliente: {}'.format(self.cliente)) 
        self.ids['lb_cliente'].text = self.cliente['cliente']['nome']       


    def voltar_lista_cliente(self, *args):
        App.get_running_app().root.current = 'selecao_cliente'

        
