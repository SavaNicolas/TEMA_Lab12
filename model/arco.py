from dataclasses import dataclass

from model.go_retailers import Go_retailer


@dataclass
class Arco:
    nodo1:Go_retailer
    nodo2: Go_retailer