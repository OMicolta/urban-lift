#src/mapa.py
import json
from src.nodo import Nodo

class Mapa:
    def __init__(self):
        self.matriz = []

    def cargar_mapa(self, ruta_json):
        with open(ruta_json) as archivo:
            datos = json.load(archivo)

        # Crear la matriz de nodos
        self.matriz = [[Nodo(nodo_json["id"], nodo_json["nombre"], 
                               nodo_json["sentido_via"], nodo_json["es_punto_interes"], 
                               nodo_json["costo"], nodo_json["semaforo"], 
                               nodo_json["calle"], nodo_json["carrera"]) 
                        for nodo_json in fila] for fila in datos["matriz"]]

        # Agregar vecinos a cada nodo
        for i in range(len(self.matriz)):
            for j in range(len(self.matriz[i])):
                nodo = self.matriz[i][j]

                # Agregar vecinos según el sentido de la vía
                if nodo.sentido_via == "doble":
                    self.agregar_vecinos_doble_sentido(nodo, i, j)
                elif nodo.sentido_via == "derecha":
                    self.agregar_vecinos_derecha(nodo, i, j)
                elif nodo.sentido_via == "izquierda":
                    self.agregar_vecinos_izquierda(nodo, i, j)

    def agregar_vecinos_doble_sentido(self, nodo, i, j):
        # Agregar vecinos de arriba y abajo
        if i > 0:
            nodo.agregar_vecino(self.matriz[i - 1][j])
        if i < len(self.matriz) - 1:
            nodo.agregar_vecino(self.matriz[i + 1][j])

        # Agregar vecinos de la izquierda y derecha
        if j > 0:
            nodo.agregar_vecino(self.matriz[i][j - 1])
        if j < len(self.matriz[i]) - 1:
            nodo.agregar_vecino(self.matriz[i][j + 1])

    def agregar_vecinos_derecha(self, nodo, i, j):
        # Agregar vecino de la derecha
        if j < len(self.matriz[i]) - 1:
            nodo.agregar_vecino(self.matriz[i][j + 1])

        # Agregar vecino de arriba o abajo, dependiendo de la orientación de la calle
        if i % 2 == 0:  # Calle par
            if i > 0:
                nodo.agregar_vecino(self.matriz[i - 1][j])
        else:  # Calle impar
            if i < len(self.matriz) - 1:
                nodo.agregar_vecino(self.matriz[i + 1][j])

    def agregar_vecinos_izquierda(self, nodo, i, j):
        # Agregar vecino de la izquierda
        if j > 0:
            nodo.agregar_vecino(self.matriz[i][j - 1])

        # Agregar vecino de arriba o abajo, dependiendo de la orientación de la calle
        if i % 2 == 0:  # Calle par
            if i < len(self.matriz) - 1:
                nodo.agregar_vecino(self.matriz[i + 1][j])
        else:  # Calle impar
            if i > 0:
                nodo.agregar_vecino(self.matriz[i - 1][j])

    def obtener_nodo(self, id_nodo):
        for fila in self.matriz:
            for nodo in fila:
                if nodo.id == id_nodo:
                    return nodo
        return None  # Nodo no encontrado
    
    def obtener_id_nodo(self, calle, carrera):
        for fila in self.matriz:
            for nodo in fila:
                if nodo.calle == calle and nodo.carrera == carrera:
                    return nodo.id
        return None  # Nodo no encontrado
    
    def estan_conectados(self, nodo1, nodo2):
        # Verificar si los nodos son vecinos en la matriz del mapa
        if abs(nodo1.calle - nodo2.calle) + abs(nodo1.carrera - nodo2.carrera) != 1:
            return False  # Los nodos no son vecinos

        # Verificar el sentido de la vía
        if nodo1.sentido_via == "doble" or nodo2.sentido_via == "doble":
            return True  # La vía es de doble sentido

        # Verificar si el sentido de la vía permite el movimiento entre los nodos
        if nodo1.calle == nodo2.calle:
            if nodo1.sentido_via == "derecha" and nodo2.carrera > nodo1.carrera:
                return True
            elif nodo1.sentido_via == "izquierda" and nodo2.carrera < nodo1.carrera:
                return True
        elif nodo1.carrera == nodo2.carrera:
            if nodo1.sentido_via == "derecha" and nodo2.calle > nodo1.calle:
                return True
            elif nodo1.sentido_via == "izquierda" and nodo2.calle < nodo1.calle:
                return True

        return False  # El sentido de la vía no permite el movimiento