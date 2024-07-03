import random

# Función para crear una matriz vacía con un tamaño dado


def crear_matriz(filas, columnas):
    return [[' ' for _ in range(columnas)] for _ in range(filas)]

# Función para imprimir la matriz con bordes


def imprimir_matriz(matriz):
    filas = len(matriz)
    columnas = len(matriz[0])

    # Imprimir la parte superior del borde
    print('╔' + '═' * (columnas * 2 - 1) + '╗')

    # Imprimir el contenido de la matriz
    for fila in matriz:
        print('║', end='')
        for valor in fila:
            print(f' {valor}', end='')
        print(' ║')

    # Imprimir la parte inferior del borde
    print('╚' + '═' * (columnas * 2 - 1) + '╝')

# Función para colocar obstáculos en la matriz


def colocar_obstaculos(matriz, num_baches, num_caminos_empedrados, num_arboles):
    filas = len(matriz)
    columnas = len(matriz[0])

    # Colocar baches (costo 2)
    for _ in range(num_baches):
        while True:
            fila = random.randint(0, filas - 1)
            columna = random.randint(0, columnas - 1)
            if matriz[fila][columna] == ' ':
                matriz[fila][columna] = '#'
                break

    # Colocar caminos empedrados (costo 1)
    for _ in range(num_caminos_empedrados):
        while True:
            fila = random.randint(0, filas - 1)
            columna = random.randint(0, columnas - 1)
            if matriz[fila][columna] == ' ':
                matriz[fila][columna] = '+'
                break

    # Colocar árboles (impenetrables)
    for _ in range(num_arboles):
        while True:
            try:
                fila = int(
                    input("Ingrese una fila para el árbol (de 0 a {}): ".format(filas - 1)))
                columna = int(
                    input("Ingrese una columna para el árbol (de 0 a {}): ".format(columnas - 1)))
                if 0 <= fila < filas and 0 <= columna < columnas:
                    if matriz[fila][columna] == ' ':
                        matriz[fila][columna] = '&'
                        break
                    else:
                        print("Coordenadas ya ocupadas. Inténtalo de nuevo.")
                else:
                    print("Coordenadas fuera de rango. Inténtalo de nuevo.")
            except ValueError:
                print("Por favor, ingrese números válidos para la fila y columna.")

    return matriz

# Función para colocar puntos de inicio y fin en bordes opuestos


def colocar_puntos_inicio_fin(matriz):
    filas = len(matriz)
    columnas = len(matriz[0])

    while True:
        # Pedir al usuario las coordenadas del punto de partida
        print("\nIngrese las coordenadas del punto de partida:")
        try:
            fila_inicio = int(
                input("Por favor, ingrese la fila del punto de partida: "))
            columna_inicio = int(
                input("Por favor, ingrese la columna del punto de partida: "))
        except ValueError:
            print("Por favor, ingrese números válidos para la fila y columna.")
            continue

        if fila_inicio < 0 or fila_inicio >= filas or columna_inicio < 0 or columna_inicio >= columnas or matriz[fila_inicio][columna_inicio] != ' ':
            print("Coordenadas fuera de rango o ya ocupadas. Inténtelo de nuevo.")
            continue

        # Validar que el punto de partida esté en un borde
        # if fila_inicio != 0 and fila_inicio != filas - 1 and columna_inicio != 0 and columna_inicio != columnas - 1:
        #     print("El punto de partida debe estar en un borde.")
        #     continue

        break

    while True:
        # Pedir al usuario las coordenadas del punto de llegada
        print("\nIngrese las coordenadas del punto de llegada:")
        try:
            fila_fin = int(
                input("Por favor, ingrese la fila del punto de llegada: "))
            columna_fin = int(
                input("Por favor, ingrese la columna del punto de llegada: "))
        except ValueError:
            print("Por favor, ingrese números válidos para la fila y columna.")
            continue

        if fila_fin < 0 or fila_fin >= filas or columna_fin < 0 or columna_fin >= columnas or matriz[fila_fin][columna_fin] != ' ':
            print("Coordenadas fuera de rango o ya ocupadas. Inténtelo de nuevo.")
            continue

        # Validar que el punto de llegada esté en un borde y en el borde opuesto del punto de partida
        # if (fila_inicio == 0 and fila_fin == filas - 1) or (fila_inicio == filas - 1 and fila_fin == 0) or (columna_inicio == 0 and columna_fin == columnas - 1) or (columna_inicio == columnas - 1 and columna_fin == 0):
        matriz[fila_inicio][columna_inicio] = 'S'
        matriz[fila_fin][columna_fin] = 'E'
        break
        # else:
        #     print(
        #         "El punto de llegada debe estar en el borde opuesto al punto de partida.")
        #     continue

    return matriz, (fila_inicio, columna_inicio), (fila_fin, columna_fin)

