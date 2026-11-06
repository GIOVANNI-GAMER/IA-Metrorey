import matplotlib.pyplot as draw
import networkx as nx
import json


def main():

    with open("metrorrey.json", "w", encoding="utf-8") as f:
        metrorrey = json.load(metrorrey, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
