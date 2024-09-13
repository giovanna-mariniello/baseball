from database.DB_connect import DBConnect


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

        print(result)

        cursor.close()
        cnx.close()




