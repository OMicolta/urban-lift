#simulacion.py
import json
from src.mapa import Mapa
from src.vehiculo import Vehiculo
from src.algoritmos import bfs, a_estrella

class Simulacion:
    def __init__(self, ruta_mapa):
        self.mapa = Mapa()
        self.mapa.cargar_mapa(ruta_mapa)
        self.vehiculos = []

        # Cargar los vehículos del JSON
        with open(ruta_mapa) as archivo:
            datos = json.load(archivo)
        for vehiculo_json in datos["vehiculos"]:
            self.agregar_vehiculo(vehiculo_json["id"], vehiculo_json["posicion"], 
                                 vehiculo_json["ocupado"], 
                                 vehiculo_json["consumo_combustible"], 
                                 vehiculo_json["capacidad"])

    def agregar_vehiculo(self, id_vehiculo, posicion, ocupado, consumo_combustible, capacidad):
        vehiculo = Vehiculo(id_vehiculo, posicion, ocupado, consumo_combustible, capacidad)
        self.vehiculos.append(vehiculo)

    def procesar_solicitud(self, origen_id, destino_id, tipo_viaje):
        origen = self.mapa.obtener_nodo(origen_id)
        destino = self.mapa.obtener_nodo(destino_id)

        # Encontrar el vehículo desocupado más cercano
        vehiculo = self.encontrar_vehiculo_cercano(origen)

        if vehiculo:
            # Calcular la ruta
            ruta = self.calcular_ruta(origen, destino, tipo_viaje)

             # Verificar si se encontró una ruta
            if ruta is None:
                return None, None, None, None, None, None  # No se encontró una ruta

            # Simular el movimiento del vehículo
            self.simular_movimiento(vehiculo, ruta)

            # Calcular los detalles del viaje
            costo = self.calcular_costo(ruta)
            distancia = len(ruta) - 1
            duracion = self.calcular_duracion(ruta)

            # Calcular otras rutas si es necesario
            otras_rutas = []
            if tipo_viaje == "Menor consumo":
                otras_rutas = self.calcular_otras_rutas(origen, destino)

            return vehiculo.id, costo, distancia, duracion, ruta, otras_rutas
        else:
            return None, None, None, None, None, None

    def encontrar_vehiculo_cercano(self, origen):
        vehiculo_cercano = None
        distancia_minima = float('inf')

        for vehiculo in self.vehiculos:
            if not vehiculo.ocupado:
                distancia = self.calcular_distancia(self.mapa.obtener_nodo(vehiculo.posicion), origen)
                print('distancia', distancia)
                if distancia < distancia_minima:
                    distancia_minima = distancia
                    vehiculo_cercano = vehiculo

        return vehiculo_cercano

    def calcular_distancia(self, nodo1, nodo2):
        # Se puede utilizar la distancia Manhattan o la distancia euclidiana
        return abs(nodo1.calle - nodo2.calle) + abs(nodo1.carrera - nodo2.carrera)

    def calcular_ruta(self, origen, destino, tipo_viaje):
        if tipo_viaje == "Más corta":
            return bfs(self.mapa, origen, destino)
        elif tipo_viaje == "Más rápida":
            return a_estrella(self.mapa, origen, destino, self.costo_tiempo)
        elif tipo_viaje == "Menor consumo":
            return a_estrella(self.mapa, origen, destino, self.costo_combustible)
        elif tipo_viaje == "Más económica":
            return a_estrella(self.mapa, origen, destino, self.costo_economico)
        elif tipo_viaje == "Tour-Trip":
            return self.calcular_ruta_tour_trip()
        else:
            raise ValueError("Tipo de viaje no válido")

    def costo_tiempo(self, nodo_actual, nodo_vecino):
        if nodo_vecino.semaforo:
            return 1 + nodo_vecino.semaforo["duracion"]  # Se suma 1 por el movimiento y la duración del semáforo
        else:
            return 1  # Solo se suma 1 por el movimiento

    def simular_movimiento(self, vehiculo, ruta):
        vehiculo.ocupado = True
        for nodo in ruta:
            vehiculo.mover(nodo.id)
            # ... (Aquí se podría implementar una lógica para visualizar el movimiento en la GUI)
        vehiculo.ocupado = False

    def costo_combustible(self, nodo_actual, nodo_vecino):
        # Se asume que el consumo de combustible es proporcional a la distancia
        return self.calcular_distancia(nodo_actual, nodo_vecino)

    def costo_economico(self, nodo_actual, nodo_vecino):
        costo_tiempo = self.costo_tiempo(nodo_actual, nodo_vecino)
        costo_combustible = self.costo_combustible(nodo_actual, nodo_vecino)
        # Ajustar los pesos según los criterios de UrbanLift
        return 0.7 * costo_tiempo + 0.3 * costo_combustible

    def calcular_ruta_tour_trip(self):
        # Implementar la lógica para calcular la ruta que visita todos los puntos de interés
        # ...
        pass

    def calcular_costo(self, ruta):
        costo_total = 0
        for i in range(1, len(ruta)):
            nodo_actual = ruta[i - 1]
            nodo_siguiente = ruta[i]

            # Se puede implementar una lógica para calcular el costo por tramo
            # considerando la distancia, el tiempo, el consumo de combustible, etc.
            # ...
            distancia = self.calcular_distancia(nodo_actual, nodo_siguiente)
            costo_tramo = distancia * 0.5  # Se asume un costo de 0.5 por unidad de distancia

            costo_total += costo_tramo

        return costo_total

    def calcular_duracion(self, ruta):
        duracion = 0
        for nodo in ruta:
            if nodo.semaforo:
                duracion += nodo.semaforo["duracion"]
            duracion += 1  # Se suma 1 por el movimiento entre nodos
        return duracion

    def calcular_otras_rutas(self, origen, destino):
        # Implementar la lógica para calcular otras rutas
        # ...
        return []  # Devolver una lista vacía por defecto