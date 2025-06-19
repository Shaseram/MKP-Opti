import os

def reformat_mkp_instance(input_file_path, output_file_path):
    """
    Lee una instancia del Multidimensional Knapsack Problem mal formateada,
    la procesa y la escribe en un nuevo archivo con el formato correcto.

    Args:
        input_file_path (str): La ruta al archivo de entrada mal formateado.
        output_file_path (str): La ruta donde se guardará el archivo formateado.
    """
    try:
        with open(input_file_path, 'r') as f_in:
            lines = f_in.readlines()
    except FileNotFoundError:
        print(f"Error: El archivo de entrada '{input_file_path}' no fue encontrado.")
        return

    # 1. Procesar la primera línea para obtener los parámetros
    # Elimina espacios en blanco al inicio/final y divide la línea
    first_line_parts = lines[0].strip().split()
    if len(first_line_parts) < 2:
        print("Error: La primera línea del archivo no tiene el formato esperado (n_objetos n_dimensiones ...)")
        return
        
    num_items = int(first_line_parts[0])
    num_dimensions = int(first_line_parts[1])
    # Guardamos la primera línea original para escribirla tal cual
    original_first_line = lines[0].strip()

    # 2. Unificar todos los demás números en una sola lista
    # Une todas las líneas restantes en una sola cadena, luego divide por espacios
    all_numbers_str = " ".join(line.strip() for line in lines[1:])
    all_numbers = [int(num) for num in all_numbers_str.split()]

    # 3. Seccionar la lista de números en sus partes correspondientes
    
    # Puntero para saber por dónde vamos en la lista 'all_numbers'
    current_pos = 0

    # Los primeros 'num_items' son los valores/beneficios
    values = all_numbers[current_pos : current_pos + num_items]
    current_pos += num_items

    # Los siguientes 'num_dimensions' bloques de 'num_items' son los pesos
    weights = []
    for _ in range(num_dimensions):
        dimension_weights = all_numbers[current_pos : current_pos + num_items]
        weights.append(dimension_weights)
        current_pos += num_items

    # Los últimos 'num_dimensions' números son las capacidades
    capacities = all_numbers[current_pos : current_pos + num_dimensions]

    # 4. Escribir los datos en el archivo de salida con el formato correcto
    with open(output_file_path, 'w') as f_out:
        # Escribir la primera línea (n_objetos, n_dimensiones, optimo)
        f_out.write(original_first_line + '\n')

        # Escribir la línea de valores
        f_out.write(" ".join(map(str, values)) + '\n')

        # Escribir las líneas de pesos para cada dimensión
        for dim_weights in weights:
            f_out.write(" ".join(map(str, dim_weights)) + '\n')

        # Escribir la línea de capacidades
        f_out.write(" ".join(map(str, capacities)) + '\n')

    print(f"¡Proceso completado! El archivo formateado ha sido guardado en '{output_file_path}'")

input_filename = "mknapcb9.txt"
output_filename = "InstanciaMKP_actual_9.txt"

# 3. Llama a la función para que haga la conversión.
reformat_mkp_instance(input_filename, output_filename)