# MKP-Opti

Proyecto de optimización para el Problema de la Mochila Multidimensional 0/1 (Multidimensional Knapsack Problem).

## Integrantes

- **Daniel Miranda - 21554586-5**
- **Pablo Silva - 20184240-9**
- **Vicente Arratia - 21404392-0**

## Descripción

Este proyecto implementa algoritmos de optimización para resolver el Problema de la Mochila Multidimensional 0/1, incluyendo:

- **Fuerza Bruta**: Solución exacta para instancias pequeñas
- **Algoritmo Genético**: Metaheurística para instancias de mayor tamaño

## Estructura del Proyecto

```
MKP-Opti/
├── src/
│   └── optimization/
│       ├── genetic_algorithm/
│       └── objective_function/
├── test/
│   ├── MKPInstances/
│   ├── experimentos.yaml
│   ├── ga_test.py
│   └── results_experiments/
└── README.md
```

## Requisitos

- Python 3.7+
- NumPy
- Matplotlib
- PyYAML

### Instalación de dependencias

```bash
pip install numpy matplotlib pyyaml
```

## Instrucciones de Ejecución

### 1. Configuración de Experimentos

Los experimentos se configuran a través del archivo `test/experimentos.yaml`. Este archivo contiene:

- **Configuración Global**: Parámetros comunes para todos los experimentos
- **Lista de Experimentos**: Diferentes configuraciones del algoritmo genético

#### Ejemplo de configuración:

```yaml
configuracion_global:
  ruta_instancia: "ruta/a/instancia.txt"
  numero_ejecuciones: 10
  population_size: 1500
  n_generations: 1500

experimentos:
  - nombre: Baseline_Repair_Ratio_Tournament
    params:
      p_mutate: 0.03
      selection_type: tournament
      tournament_size: 5
      crossover_type: uniform
      elitism_count: 5
      constraint_strategy: repair
      repair_heuristic: ratio
      initial_population_density: 0.2
```

### 2. Ejecución del Algoritmo Genético

Para ejecutar los experimentos configurados:

```bash
cd test/
python ga_test.py
```

### 3. Parámetros Configurables

#### Configuración Global:
- `ruta_instancia`: Ruta al archivo de instancia MKP
- `numero_ejecuciones`: Número de ejecuciones por experimento
- `population_size`: Tamaño de la población
- `n_generations`: Número de generaciones

#### Parámetros del Algoritmo Genético:
- `p_mutate`: Probabilidad de mutación (0.0 - 1.0)
- `selection_type`: Tipo de selección (`tournament`, `roulette`)
- `tournament_size`: Tamaño del torneo (si se usa selección por torneo)
- `crossover_type`: Tipo de cruce (`uniform`, `single_point`, `two_points`)
- `elitism_count`: Número de individuos élite a conservar
- `constraint_strategy`: Estrategia para manejar restricciones (`repair`, `penalty_function`)
- `repair_heuristic`: Heurística de reparación (`ratio`, `heaviest`)
- `penalty_factor`: Factor de penalización (si se usa penalty_function)
- `initial_population_density`: Densidad inicial de la población (0.0 - 1.0)

### 4. Resultados

Los resultados se guardan automáticamente en la carpeta `test/results_experiments/` con la siguiente estructura:

```
results_experiments/
└── [nombre_instancia]/
    ├── resumen_experimentos_[instancia].csv
    └── [nombre_experimento]/
        ├── reporte_detallado.txt
        ├── grafico_convergencia.png
        └── grafico_boxplot.png
```

#### Archivos generados:
- **reporte_detallado.txt**: Estadísticas completas del experimento
- **grafico_convergencia.png**: Gráfico de convergencia promedio
- **grafico_boxplot.png**: Distribución de resultados finales
- **resumen_experimentos.csv**: Resumen comparativo de todos los experimentos

### 5. Personalización de Experimentos

Para crear nuevos experimentos:

1. Editar el archivo `test/experimentos.yaml`
2. Agregar nuevas configuraciones en la sección `experimentos`
3. Comentar/descomentar experimentos según sea necesario
4. Ejecutar `python ga_test.py`

### 6. Rutas de Archivos

**Importante**: Asegúrese de actualizar las rutas en el archivo de configuración según su estructura de directorios:

- `RUTA_BASE_RESULTADOS`: Carpeta donde se guardarán los resultados
- `RUTA_ARCHIVO_YAML`: Ruta al archivo de configuración
- `ruta_instancia`: Ruta a la instancia MKP a resolver

## Ejemplo de Uso Completo

1. **Preparar la instancia**: Colocar el archivo de instancia MKP en `test/MKPInstances/`

2. **Configurar experimento**: Editar `test/experimentos.yaml` con la ruta correcta

3. **Ejecutar**: 
   ```bash
   cd test/
   python ga_test.py
   ```

4. **Analizar resultados**: Revisar los archivos generados en `test/results_experiments/`

## Notas Técnicas

- El algoritmo implementa diferentes estrategias de manejo de restricciones
- Soporte para múltiples tipos de selección y cruce
- Generación automática de gráficos y reportes estadísticos
- Configuración flexible mediante archivos YAML
- Seguimiento detallado de la convergencia del algoritmo