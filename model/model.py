import copy

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


        ###parte 2
        self._soluzioneOttima = []
        self._massimoPesi = 0
        ####

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



    ########parte 2

    def getCamminoOttimo(self, N_archi):
        self._soluzioneOttima = []
        self._massimoPesi = 0  # inizializzate anche nell'init

        parziale = []
        self._ricorsione(parziale, N_archi) #nodoPartenza è anche il vertice di destinazione

        return self._soluzioneOttima, self._massimoPesi #return di quello che mi chiede il testo

    def _ricorsione(self, parziale, N_archi):
        # condizione terminale, quindi verificare se parziale è una soluzione e
        # verificare se parziale è meglio del best
        # esco
        if len(parziale)-1 == N_archi+1 and parziale[-1] == parziale[0]:  # sono arrivato a destinazione e ho N_archi
            if self._getPeso(parziale) > self._massimoPesi:  # massimizzare i pesi
                self._massimoPesi = self._getPeso(parziale)
                self._soluzioneOttima = copy.deepcopy(parziale)

            # ricorsione, posso ancora aggiungere nodi
            # partendo dall'ultimo nodo, prendo i vicini e aggiungo un nodo alla volta

        #condizione posti prima dell'ultimo: nodi intermedi devono essere diversi tra loro
        if len(parziale)<N_archi:
            if len(parziale)==0:#se parziale è vuota da dove lo prendo il nodo iniziale????
                #itero su tutti i nodi, li appendo, chiamo ricorsione e poi back traking
                for n in self.getNodi():
                    parziale.append(n)
                    self._ricorsione(parziale, N_archi)
                    parziale.pop()  # backtracking

            else:#se non è uguale a zero vado normale
                for n in self._grafo.neighbors(parziale[-1]):  # prendo i vicini, da dove lo prendo il primo?
                    # verifico che non abbiamo già n in parziale
                    if n not in parziale:
                        parziale.append(n)
                        self._ricorsione(parziale, N_archi)
                        parziale.pop()  # backtracking

        #condizione ultimo posto in parziale:ultimo posto deve essere per forza nodoD
        if len(parziale)==N_archi: #significa che mi manca chiamare l'ultimo
            for n in self._grafo.neighbors(parziale[-1]):  # prendo i vicini
                # verifico che ci sia nodo Destinazione
                if n == parziale[0]:
                    parziale.append(n)
                    self._ricorsione(parziale, N_archi)
                    parziale.pop()  # backtracking,serve?

    def _getPeso(self, parziale):
        # sommo il valore dei pesi di tutti gli archi(nodi-1)
        # parziale è una lista di nodi
        peso = 0
        for i in range(0, len(list(parziale)) - 1):
            peso += self._grafo[parziale[i]][parziale[i + 1]]["weight"]  # archi tra i nodi

        return peso