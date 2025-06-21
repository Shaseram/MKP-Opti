# Archivo: src/optimization/objective_function/MKPObjectiveFunction.py

from src.optimization.objective_function.ObjectiveFunction import ObjectiveFunction

class MKPObjectiveFunction(ObjectiveFunction):
  def __init__(self,
               is_minimization: bool, 
               lista_restricciones: list[list[float]], 
               lista_capacidades: list[float], 
               optimo: float,
               lista_valores: list[float], 
               cantidad_restricciones: int, 
               cantidad_variables: int,
               
               constraint_strategy: str = 'death_penalty',
               penalty_factor: float = 1.0):
    
    super().__init__(is_minimization)
    
    self.__lista_restricciones = lista_restricciones
    self.__lista_capacidades = lista_capacidades
    self.__lista_valores = lista_valores
    self.__cantidad_restricciones = cantidad_restricciones
    self.__optimo = optimo
    self.__cantidad_variables = cantidad_variables
    
    self.constraint_strategy = constraint_strategy
    self.penalty_factor = penalty_factor
    



  def evaluate(self, solution):
    """
    Evalúa el fitness de una solución. Su comportamiento cambia según la
    'constraint_strategy' definida en la inicialización.
    """
    valor_total = 0.0
    peso_total_por_restriccion = [0.0] * self.__cantidad_restricciones

    for j in range(self.__cantidad_variables):
        if solution[j] == 1:
            valor_total += self.__lista_valores[j]
            for k in range(self.__cantidad_restricciones):
                peso_total_por_restriccion[k] += self.__lista_restricciones[k][j]

    total_violation = 0.0
    for i in range(self.__cantidad_restricciones):
        exceso = peso_total_por_restriccion[i] - self.__lista_capacidades[i]
        if exceso > 0:
            total_violation += exceso

    if total_violation == 0:
      return valor_total
    else:
      if self.constraint_strategy == 'death_penalty':
        return 0.0
      
      elif self.constraint_strategy == 'penalty_function':
        return -self.penalty_factor * total_violation
      
      elif self.constraint_strategy == 'repair':
        return 0.0

  def get_weight(self, solution) -> int:
    print("Advertencia: El método get_weight puede no estar implementado para MKP.")
    return 0