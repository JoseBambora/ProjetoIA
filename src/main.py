from Grafo import Grafo
import threading

grafo = Grafo()
grafo.add_info("../nossapista")

greedy = grafo.greedy()
a_star = grafo.a_star()
menor = grafo.custoUniforme()
bfs = grafo.procura_BFS()
dfs = grafo.procura_DFS()

# grafo.draw_turtle(greedy[0],"Procura Gulosa")
# grafo.draw_turtle(a_star[0],"Procura A Estela")
# grafo.draw_turtle(menor[0], "Procura Uniforme")
# grafo.draw_turtle(bfs[0],   "Procura Largura")
grafo.draw_turtle(dfs[0],   "Procura Profundidade")


# print(grafo.toMatrizPath(greedy[0],greedy[1],'.'))
# print(grafo.toMatriz())
# path1 = grafo.procura_BFS()
# path2 = grafo.procura_DFS()
# print(grafo.toMatrizPath(path1[0],path1[1],'.'))
# print(grafo.toMatrizPath(path1[2],0,'+'))
# print(grafo.toMatrizPath(path2[0],path2[1],'.'))
# print(grafo.toMatrizPath(path2[2],0,'+'))


# print(grafo.toMatrizPath(greedy[0],greedy[1],'.'))
# print(grafo.toMatriz())
# path1 = grafo.procura_BFS()
# path2 = grafo.procura_DFS()
# print(grafo.toMatrizPath(path1[0],path1[1],'.'))
# print(grafo.toMatrizPath(path1[2],0,'+'))
# print(grafo.toMatrizPath(path2[0],path2[1],'.'))
# print(grafo.toMatrizPath(path2[2],0,'+'))
