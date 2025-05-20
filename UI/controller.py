import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self._listCountry = []

    def fillDD(self):
        self._listCountry = self._model.getCountries()
        for country in self._listCountry:
            self._view.ddcountry.options.append(ft.dropdown.Option(country))


    def handle_graph(self, e):
        # anno, controlla se è selezionato e converti in intero
        self._view.txt_result.controls.clear()
        # prendo anno dall'input
        anno = self._view.ddyear.value
        # controlli
        if anno is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("seleziona un valore"))
            self._view.update_page()
            return

        # converto in intero
        try:
            anno = int(anno)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("data non valida"))
            self._view.update_page()
            return
        #country, controlla se è selezionata

        country= self._view.ddcountry.value
        if country is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("seleziona una nazione"))
            self._view.update_page()
            return

        #creo grafo
        self._model.buildGraph(country,anno)

        # stampo txt result
        self._view.txt_result.controls.append(ft.Text("grafo correttamente creato"))
        self._view.txt_result.controls.append(
            ft.Text(f"il grafo ha {self._model.getNumNodi()} nodi e {self._model.getNumArchi()} archi"))
        self._view.update_page()

        # posso abilitare bottoni
        self._view.btn_volume.disabled = False
        self._view.btn_path.disabled = False

        self._view.update_page()



    def handle_volume(self, e):
        #pulisco risultati
        self._view.txtOut2.controls.clear()
        #una volta che ho creato il grafo posso trovare il volume
        #archi incidenti significa che devo prendere i pesi degli archi tra vicini e sommare
        #per ogni nodo trovo gli edges
        self.grafo= self._model.getGraph()
        self.nodi= self._model.getNodi() #lista di nodi
        for n in self.nodi:
            archi_incidenti= list(self.grafo.edges(n, data=True)) #lista di archi [(u,v)]
            if not archi_incidenti:
                continue

            somma=0
            for i in archi_incidenti: #i è una tupla
                somma+= i[2]["weight"]

            self._view.txtOut2.controls.append(ft.Text(f"{n}: {somma}"))
            self._view.update_page()


#######parte 2

    def handle_path(self, e):
        # pulisco risultati
        self._view.txtOut3.controls.clear()
        ##num archi deve essere inserito, deve essere > 2 e devo convertirlo in intero
        N_archi= self._view.txtN.value
        # controlli
        if N_archi is None:
            self._view.txtOut3.controls.clear()
            self._view.txtOut3.controls.append(ft.Text("seleziona un valore"))
            self._view.update_page()
            return

        # converto in intero
        try:
            N_archi = int(N_archi)
        except ValueError:
            self._view.txtOut3.controls.clear()
            self._view.txtOut3.controls.append(ft.Text("data non valida"))
            self._view.update_page()
            return

        #chiamo ricorsione
        path,max=self._model.getCamminoOttimo(N_archi)

        self._view.txtOut3.controls.append(ft.Text(f"il percorso ottimo ha peso: {max}"))
        self._view.update_page()

        for p in path: #sistema questo in base a quello che ti dice il testo
            self._view.txtOut3.controls.append(ft.Text(p))
        self._view.update_page()




