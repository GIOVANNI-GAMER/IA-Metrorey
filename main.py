import matplotlib.pyplot as plt
import networkx as nx
import json


COLORES = {"amarillo": "#F2B705", "verde": "#2E9E4F", "rojo": "#D62828"}


def dibujar_grafo(G: nx.Graph, metrorrey: dict) -> None:
    # Posición real de cada nodo: x = longitud, y = latitud
    pos = {nodo: (G.nodes[nodo]["lon"], G.nodes[nodo]["lat"]) for nodo in G.nodes}

    # Color de cada línea según el JSON ("L1" -> amarillo, ...)
    color_linea = {
        nombre: COLORES[datos["color"]] for nombre, datos in metrorrey["lineas"].items()
    }

    # Separamos aristas de tramo (misma línea) y de transbordo (distinta línea)
    tramos = [(a, b) for a, b in G.edges if a[1] == b[1]]
    transbordos = [(a, b) for a, b in G.edges if a[1] != b[1]]

    # Etiqueta = nombre de la estación, una sola vez por estación
    # (los dos nodos de un transbordo están en el mismo punto)
    etiquetas = {}
    for nodo in G.nodes:
        if nodo[0] not in etiquetas.values():
            etiquetas[nodo] = nodo[0]

    fig, ax = plt.subplots(figsize=(12, 9))
    nx.draw_networkx_edges(
        G, pos, edgelist=tramos, width=4,
        edge_color=[color_linea[a[1]] for a, b in tramos], ax=ax,
    )
    nx.draw_networkx_edges(
        G, pos, edgelist=transbordos, width=2, style="dashed", edge_color="gray", ax=ax,
    )
    nx.draw_networkx_nodes(
        G, pos, node_size=60, node_color="white", edgecolors="black", ax=ax,
    )
    nx.draw_networkx_labels(
        G, pos, labels=etiquetas, font_size=7,
        verticalalignment="bottom", ax=ax,
    )

    ax.set_title("Metrorrey: líneas 1, 2 y 3")
    ax.set_aspect("equal")  # para que el mapa no salga deformado
    ax.axis("off")
    plt.tight_layout()
    plt.show()


def main():

    with open("metrorrey.json", "r", encoding="utf-8") as f:
        metrorrey: dict = json.load(f)

    G: nx.Graph = nx.Graph()

    # Este bucle crea la esttructura de cada linea
    for nombre_linea, datos_linea in metrorrey["lineas"].items():
        for tramo in datos_linea["tramos"]:
            origen = (tramo["desde"], nombre_linea)
            destino = (tramo["hasta"], nombre_linea)
            G.add_edge(origen, destino, tiempo=tramo["minutos"])

    # Este bucle une cada linea por los trasbordos
    for transbordo in metrorrey["transbordos"]:
        linea_a, linea_b = transbordo["lineas"]
        estacion = transbordo["estacion"]
        G.add_edge((estacion, linea_a), (estacion, linea_b), tiempo=transbordo["minutos"])

    # Este bucle le pasa a cada nodo sus coordenadas para calcular h(n)
    for nodo in G.nodes:
        nombre_estacion = nodo[0]
        coords = metrorrey["coordenadas"][nombre_estacion]
        G.nodes[nodo]["lat"] = coords["lat"]
        G.nodes[nodo]["lon"] = coords["lon"]

    dibujar_grafo(G, metrorrey)


if __name__ == "__main__":
    main()
