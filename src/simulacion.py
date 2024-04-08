#src/simulacion.py
import json
import random
import time
from src.mapa import Mapa
from src.vehiculo import Vehiculo
from src.algoritmos import bfs, a_estrella, dfs

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
            ruta = self.calcular_ruta(origen, destino, tipo_viaje, vehiculo)

             # Verificar si se encontró una ruta
            if ruta is None:
                return None, None, None, None, None, None  # No se encontró una ruta

            # Simular el movimiento del vehículo
            #self.simular_movimiento(vehiculo, ruta)

            # Calcular los detalles del viaje
            costo = self.calcular_costo(ruta)
            distancia = len(ruta) - 1
            duracion = self.calcular_duracion(ruta)

            # Calcular otras rutas si es necesario
            otras_rutas = []
            if tipo_viaje == "Menor consumo":
                otras_rutas = self.calcular_otras_rutas(origen, destino, ruta, vehiculo)

            return vehiculo.id, costo, distancia, duracion, ruta, otras_rutas
        else:
            return None, None, None, None, None, None

    def encontrar_vehiculo_cercano(self, origen):
        vehiculo_cercano = None
        distancia_minima = float('inf')

        for vehiculo in self.vehiculos:
            if not vehiculo.ocupado:
                distancia = self.calcular_distancia(self.mapa.obtener_nodo(vehiculo.posicion), origen)
                if distancia < distancia_minima:
                    distancia_minima = distancia
                    vehiculo_cercano = vehiculo

        return vehiculo_cercano

    def calcular_distancia(self, nodo1, nodo2):
        # Distancia Manhattan
        return abs(nodo1.calle - nodo2.calle) + abs(nodo1.carrera - nodo2.carrera)

    def calcular_ruta(self, origen, destino, tipo_viaje, vehiculo):
        if tipo_viaje == "Más corta":
            return bfs(self.mapa, origen, destino)
        elif tipo_viaje == "Más rápida":
            return a_estrella(self.mapa, origen, destino, self.costo_tiempo)
        elif tipo_viaje == "Menor consumo":
            def funcion_costo_combustible(nodo_actual, nodo_vecino):
                return self.costo_combustible(nodo_actual, nodo_vecino, vehiculo) 
            return a_estrella(self.mapa, origen, destino, funcion_costo_combustible)
        elif tipo_viaje == "Más económica":
            return a_estrella(self.mapa, origen, destino, lambda nodo_actual, nodo_vecino: self.costo_economico(nodo_actual, nodo_vecino, vehiculo))
        elif tipo_viaje == "Tour-Trip":
            return self.calcular_ruta_tour_trip()
        else:
            raise ValueError("Tipo de viaje no válido")

    def costo_tiempo(self, nodo_actual, nodo_vecino):
        if nodo_vecino.semaforo:
            return 1 + nodo_vecino.semaforo["duracion"]  # Se suma 1 por el movimiento y la duración del semáforo
        else:
            return 1  # Solo se suma 1 por el movimiento

    def simular_movimiento(self, vehiculo, ruta, mapa_contenedor, matriz_visualizacion): 
        vehiculo.ocupado = True
        for nodo in ruta:
            # Obtener las coordenadas del nodo actual
            i_actual, j_actual = self.mapa.obtener_coordenadas_nodo(vehiculo.posicion)

            # Mover el vehículo al siguiente nodo
            vehiculo.mover(nodo.id)
            
            # Obtener las coordenadas del siguiente nodo
            i_siguiente, j_siguiente = self.mapa.obtener_coordenadas_nodo(nodo.id)

            # Actualizar la matriz de visualización
            matriz_visualizacion[i_actual][j_actual] = matriz_visualizacion[i_actual][j_actual].replace(f" 🚓V{vehiculo.id}", "")  # Eliminar solo el vehículo
            matriz_visualizacion[i_siguiente][j_siguiente] += f" 🚓V{vehiculo.id}"  # Agregar el vehículo al siguiente nodo

            # Actualizar la tabla en la GUI
            mapa_contenedor.table(matriz_visualizacion)

            # Pausa para la visualización 
            time.sleep(0.8) 

        vehiculo.ocupado = False

    def costo_combustible(self, nodo_actual, nodo_vecino, vehiculo):
        # Obtener la eficiencia del combustible del vehículo
        eficiencia_combustible = vehiculo.consumo_combustible

        # Calcular la distancia entre los nodos
        distancia = self.calcular_distancia(nodo_actual, nodo_vecino)

        # Calcular el consumo de combustible
        consumo_combustible = distancia / eficiencia_combustible
        
        return consumo_combustible

    def costo_economico(self, nodo_actual, nodo_vecino, vehiculo):
        costo_tiempo = self.costo_tiempo(nodo_actual, nodo_vecino)
        costo_combustible = self.costo_combustible(nodo_actual, nodo_vecino, vehiculo)
        # Ajustar los pesos según los criterios de UrbanLift
        return 0.7 * costo_tiempo + 0.3 * costo_combustible

    def calcular_ruta_tour_trip(self):
        # Obtener la lista de puntos de interés
        puntos_interes = [nodo for fila in self.mapa.matriz for nodo in fila if nodo.es_punto_interes]

        # Si no hay puntos de interés, devolver None
        if not puntos_interes:
            return None

        # Función para verificar si todos los puntos de interés han sido visitados
        def todos_visitados(visitados):
            for punto in puntos_interes:
                if punto not in visitados:
                    return False
            return True

        # Iniciar la búsqueda desde el primer punto de interés
        ruta = dfs(self.mapa, puntos_interes[0], todos_visitados) 

        # Si se encontró una ruta, agregar el punto de origen al final
        if ruta:
            ruta.append(puntos_interes[0])

        return ruta

    def calcular_costo(self, ruta):
        costo_total = 0
        for i in range(1, len(ruta)):
            nodo_actual = ruta[i - 1]
            nodo_siguiente = ruta[i]

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

    def calcular_otras_rutas(self, origen, destino, ruta_menor_consumo, vehiculo):
        otras_rutas = []

        # Calcular algunas rutas alternativas
        for _ in range(3):  # Calcular 3 rutas alternativas
            # Modificar la función de costo para explorar diferentes rutas
            funcion_costo_modificada = lambda nodo_actual, nodo_vecino, vehiculo=vehiculo: self.costo_combustible(nodo_actual, nodo_vecino, vehiculo) * random.uniform(0.8, 1.2)  # Se pasa el vehículo como argumento por defecto

            ruta_alternativa = a_estrella(self.mapa, origen, destino, funcion_costo_modificada)

            # Verificar que la ruta alternativa sea diferente a la ruta principal
            if ruta_alternativa is not None and ruta_alternativa not in otras_rutas and ruta_alternativa != ruta_menor_consumo:
                otras_rutas.append(ruta_alternativa)

        return otras_rutas