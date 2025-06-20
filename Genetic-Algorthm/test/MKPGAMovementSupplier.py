# Archivo: src/optimization/genetic_algorithm/movements_supplier/MKPGAMovementSupplier.py

import random
import numpy as np
from src.optimization.genetic_algorithm.movements_supplier.GeneticAlgorithmMovementsSupplier import GAMovementsSupplier
from src.optimization.genetic_algorithm.GeneticAlgorithmParameters import GAParameters
from src.optimization.objective_function.ObjectiveFunction import ObjectiveFunction


class MKPGAMovementSupplier(GAMovementsSupplier):
    def __init__(self, ga_params: GAParameters):
        super().__init__(ga_params)

    def create_individual(self):
        """
        Crea un individuo inicial basándose en la densidad de población
        definida en los parámetros.
        """
        # La probabilidad ahora se lee desde el objeto de parámetros
        probabilidad_de_incluir = self.ga_params.initial_population_density
        
        return [1 if random.random() < probabilidad_de_incluir else 0 for _ in range(self.ga_params.n_genes)]
    # ==================================================================
    # 1. SELECCIÓN (ACTÚA COMO DESPACHADOR)
    # ==================================================================
    def select(self, population_with_fitness: list[tuple[float, list[int]]]):
        selection_method = self.ga_params.selection_type
        if selection_method == 'tournament':
            return self._select_tournament(population_with_fitness)
        elif selection_method == 'roulette':
            return self._select_roulette(population_with_fitness)

    def _select_tournament(self, population_with_fitness):
        """Selección por torneo generalizada."""
        k = self.ga_params.tournament_size
        # Seleccionar k individuos al azar de la población para el torneo
        tournament_contenders = random.sample(population_with_fitness, k)
        # El ganador es el que tiene el mayor fitness (índice 0 de la tupla)
        winner = max(tournament_contenders, key=lambda item: item[0])
        return winner[1]  # Retorna solo el individuo (cromosoma, índice 1 de la tupla)

    def _select_roulette(self, population_with_fitness):
        """Selección por rueda de ruleta."""
        fitnesses, population = zip(*population_with_fitness)
        
        # Manejar caso de fitness negativo o todo cero
        min_fitness = min(fitnesses)
        shifted_fitnesses = [f - min_fitness for f in fitnesses]
        total_fitness = sum(shifted_fitnesses)

        if total_fitness == 0:
            return random.choice(population) # Si todos son iguales, elige al azar

        selection_probs = [f / total_fitness for f in shifted_fitnesses]
        selected_index = np.random.choice(len(population), p=selection_probs)
        return population[selected_index]
    
    # ==================================================================
    # 2. CRUZAMIENTO (ACTÚA COMO DESPACHADOR)
    # ==================================================================
    def crossing(self, father_1, father_2):
        crossover_method = self.ga_params.crossover_type
        if crossover_method == 'single_point':
            return self._crossing_single_point(father_1, father_2)
        elif crossover_method == 'two_points':
            return self._crossing_two_points(father_1, father_2)
        elif crossover_method == 'uniform':
            return self._crossing_uniform(father_1, father_2)

    def _crossing_single_point(self, father_1, father_2):
        crossover_point = random.randint(1, self.ga_params.n_genes - 1)
        child1 = father_1[:crossover_point] + father_2[crossover_point:]
        child2 = father_2[:crossover_point] + father_1[crossover_point:]
        return child1, child2

    def _crossing_uniform(self, padre1, padre2):
        hijo1, hijo2 = list(padre1), list(padre2)
        for i in range(self.ga_params.n_genes):
            if random.random() < 0.5:
                hijo1[i], hijo2[i] = hijo2[i], hijo1[i]  # Intercambiar genes
        return hijo1, hijo2
    
    def _crossing_two_points(self, padre1, padre2):
        tamaño = self.ga_params.n_genes
        punto1 = random.randint(1, tamaño - 2)
        punto2 = random.randint(punto1, tamaño - 1)
        if punto1 == punto2: # Asegurar que no sean el mismo punto
            return self._crossing_single_point(padre1, padre2)
        
        hijo1 = padre1[:punto1] + padre2[punto1:punto2] + padre1[punto2:]
        hijo2 = padre2[:punto1] + padre1[punto1:punto2] + padre2[punto2:]
        return hijo1, hijo2

    # ==================================================================
    # 3. MUTACIÓN
    # ==================================================================
    def mutate(self, genome, prob_mutacion):
        new_genome = list(genome) # Crear una copia para no modificar el original
        for i in range(len(new_genome)):
            if random.random() <= prob_mutacion:
                new_genome[i] = 1 - new_genome[i] # Invierte el bit (0->1, 1->0)
        return new_genome

    # ==================================================================
    # 4. REPARACIÓN DE INDIVIDUOS (ACTÚA COMO DESPACHADOR)
    # ==================================================================
    def repair_individual(self, individual, objective_function: ObjectiveFunction):
        # Si la estrategia no es reparar, no hacemos nada.
        if self.ga_params.constraint_strategy != 'repair':
            return individual
            
        # Si ya es factible, tampoco hacemos nada para ahorrar tiempo.
        if self._is_feasible(individual, objective_function):
            return individual
            
        heuristic = self.ga_params.repair_heuristic
        if heuristic == 'random':
            return self._repair_by_random(individual, objective_function)
        elif heuristic == 'least_value':
            return self._repair_by_least_value(individual, objective_function)
        elif heuristic == 'heaviest':
            return self._repair_by_heaviest(individual, objective_function)
        else: # 'ratio' es el default
            return self._repair_by_ratio(individual, objective_function)

    def _is_feasible(self, individual, objective_function):
        # Esta función helper es clave para no repetir código.
        # Necesitamos acceder a los datos del problema desde la función objetivo.
        # NOTA: Usamos los nombres con __ porque son 'privados' en tu clase original.
        capacities = objective_function._MKPObjectiveFunction__lista_capacidades
        weights_matrix = objective_function._MKPObjectiveFunction__lista_restricciones
        
        current_weights = [0.0] * len(capacities)
        for i, gene in enumerate(individual):
            if gene == 1:
                for d in range(len(capacities)):
                    current_weights[d] += weights_matrix[d][i]
        
        for d in range(len(capacities)):
            if current_weights[d] > capacities[d]:
                return False # Si una restricción se viola, es infactible
        return True # Si el bucle termina, es factible

    def _repair_by_random(self, individual, objective_function):
        repaired_ind = list(individual)
        while not self._is_feasible(repaired_ind, objective_function):
            items_in_knapsack = [i for i, gene in enumerate(repaired_ind) if gene == 1]
            if not items_in_knapsack: break
            index_to_remove = random.choice(items_in_knapsack)
            repaired_ind[index_to_remove] = 0
        return repaired_ind

    def _repair_by_least_value(self, individual, objective_function):
        repaired_ind = list(individual)
        values = objective_function._MKPObjectiveFunction__lista_valores
        while not self._is_feasible(repaired_ind, objective_function):
            items_in_knapsack = [(i, values[i]) for i, gene in enumerate(repaired_ind) if gene == 1]
            if not items_in_knapsack: break
            worst_item_index, _ = min(items_in_knapsack, key=lambda x: x[1])
            repaired_ind[worst_item_index] = 0
        return repaired_ind
    
    def _repair_by_heaviest(self, individual, objective_function):
        repaired_ind = list(individual)
        weights_matrix = objective_function._MKPObjectiveFunction__lista_restricciones
        while not self._is_feasible(repaired_ind, objective_function):
            # Calculamos un "peso total" para cada item como la suma de su peso en todas las dimensiones
            items_in_knapsack = [(i, sum(weights_matrix[d][i] for d in range(len(weights_matrix)))) for i, gene in enumerate(repaired_ind) if gene == 1]
            if not items_in_knapsack: break
            worst_item_index, _ = max(items_in_knapsack, key=lambda x: x[1])
            repaired_ind[worst_item_index] = 0
        return repaired_ind
    
    def _repair_by_ratio(self, individual, objective_function):
        repaired_ind = list(individual)
        values = objective_function._MKPObjectiveFunction__lista_valores
        weights_matrix = objective_function._MKPObjectiveFunction__lista_restricciones
        while not self._is_feasible(repaired_ind, objective_function):
            # Calculamos el ratio valor / suma de pesos
            items_in_knapsack = []
            for i, gene in enumerate(repaired_ind):
                if gene == 1:
                    total_weight = sum(weights_matrix[d][i] for d in range(len(weights_matrix)))
                    ratio = values[i] / total_weight if total_weight > 0 else float('inf')
                    items_in_knapsack.append((i, ratio))

            if not items_in_knapsack: break
            worst_item_index, _ = min(items_in_knapsack, key=lambda x: x[1])
            repaired_ind[worst_item_index] = 0
        return repaired_ind