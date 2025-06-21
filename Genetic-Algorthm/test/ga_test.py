import sys
import os
import time
import csv
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import yaml

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)


from src.optimization.optimization_algorithm import OptimizationAlgorithm
from src.optimization.genetic_algorithm.movements_supplier.GeneticAlgorithmMovementsSupplier import GAMovementsSupplier
from src.optimization.genetic_algorithm.GeneticAlgorithmParameters import GAParameters
from src.optimization.genetic_algorithm.genetic_algorithm import GeneticAlgorithm
from src.optimization.objective_function.ObjectiveFunction import ObjectiveFunction

from MKPGAMovementSupplier import MKPGAMovementSupplier
from MKPInstance import MKPInstance
from MKPObjectiveFunction import MKPObjectiveFunction

# --- PANEL DE CONTROL PRINCIPAL ---
INSTANCIA_A_PROBAR = "InstanciaMKP_actual_5"
# Define la carpeta donde se guardarán TODOS los resultados
RUTA_BASE_RESULTADOS = "/home/daniel/PERSONAL/UNIVERSIDAD/OPTI/MKP-Opti/Genetic-Algorthm/test/results_experiments"
RUTA_ARCHIVO_YAML = "/home/daniel/PERSONAL/UNIVERSIDAD/OPTI/MKP-Opti/Genetic-Algorthm/test/experimentos.yaml" # <--- RUTA A NUESTRO ARCHIVO DE CONFIGURACIÓN

# --- LISTA DE EXPERIMENTOS A REALIZAR ---

def cargar_configuracion_desde_yaml(ruta_yaml):
    """Carga la configuración global y los experimentos desde un archivo YAML."""
    try:
        with open(ruta_yaml, 'r', encoding='utf-8') as f:
            config_data = yaml.safe_load(f)
        
        global_config = config_data.get("configuracion_global")
        if not all(k in global_config for k in ["ruta_instancia", "population_size", "n_generations"]):
            print("Error: El YAML debe tener 'configuracion_global' con 'ruta_instancia', 'population_size', y 'n_generations'.")
            return None, None

        experimentos = [exp for exp in config_data.get("experimentos", []) if exp and exp.get("nombre")]
        if not experimentos:
            print("Advertencia: El archivo YAML no contiene experimentos válidos.")
            return global_config, None
            
        print(f"Cargada configuración global para la tanda.")
        print(f"Cargados {len(experimentos)} experimentos desde '{ruta_yaml}'.")
        return global_config, experimentos
    except (FileNotFoundError, yaml.YAMLError) as e:
        print(f"Error procesando el archivo YAML '{ruta_yaml}': {e}")
        return None, None

# ==============================================================================
# 2. FUNCIONES DE EXPORTACIÓN Y GRAFICACIÓN
# ==============================================================================

def exportar_reporte_detallado(ruta_archivo, config, resultados_fitness, tiempos_ejecucion, optima_sol):
    """Exporta un reporte detallado en .txt para un experimento completo."""
    with open(ruta_archivo, 'w', encoding='utf-8') as f:
        f.write(f"--- Reporte de Resultados para el Experimento: {config['nombre']} ---\n")
        f.write(f"Instancia: {INSTANCIA_A_PROBAR}\n")
        f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Número de Ejecuciones: {len(resultados_fitness)}\n\n")

        f.write("--- Parámetros de Configuración ---\n")
        for key, value in config['params'].items():
            f.write(f"{key}: {value}\n")
        f.write("\n")

        f.write("--- Estadísticas de Resultados ---\n")
        f.write(f"Mejor Fitness Encontrado (en todas las ejecuciones): {max(resultados_fitness):.4f}\n")
        f.write(f"Peor Fitness Encontrado: {min(resultados_fitness):.4f}\n")
        f.write(f"Fitness Promedio: {np.mean(resultados_fitness):.4f}\n")
        f.write(f"Desviación Estándar del Fitness: {np.std(resultados_fitness):.4f}\n")
        f.write(f"Tiempo de Ejecución Promedio: {np.mean(tiempos_ejecucion):.4f}s\n\n")

        f.write("--- Mejor Solución Global Encontrada ---\n")
        f.write(f"Fitness: {optima_sol['fitness']}\n")
        f.write(f"Vector: {' '.join(map(str, optima_sol['solucion']))}\n")

