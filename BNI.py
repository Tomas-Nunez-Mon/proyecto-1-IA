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

class NodoSudoku:
    def __init__(self, tablero, padre=None, costo=0):
        self.tablero = deepcopy(tablero)
        self.padre = padre
        self.costo = costo
        self.f = self.costo + self.heuristica()

    def __lt__(self, otroNodo):
        return self.f < otroNodo.f

    def __str__(self):
        return '\n'.join(' '.join(str(x) if x != 0 else '.' for x in fila) for fila in self.tablero)

    def __eq__(self, otroNodo):
        return np.array_equal(self.tablero, otroNodo.tablero)

    def heuristica(self):
        return np.sum(self.tablero == 0)

    def esMeta(self):
        return self.heuristica() == 0 and self.esValido()

    def esValido(self):
        for i in range(9):
            fila = [n for n in self.tablero[i, :] if n != 0]
            if len(fila) != len(set(fila)): return False
            col = [n for n in self.tablero[:, i] if n != 0]
            if len(col) != len(set(col)): return False
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                sub = [n for n in self.tablero[i:i+3, j:j+3].flatten() if n != 0]
                if len(sub) != len(set(sub)): return False
        return True

    def sucesores(self, ABIERTOS, CERRADOS):
        listaSucesores = []
        for i in range(9):
            for j in range(9):
                if self.tablero[i, j] == 0:
                    for num in range(1, 10):
                        nuevoTablero = deepcopy(self.tablero)
                        nuevoTablero[i, j] = num
                        nuevoNodo = NodoSudoku(nuevoTablero, self, self.costo + 1)
                        if nuevoNodo.esValido() and nuevoNodo not in ABIERTOS and nuevoNodo not in CERRADOS:
                            listaSucesores.append(nuevoNodo)
                    return listaSucesores
        return listaSucesores
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
esquema = "DFS"
respuesta, nodosRevisados = busquedaNoInformada(inicial, esquema)
if respuesta is None:
    print("No se encontró solución")
else:
    print(f"Cantidad de nodos revisados: {nodosRevisados} nodos")
    print(f"\nSolución encontrada por {esquema}: ")
    for nodo in respuesta:
        print(f"\n{nodo}")