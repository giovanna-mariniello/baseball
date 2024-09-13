import itertools

import networkx as nx

from database.DAO import DAO
from model.team import Team


class Model:
    def __init__(self):
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


















