from database.DB_connect import DBConnect
from model.arco import Arco
from model.go_retailers import Go_retailer


class DAO():
    @staticmethod
    def getCountries():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
        select distinct g.Country as Country
from go_retailers g
order by g.Country
"""
        cursor.execute(query)

        for row in cursor:
            result.append(row["Country"])
            # equivalente a fare (ArtObject(object_id= row["object_id"])
        cursor.close()
        conn.close()
        return result#lista di nazioni

    @staticmethod
    def getRetailers(nation):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
            select *
from go_retailers g
where g.Country =%s

    """
        cursor.execute(query, (nation,))

        for row in cursor:
            result.append(Go_retailer(**row))
            # equivalente a fare (ArtObject(object_id= row["object_id"])
        cursor.close()
        conn.close()
        return result  # lista di retailer

    @staticmethod
    def getAllRetailers():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
                select *
    from go_retailers 
        """
        cursor.execute(query)

        for row in cursor:
            result.append(Go_retailer(**row))
            # equivalente a fare (ArtObject(object_id= row["object_id"])
        cursor.close()
        conn.close()
        return result  # lista di retailer

    @staticmethod
    def getEdges(u, v, anno, idMap):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
        select g1.Retailer_code as nodo1,g2.Retailer_code as nodo2,g1.Product_number as prodotto
from go_daily_sales g1, go_daily_sales g2
where g1.Product_number =g2.Product_number
and g1.Retailer_code = %s 
and g2.Retailer_code = %s
and YEAR(g1.`Date`)= %s
and YEAR(g2.`Date`)= %s
group by g1.Retailer_code,g2.Retailer_code,g1.Product_number"""
        cursor.execute(query,(u,v,anno,anno))

        for row in cursor:
            result.append(Arco(idMap[row["nodo1"]],idMap[row["nodo2"]]))
            # equivalente a fare (ArtObject(object_id= row["object_id"])
        cursor.close()
        conn.close()
        return result  # lista di retailer