class Vehiculo:
    def __init__(self, id, posicion, ocupado, consumo_combustible, capacidad):
        self.id = id
        self.posicion = posicion  # ID del nodo en el que se encuentra el vehículo
        self.ocupado = ocupado
        self.consumo_combustible = consumo_combustible
        self.capacidad = capacidad

    def mover(self, id_nodo_destino):
        self.posicion = id_nodo_destino

    # ... (Otros métodos)