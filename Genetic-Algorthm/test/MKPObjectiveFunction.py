# Archivo: src/optimization/objective_function/MKPObjectiveFunction.py

from src.optimization.objective_function.ObjectiveFunction import ObjectiveFunction

class MKPObjectiveFunction(ObjectiveFunction):
  def __init__(self,
               # Parámetros del problema
               is_minimization: bool, 
               lista_restricciones: list[list[float]], 
               lista_capacidades: list[float], 
               optimo: float,
               lista_valores: list[float], 
               cantidad_restricciones: int, 
               cantidad_variables: int,
               
               # Parámetros para controlar la evaluación (leídos desde GAParameters)
               constraint_strategy: str = 'death_penalty',
               penalty_factor: float = 1.0):
    
    super().__init__(is_minimization)
    
    # Atributos del problema
    self.__lista_restricciones = lista_restricciones
    self.__lista_capacidades = lista_capacidades
    self.__lista_valores = lista_valores
    self.__cantidad_restricciones = cantidad_restricciones
    self.__optimo = optimo
    self.__cantidad_variables = cantidad_variables
    
    # Atributos de la estrategia
    self.constraint_strategy = constraint_strategy
    self.penalty_factor = penalty_factor


  def evaluate(self, solution: list[int]) -> float:
    """
    Evalúa el fitness de una solución. Su comportamiento cambia según la
    'constraint_strategy' definida en la inicialización.
    """
    valor_total = 0.0
    peso_total_por_restriccion = [0.0] * self.__cantidad_restricciones

    # 1. Calcular valor y pesos acumulados (esto se hace siempre)
    for j in range(self.__cantidad_variables):
        if solution[j] == 1:
            valor_total += self.__lista_valores[j]
            for k in range(self.__cantidad_restricciones):
                peso_total_por_restriccion[k] += self.__lista_restricciones[k][j]

    # 2. Calcular la violación total de las restricciones
    total_violation = 0.0
    for i in range(self.__cantidad_restricciones):
        exceso = peso_total_por_restriccion[i] - self.__lista_capacidades[i]
        if exceso > 0:
            total_violation += exceso

    # 3. Devolver el fitness según la estrategia
    if total_violation == 0:
      # Si no hay violación, la solución es factible.
      # Esto se aplica a soluciones factibles desde el inicio o a las que fueron reparadas.
      return valor_total
    else:
      # Si hay violación, la solución es infactible. Aplicamos la estrategia correspondiente.
      if self.constraint_strategy == 'death_penalty':
        return 0.0 # Castigo simple: fitness es cero.
      
      elif self.constraint_strategy == 'penalty_function':
        # Castigo dinámico: el fitness es negativo y proporcional a la violación.
        # Un fitness negativo asegura que cualquier solución factible (>=0) sea siempre mejor.
        return -self.penalty_factor * total_violation
      
      elif self.constraint_strategy == 'repair':
        # Este caso teóricamente no debería ocurrir si la reparación funciona bien,
        # pero si llegara una solución infactible, le damos un fitness de 0 como fallback.
        return 0.0

  def get_weight(self, solution) -> int:
    # NOTA: Este método parece ser para un problema de mochila simple (no multidimensional)
    # y asume la existencia de 'self.__weights'. Podrías necesitar revisarlo o eliminarlo
    # si no lo estás utilizando para MKP.
    print("Advertencia: El método get_weight puede no estar implementado para MKP.")
    return 0