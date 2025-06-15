from src.optimization.optimization_algorithm import OptimizationAlgorithm
from src.optimization.genetic_algorithm.movements_supplier.GeneticAlgorithmMovementsSupplier import GAMovementsSupplier
from src.optimization.genetic_algorithm.GeneticAlgorithmParameters import GAParameters
from src.optimization.genetic_algorithm.genetic_algorithm import GeneticAlgorithm
from src.optimization.objective_function.ObjectiveFunction import ObjectiveFunction

from Instances import Instances
from MKPGAMovementSupplier import MKPGAMovementSupplier
from MKPInstance import MKPInstance
from MKPObjectiveFunction import MKPObjectiveFunction

"""
Parametros MKP
"""
population_size = 1000
n_generation = 1000
p_mutate = 0.1

mkp_parameters: Instances = MKPInstance("test/MKPInstances/Actual.txt")
n_genes = mkp_parameters.cantidad_variables
ga_params: GAParameters = GAParameters(population_size, n_genes, n_generation, p_mutate)
mkp_obj_function: ObjectiveFunction = MKPObjectiveFunction(False, mkp_parameters.lista_restricciones, 
                                                            mkp_parameters.lista_capacidades, mkp_parameters.optimo,
                                                                mkp_parameters.valores_variables, 
                                                                mkp_parameters.cantidad_restricciones, mkp_parameters.cantidad_variables)
mkp_movement_supplier: GAMovementsSupplier = MKPGAMovementSupplier(ga_params)

genetic_algorithm: OptimizationAlgorithm = GeneticAlgorithm(ga_params, mkp_movement_supplier, mkp_obj_function)

best_solution, best_fitness = genetic_algorithm.run()
print(f"Solution = {best_solution} | Fitness = {best_fitness}")