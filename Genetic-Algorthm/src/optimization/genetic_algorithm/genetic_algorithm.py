from src.optimization.optimization_algorithm import OptimizationAlgorithm
from src.optimization.genetic_algorithm.GeneticAlgorithmParameters import GAParameters
from src.optimization.genetic_algorithm.movements_supplier.GeneticAlgorithmMovementsSupplier import GAMovementsSupplier
from src.optimization.objective_function.ObjectiveFunction import ObjectiveFunction
from collections import Counter
import time


class GeneticAlgorithm(OptimizationAlgorithm):
  def __init__(self,
               ga_params: GAParameters,
               movements_supplier: GAMovementsSupplier,
               objective_function: ObjectiveFunction):
    self.__ga_params: GAParameters = ga_params
    self.__movements_supplier: GAMovementsSupplier = movements_supplier
    self.__function: ObjectiveFunction = objective_function

  def run(self) -> tuple:
    population = self.__movements_supplier.create_population()
    fitness = self.__movements_supplier.compute_population_fitness(self.__function, population)
    generacion_track = []
    best_individual, best_fitness = self.__movements_supplier.get_best(self.__function, population, fitness)

    population_with_fitness = list(zip(fitness, population))
    
    track_time_per_gen = []
    start_total = time.time()

    for i in range(self.__ga_params.n_generations):
      gen_start = time.time()
      
      new_population = []
      new_fitness = []
      parents = self.__movements_supplier.select(population_with_fitness)

      while len(new_population) < self.__ga_params.population_size:
        offsping1, offspring2 = self.__movements_supplier.crossing(parents[0], parents[1])
        h1 = self.__movements_supplier.mutate(offsping1, self.__ga_params.p_mutate)
        #print(h1)
        #print(f"\nCalculando fitess Hijo . . .")
        new_fitness.append(self.__function.evaluate(h1))
        new_population.append(h1)

        if len(new_population) < self.__ga_params.population_size:
          h2 = self.__movements_supplier.mutate(offspring2, self.__ga_params.p_mutate)
          #print(h2)
          #print(f"\nCalculando fitess Hijo . . .")
          new_fitness.append(self.__function.evaluate(h2))
          new_population.append(h2)
      
      print(f"Gen actual -> {i+1}")

      new_population_with_fitness = list(zip(new_fitness, new_population))
      population_with_fitness = self.generate_new_population(new_population_with_fitness, population_with_fitness)

      fitness, population = zip(*population_with_fitness)
      current_best_individual, current_best_fitness = self.__movements_supplier.get_best(self.__function, population,
                                                                                         fitness)

      if self.__function.compare_objective_values(current_best_fitness, best_fitness) > 0:
        best_individual = current_best_individual
        best_fitness = current_best_fitness

      generacion_track.append(max(population_with_fitness, key=lambda x: x[0])[0])
      print(f"\nGeneración {i + 1}/{self.__ga_params.n_generations}, Mejor fitness: {best_fitness}\n")
      elapsed_gen = time.time() - gen_start
      track_time_per_gen.append(elapsed_gen)

      # if (self.validate_termination(fitness)): 
      #   # print(self.__function.get_history())
      #   return best_individual, best_fitness
    
    total_time = time.time() - start_total
    print("===============================================")
    for idx, (fit, tgen) in enumerate(zip(generacion_track, track_time_per_gen), start=1):
        print(f"Generación {idx} | Mejor Fitness = {fit} | Tiempo = {tgen:.3f} s")
    print(f"Tiempo total de ejecución: {total_time:.3f} s\n")

    # print(self.__function.get_history())
    return best_individual, best_fitness, generacion_track, total_time

  def generate_new_population(self, new_population_with_fitness, population_with_fitness):

    temp_population = new_population_with_fitness + population_with_fitness
    temp_population.sort(key=lambda x: x[0], reverse=True)

    return temp_population[0:self.__ga_params.population_size]

  def validate_termination(self, fitness):
    fitness_count = Counter(fitness)

    total_gen = len(fitness)
    limit = total_gen * 0.95

    terminate = any(value >= limit for value in fitness_count.values())

    if terminate:
      print("El 95% o más de la población tiene el mismo valor de fitness.")
      print(fitness_count)
      return True
    else:
      return False

