import matplotlib.pyplot as draw
import networkx as nx
import json


def main():

    with open("metrorrey.json", "r", encoding="utf-8") as f:
        metrorrey = json.load(f)


if __name__ == "__main__":
    main()
