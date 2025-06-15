class Problem():
    def __init__(self):
        self.cantidad_variables = None
        self.cantidad_restricciones = None
        self.optimo = None
        self.valores_variables = []
        self.lista_restricciones = []
        self.lista_capacidades = []


    def get_data(self):

        return {
            "cantidad_variables": self.cantidad_variables,
            "cantidad_restricciones": self.cantidad_restricciones,
            "optimo": self.optimo,
            "valores_variables": self.valores_variables,
            "lista_restricciones": self.lista_restricciones,
            "lista_capacidades": self.lista_capacidades
        }


    