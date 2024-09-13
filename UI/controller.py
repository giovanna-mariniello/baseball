import flet as ft

from UI.view import View
from model.model import Model


class Controller:
    def __init__(self, view:View, model:Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fill_dd_anno(self):
        lista_anni = self._model.get_all_anni()

        for anno in lista_anni:
            self._view._dd_anno.options.append(ft.dropdown.Option(anno))

        self._view.update_page()

    def handleCreaGrafo(self, e):
        pass

    def handleDettagli(self, e):
        pass

    def handlePercorso(self, e):
        pass