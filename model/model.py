import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        pass

    def __init__(self):
        self._retailersAll = DAO.getAllRetailers()  # lista con tutti i retailer
        # creo grafo
        self._grafo = nx.Graph() #semplice, non orientato e pesato
        # mappa di oggetti
        self.idMapRetailers = {}
        for p in self._retailersAll:
            self.idMapRetailers[p.Retailer_code] = p

    def buildGraph(self,nazione,anno):
        self._grafo.clear()
        self._retailers = self.getRetailers(nazione)  # retailer presi in base alla nazionalità
        # aggiungiamo i nodi(li ho nelle fermate)
        self._grafo.add_nodes_from(self._retailers)
        # aggiungo archi
        self.addEdges(anno,self.idMapRetailers)

    def addEdges(self,anno,idMap):
        for u in self._retailers:
            for v in self._retailers:
                if u !=v:
                    idU= u.Retailer_code
                    idV= v.Retailer_code
                    edges= DAO.getEdges(idU,idV,anno,idMap) #lista di archi tra u e v
                    if not edges:
                        continue
                    # arco ha sempre stessi nodi u,v --> quindi è inutile iterare
                    if self._grafo.has_edge(edges[0].nodo1, edges[0].nodo2):  # controllo se esiste già l'arco
                        continue
                    else:
                        self._grafo.add_edge(edges[0].nodo1, edges[0].nodo2, weight=len(edges))


    def getCountries(self):
        return DAO.getCountries()

    def getRetailers(self,nation):
        return DAO.getRetailers(nation)

    def getNumNodi(self):
        return len(self._grafo.nodes())

    def getNumArchi(self):
        return len(self._grafo.edges())

    def getNodi(self):
        return list(self._grafo.nodes())
    def getGraph(self):
        return self._grafo