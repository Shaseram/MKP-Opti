import sys
import os

# Obtener la ruta absoluta del directorio del proyecto (que está un nivel arriba de 'test')
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Agregar la raíz del proyecto al sys.path para que Python pueda encontrar el módulo 'src'
sys.path.insert(0, project_root)

from datetime import datetime

def exportar_resultados_a_txt(solucion, fitness, historial_fitness, nombre_archivo, population_size, n_generation, p_mutate, total_time):
    """
    Exporta los resultados de un algoritmo genético a un archivo de texto.

    Args:
        solucion (list or array): La mejor solución encontrada (vector de 0s y 1s).
        fitness (float or int): El valor de fitness de la mejor solución.
        historial_fitness (list or array): Una lista con el mejor fitness de cada generación.
        nombre_archivo (str): El nombre del archivo de salida (ej. "resultados_ga.txt").
    """
    try:
        # Usamos 'with open' que se encarga de cerrar el archivo automáticamente
        with open(nombre_archivo, 'w', encoding='utf-8') as f:
            # 1. Escribir un encabezado con información general y fecha
            now = datetime.now()
            f.write("--- Resultados del Algoritmo Genético ---\n")
            f.write(f"TIEMPO DE EJECUCIÓN -> {total_time}\n\n")
            
            f.write("--- Parámetros ---\n")
            f.write(f"TAMAÑO POBLACIÓN -> {population_size}\n\n")
            f.write(f"NÚMERO GENERACIONES -> {n_generation}\n\n")
            f.write(f"PROBABILIDAD MUTACIÓN -> {p_mutate}\n\n")
            
            # 2. Escribir la mejor solución y su fitness
            f.write("== Mejor Solución Encontrada ==\n")
            f.write(f"Mejor Fitness: {fitness}\n")
            f.write("Vector de la Solución:\n")
            # Convertimos la lista de la solución a un string separado por espacios
            solucion_str = " ".join(map(str, solucion))
            f.write(f"{solucion_str}\n\n")

            # 3. Escribir el historial de fitness por generación
            f.write("== Historial de Fitness por Generación ==\n")
            # Usamos enumerate para obtener el número de la generación (empezando en 1)
            for i, valor_fitness in enumerate(historial_fitness):
                f.write(f"Generación {i + 1}: {valor_fitness}\n")
        
        print(f"Resultados exportados exitosamente a '{nombre_archivo}'")

    except IOError as e:
        print(f"Error al escribir en el archivo '{nombre_archivo}': {e}")
        
        
import os

def obtener_siguiente_numero_ejecucion(ruta_resultados, nombre_instancia):
    """
    Revisa la carpeta de resultados para encontrar el mayor número de ejecución
    y devuelve el siguiente.
    """
    # Asegurarse de que la carpeta de resultados exista
    os.makedirs(ruta_resultados, exist_ok=True)
    
    max_c = -1
    prefijo = f"resultados_ejecucion_"

    try:
        # Listar todos los archivos en el directorio
        for archivo in os.listdir(ruta_resultados):
            # Verificar si el archivo corresponde al patrón de resultados
            if archivo.startswith(prefijo) and archivo.endswith(f"_{nombre_instancia}"):
                # Extraer el número del nombre del archivo
                try:
                    parte_media = archivo[len(prefijo):-len(f"_{nombre_instancia}")]
                    num_actual = int(parte_media)
                    if num_actual > max_c:
                        max_c = num_actual
                except ValueError:
                    # El archivo coincide con el patrón pero no tiene un número válido, lo ignoramos.
                    continue
        
        # El siguiente número es el máximo encontrado + 1
        return max_c + 1
        
    except OSError as e:
        print(f"Error leyendo el directorio {ruta_resultados}: {e}")
        return 0

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
population_size = 5000
n_generation = 5000
p_mutate = 0.066666666666666666666666666


instance = "InstanciaMKP_actual_9"
mkp_parameters: Instances = MKPInstance(f"test/MKPInstances/{instance}.txt")
n_genes = mkp_parameters.cantidad_variables
ga_params: GAParameters = GAParameters(population_size, n_genes, n_generation, p_mutate)
mkp_obj_function: ObjectiveFunction = MKPObjectiveFunction(False, mkp_parameters.lista_restricciones, 
                                                            mkp_parameters.lista_capacidades, mkp_parameters.optimo,
                                                                mkp_parameters.valores_variables, 
                                                                mkp_parameters.cantidad_restricciones, mkp_parameters.cantidad_variables)
mkp_movement_supplier: GAMovementsSupplier = MKPGAMovementSupplier(ga_params)

genetic_algorithm: OptimizationAlgorithm = GeneticAlgorithm(ga_params, mkp_movement_supplier, mkp_obj_function)

best_solution, best_fitness, ga_track, total_time = genetic_algorithm.run()
print(f"Solution = {best_solution} | Fitness = {best_fitness}")


ruta_base_resultados = "/home/daniel/PERSONAL/UNIVERSIDAD/OPTI/MKP-Opti/Genetic-Algorthm/test/results"
c = obtener_siguiente_numero_ejecucion(ruta_base_resultados, instance)
nombre_del_archivo = f"{ruta_base_resultados}/resultados_ejecucion_{c}_{instance}"
print(f"Esta es la ejecución N° {c}. Se guardará en: {nombre_del_archivo}")

exportar_resultados_a_txt(best_solution, best_fitness, ga_track, nombre_del_archivo, population_size, n_generation, p_mutate, total_time)
