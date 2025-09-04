import numpy as np
from  heapq import heappush, heappop
from copy import deepcopy

ESTADO_BASE = np.array([
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
])

from numpy import array, copy, zeros, array_equal

class NodoSudoku:
    def __init__(self, tablero, padre=None, costo=0):
        self.tablero = copy(tablero)   # Estado actual (9x9)
        self.padre = padre             # Nodo padre
        self.costo = costo             # Profundidad / pasos (rellenos de celdas)

    def __lt__(self, otroNodo):
        return self.costo < otroNodo.costo  # BFS usa costo como nivel

    def __str__(self):
        return '\n'.join(' '.join(str(x) if x != 0 else '.' for x in fila) for fila in self.tablero)

    def __eq__(self, otroNodo):
        return array_equal(self.tablero, otroNodo.tablero)

    def es_valido(self, fila, col, num):
        """ Verifica si se puede colocar 'num' en (fila, col) según reglas de Sudoku """
        # Verificar fila
        if num in self.tablero[fila]:
            return False
        # Verificar columna
        if num in self.tablero[:, col]:
            return False
        # Verificar subcuadro 3x3
        start_row, start_col = (fila // 3) * 3, (col // 3) * 3
        if num in self.tablero[start_row:start_row+3, start_col:start_col+3]:
            return False
        return True

    def aplicaRegla(self, fila, col, num):
        """Genera un nuevo nodo colocando num en la posición vacía (fila, col)"""
        sucesor = NodoSudoku(self.tablero, self, self.costo + 1)
        sucesor.tablero[fila, col] = num
        return sucesor

    def sucesores(self, ABIERTOS, CERRADOS):
        listaSucesores = []
        # Buscar la primera celda vacía (0)
        vacias = [(i, j) for i in range(9) for j in range(9) if self.tablero[i, j] == 0]
        if not vacias:
            return listaSucesores  # No hay sucesores si no hay celdas vacías

        fila, col = vacias[0]  # Tomamos la primera celda vacía
        for num in range(1, 10):
            if self.es_valido(fila, col, num):
                sucesor = self.aplicaRegla(fila, col, num)
                if sucesor not in ABIERTOS and sucesor not in CERRADOS:
                    listaSucesores.append(sucesor)
        return listaSucesores

    def esMeta(self):
        """Verifica si el tablero está completo y válido"""
        # Si todavía hay ceros → no es solución
        if (self.tablero == 0).any():
            return False
        # Revisar filas y columnas
        for i in range(9):
            if len(set(self.tablero[i])) != 9:   # Fila con repetidos
                return False
            if len(set(self.tablero[:, i])) != 9:  # Columna con repetidos
                return False
        # Revisar subcuadros 3x3
        for r in range(0, 9, 3):
            for c in range(0, 9, 3):
                bloque = self.tablero[r:r+3, c:c+3].flatten()
                if len(set(bloque)) != 9:
                    return False
        return True

# ------------fin clase nodo ------------------------

def ingresaLista(lista, nodo, esquema):
    if esquema == "BFS":
        lista.append(nodo)    #BFS: Ingreso al final
    if esquema == "DFS":
        lista.insert(0, nodo)    #DFS: Ingreso al inicio
    if esquema == "UCS":
        heappush(lista, nodo)
    return lista

def Solucion(nodo, inicial):
    solucion = []
    while nodo is not inicial:
        solucion = [str(nodo)] + solucion
        nodo = nodo.padre
    return [str(inicial)] + solucion

def busquedaNoInformada(nodoInicial, esquema):
    ABIERTOS = [nodoInicial]
    CERRADOS = []
    exito = False
    fracaso = False
    cont = 0
    while not exito and not fracaso:
        cont += 1
        #print(f"cont: {cont}")
        if esquema == "UCS":
            nodoActual = heappop(ABIERTOS)
        else:
            nodoActual = ABIERTOS.pop(0)
        #print("\nNodo actual: ")
        #print(nodoActual)

        CERRADOS.append(nodoActual)
        if nodoActual.esMeta():
            exito = True
        else:
            listaSucesores = nodoActual.sucesores(ABIERTOS, CERRADOS)
            for nodo in listaSucesores:
                ABIERTOS = ingresaLista(ABIERTOS, nodo, esquema)
            if ABIERTOS == []:
                fracaso = True
    if exito:
        return Solucion(nodoActual, inicial), len(CERRADOS)
    else:
        return None

#---- BLOQUE PRINCIPAL:
# Cambiar el esquema por "BFS", "DFS", "UCS"
inicial = NodoSudoku(ESTADO_BASE) 
MAX = 10000
esquema = "BFS"
respuesta, nodosRevisados = busquedaNoInformada(inicial, esquema)
if respuesta is None:
    print("No se encontró solución")
else:
    print(f"Cantidad de nodos revisados: {nodosRevisados} nodos")
    print(f"\nSolución encontrada por {esquema}: ")
    for nodo in respuesta:
        print(f"\n{nodo}")