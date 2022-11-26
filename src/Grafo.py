from Nodo import Nodo
from queue import Queue
from math import inf
from math import sqrt


class Grafo:
    def __init__(self):
        self.m_nodes = {}
        self.m_graph = {}
        self.m_h = {}
        self.heigth = 0
        self.width = 0
        self.inicialPos = (0, 0)
        self.finalPos = []

    def __str__(self):
        out = ""
        for key in self.m_graph.keys():
            out = out + "node " + str(key) + ": " + str(self.m_graph[key]) + "\n"
        for key in self.m_nodes.keys():
            out = out + "node " + str(key) + ": " + str(self.m_nodes[key]) + "\n"
        return out

    # Adiciona a aresta, no modo não direcionado
    def add_aresta(self, coords1, coords2):
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
        self.width = len(line) - 1
        while line:
            for x in range(0, self.width):
                ch = line.__getitem__(x)
                nodo = Nodo((x, y), (ch, self.aux_custo(ch)))
                if ch == 'P':
                    self.inicialPos = (x, y)
                if ch == 'F':
                    self.finalPos.append((x, y))
                self.m_nodes[(x, y)] = nodo
                self.m_graph[(x, y)] = []
            y += 1
            line = file.readline()
        self.heigth = y
        file.close()
        for key in self.m_graph.keys():
            x = key[0]
            y = key[1]
            if y + 1 < self.heigth:
                self.add_aresta((x, y), (x, y + 1))
            if x + 1 < self.width:
                self.add_aresta((x, y), (x + 1, y))
            if y + 1 < self.heigth and x + 1 < self.width:
                self.add_aresta((x, y), (x + 1, y + 1))
            if x + 1 < self.width and y - 1 >= 0:
                self.m_graph[key].append((x + 1, y - 1))
            if x - 1 >= 0 and y + 1 < self.heigth:
                self.m_graph[key].append((x - 1, y + 1))
        self.define_dis()

    def matrizToString(self, matriz):
        out = ""
        for i in range(self.width + 2):
            out += '_'
        out += '\n'
        for x in matriz.keys():
            out += '|'
            for c in matriz[x]:
                out = out + c
            out = out + "|\n"
        for i in range(self.width + 2):
            out += '_'
        return out

    # Devolve o grafo sub a forma de string que representa uma matriz
    def toMatriz(self):
        matriz = {}
        for (x, y) in self.m_graph.keys():
            if not matriz.__contains__(y):
                matriz[y] = []
            matriz[y].append(self.m_nodes[(x, y)].elem[0])
        return self.matrizToString(matriz)

    def printPath(self, path, num):
        out = "[ "
        i = 0
        for c in path:
            out += str(c) + ' '
            i += 1
            if i % 8 == 0:
                out += '\n  '
                for j in range(num):
                    out += ' '
        return out + ']'

    # Printa o caminho realizado no grafo
    def toMatrizPath(self, path, custo, c):
        matriz = {}
        for (x, y) in self.m_graph.keys():
            if not matriz.__contains__(y):
                matriz[y] = []
            if (x, y) not in path:
                matriz[y].append(self.m_nodes[(x, y)].elem[0])
            else:
                matriz[y].append(c)
        res = self.matrizToString(matriz)
        if(custo != 0):
            res += "\nCusto: " + str(custo) + "\nCaminho: " + self.printPath(path, len('Caminho: '))
        return res
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
        finalpos = (0, 0)
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
        return path, self.calcula_custo(path), visited

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
        x, y = self.procura_DFS_Recursiva(start, end, [], visited)
        return x, y, visited

    def define_dis(self):
        for nodo in self.m_nodes.values():
            dist = inf
            for (x, y) in self.finalPos:
                d = sqrt((x - nodo.coords[0]) ** 2 + (y - nodo.coords[1]) ** 2)
                if dist > d:
                    dist = d
            nodo.heuristica = dist

    def get_ponto(self, pos, velocidade, orientacao):
        p = pos
        for i in range(0, velocidade):
            l = self.m_graph[p]
            for (x, y) in l:
                if (orientacao == 0) and p[0] - 1 == x and p[1] == y:
                    p = (x, y)
                    if x == 0:
                        return p
                    break
                elif orientacao == 1 and p[0] + 1 == x and p[1] == y:
                    p = (x, y)
                    if x == self.width - 1:
                        return p
                    break
                elif orientacao == 2 and p[1] - 1 == y and p[0] == x:
                    p = (x, y)
                    if y == 0:
                        return p
                    break
                elif orientacao == 3 and p[1] + 1 == y and p[0] == x:
                    p = (x, y)
                    if x == self.heigth - 1:
                        return p
                    break
        return p

    # Devolve a set de posições para uma velocidade
    def heuristica_pos(self, pos, velocity):
        la = self.m_graph[pos]
        l = set()
        if velocity > 1:
            for c in la:
                if self.m_nodes[c].heuristica < self.m_nodes[pos].heuristica:
                    aux = self.heuristica_pos(c, velocity - 1)
                    l.update(aux)
        else:
            l.update(la)
        return l

    def get_best(self, set):
        bestPos = (0, 0)
        heu = inf
        for (x, y) in set:
            if heu > self.m_nodes[(x, y)].heuristica:
                bestPos = (x, y)
                heu = self.m_nodes[(x, y)].heuristica
        return bestPos, heu

    def heuristica(self, pos, velocidade):
        if velocidade > 1:
            s1 = self.heuristica_pos(pos, velocidade - 1)
        else:
            s1 = set()
        s2 = self.heuristica_pos(pos, velocidade)
        s3 = self.heuristica_pos(pos, velocidade + 1)
        b1, h1 = self.get_best(s1)
        b2, h2 = self.get_best(s2)
        b3, h3 = self.get_best(s3)
        h = min(h1, h2, h3)
        if h1 == h:
            return b1, -1, velocidade - 1
        elif h2 == h:
            return b2, 0, velocidade
        return b3, 1, velocidade + 1
