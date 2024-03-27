#algoritmos.py
from collections import deque
from heapq import heappush, heappop

from collections import deque

def bfs(mapa, origen, destino):
    cola = deque([origen])
    visitados = {origen}
    padre = {}

    while cola:
        nodo_actual = cola.popleft()
        if nodo_actual == destino:
            return reconstruir_ruta(padre, destino)

        for vecino in nodo_actual.vecinos:
            # Verificar si el vecino está conectado al nodo actual en el mapa
            if mapa.estan_conectados(nodo_actual, vecino):
                if vecino not in visitados:
                    visitados.add(vecino)
                    padre[vecino] = nodo_actual
                    cola.append(vecino)

    return None  # No se encontró una ruta


def a_estrella(mapa, origen, destino, funcion_costo):
    abierto = []
    heappush(abierto, (0, origen))  # (costo, nodo)
    cerrado = set()
    padre = {}
    costo_acumulado = {origen: 0}

    while abierto:
        _, nodo_actual = heappop(abierto)

        if nodo_actual == destino:
            return reconstruir_ruta(padre, destino)

        cerrado.add(nodo_actual)

        for vecino in nodo_actual.vecinos:
            costo_tentativo = costo_acumulado[nodo_actual] + funcion_costo(nodo_actual, vecino)
            if vecino not in cerrado and (vecino not in costo_acumulado or costo_tentativo < costo_acumulado[vecino]):
                costo_acumulado[vecino] = costo_tentativo
                prioridad = costo_tentativo + funcion_costo(vecino, destino)  # Heurística
                heappush(abierto, (prioridad, vecino))
                padre[vecino] = nodo_actual

    return None  # No se encontró una ruta


def reconstruir_ruta(padre, destino):
    ruta = [destino]
    while destino in padre:
        destino = padre[destino]
        ruta.append(destino)
    ruta.reverse()
    return ruta