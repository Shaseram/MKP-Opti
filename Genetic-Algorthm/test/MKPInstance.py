from Instances import Instances

class MKPInstance(Instances):
    def __init__(self, file_path: str):
        """
        Extiende la clase base para una instancia del problema Knapsack.
        """
        super().__init__(file_path)
        self.cantidad_variables = None
        self.cantidad_restricciones = None
        self.optimo = None
        self.lista_restricciones = []
        self.lista_capacidades = []
        self.load()

    def load(self):
        
        with open(self.file_path, 'r') as file:
            lines = file.readlines()

        datos = lines[0].strip().split()
        self.cantidad_variables = int(datos[0])
        self.cantidad_restricciones = int(datos[1])
        self.optimo = float(datos[2])
        self.valores_variables = [float(valor) for valor in lines[1].strip().split()]
        
        largo = len(lines)
        for line in lines[2:(largo-1)]:
            
            datos = line.strip().split()
            self.lista_restricciones.append([float(valor) for valor in datos])
            
        datos = lines[largo-1].strip().split()
        self.lista_capacidades = [float(valor) for valor in datos]


    