def generar_grafico_convergencia(ruta_archivo, all_histories, config_nombre):
    """Genera y guarda un gráfico de convergencia promedio con desviación estándar."""
    # Rellenar historiales para que todos tengan la misma longitud
    max_len = max(len(h) for h in all_histories)
    all_histories_padded = [np.pad(h, (0, max_len - len(h)), 'edge') for h in all_histories]
    
    mean_fitness = np.mean(all_histories_padded, axis=0)
    std_fitness = np.std(all_histories_padded, axis=0)
    
    plt.figure(figsize=(12, 7))
    plt.plot(mean_fitness, label="Fitness Promedio", color='blue')
    plt.fill_between(range(max_len), mean_fitness - std_fitness, mean_fitness + std_fitness, color='blue', alpha=0.2, label="Desviación Estándar")
    plt.title(f"Convergencia Promedio - {config_nombre}")
    plt.xlabel("Generación")
    plt.ylabel("Mejor Fitness")
    plt.grid(True)
    plt.legend()
    plt.savefig(ruta_archivo)
    plt.close()

def generar_boxplot_fitness(ruta_archivo, final_fitnesses, config_nombre):
    """Genera y guarda un boxplot de los resultados de fitness finales."""
    plt.figure(figsize=(8, 6))
    plt.boxplot(final_fitnesses, patch_artist=True)
    plt.title(f"Distribución de Fitness Final - {config_nombre}")
    plt.ylabel("Mejor Fitness")
    plt.xticks([1], [config_nombre])
    plt.grid(True)
    plt.savefig(ruta_archivo)
    plt.close()

def actualizar_resumen_csv(ruta_csv, datos_experimento):
    """Añade una fila a un archivo CSV de resumen. Crea el archivo y el encabezado si no existen."""
    escribir_encabezado = not os.path.exists(ruta_csv)
    
    with open(ruta_csv, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=datos_experimento.keys())
        if escribir_encabezado:
            writer.writeheader()
        writer.writerow(datos_experimento)

# ==============================================================================
# 3. BUCLE PRINCIPAL DE EJECUCIÓN
# ==============================================================================

