import copy
import itertools

import networkx as nx

from database.DAO import DAO
from model.team import Team


class Model:
    def __init__(self):
        self._bestScore = None
        self._bestPath = None
        self._lista_anni = []
        self._grafo = nx.Graph()
        self._nodi = []
        self._archi = []
        self._id_map_teams = {}

    def get_all_anni(self):
        self._lista_anni = DAO.get_all_anni()
        print(f"Lista anni: {self._lista_anni}")
        return self._lista_anni

    def get_teams_anno(self, anno):
        return DAO.get_teams_anno(anno)

    def build_grafo(self, anno):
        self._grafo.clear()

        self._nodi = self.get_teams_anno(anno)
        for n in self._nodi:
            self._id_map_teams[n.ID] = n

        if len(self._nodi) == 0:
            print("Lista squadre vuota")
            print("Seleziona un altro anno")
            return

        self._grafo.add_nodes_from(self._nodi)
        print(f"Numero nodi: {len(self._grafo.nodes)}")



        # for n1 in self._grafo.nodes:
        #     for n2 in self._grafo.nodes:
        #         if n1 != n2:
        #             self._grafo.add_edge(n1, n2)
        #             self._archi.append((n1, n2))

        # uso tool python che mi crea tutte le possibili combinazioni tra gli elementi di una lista (senza ripetizioni, se ho (a, b) non mette (b,a))
        self._archi = itertools.combinations(self._nodi, 2)
        self._grafo.add_edges_from(self._archi)
        print(f"Numero archi: {len(self._grafo.edges)}")

        salari_teams = DAO.get_somma_salari_team(anno, self._id_map_teams)
        for a in self._grafo.edges:
            n1 = a[0]
            n2 = a[1]
            self._grafo[n1][n2]["weight"] = salari_teams[n1] + salari_teams[n2]

    def get_num_nodi(self):
        return self._grafo.number_of_nodes()

    def get_num_archi(self):
        return self._grafo.number_of_edges()

    def get_sorted_vicini(self, n):
        vicini = self._grafo.neighbors(n)
        vicini_tuple = []

        for v in vicini:
            vicini_tuple.append((v, self._grafo[n][v]["weight"]))

        vicini_tuple.sort(key=lambda x:x[1], reverse=True)

        return vicini_tuple

    def get_percorso(self, n0):
        self._bestPath = []
        self._bestScore = 0

        parziale = [n0]
        lista_vicini = []

        for n in self._grafo.neighbors(n0):
            peso_arco = self._grafo[n0][n]["weight"]
            lista_vicini.append((n, peso_arco))

        lista_vicini.sort(key=lambda x:x[1], reverse=True)


        parziale.append(lista_vicini[0][0])
        self.ricorsione_v2(parziale)
        parziale.pop()


        return self.get_pesi_path(self._bestPath), self._bestScore

    def ricorsione(self, parziale):
        # in questo caso non abbiamo vincoli di lunghezza, quindi la condzione di terminazione
        # si ha quando non ci sono più possibili vicini da aggiungere

        # verifico se sol attuale è la best
        if self.get_score(parziale) > self._bestScore:
            self._bestPath = copy.deepcopy(parziale)
            self._bestScore = self.get_score(parziale)

        # verifico se posso aggiungere un altro elemento
        # aggiungo e faccio ricorsione
        for v in self._grafo.neighbors(parziale[-1]):
            peso_arco = self._grafo[parziale[-1]][v]["weight"]
            if v not in parziale and self.is_decrescente(peso_arco, parziale):
                parziale.append(v)
                self.ricorsione(parziale)
                parziale.pop()

    def ricorsione_v2(self, parziale):
        # versione più efficiente della ricorsione
        # visto che gli archi devono essere di pesi decrescenti,
        # tra tutti i vicini possibili, prendo quello con peso maggiore

        # creo una lista di tuple (nodo_arco, peso) e la ordino per peso decrescente
        # da questa lista prendo solo quello di peso maggiore, senza ciclare su tutti i vicini

        # in questo modo riduco le chiamate alla funzione ricorsiva e quindi il metodo è più veloce

        if self.get_score(parziale) > self._bestScore:
            self._bestPath = copy.deepcopy(parziale)
            self._bestScore = self.get_score(parziale)

        lista_vicini = []
        for v in self._grafo.neighbors(parziale[-1]):

           peso_arco = self._grafo[parziale[-1]][v]["weight"]
           lista_vicini.append((v, peso_arco))

        lista_vicini.sort(key=lambda x:x[1], reverse=True)


        for v1 in lista_vicini:
            nodo = v1[0]
            peso_arco = v1[1]
            if nodo not in parziale and self.is_decrescente(peso_arco, parziale):
                parziale.append(nodo)
                self.ricorsione_v2(parziale)
                parziale.pop()
                return


    def get_score(self, lista_nodi):
        if(len(lista_nodi)) == 1:
            return 0

        score = 0

        for i in range(0, len(lista_nodi)-1):
            n_p = lista_nodi[i]
            n_a = lista_nodi[i+1]
            score += self._grafo[n_p][n_a]["weight"]

        return score

    def is_decrescente(self, peso_arco, parziale):
        peso_arco_prec = self._grafo[parziale[-2]][parziale[-1]]["weight"]
        if peso_arco < peso_arco_prec:
            return True

        return False

    def get_pesi_path(self, path):

        lista_tuple = []
        lista_tuple.append((path[0], 0))

        for i in range(0, len(path)-1):
            lista_tuple.append((path[i+1], self._grafo[path[i]][path[i+1]]["weight"]))

        return lista_tuple

























