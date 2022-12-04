from Grafo import Grafo

l = [1,2,3,4] + [1,2,3,4]
grafo = Grafo()
grafo.add_info("../nossapista")
greedy = grafo.greedy()
# print(greedy)
# print(greedy1)
print(grafo.toMatrizPath(greedy[0],greedy[1],'.'))
# print(grafo.toMatrizPath(greedy[0],greedy[1],'.'))
# print(grafo.toMatriz())
# path1 = grafo.procura_BFS()
# path2 = grafo.procura_DFS()
# print(grafo.toMatrizPath(path1[0],path1[1],'.'))
# print(grafo.toMatrizPath(path1[2],0,'+'))
# print(grafo.toMatrizPath(path2[0],path2[1],'.'))
# print(grafo.toMatrizPath(path2[2],0,'+'))
