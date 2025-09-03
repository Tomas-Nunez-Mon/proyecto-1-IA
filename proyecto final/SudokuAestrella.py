import numpy as np
from copy import deepcopy
from heapq import heappush, heappop

# ============================
# ESTADO BASE CONSTANTE
# ============================
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

# ============================
# CLASE NODO SUDOKU
# ============================
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

# ============================
# FUNCIONES A*
# ============================
def ingresaLista(lista, nodo):
    heappush(lista, nodo)
    return lista

def Solucion(nodo, inicial):
    solucion = []
    while nodo is not inicial:
        solucion = [str(nodo)] + solucion
        nodo = nodo.padre
    return [str(inicial)] + solucion

def Aestrella(nodoInicial, MAX=5000):
    ABIERTOS = []
    heappush(ABIERTOS, nodoInicial)
    CERRADOS = []
    éxito = False
    fracaso = False
    cont = 0
    while not éxito and not fracaso and cont <= MAX:
        nodoActual = heappop(ABIERTOS)
        CERRADOS.append(nodoActual)

        if nodoActual.esMeta():
            éxito = True
        else:
            listaSucesores = nodoActual.sucesores(ABIERTOS, CERRADOS)
            for nodo in listaSucesores:
                heappush(ABIERTOS, nodo)
            if ABIERTOS == []:
                fracaso = True
        cont += 1

    if éxito:
        return Solucion(nodoActual, nodoInicial), cont
    else:
        return None, cont

# ============================
# EJECUCIÓN PRINCIPAL
# ============================

inicial = NodoSudoku(ESTADO_BASE)  # nodo raíz
MAX = 10000

respuesta, nodosRevisados = Aestrella(inicial, MAX)

if respuesta is None:
    print(f"Cantidad de nodos revisados: {nodosRevisados} nodos")
    print("No se encontró solución")
else:
    print(f"Cantidad de nodos revisados: {nodosRevisados} nodos")
    for nodo in respuesta:
        print(f"\n{nodo}")
