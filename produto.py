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

class ProdutoRecycleGridLayout(FocusBehavior, LayoutSelectionBehavior, 
                                                RecycleGridLayout):
    pass

class TabelaRecycleGridLayout(FocusBehavior, LayoutSelectionBehavior,
                                            RecycleGridLayout):
    pass


class Linha_produto(GridLayout, RecycleDataViewBehavior, Button):
    
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)
    _data_selected = None
    cols = 1

    def refresh_view_attrs(self, rv, index, data):
        
        self.index = index
        #self.descricao_text = data['produto']['descricao']
        #self.codigo_text = data['produto']['codigo']
        #self.estoque_text = data['produto']['estoque']

        return super(Linha_produto, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):

        if super(Linha_produto, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        
        self.selected = is_selected
        self._data_selected = rv.data[index]

        return True

    def on_press(self, *args):
        App.get_running_app().root.get_screen('detalhe_produto').produto = self._data_selected
        App.get_running_app().root.current = 'detalhe_produto'

class Linha_tabela(GridLayout, RecycleDataViewBehavior):

    cols = 1

    def refresh_view_attrs(self, rv, index, data):

        self.descricao_text = data['descricao']['text']
        self.preco_text = data['preco']['text']
        
        return super(Linha_tabela, self).refresh_view_attrs(rv, index, data)

    
class Detalhe_produto(Screen):

    produto = ObjectProperty(None)
    descricao = StringProperty('')
    codigo = StringProperty('')

    def __init__(self, **kwargs):
        super(Detalhe_produto, self).__init__(**kwargs)

    def on_produto(self, *args):
            self.descricao = self.produto['descricao']['text']
            self.codigo = self.produto['descricao']['text']


class Lista_produto(Screen):
    
    def __init__(self, **kwargs):
        super(Lista_produto, self).__init__(**kwargs)
        Clock.schedule_once(self._setup, 0)

    def _setup(self, *args):
        p1 = {'produto':
                        {
                            'descricao':'Produto com a descricao',
                            'codigo':'14523', 
                            'estoque':'100'
                        }
            }

        p2 = {'produto':
                        {
                            'descricao':'Produto 2',
                            'codigo':'15943', 
                            'estoque':'130'
                        }
            }

        self.ids['recycle_produto'].data.append(p1)
        self.ids['recycle_produto'].data.append(p2)