if __name__ == "__main__":
    global_config, EXPERIMENTOS = cargar_configuracion_desde_yaml(RUTA_ARCHIVO_YAML)
    if not global_config or not EXPERIMENTOS:
        sys.exit("No se pudo cargar la configuración o los experimentos. El programa terminará.")

    ruta_instancia_relativa = global_config["ruta_instancia"]
    NUM_EJECUCIONES_POR_EXPERIMENTO = global_config.get("numero_ejecuciones", 10)
    
    POPULATION_SIZE_GLOBAL = global_config["population_size"]
    N_GENERATIONS_GLOBAL = global_config["n_generations"]
    
    nombre_instancia = os.path.splitext(os.path.basename(ruta_instancia_relativa))[0]
    
    print(f"Cargando instancia: {nombre_instancia}...")
    ruta_instancia_completa = os.path.join(project_root, ruta_instancia_relativa) if not os.path.isabs(ruta_instancia_relativa) else ruta_instancia_relativa
    mkp_instance = MKPInstance(ruta_instancia_completa)

    ruta_base_instancia = os.path.join(RUTA_BASE_RESULTADOS, nombre_instancia)
    os.makedirs(ruta_base_instancia, exist_ok=True)
    ruta_resumen_csv = os.path.join(ruta_base_instancia, f"resumen_experimentos_{nombre_instancia}.csv") 

    for experimento in EXPERIMENTOS:
        config_nombre = experimento["nombre"]
        params_experimento = experimento["params"]
        
        print(f"\n{'='*80}\n--- Ejecutando Experimento: {config_nombre} para Instancia: {nombre_instancia} ---\n{'='*80}")

        ruta_experimento_actual = os.path.join(ruta_base_instancia, config_nombre)
        os.makedirs(ruta_experimento_actual, exist_ok=True)

        resultados_fitness_experimento = []
        tiempos_experimento = []
        historias_experimento = []
        mejor_solucion_global = {"fitness": -1, "solucion": []}

        for i in range(NUM_EJECUCIONES_POR_EXPERIMENTO):
            print(f"  -> Ejecución {i + 1}/{NUM_EJECUCIONES_POR_EXPERIMENTO}...")

            parametros_completos = {
                "population_size": POPULATION_SIZE_GLOBAL,
                "n_generations": N_GENERATIONS_GLOBAL,
                "n_genes": mkp_instance.cantidad_variables
            }
            parametros_completos.update(params_experimento)

            ga_params = GAParameters(**parametros_completos)

            mkp_obj_function = MKPObjectiveFunction(False, mkp_instance.lista_restricciones, 
                                                    mkp_instance.lista_capacidades, mkp_instance.optimo,
                                                    mkp_instance.valores_variables, 
                                                    mkp_instance.cantidad_restricciones, mkp_instance.cantidad_variables,
                                                    constraint_strategy=ga_params.constraint_strategy,
                                                    penalty_factor=ga_params.penalty_factor)
            
            mkp_movement_supplier = MKPGAMovementSupplier(ga_params)
            genetic_algorithm = GeneticAlgorithm(ga_params, mkp_movement_supplier, mkp_obj_function)

            best_solution, best_fitness, ga_track, total_time = genetic_algorithm.run()

            resultados_fitness_experimento.append(best_fitness)
            tiempos_experimento.append(total_time)
            historias_experimento.append(ga_track)

            if best_fitness > mejor_solucion_global["fitness"]:
                mejor_solucion_global["fitness"] = best_fitness
                mejor_solucion_global["solucion"] = best_solution
        
        print(f"--- Experimento '{config_nombre}' completado. Generando reportes... ---")

        parametros_reporte = {
            "population_size": POPULATION_SIZE_GLOBAL,
            "n_generations": N_GENERATIONS_GLOBAL,
            **params_experimento
        }
        
        experimento_para_reporte = {"nombre": config_nombre, "params": parametros_reporte}
        ruta_txt = os.path.join(ruta_experimento_actual, "reporte_detallado.txt")
        exportar_reporte_detallado(ruta_txt, experimento, resultados_fitness_experimento, tiempos_experimento, mejor_solucion_global)

        ruta_convergencia = os.path.join(ruta_experimento_actual, "grafico_convergencia.png")
        generar_grafico_convergencia(ruta_convergencia, historias_experimento, config_nombre)

        ruta_boxplot = os.path.join(ruta_experimento_actual, "grafico_boxplot.png")
        generar_boxplot_fitness(ruta_boxplot, resultados_fitness_experimento, config_nombre)
        
        datos_para_csv = {
            "Experimento": config_nombre,
            "Instancia": nombre_instancia,
            "Mejor_Fitness": max(resultados_fitness_experimento),
            "Fitness_Promedio": np.mean(resultados_fitness_experimento),
            "Fitness_Std_Dev": np.std(resultados_fitness_experimento),
            "Tiempo_Promedio_s": np.mean(tiempos_experimento),
            **parametros_reporte 
        }
        actualizar_resumen_csv(ruta_resumen_csv, datos_para_csv)
        
        print(f"Reportes para '{config_nombre}' guardados en: {ruta_experimento_actual}")

    print(f"\n¡Todos los experimentos para la instancia {nombre_instancia} han finalizado exitosamente!")