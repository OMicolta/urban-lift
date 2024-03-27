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
        # ... (Lógica para agregar vecinos según los sentidos de las calles)

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