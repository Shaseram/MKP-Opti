class GAParameters:
  """
  Clase para almacenar todos los parámetros de configuración para el Algoritmo Genético.
  Funciona como un panel de control para los experimentos.
  """
  def __init__(self,
                # --- Parámetros base del problema ---
                population_size: int,
                n_genes: int,
                n_generations: int,
                p_mutate: float,

                # --- Parámetros para experimentación (con valores por defecto) ---

                # 1. Estrategia de Selección de Padres
                selection_type: str = 'tournament',   # Opciones: 'tournament', 'roulette'
                tournament_size: int = 3,             # Relevante solo si selection_type es 'tournament'

                # 2. Estrategia de Cruzamiento
                crossover_type: str = 'single_point', # Opciones: 'single_point', 'two_points', 'uniform'

                # 3. Elitismo
                elitism_count: int = 2,               # Número de mejores individuos que pasan directamente

                # 4. Estrategia de Manejo de Restricciones
                constraint_strategy: str = 'death_penalty', # Opciones: 'death_penalty', 'penalty_function', 'repair'
                
                # 5. Heurística de Reparación (si se usa 'repair')
                repair_heuristic: str = 'ratio',      # Opciones: 'ratio', 'random', 'least_value', 'heaviest'
                
                # 6. Factor de Penalización (si se usa 'penalty_function')
                penalty_factor: float = 1.0,           
                
                initial_population_density: float = 0.15

                ):
    
    # --- Asignación de parámetros ---
    self.population_size = population_size
    self.n_genes = n_genes
    self.n_generations = n_generations
    self.p_mutate = p_mutate
    
    self.selection_type = selection_type
    self.tournament_size = tournament_size
    self.crossover_type = crossover_type
    self.elitism_count = elitism_count
    self.constraint_strategy = constraint_strategy
    self.repair_heuristic = repair_heuristic
    self.penalty_factor = penalty_factor
    self.initial_population_density = initial_population_density

    # --- Bloque de validación (buena práctica para evitar errores de tipeo) ---
    if self.selection_type not in ['tournament', 'roulette']:
        raise ValueError(f"Error: selection_type '{self.selection_type}' no es válido. Opciones: 'tournament', 'roulette'.")

    if self.crossover_type not in ['single_point', 'two_points', 'uniform']:
        raise ValueError(f"Error: crossover_type '{self.crossover_type}' no es válido. Opciones: 'single_point', 'two_points', 'uniform'.")

    if self.constraint_strategy not in ['death_penalty', 'penalty_function', 'repair']:
        raise ValueError(f"Error: constraint_strategy '{self.constraint_strategy}' no es válido. Opciones: 'death_penalty', 'penalty_function', 'repair'.")

    if self.repair_heuristic not in ['ratio', 'random', 'least_value', 'heaviest']:
        raise ValueError(f"Error: repair_heuristic '{self.repair_heuristic}' no es válido. Opciones: 'ratio', 'random', 'least_value', 'heaviest'.")

    if self.elitism_count < 0 or self.elitism_count >= self.population_size:
        raise ValueError("Error: elitism_count debe ser un número positivo y menor que el tamaño de la población.")