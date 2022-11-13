from Grafo import Grafo

grafo = Grafo()
grafo.add_info("../nossapista")
print(grafo.toMatriz())
path1 = grafo.procura_BFS()
path2 = grafo.procura_DFS()
print(grafo.toMatrizPath(path1))
print(grafo.toMatrizPath(path2))
