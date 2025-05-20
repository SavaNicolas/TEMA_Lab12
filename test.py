from model.model import Model

m= Model()
print(m.getRetailers("Australia"))
grafo=m.buildGraph("Australia")
print(m.getNumNodi())



