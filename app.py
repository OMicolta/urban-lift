#app.py
import streamlit as st
from src.simulacion import Simulacion

st.title("UrbanLift - Simulador de transporte")

# Mapa de la ciudad
st.header("Mapa de la ciudad")

# Se carga el mapa del JSON
simulacion = Simulacion("data/mapa.json")
matriz_mapa = simulacion.mapa.matriz

# Se crea una nueva matriz para dibujar el mapa
matriz_visualizacion = [[" " for _ in range(len(fila))] for fila in matriz_mapa]

# Mostrar la información de cada nodo y los vehículos
for i in range(len(matriz_mapa)):
    for j in range(len(matriz_mapa[i])):
        nodo = matriz_mapa[i][j]

        # Marcar puntos de interés
        if nodo.es_punto_interes:
            matriz_visualizacion[i][j] = "🕍"

        # Mostrar el nombre del lugar
        if nodo.nombre:
            matriz_visualizacion[i][j] += nodo.nombre

        # Mostrar el sentido de la vía con emojis
        if nodo.sentido_via:
            sentidos_str = ""
            for sentido in nodo.sentido_via:
                if sentido == "arriba":
                    sentidos_str += "⬆️"
                elif sentido == "abajo":
                    sentidos_str += "⬇️"
                elif sentido == "izquierda":
                    sentidos_str += "⬅️"
                elif sentido == "derecha":
                    sentidos_str += "➡️"
            matriz_visualizacion[i][j] += f" {sentidos_str}"

        # Mostrar el semáforo con emojis si lo hay
        if nodo.semaforo:
            if nodo.semaforo is not None:
                matriz_visualizacion[i][j] += f" 🚦"

        # Mostrar el carro con emoji si lo hay
        for vehiculo in simulacion.vehiculos:
            if vehiculo.posicion == nodo.id:
                if vehiculo.ocupado:
                    matriz_visualizacion[i][j] += f" 🚗V{vehiculo.id}"
                else:
                    matriz_visualizacion[i][j] += f" 🚓V{vehiculo.id}"
        

# Mostrar la matrix
tabla_mapa = st.table(matriz_visualizacion)

# Panel de solicitud de viaje
st.sidebar.header("Solicitar viaje")

# Obtener la lista de nombres de lugares
nombres_nodos = [nodo.nombre for fila in simulacion.mapa.matriz for nodo in fila if nodo.nombre]

# Selectbox para el lugar de origen
lugar_origen = st.sidebar.selectbox("Lugar de origen", nombres_nodos)

# Selectbox para el lugar de destino
lugar_destino = st.sidebar.selectbox("Lugar de destino", nombres_nodos)

# Tipo de recorrido
tipo_viaje = st.sidebar.selectbox("Tipo de viaje", ["Más corta", "Más rápida", "Menor consumo", "Más económica", "Tour-Trip"])

# Botón para iniciar la simulación
if st.sidebar.button("Iniciar simulación"):
   
    # Obtener los IDs de los nodos de origen y destino
    origen_id = simulacion.mapa.obtener_id_nodo_por_nombre(lugar_origen)
    destino_id = simulacion.mapa.obtener_id_nodo_por_nombre(lugar_destino)

    # Procesar la solicitud de viaje
    id_vehiculo, costo, distancia, duracion, ruta, otras_rutas = simulacion.procesar_solicitud(
        origen_id, destino_id, tipo_viaje
    )

    # Mostrar los resultados de la simulación
    if id_vehiculo is not None:
        st.header("Información de la simulación")

        # Contenedor para la tabla del mapa
        mapa_contenedor = st.empty()

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

            # Se calculan rutas alternativas
            for ruta in otras_rutas:
                costo = simulacion.calcular_costo(ruta)
                distancia = len(ruta) - 1
                duracion = simulacion.calcular_duracion(ruta)
                ruta_secuencia = [nodo.nombre for nodo in ruta]

                st.write(f"Ruta: {ruta_secuencia}")
                st.write(f"Costo: {costo}, Distancia: {distancia}, Duración: {duracion}")

        elif tipo_viaje == "Tour-Trip":
            # Mostrar información sobre los puntos de interés visitados
            st.subheader("Puntos de interés visitados")

            for nodo in ruta:
                if nodo.es_punto_interes:
                    st.write(f"- {nodo.nombre}")

        # Simular el movimiento del vehículo
        for vehiculo in simulacion.vehiculos:
            if vehiculo.id == id_vehiculo:
                simulacion.simular_movimiento(vehiculo, ruta, mapa_contenedor, matriz_visualizacion)
                break 
    else:
        st.error("No hay vehículos disponibles")