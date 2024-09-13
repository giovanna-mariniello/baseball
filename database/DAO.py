from database.DB_connect import DBConnect
from model.team import Team


class DAO():
    @staticmethod
    def get_all_anni():
        cnx = DBConnect.get_connection()
        result = []

        cursor = cnx.cursor(dictionary=True)
        query = """ SELECT DISTINCT(YEAR)
                    FROM teams t
                    WHERE t.year >= 1980
                    ORDER BY year DESC """

        cursor.execute(query)
        for row in cursor:
            result.append(row["YEAR"])

        #print(result)

        cursor.close()
        cnx.close()

        return result

    @staticmethod
    def get_teams_anno(anno):
        cnx = DBConnect.get_connection()
        result = []

        cursor = cnx.cursor(dictionary=True)
        query = """ SELECT *
                FROM teams t
                WHERE t.year = %s """

        cursor.execute(query, (anno, ))

        for row in cursor:
            result.append(Team(**row))



        cursor.close()
        cnx.close()

        return result

    @staticmethod
    def get_somma_salari_team(anno, id_map_teams):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)

        query = """ SELECT t.teamCode , t.ID , sum(s.salary) as totSalary
                    FROM salaries s , teams t , appearances a 
                    WHERE s.`year` = t.`year` and t.`year` = a.`year` 
                    and a.`year` = %s
                    and t.ID = a.teamID 
                    and s.playerID = a.playerID 
                    GROUP by t.teamCode """

        cursor.execute(query, (anno,))

        result = {} # diz che ha come chiave l'oggetto team e come valore il totSalary in quell'anno
        for row in cursor:
            result[id_map_teams[row["ID"]]] = row["totSalary"]

        #print("--------------------------Risultato------------------")
        #print(result)


        cursor.close()
        cnx.close()

        return result