# Función para verificar la conectividad usando DFS


def verificar_conectividad(matriz, start, end):
    filas = len(matriz)
    columnas = len(matriz[0])
    visitado = [[False] * columnas for _ in range(filas)]

    def dfs(fila, columna):
        if (fila, columna) == end:
            return True
        visitado[fila][columna] = True
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nueva_fila, nueva_columna = fila + dx, columna + dy
            if 0 <= nueva_fila < filas and 0 <= nueva_columna < columnas:
                if not visitado[nueva_fila][nueva_columna] and matriz[nueva_fila][nueva_columna] != '#':
                    if dfs(nueva_fila, nueva_columna):
                        return True
        return False

    return dfs(start[0], start[1])

# Función heurística para A* (distancia Manhattan)


def heuristica(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# Función para el algoritmo A*


def a_star(matriz, start, end):
    filas = len(matriz)
    columnas = len(matriz[0])

    # Movimientos posibles (arriba, abajo, izquierda, derecha)
    movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # Inicializar la lista abierta y la cerrada
    open_set = [(0, start)]
    g_score = {start: 0}
    f_score = {start: heuristica(start, end)}
    came_from = {}

    while open_set:
        # Obtener el nodo con la menor puntuación f
        open_set.sort()
        _, current = open_set.pop(0)

        if current == end:
            # Reconstruir el camino
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path

        for dx, dy in movimientos:
            vecino = (current[0] + dx, current[1] + dy)

            if 0 <= vecino[0] < filas and 0 <= vecino[1] < columnas:
                if matriz[vecino[0]][vecino[1]] != '#':  # No atravesar árboles
                    # Costo del vecino
                    if matriz[vecino[0]][vecino[1]] == 'E':
                        costo_vecino = 0  # Punto de llegada
                    elif matriz[vecino[0]][vecino[1]] == '+':
                        costo_vecino = 2  # Camino empedrado
                    elif matriz[vecino[0]][vecino[1]] == '#':
                        costo_vecino = 3  # Bache
                    else:
                        costo_vecino = 1  # Espacio vacío

                    tentative_g_score = g_score[current] + costo_vecino

                    if vecino not in g_score or tentative_g_score < g_score[vecino]:
                        came_from[vecino] = current
                        g_score[vecino] = tentative_g_score
                        f_score[vecino] = tentative_g_score + \
                            heuristica(vecino, end)
                        if vecino not in [n for _, n in open_set]:
                            open_set.append((f_score[vecino], vecino))

    return None  # No se encontró un camino


# Crear una matriz de ejemplo
filas = 15
columnas = 15
matriz = crear_matriz(filas, columnas)

# Colocar obstáculos aleatorios
matriz = colocar_obstaculos(matriz, num_baches=25,
                            num_caminos_empedrados=30, num_arboles=7)

# Imprimir la matriz con obstáculos
print("Matriz con obstáculos:")
imprimir_matriz(matriz)

# Colocar puntos de partida y llegada
matriz, start, end = colocar_puntos_inicio_fin(matriz)

# Imprimir la matriz resultante
print("Matriz generada:")
imprimir_matriz(matriz)
print(f"Punto de partida: {start}")
print(f"Punto de llegada: {end}")

# Verificar si existe al menos un camino válido usando DFS
if verificar_conectividad(matriz, start, end):
    # Encontrar el camino más corto utilizando A*
    camino = a_star(matriz, start, end)

    # Imprimir el camino encontrado
    if camino:
        print("\nCamino encontrado:")
        matriz_camino = [list(row) for row in matriz]
        for paso in camino[1:-1]:
            matriz_camino[paso[0]][paso[1]] = '*'
        imprimir_matriz(matriz_camino)
    else:
        print("\nNo se encontró un camino válido.")
else:
    print("\nNo hay un camino válido desde el punto de partida al punto de llegada.")
