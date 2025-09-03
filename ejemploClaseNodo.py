import numpy as np
from copy import deepcopy
from  heapq import heappush, heappop
# ============================
# ESTADO BASE CONSTANTE
# 0 representa casilla vacía
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

class NodoSudoku:
    def __init__(self, tablero, padre=None, costo=0):
        self.tablero = deepcopy(tablero)   # matriz 9x9
        self.padre = padre
        self.costo = costo
        self.f = self.costo + self.heuristica()  # heurística de A*

    def __lt__(self, otroNodo):
        return self.f < otroNodo.f

    def __str__(self):
        return '\n'.join(' '.join(str(x) if x != 0 else '.' for x in fila) for fila in self.tablero)

    def __eq__(self, otroNodo):
        return np.array_equal(self.tablero, otroNodo.tablero)

    def heuristica(self):
        """Heurística: número de casillas vacías"""
        return np.sum(self.tablero == 0)

    def esMeta(self):
        """Verifica si el tablero está completo y válido"""
        return self.heuristica() == 0 and self.esValido()

    def esValido(self):
        """Chequea reglas de Sudoku"""
        for i in range(9):
            fila = [n for n in self.tablero[i, :] if n != 0]
            if len(fila) != len(set(fila)): return False

            col = [n for n in self.tablero[:, i] if n != 0]
            if len(col) != len(set(col)): return False

        # Subcuadros 3x3
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                sub = [n for n in self.tablero[i:i+3, j:j+3].flatten() if n != 0]
                if len(sub) != len(set(sub)): return False

        return True

    def sucesores(self, ABIERTOS, CERRADOS):
        """Genera sucesores llenando la primera casilla vacía encontrada"""
        listaSucesores = []
        for i in range(9):
            for j in range(9):
                if self.tablero[i, j] == 0:  # celda vacía
                    for num in range(1, 10):
                        nuevoTablero = deepcopy(self.tablero)
                        nuevoTablero[i, j] = num
                        nuevoNodo = NodoSudoku(nuevoTablero, self, self.costo + 1)
                        if nuevoNodo.esValido() and nuevoNodo not in ABIERTOS and nuevoNodo not in CERRADOS:
                            listaSucesores.append(nuevoNodo)
                    return listaSucesores
        return listaSucesores


# ================================
# Crear el nodo inicial del juego
# ================================
nodo_inicial = NodoSudoku(ESTADO_BASE)

print("Estado base inicial:")
print(nodo_inicial)

