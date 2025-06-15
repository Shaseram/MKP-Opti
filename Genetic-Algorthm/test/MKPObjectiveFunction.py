from src.optimization.objective_function.ObjectiveFunction import ObjectiveFunction


class MKPObjectiveFunction(ObjectiveFunction):
  def __init__(self, is_minimization: bool, lista_restricciones: list[float], lista_capacidades: list[int], optimo: float,
               lista_valores: list[float], cantidad_restricciones: int, cantidad_variables: int):
    super().__init__(is_minimization) # Deberia de ser false, es de maximizacion
    self.__lista_restricciones = lista_restricciones
    self.__lista_capacidades = lista_capacidades
    self.__lista_valores = lista_valores
    self.__cantidad_restricciones = cantidad_restricciones
    self.__optimo = optimo
    self.__cantidad_variables = cantidad_variables

  def evaluate(self, solution) -> float:

    valor_total = 0.0
    peso_total_por_restriccion = [0.0] * self.__cantidad_restricciones

    # Calcular valor y pesos acumulados
    for j in range(self.__cantidad_variables):
        if solution[j] == 1:
            valor_total += self.__lista_valores[j]

            for k in range(self.__cantidad_restricciones):
                peso_total_por_restriccion[k] += self.__lista_restricciones[k][j]
                

    # Verificar factibilidad (si las capacidades se respetan)
    for i in range(self.__cantidad_restricciones):
        if peso_total_por_restriccion[i] > self.__lista_capacidades[i]:
            return 0 

    return valor_total
        
  

  def get_weight(self, solution) -> int:
    weight_cont = 0
    
    for i,bit in enumerate(solution):
      if bit == 1:
        weight = self.__weights[i]
        weight_cont += weight
        
    return weight_cont


