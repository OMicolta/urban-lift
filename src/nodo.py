#src/nodo.py
class Nodo:
    def __init__(self, id, nombre, sentido_via, es_punto_interes, costo, semaforo, calle, carrera):
        self.id = id
        self.nombre = nombre
        self.sentido_via = sentido_via  # Array de tipo string
        self.es_punto_interes = es_punto_interes
        self.costo = costo
        self.semaforo = semaforo
        self.calle = calle
        self.carrera = carrera
        self.vecinos = []

    def __str__(self):
        # Mostrar el nombre del nodo (si tiene uno)
        if self.nombre:
            return self.nombre

        # Mostrar el sentido de la vía
        if self.sentido_via:
            return ", ".join(self.sentido_via)  # Mostrar los sentidos separados por comas

        # Si no hay información relevante, mostrar un espacio en blanco
        return " "

    def agregar_vecino(self, nodo):
        self.vecinos.append(nodo)

    def __lt__(self, other):
        # Se puede utilizar cualquier criterio para comparar los nodos
        # En este caso, se utiliza el costo acumulado
        return self.costo < other.costo