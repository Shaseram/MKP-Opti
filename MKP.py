from Problem import Problem

# Momentaneo - Cambiar?
def generarSoluciones():
    n = 4

    binaryList = []

    for i in range(2**n):
        binaryList.append(format(i, f'0{n}b'))

    print(binaryList) 

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

problemas = cargarInstancia()

problema = problemas[6]

print(problema.get_data())






