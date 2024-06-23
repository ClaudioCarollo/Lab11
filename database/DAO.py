from database.DB_connect import DBConnect
from model.product import Go_product
from model.connessione import Connessione

class DAO():
    @staticmethod
    def getColor():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct gp.Product_color as color
                        from go_products gp 
                        order by gp.Product_color  """
            cursor.execute(query, )
            for row in cursor:
                result.append(row["color"])
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAllNodes(color):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct *
                        from go_products gp 
                        where gp.Product_color =%s """
            cursor.execute(query, (color, ))
            for row in cursor:
                result.append(Go_product(**row))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAllConnesioni(year, color, idmap):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select gp1.Product_number as Product1, gp2.Product_number as Product2, count(distinct gds1.`Date`) as peso
                        from go_products gp1, go_products gp2,  go_daily_sales gds1, go_daily_sales gds2 
                        where gds2.`Date` = gds1.`Date`and year(gds1.`Date`)= %s and gds1.Retailer_code = gds2.Retailer_code and gp1.Product_number < gp2.Product_number and gp1.Product_color = gp2.Product_color and gp1.Product_color = %s and gp1.Product_number = gds1.Product_number and gp2.Product_number = gds2.Product_number
                        group by gp1.Product_number, gp2.Product_number """
            cursor.execute(query, (year, color))
            for row in cursor:
                result.append(Connessione(idmap[row["Product1"]],idmap[row["Product2"]], row["peso"]))
            cursor.close()
            cnx.close()
        return result
