from database.DAO import DAO


class Model:
    def __init__(self):
        self._lista_anni = []

    def get_all_anni(self):
        self._lista_anni = DAO.get_all_anni()
        print(f"Lista anni: {self._lista_anni}")
        return self._lista_anni