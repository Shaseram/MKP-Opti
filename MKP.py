import time
from Problem import Problem

def cargarInstancia():
     lista_problemas = []
     
     with open('In1.txt', 'r') as file:
         lines = file.readlines()
 
     cantidad_problemas = int(lines[0].strip())
 
     linea_actual = 2
     for index in range(cantidad_problemas):
         problema = Problem()
 
         datos = lines[linea_actual].strip().split()
         problema.cantidad_variables = int(datos[0])
         problema.cantidad_restricciones = int(datos[1])
         problema.optimo = float(datos[2])
         
         linea_actual += 1
 
         datos = lines[linea_actual].strip().split()
         problema.valores_variables = [float(valor) for valor in datos]
         linea_actual += 1
 
 
         for i in range(problema.cantidad_restricciones):
             datos = lines[linea_actual].strip().split()
             problema.lista_restricciones.append([float(valor) for valor in datos])
             linea_actual += 1
 
         datos = lines[linea_actual].strip().split()
         problema.lista_capacidades = [float(valor) for valor in datos]
         linea_actual += 1
 
         lista_problemas.append(problema)
 
         if index < cantidad_problemas - 1:
             linea_actual += 1
     
     return lista_problemas

def evaluar_solucion(solucion_binaria, problema):
    """
    Evalúa una solución binaria para un problema MKP.

    Args:
        solucion_binaria (list): Lista de 0s y 1s representando la selección de ítems.
        problema (Problem): Objeto Problem con los datos de la instancia.

    Returns:
        tuple: (float, bool) - El valor total de la solución y si es factible.
               Retorna (0.0, False) si la solución no es válida o no es factible.
    """
    
    valor_total = 0.0
    peso_total_por_restriccion = [0.0] * problema.cantidad_restricciones
    es_factible = True

    # Calcular valor y pesos acumulados
    for j in range(problema.cantidad_variables):
        if solucion_binaria[j] == 1:
            valor_total += problema.valores_variables[j]

            for k in range(problema.cantidad_restricciones):
                peso_total_por_restriccion[k] += problema.lista_restricciones[k][j]
                

    # Verificar factibilidad (si las capacidades se respetan)
    for i in range(problema.cantidad_restricciones):
        if peso_total_por_restriccion[i] > problema.lista_capacidades[i]:
            es_factible = False
            break 

    return valor_total, es_factible

def resolver_mkp_fuerza_bruta(problema):
    """
    Resuelve una instancia del MKP usando fuerza bruta (enumeración exhaustiva).

    Args:
        problema (Problem): Objeto Problem con los datos de la instancia.

    Returns:
        tuple: (list, float) - La mejor solución encontrada (lista de 0s y 1s)
               y su valor. Retorna (None, 0.0) si n es demasiado grande o no se
               encuentra solución factible.
    """
    n = problema.cantidad_variables
    mejor_valor = 0.0
    mejor_solucion = [0] * n 

    # --- Límite de Seguridad para Fuerza Bruta ---
    if n >= MAX_N_FUERZA_BRUTA:
        print(f"ADVERTENCIA: n={n} es demasiado grande para fuerza bruta (límite={MAX_N_FUERZA_BRUTA}). Omitiendo problema.")
        return None, 0.0
    # -----------------------------------------

    num_soluciones = 2**n
    print(f"\n--- Resolviendo problema con n={n}, m={problema.cantidad_restricciones} (Óptimo conocido: {problema.optimo}) ---")
    print(f"Evaluando {num_soluciones} posibles soluciones...")
    start_time = time.time()

    for i in range(num_soluciones):
        solucion_actual = [int(bit) for bit in format(i, f'0{n}b')]
        valor_actual, es_factible = evaluar_solucion(solucion_actual, problema)

        if valor_actual == problema.optimo:
            end_time = time.time()
            tiempo_transcurrido = end_time - start_time
            print(f"Evaluación completa en {tiempo_transcurrido:.4f} segundos.")
            
            return solucion_actual,valor_actual

        if es_factible and valor_actual > mejor_valor:
            mejor_valor = valor_actual
            mejor_solucion = solucion_actual
            
    end_time = time.time()
    tiempo_transcurrido = end_time - start_time
    print(f"Evaluación completa en {tiempo_transcurrido:.4f} segundos.")

    return mejor_solucion, mejor_valor


if __name__ == "__main__":
    
    lista_problemas = cargarInstancia()
    MAX_N_FUERZA_BRUTA = 51
    if lista_problemas:
        print(f"Se cargaron {len(lista_problemas)} instancias del problema.")

        for idx, prob in enumerate(lista_problemas):
            print(f"\n=====================================")
            print(f"Procesando Instancia #{idx+1}")
            print(f"-------------------------------------")
            print("Datos del problema:")
            print(f"Cantidad variables: {prob.cantidad_variables}") 
            print(f"Cantidad restricciones: {prob.cantidad_restricciones}")
            print(f"Óptimo conocido: {prob.optimo}")
            print(f"Valores variables: {prob.valores_variables}")
            print(f"Lista restricciones: {prob.lista_restricciones}")
            print(f"Lista capacidades: {prob.lista_capacidades}")

            solucion_encontrada, valor_encontrado = resolver_mkp_fuerza_bruta(prob)

            if solucion_encontrada is not None:
                print(f"\nResultados para Instancia #{idx+1}:")
                print(f"  Mejor solución encontrada: {solucion_encontrada}")
                print(f"  Valor de la solución:    {valor_encontrado:.2f}")
                print(f"  Óptimo conocido:         {prob.optimo:.2f}")
                if abs(valor_encontrado - prob.optimo) == 0: 
                    print("  ¡El valor encontrado coincide con el óptimo conocido!")


        print("\n=====================================")
        print("Procesamiento de todas las instancias completado.")
