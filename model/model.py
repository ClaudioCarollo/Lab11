import copy

from database.DAO import DAO
import networkx as nx
class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._idMap = {}

    def getColor(self):
        colori = DAO.getColor()
        return colori

    def getAllNodes(self, color):
        nodi = DAO.getAllNodes(color)
        return nodi

    def buildGraph(self, color, year):
        nodi = self.getAllNodes(color)
        self._grafo.add_nodes_from(nodi)
        for n in nodi:
            self._idMap[n.Product_number] = n
        connessioni = DAO.getAllConnesioni(year, color, self._idMap)
        for c in connessioni:
            self._grafo.add_edge(c.product1, c.product2, weight = c.peso)

    def getArchiPesoMax(self):
        pesi = []
        pesimax = []
        for n1 in self._grafo.nodes:
            for n2 in self._grafo.nodes:
                if self._grafo.has_edge(n1,n2) and (n2, n1, self._grafo[n2][n1]["weight"]) not in pesi:
                    pesi.append((n1, n2, self._grafo[n1][n2]["weight"]))
        pesi.sort(key=lambda x: x[2], reverse=True)
        for i in range(0,3):
            pesimax.append(pesi[i])
        return pesimax

    def getNodoRicorrente(self):
        pesi_max = self.getArchiPesoMax()
        nodi = []
        nodi_ricorrenti = []
        max = 0
        for n in pesi_max:
            nodi.append(n[0])
            nodi.append(n[1])
        for j in nodi:
            i = 0
            for k in nodi:
                if j == k:
                    i+=1
            if i>max:
                max = i
        for l in nodi:
            y = 0
            for m in nodi:
                if l == m:
                    y+=1
            if y == max:
                if l.Product_number not in nodi_ricorrenti:
                    nodi_ricorrenti.append(l.Product_number)
        return nodi_ricorrenti

    def getPath(self, nodo):
        # caching con variabili della classe (percorso migliore e peso maggiore)
        self._bestComp = []

        vicini = self._grafo.neighbors(nodo)
        for n in vicini:
            # inizializzo il parziale con il nodo iniziale
            parziale = [nodo, n]
            self._ricorsione(parziale)
        return self._bestComp

    def _ricorsione(self, parziale):
        # verifico se soluzione è migliore di quella salvata in cache

        if len(parziale) >= len(self._bestComp):
            self._bestComp = copy.deepcopy(parziale)

        # verifico se posso aggiungere un altro elemento
        for a in self._grafo.neighbors(parziale[-1]):
            if a not in parziale and self._grafo[parziale[-1]][a]["weight"] > self._grafo[parziale[-2]][parziale[-1]]["weight"]:
                parziale.append(a)
                self._ricorsione(parziale)
                parziale.pop()  # rimuovo l'ultimo elemento aggiunto: backtracking
