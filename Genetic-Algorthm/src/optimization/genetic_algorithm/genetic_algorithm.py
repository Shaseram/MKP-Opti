# Archivo: src/optimization/genetic_algorithm/GeneticAlgorithm.py

import time
from collections import Counter
import numpy as np
from src.optimization.optimization_algorithm import OptimizationAlgorithm
from src.optimization.genetic_algorithm.GeneticAlgorithmParameters import GAParameters
from src.optimization.genetic_algorithm.movements_supplier.GeneticAlgorithmMovementsSupplier import GAMovementsSupplier
from src.optimization.objective_function.ObjectiveFunction import ObjectiveFunction

class GeneticAlgorithm(OptimizationAlgorithm):
  def __init__(self,
               ga_params: GAParameters,
               movements_supplier: GAMovementsSupplier,
               objective_function: ObjectiveFunction):
    self.__ga_params: GAParameters = ga_params
    self.__movements_supplier: GAMovementsSupplier = movements_supplier
    self.__function: ObjectiveFunction = objective_function

  def run(self) -> tuple:
    # --- 0. INICIALIZACIÓN ---
    population = self.__movements_supplier.create_population()
    fitness = self.__movements_supplier.compute_population_fitness(self.__function, population)
    
    best_individual, best_fitness = self.__movements_supplier.get_best(self.__function, population, fitness)
    print(f"Mejor fitness inicial: {best_fitness}")

    # Variables para seguimiento
    generacion_track = [best_fitness]
    track_time_per_gen = []
    start_total = time.time()

    for i in range(self.__ga_params.n_generations):
      gen_start = time.time()
      
      population_with_fitness = list(zip(fitness, population))
      
      new_population = []

      # --- 1. ELITISMO ---
      if self.__ga_params.elitism_count > 0:
        # Ordenamos la población actual de mejor a peor fitness
        population_with_fitness.sort(key=lambda x: x[0], reverse=True)
        # Añadimos los 'N' mejores a la nueva población
        elites = [ind for fit, ind in population_with_fitness[:self.__ga_params.elitism_count]]
        new_population.extend(elites)

      # --- 2. BUCLE DE CREACIÓN DE DESCENDENCIA ---
      while len(new_population) < self.__ga_params.population_size:
        
        # 2.1. SELECCIÓN DE PADRES 
        parent1 = self.__movements_supplier.select(population_with_fitness)
        parent2 = self.__movements_supplier.select(population_with_fitness)

        # 2.2. CRUZAMIENTO
        offspring1, offspring2 = self.__movements_supplier.crossing(parent1, parent2)
        
        # 2.3. MUTACIÓN
        offspring1 = self.__movements_supplier.mutate_2(offspring1, self.__ga_params.p_mutate)
        offspring2 = self.__movements_supplier.mutate_2(offspring2, self.__ga_params.p_mutate)

        # 2.4. REPARACIÓN
        # Si la estrategia es 'repair', aquí se arreglan los hijos.
        # Si no, esta función los devuelve sin cambios.
        offspring1 = self.__movements_supplier.repair_individual(offspring1, self.__function)
        offspring2 = self.__movements_supplier.repair_individual(offspring2, self.__function)

        # 2.5. AÑADIR NUEVOS HIJOS A LA POBLACIÓN
        new_population.append(offspring1)
        if len(new_population) < self.__ga_params.population_size:
            new_population.append(offspring2)

      # --- 3. REEMPLAZO DE LA POBLACIÓN ---
      # La población de la siguiente generación está completa.
      population = new_population
      fitness = self.__movements_supplier.compute_population_fitness(self.__function, population)
      
      # --- 4. SEGUIMIENTO Y ACTUALIZACIÓN ---
      current_best_individual, current_best_fitness = self.__movements_supplier.get_best(self.__function, population, fitness)

      if self.__function.compare_objective_values(current_best_fitness, best_fitness) > 0:
        best_individual = current_best_individual
        best_fitness = current_best_fitness

      generacion_track.append(best_fitness)
      print(f"Generación {i + 1}/{self.__ga_params.n_generations}, Mejor fitness: {best_fitness}")
      
      elapsed_gen = time.time() - gen_start
      track_time_per_gen.append(elapsed_gen)

      if self.validate_termination(fitness):
          break

    # --- 5. FIN Y REPORTE ---
    total_time = time.time() - start_total
    print("===============================================")
    for idx, (fit, tgen) in enumerate(zip(generacion_track, track_time_per_gen), start=1):
        print(f"Generación {idx} | Mejor Fitness = {fit} | Tiempo = {tgen:.3f} s")
    print(f"Tiempo total de ejecución: {total_time:.3f} s\n")

    return best_individual, best_fitness, generacion_track, total_time

  def validate_termination(self, fitness):
    fitness_count = Counter(fitness)
    total_gen = len(fitness)
    limit = total_gen * 0.95
    terminate = any(value >= limit for value in fitness_count.values())

    if terminate:
      print("\nCondición de terminación alcanzada: El 95% o más de la población tiene el mismo valor de fitness.")
      return True
    else:
      return False