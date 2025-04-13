import time
from Problem import Problem

def cargarInstancia():
    lista_problemas = []
    try:
        with open('In1.txt', 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print("Error: No se encontró el archivo 'In1.txt'. Asegúrate de que esté en el mismo directorio.")
        return []

    try:
        cantidad_problemas = int(lines[0].strip())
        linea_actual = 2 # Empezamos en la línea 2 (índice 1 es línea en blanco)
        
        for index in range(cantidad_problemas):
            if linea_actual >= len(lines):
                print(f"Error: El archivo no contiene suficientes líneas para el problema {index+1}")
                break
            
            problema = Problem()

            # Leer n, m, optimo
            datos = lines[linea_actual].strip().split()
            if len(datos) < 3:
                 print(f"Error: Formato incorrecto en línea {linea_actual + 1} para n, m, optimo.")
                 break
            problema.cantidad_variables = int(datos[0])
            problema.cantidad_restricciones = int(datos[1])
            problema.optimo = float(datos[2])
            linea_actual += 1

            # Leer valores/beneficios
            if linea_actual >= len(lines):
                 print(f"Error: Faltan líneas para valores (problema {index+1}).")
                 break
            datos = lines[linea_actual].strip().split()
            if len(datos) != problema.cantidad_variables:
                 print(f"Error: Inconsistencia en cantidad de valores en línea {linea_actual + 1} (problema {index+1}). Esperados {problema.cantidad_variables}, encontrados {len(datos)}.")
                 # break # Podríamos parar, o intentar continuar con lo que hay
            problema.valores_variables = [float(valor) for valor in datos]
            linea_actual += 1

            # Leer matriz de restricciones
            problema.lista_restricciones = []
            for i in range(problema.cantidad_restricciones):
                if linea_actual >= len(lines):
                    print(f"Error: Faltan líneas para restricciones (problema {index+1}, restricción {i+1}).")
                    problema.lista_restricciones = [] # Marcar como incompleto
                    break
                datos = lines[linea_actual].strip().split()
                if len(datos) != problema.cantidad_variables:
                     print(f"Error: Inconsistencia en cantidad de pesos en línea {linea_actual + 1} (problema {index+1}, restricción {i+1}). Esperados {problema.cantidad_variables}, encontrados {len(datos)}.")
                problema.lista_restricciones.append([float(valor) for valor in datos])
                linea_actual += 1
            
            if not problema.lista_restricciones and problema.cantidad_restricciones > 0: # Si hubo error leyendo restricciones
                 linea_actual += problema.cantidad_restricciones - len(problema.lista_restricciones) # Intentar saltar líneas restantes
                 if linea_actual >= len(lines): continue # Saltar al siguiente problema si no quedan líneas

            # Leer capacidades
            if linea_actual >= len(lines):
                 print(f"Error: Faltan líneas para capacidades (problema {index+1}).")
                 break
            datos = lines[linea_actual].strip().split()
            if len(datos) != problema.cantidad_restricciones:
                 print(f"Error: Inconsistencia en cantidad de capacidades en línea {linea_actual + 1} (problema {index+1}). Esperados {problema.cantidad_restricciones}, encontrados {len(datos)}.")
            problema.lista_capacidades = [float(valor) for valor in datos]
            linea_actual += 1

            lista_problemas.append(problema)

            # Saltar la línea en blanco entre problemas si no es el último
            if index < cantidad_problemas - 1:
                linea_actual += 1
                
    except (ValueError, IndexError) as e:
        print(f"Error procesando el archivo 'In1.txt' en la línea {linea_actual + 1}: {e}")
        print("Verifica el formato del archivo según la descripción.")

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
    if not isinstance(solucion_binaria, list) or len(solucion_binaria) != problema.cantidad_variables:
        #print("Error: Solución binaria inválida.")
        return 0.0, False # Solución inválida

    valor_total = 0.0
    peso_total_por_restriccion = [0.0] * problema.cantidad_restricciones
    es_factible = True

    # Calcular valor y pesos acumulados
    for j in range(problema.cantidad_variables):
        if solucion_binaria[j] == 1:
            valor_total += problema.valores_variables[j]
            for k in range(problema.cantidad_restricciones):
                
                # Asegurarse de que hay suficientes datos en lista_restricciones
                if k < len(problema.lista_restricciones) and j < len(problema.lista_restricciones[k]):
                     peso_total_por_restriccion[k] += problema.lista_restricciones[k][j]
                else:
                     print(f"Advertencia: Datos de restricción faltantes para item {j}, restricción {k}. Asumiendo peso 0.")


    # Verificar factibilidad (si las capacidades se respetan)
    for k in range(problema.cantidad_restricciones):
         # Asegurarse de que hay suficientes datos en lista_capacidades
        if k < len(problema.lista_capacidades):
            if peso_total_por_restriccion[k] > problema.lista_capacidades[k]:
                es_factible = False
                break # Si una restricción falla, la solución no es factible
        else:
             print(f"Advertencia: Datos de capacidad faltantes para restricción {k}. No se puede verificar factibilidad completa.")
             es_factible = False # Considerar no factible si faltan datos
             break


    if not es_factible:
        return 0.0, False # Si no es factible, el valor acumulado no importa para la optimización

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
    mejor_solucion = [0] * n # Empezar con la mochila vacía como la mejor inicial

    # --- Límite de Seguridad para Fuerza Bruta ---
    if n > MAX_N_FUERZA_BRUTA:
        print(f"ADVERTENCIA: n={n} es demasiado grande para fuerza bruta (límite={MAX_N_FUERZA_BRUTA}). Omitiendo problema.")
        return None, 0.0
    # -----------------------------------------

    num_soluciones = 2**n
    print(f"\n--- Resolviendo problema con n={n}, m={problema.cantidad_restricciones} (Óptimo conocido: {problema.optimo}) ---")
    print(f"Evaluando {num_soluciones} posibles soluciones...")
    start_time = time.time()

    # Iterar a través de todos los enteros de 0 a 2^n - 1
    for i in range(num_soluciones):
        # Generar la representación binaria de 'i' como una lista de 0s y 1s de longitud 'n'
        solucion_actual = [int(bit) for bit in format(i, f'0{n}b')]

        # Evaluar la solución actual
        valor_actual, es_factible = evaluar_solucion(solucion_actual, problema)

        # Si es factible y mejora la mejor encontrada hasta ahora
        if es_factible and valor_actual > mejor_valor:
            mejor_valor = valor_actual
            mejor_solucion = solucion_actual
            # print(f"  Nueva mejor solución encontrada: Valor={mejor_valor:.2f}, Sol={mejor_solucion}")


    end_time = time.time()
    tiempo_transcurrido = end_time - start_time
    print(f"Evaluación completa en {tiempo_transcurrido:.4f} segundos.")

    if mejor_solucion is None and n <= MAX_N_FUERZA_BRUTA:
         print("No se encontró ninguna solución factible.")
         mejor_solucion = [0] * n # Devolver mochila vacía si no hay nada factible

    return mejor_solucion, mejor_valor

# --- Script Principal ---
if __name__ == "__main__":
    MAX_N_FUERZA_BRUTA = 30
    lista_problemas = cargarInstancia()

    if lista_problemas:
        print(f"Se cargaron {len(lista_problemas)} instancias del problema.")

        for idx, prob in enumerate(lista_problemas):
            print(f"\n=====================================")
            print(f"Procesando Instancia #{idx+1}")
            print(f"-------------------------------------")
            print("Datos del problema:")
            print(prob.get_data()) # Descomentar si quieres ver todos los datos leídos

            solucion_encontrada, valor_encontrado = resolver_mkp_fuerza_bruta(prob)

            if solucion_encontrada is not None:
                print(f"\nResultados para Instancia #{idx+1}:")
                print(f"  Mejor solución encontrada: {solucion_encontrada}")
                print(f"  Valor de la solución:    {valor_encontrado:.2f}")
                print(f"  Óptimo conocido:         {prob.optimo:.2f}")
                if abs(valor_encontrado - prob.optimo) < 1e-6: # Comparación con tolerancia
                    print("  ¡El valor encontrado coincide con el óptimo conocido!")
                else:
                    diferencia = abs(valor_encontrado - prob.optimo)
                    gap = (diferencia / prob.optimo) * 100 if prob.optimo > 1e-9 else float('inf')
                    print(f"  Diferencia con el óptimo: {diferencia:.2f} ({gap:.2f}%)")
            else:
                 print(f"\nNo se procesó la Instancia #{idx+1} (n > {MAX_N_FUERZA_BRUTA}).")

        print("\n=====================================")
        print("Procesamiento de todas las instancias completado.")