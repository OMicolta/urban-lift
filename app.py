#app.py
import streamlit as st
from src.simulacion import Simulacion

st.title("UrbanLift - Simulador de transporte")

# Mapa de la ciudad
st.header("Mapa de la ciudad")

# Se asume que la simulación tiene un atributo 'mapa' que contiene la matriz
simulacion = Simulacion("data/mapa-test.json")
matriz_mapa = simulacion.mapa.matriz

# Se crea una nueva matriz para mostrar la información de los nodos y los vehículos
matriz_visualizacion = [[" " for _ in range(len(fila))] for fila in matriz_mapa]

# Mostrar la información de cada nodo y los vehículos
for i in range(len(matriz_mapa)):
    for j in range(len(matriz_mapa[i])):
        nodo = matriz_mapa[i][j]

        # Mostrar el nombre del nodo (si tiene uno)
        if nodo.nombre:
            matriz_visualizacion[i][j] = nodo.nombre

        # Mostrar el sentido de la vía
        if nodo.sentido_via:
            if nodo.sentido_via == "doble":
                matriz_visualizacion[i][j] += " <->"
            elif nodo.sentido_via == "derecha":
                matriz_visualizacion[i][j] += " ->"
            elif nodo.sentido_via == "izquierda":
                matriz_visualizacion[i][j] += " <-"

        # Mostrar la ubicación de los vehículos
        for vehiculo in simulacion.vehiculos:
            if vehiculo.posicion == nodo.id:
                matriz_visualizacion[i][j] += f" V{vehiculo.id}"

# Mostrar la tabla
tabla_mapa = st.table(matriz_visualizacion)

# Panel de solicitud de viaje
st.sidebar.header("Solicitar viaje")
origen_calle = st.sidebar.number_input("Calle de origen")
origen_carrera = st.sidebar.number_input("Carrera de origen")
destino_calle = st.sidebar.number_input("Calle de destino")
destino_carrera = st.sidebar.number_input("Carrera de destino")
tipo_viaje = st.sidebar.selectbox("Tipo de viaje", ["Más corta", "Más rápida", "Menor consumo", "Más económica", "Tour-Trip"])

# Botón para iniciar la simulación
if st.sidebar.button("Iniciar simulación"):
    # Implementar lógica de simulación y mostrar resultados

    # Agregar vehículos a la simulación (opcional)
    # simulacion.agregar_vehiculo(consumo_combustible)

    # Obtener los IDs de los nodos de origen y destino
    origen_id = simulacion.mapa.obtener_id_nodo(origen_calle, origen_carrera)
    destino_id = simulacion.mapa.obtener_id_nodo(destino_calle, destino_carrera)

    # Procesar la solicitud de viaje
    id_vehiculo, costo, distancia, duracion, ruta, otras_rutas = simulacion.procesar_solicitud(
        origen_id, destino_id, tipo_viaje
    )

    # Mostrar los resultados de la simulación
    if id_vehiculo is not None:
        st.header("Información de la simulación")

        # Mostrar mapa con la ruta del viaje
        ruta_coordenadas = [nodo.nombre for nodo in ruta]

        # Mostrar detalles del viaje
        st.write(f"Ruta: {ruta_coordenadas}")
        st.write(f"Vehículo: {id_vehiculo}")
        st.write(f"Costo: {costo}")
        st.write(f"Distancia: {distancia}")
        st.write(f"Duración: {duracion}")

        # Mostrar información adicional según el tipo de viaje
        if tipo_viaje == "Menor consumo":
            # Mostrar la comparación con otras rutas
            st.subheader("Comparación con otras rutas")

            # Se asume que la simulación calcula las otras rutas
            # y las almacena en una lista llamada 'otras_rutas'
            costo = simulacion.calcular_costo(ruta)
            distancia = len(ruta) - 1
            duracion = simulacion.calcular_duracion(ruta)

            st.write(f"Costo: {costo}, Distancia: {distancia}, Duración: {duracion}")

        elif tipo_viaje == "Tour-Trip":
            # Mostrar información sobre los puntos de interés visitados
            st.subheader("Puntos de interés visitados")

            # Se asume que la ruta contiene los puntos de interés visitados
            for nodo in ruta:
                if nodo.punto_interes:
                    st.write(f"- {nodo.punto_interes}")
    else:
        st.error("No hay vehículos disponibles")