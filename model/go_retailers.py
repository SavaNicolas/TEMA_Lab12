from dataclasses import dataclass



@dataclass
class Go_retailer:
    Retailer_code:int #chiave
    Retailer_name:str
    Type:str
    Country:str


    def __hash__(self):
        return self.Retailer_code

    def __str__(self):
        return f"{self.Retailer_name}"

    def __eq__(self, other):
        return self.Retailer_code == other.Retailer_code