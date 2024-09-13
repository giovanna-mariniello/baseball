import flet as ft

from UI.view import View
from model.model import Model


class Controller:
    def __init__(self, view:View, model:Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self.team_scelto = None

    def fill_ddAnno(self):
        lista_anni = self._model.get_all_anni()

        for anno in lista_anni:
            self._view._ddAnno.options.append(ft.dropdown.Option(anno))

        self._view.update_page()

    def handle_ddAnno_selection(self, e):
        self._view._txtOutSquadre.controls.clear()
        anno = int(self._view._ddAnno.value)
        teams = self._model.get_teams_anno(anno)

        self._view._txtOutSquadre.controls.append(ft.Text(f"Nell'anno selezionato ({anno}) hanno giocato {len(teams)} squadre"))
        for t in teams:
            self._view._txtOutSquadre.controls.append(ft.Text(f"{t.teamCode} ({t.name})"))
            self._view._ddSquadra.options.append(ft.dropdown.Option(text=f"{t.teamCode} ({t.name})", data=t, on_click=self.leggi_ddSquadra))

        self._view.update_page()

    def leggi_ddSquadra(self, e):
        if e.control.data is None:
            self.team_scelto = None
        else:
            self.team_scelto = e.control.data


    def handleCreaGrafo(self, e):
        self._view._txt_result.controls.clear()

        anno = self._view._ddAnno.value
        if anno is None:
            self._view._txt_result.controls.append(ft.Text("Per favore seleziona un anno"))
            return

        self._model.build_grafo(anno)

        self._view._txt_result.controls.append(ft.Text(f"Grafo correttamente creato con {self._model.get_num_nodi()} nodi e {self._model.get_num_archi()} archi."))

        self._view.update_page()


    def handleDettagli(self, e):
        self._view._txt_result.controls.clear()
        nodo = self.team_scelto
        vicini = self._model.get_sorted_vicini(nodo)

        self._view._txt_result.controls.append(ft.Text(f"Adiacenti per la squadra {nodo}"))
        for v in vicini:
            self._view._txt_result.controls.append(ft.Text(f"{v[1]} - {v[0]}"))

        self._view.update_page()


    def handlePercorso(self, e):
        pass