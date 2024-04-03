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
                for sentido in nodo.sentido_via:
                    if sentido == "arriba":
                        if i > 0:
                            nodo.agregar_vecino(self.matriz[i - 1][j])
                    elif sentido == "abajo":
                        if i < len(self.matriz) - 1:
                            nodo.agregar_vecino(self.matriz[i + 1][j])
                    elif sentido == "izquierda":
                        if j > 0:
                            nodo.agregar_vecino(self.matriz[i][j - 1])
                    elif sentido == "derecha":
                        if j < len(self.matriz[i]) - 1:
                            nodo.agregar_vecino(self.matriz[i][j + 1])

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

        # Verificar si el sentido de la vía permite el movimiento entre los nodos
        if nodo1.calle == nodo2.calle:
            if "derecha" in nodo1.sentido_via and nodo2.carrera > nodo1.carrera:
                return True
            elif "izquierda" in nodo1.sentido_via and nodo2.carrera < nodo1.carrera:
                return True
        elif nodo1.carrera == nodo2.carrera:
            if "abajo" in nodo1.sentido_via and nodo2.calle > nodo1.calle:
                return True
            elif "arriba" in nodo1.sentido_via and nodo2.calle < nodo1.calle:
                return True

        return False  # El sentido de la vía no permite el movimiento
    
    def obtener_id_nodo_por_nombre(self, nombre_nodo):
        for fila in self.matriz:
            for nodo in fila:
                if nodo.nombre == nombre_nodo:
                    return nodo.id
        return None  # Nodo no encontrado
    
    def obtener_coordenadas_nodo(self, id_nodo):
        for i in range(len(self.matriz)):
            for j in range(len(self.matriz[i])):
                nodo = self.matriz[i][j]
                if nodo.id == id_nodo:
                    return nodo.calle, nodo.carrera
        return None  # Nodo no encontrado