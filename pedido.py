from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.properties import BooleanProperty, ObjectProperty, StringProperty
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.uix.popup import Popup


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
    
        if super(Linha_pedido_cliente, self).on_touch_down(touch):
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
        App.get_running_app().root.get_screen('pedido').cliente = self._data_selected
        App.get_running_app().root.current = 'pedido'
        

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

class Pedido(Screen):

    cliente = ObjectProperty(None)
    item = ObjectProperty(None)
    total_itens = StringProperty('')
    total_pedido = StringProperty('')

    def __init__(self, **kwargs):
        super(Pedido, self).__init__(**kwargs)

    def on_cliente(self, *args):
        print('cliente: {}'.format(self.cliente)) 
        self.ids['lb_cliente'].text = self.cliente['cliente']['nome']

    def on_item(self, *args):
        self.data_pedido = App.get_running_app().root.get_screen('pedido').ids['recycle_item_pedido'].data
        self.data_pedido.append(self.item)
        self.total_itens = self.get_total_itens(self.data_pedido)
        self.total_pedido = self.get_total_pedido(self.data_pedido)

    def voltar_lista_cliente(self, *args):
        App.get_running_app().root.current = 'selecao_cliente'

    def show_pedido(self, *args):
        App.get_running_app().root.current = 'pedido'

    def show_adicionar_produto(self, *args):
        App.get_running_app().root.current = 'produto_pedido'

    def get_total_itens(self, data_pedido ,*args):

        quantidade = 0

        if data_pedido != None:
            quantidade = len(self.data_pedido)

        return str(quantidade)

    def get_total_pedido(self, data_pedido, *args):
        total = 0.0

        if data_pedido != None:
            for data in self.data_pedido:
                qtd   = data['produto']['quantidade']
                preco = data['produto']['preco']
                total_produto = float(qtd) * float(preco)
                total = total + total_produto

        return str(total)
            
            


class Remover_produto(Popup):
    
    def __init__(self, produto, **kwargs):
        super(Remover_produto, self).__init__(**kwargs)
        self.produto = produto

    def remover(self, *args):
        data = App.get_running_app().root.get_screen('pedido').ids['recycle_item_pedido'].data
        data.remove(self.produto)
 
        self.dismiss()

    

class ItemPedidoRecycleGridLayout(FocusBehavior, LayoutSelectionBehavior,
                        RecycleGridLayout):
    pass

class Item_pedido(GridLayout, Button, RecycleDataViewBehavior):

    cols = 1
    selectable = BooleanProperty(True)
    selected = BooleanProperty(False)
    index = None
    _data_selected = None
    data = None
    alterar_qtd = None
    remove_produto = None
    tempo_precionado = 0

    def refresh_view_attrs(self, rv, index, data):
        
        self.data = data
        self.index = index
        #self.codigo_text = data['produto']['codigo']
        self.descricao_text = data['produto']['descricao']
        self.quantidade_text = data['produto']['quantidade']
        self.preco_text = data['produto']['preco']

        preco = float(data['produto']['preco'])
        quantidade = float(data['produto']['quantidade'])

        total = round(preco * quantidade)

        self.total_text = str(total)

        return super(Item_pedido, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        print('on_touch_down')
        self.alterar_qtd = None
        self.remove_produto = None
        self.tempo_precionado = 0
        Clock.schedule_interval(self._remover_produto, 0.5)

        return True #super().on_touch_down(touch)

    def on_touch_up(self, touch):
        print('on_touch_up')
        Clock.unschedule(self._remover_produto)
        
        if self.tempo_precionado < 3:
             if self.alterar_qtd == None:
                print('tempo_precionado: {}'.format(self.tempo_precionado))
                self.alterar_qtd = Alterar_qtd(self._data_selected)
                self.alterar_qtd.open()

        return True #super().on_touch_up(touch)

    def _remover_produto(self, *args):
        print('_remover_produto')
        self.tempo_precionado = self.tempo_precionado + 1
        print('_remover_produto:tempo_precionado: {}'.format(self.tempo_precionado))
        if self.tempo_precionado >= 3:
            print('if show remover_produto')
            if self.remove_produto == None:
                self.remove_produto = Remover_produto(self._data_selected)
                self.remove_produto.open()
        if self.tempo_precionado > 4:
            Clock.unschedule(self._remover_produto)

    def apply_selection(self, rv, index, is_selected):
        
        self.selected = is_selected
        self._data_selected = rv.data[index]
        
        return True
   

class Produto_pedido(Screen):

    produto = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super(Produto_pedido, self).__init__(**kwargs)
        Clock.schedule_once(self._setup, 0)

    def on_produto(self, *args):
        self.ids['recycle_produto_lista'].data.append(self.produto)

    def _setup(self, *args):
        p1 = {'produto':
                        {
                         'descricao':'Produto 1', 
                         'codigo':'17852',
                         'preco':'1.20',
                         'quantidade': '100'
                         }
                }

        p2 = {'produto':
                        {'descricao':'Produto 2', 
                         'codigo':'14654',
                         'preco':'3.50',
                         'quantidade': '130'
                         }
                }

        p3 = {'produto':
                        {'descricao':'Produto 3', 
                         'codigo':'14654',
                         'preco':'3.50',
                         'quantidade': '130'
                         }
                }
        
        self.ids['recycle_produto_lista'].data.append(p1)
        self.ids['recycle_produto_lista'].data.append(p2)
        self.ids['recycle_produto_lista'].data.append(p3)
    
    def voltar(self, *args):
        App.get_running_app().root.current = 'pedido'

class LinhaProdutoRecycleGridLayout(FocusBehavior, LayoutSelectionBehavior,
                        RecycleGridLayout):
    pass 

class Linha_produto_pedido(GridLayout, Button, RecycleDataViewBehavior):
    
    cols = 1
    selectable = BooleanProperty(True)
    selected = BooleanProperty(False)
    index = None
    _data_selected = None

    def refresh_view_attrs(self, rv, index, data):

        self.index = index
        self.codigo_text = data['produto']['codigo']
        self.descricao_text = data['produto']['descricao']
        self.preco_text = data['produto']['preco']


        return super(Linha_produto_pedido, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        
        if super(Linha_produto_pedido, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):

        self.selected = is_selected
        self._data_selected = rv.data[index]
        

        return True

    def on_press(self):
        print('produto selecionado: {}'.format(self._data_selected))
        qtd_popup = Qtd_popup(self._data_selected)
        qtd_popup.open()
        

class Qtd_popup(Popup):

    
    def __init__(self, produto=None, **kwargs):
        super(Qtd_popup, self).__init__(**kwargs)
        self.produto = produto

    def adicionar(self, *args):
        data = App.get_running_app().root.get_screen('pedido').ids['recycle_item_pedido'].data
        is_incluso = self.produto in data
        if is_incluso:
            existe_produto = Existe_produto()
            existe_produto.open()
            
        else:
            self.produto['produto']['quantidade'] = self.ids['txt_quantidade'].text        
            App.get_running_app().root.get_screen('pedido').item = self.produto

        self.dismiss()

class Alterar_qtd(Popup):

    def __init__(self, produto, **kwargs):
        super(Alterar_qtd, self).__init__(**kwargs)
        self.produto = produto
        self.ids['txt_quantidade'].text = self.produto['produto']['quantidade']


    def alterar(self, *args):
        self.produto['produto']['quantidade'] = self.ids['txt_quantidade'].text

        self.dismiss()

class Existe_produto(Popup):
    
    def __init__(self, **kwargs):
        super(Existe_produto, self).__init__(**kwargs)
    
