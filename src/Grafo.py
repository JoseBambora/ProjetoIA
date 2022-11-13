from Nodo import Nodo
from queue import Queue

class Grafo:
    def __init__(self):
        self.m_nodes = {}
        self.m_graph = {}
        self.m_h = {}
        self.heigth = 0
        self.width = 0
        self.inicialPos = (0,0)
        self.finalPos = []

    def __str__(self):
        out = ""
        for key in self.m_graph.keys():
            out = out + "node " + str(key) + ": " + str(self.m_graph[key]) + "\n"
        for key in self.m_nodes.keys():
            out = out + "node " + str(key) + ": " + str(self.m_nodes[key]) + "\n"
        return out

    # Adiciona a aresta, no modo não direcionado
    def add_aresta(self,coords1,coords2):
        self.m_graph[coords1].append(coords2)
        self.m_graph[coords2].append(coords1)

    # Calcula custo
    def aux_custo(self, char):
        if char == 'X':
            return 25
        else:
            return 1

    # Converte ficheiro em grafo
    def add_info(self, namefile):
        file = open(namefile, "r")
        y = 0
        line = file.readline()
        self.width = len(line)-1
        while line:
            for x in range(0,self.width):
                ch = line.__getitem__(x)
                nodo = Nodo((x, y), (ch, self.aux_custo(ch)))
                if ch == 'P':
                    self.inicialPos = (x ,y)
                if ch == 'F':
                    self.finalPos.append((x,y))
                self.m_nodes[(x, y)] = nodo
                self.m_graph[(x, y)] = []
            y += 1
            line = file.readline()
        self.heigth = y
        file.close()
        for key in self.m_graph.keys():
            x = key[0]
            y = key[1]
            if y+1 < self.heigth:
                self.add_aresta((x, y), (x, y+1))
            if x+1 < self.width:
                self.add_aresta((x, y), (x+1, y))
            if y+1 < self.heigth and x+1 < self.width:
                self.add_aresta((x, y), (x+1, y+1))
            if x+1 < self.width and y-1 >= 0:
                self.m_graph[key].append((x+1, y-1))
            if x-1 >= 0 and y+1 < self.heigth:
                self.m_graph[key].append((x-1, y+1))

    def matrizToString(self, matriz):
        out = ""
        for x in matriz.keys():
            for c in matriz[x]:
                out = out + c
            out = out + "\n"
        return out

    # Devolve o grafo sub a forma de string que representa uma matriz
    def toMatriz(self):
        matriz = {}
        for (x, y) in self.m_graph.keys():
            if not matriz.__contains__(y):
                matriz[y] = []
            matriz[y].append(self.m_nodes[(x, y)].elem[0])
        return self.matrizToString(matriz)

    # Printa o caminho realizado no grafo
    def toMatrizPath(self, path):
        matriz = {}
        for (x, y) in self.m_graph.keys():
            if not matriz.__contains__(y):
                matriz[y] = []
            if (x, y) not in path[0]:
                matriz[y].append(self.m_nodes[(x, y)].elem[0])
            else:
                matriz[y].append(' ')
        return self.matrizToString(matriz)

    # Adiciona a aresta, no modo não direcionado
    def add_aresta(self, coords1, coords2):
        self.m_graph[coords1].append(coords2)
        self.m_graph[coords2].append(coords1)

    # Calcula o custo do caminho encontrado
    def calcula_custo(self, path):
        teste = path
        custo = 0
        i = 0
        while i + 1 < len(path):
            custo = custo + self.m_nodes[teste[i]].elem[1]
            i = i + 1
        return custo

    # Procura em largura
    def procura_BFS(self):
        start = self.inicialPos
        end = self.finalPos
        visited = set()
        fila = Queue()
        visited.add(start)
        fila.put(start)
        parent = dict()
        parent[start] = None
        path_found = False
        finalpos = (0,0)
        while not fila.empty() and path_found == False:
            nodo_atual = fila.get()
            if nodo_atual in end:
                finalpos = nodo_atual
                path_found = True
            else:
                for adjacente in self.m_graph[nodo_atual]:
                    if adjacente not in visited:
                        fila.put(adjacente)
                        parent[adjacente] = nodo_atual
                        visited.add(adjacente)
        path = []
        if path_found:
            path.append(finalpos)
            end = finalpos
            while parent[end] is not None:
                path.append(parent[end])
                end = parent[end]
            path.reverse()
            custo = self.calcula_custo(path)
        return (path, custo)

        # Procura em profundidade
    def procura_DFS_Recursiva(self, start, end, path, visited):
        path.append(start)
        visited.add(start)
        if start in end:
            # calcular o custo do caminho funçao calcula custo.
            custoT = self.calcula_custo(path)
            return path, custoT
        for adjacente in self.m_graph[start]:
            if adjacente not in visited:
                resultado = self.procura_DFS_Recursiva(adjacente, end, path, visited)
                if resultado is not None:
                    return resultado
        path.pop()  # se nao encontra remover o que está no caminho......
        return None

    def procura_DFS(self):
        start = self.inicialPos
        end = self.finalPos
        visited = set()
        return self.procura_DFS_Recursiva(start, end, [], visited)