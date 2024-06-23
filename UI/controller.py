import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._selected_product = None
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._listYear = []
        self._listColor = []

    def fillDD(self):
        for i in range(2015, 2019):
            self._view._ddyear.options.append(ft.dropdown.Option(str(i)))
        self._view.update_page()
        colori = self._model.getColor()
        for c in colori:
            self._view._ddcolor.options.append(ft.dropdown.Option(c))
        self._view.update_page()


    def handle_graph(self, e):
        self._model._grafo.clear()
        colore = self._view._ddcolor.value
        anno = self._view._ddyear.value
        if colore is None:
            self._view.txtOut.controls.append(ft.Text("Inserisci un Colore!", color='red'))
            self._view.update_page()
        if anno is None:
            self._view.txtOut.controls.append(ft.Text("Inserisci un Anno!", color='red'))
            self._view.update_page()
        else:
            self._model.buildGraph(colore, anno)
            self._view.txtOut.controls.append(ft.Text("Grafo creato correttamente", color='green'))
            self._view.txtOut.controls.append(ft.Text(
                f"Numero nodi: {len(self._model._grafo.nodes)} nodi, Numero archi: {len(self._model._grafo.edges)}",
                color='green'))
            self._view.update_page()
            pesimax = self._model.getArchiPesoMax()
            for p in pesimax:
                self._view.txtOut.controls.append(ft.Text(
                    f"Arco da: {p[0].Product_number}, a: {p[1].Product_number}, peso:{p[2]}"))
            self._view.update_page()
            nodi_ricorrenti = self._model.getNodoRicorrente()
            self._view.txtOut.controls.append(ft.Text(
                f"i nodi ripetuti sono: {nodi_ricorrenti}"))
            self.fillDDProduct()
            self._view.update_page()





    def fillDDProduct(self):
        nodi = self._model._grafo.nodes
        for n in nodi:
            self._view._ddnode.options.append(ft.dropdown.Option(text=n.Product_number, data=n, on_click=self.readDDproducts))
        self._view.update_page()


    def handle_search(self, e):
        self._view.txtOut2.controls.clear()
        if len(self._model._grafo.nodes) == 0:
            self._view.txtOut2.controls.append(ft.Text("Creare un grafo!", color='red'))
            self._view.update_page()
            return
        if self._selected_product is None:
            self._view.txtOut2.controls.append(ft.Text("Selezionare una prodotto!", color='red'))
            self._view.update_page()
            return
        componenti = self._model.getPath(self._selected_product)
        if componenti:
            self._view.txtOut2.controls.append(ft.Text(f"Numero archi percorso più lungo: {len(componenti)-1}"))
            self._view.update_page()
            return
        else:
            self._view.txtOut2.controls.append(ft.Text("Nessun percorso trovato!", color='red'))
            self._view.update_page()
            return

    def readDDproducts(self, e):
        if e.control.data is None:
            self._selected_product = None
        else:
            self._selected_product = e.control.data
