import turtle

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
        if (custo != 0):
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

    def procura_DFS_Recursiva(self, start, end, visited):
        visited.add(start)
        if start in end:
            path = [start]
            custoT = self.m_nodes[start].elem[1]
            return path, custoT
        for adjacente in self.m_graph[start]:
            if adjacente not in visited:
                resultado = self.procura_DFS_Recursiva(adjacente, end, visited)
                if resultado is not None:
                    if start == self.inicialPos:
                        return [start] + resultado[0], self.calcula_custo([start] + resultado[0])
                    else:
                        return [start] + resultado[0], 0
        return None

    # Procura em profundidade
    def procura_DFS(self):
        start = self.inicialPos
        end = self.finalPos
        visited = set()
        x, y = self.procura_DFS_Recursiva(start, end, visited)
        return x, y, visited

    def procura_iterativa_Recursiva(self, start, end, visited, iteracoes):
        visited.add(start)
        if start in end:
            path = [start]
            custoT = self.m_nodes[start].elem[1]
            return path, custoT
        if iteracoes == 0:
            return None
        for adjacente in self.m_graph[start]:
            if adjacente not in visited:
                resultado = self.procura_iterativa_Recursiva(adjacente, end, visited, iteracoes - 1)
                if resultado is not None:
                    if start == self.inicialPos:
                        return [start] + resultado[0], self.calcula_custo([start] + resultado[0])
                    else:
                        return [start] + resultado[0], 0
        return None

    # Procura em profundidade
    def procura_iterativa(self, iteracoes):
        start = self.inicialPos
        end = self.finalPos
        visited = set()
        c = self.procura_iterativa_Recursiva(start, end, visited, iteracoes)
        if c is None:
            return c
        return c[0], c[1], visited

    def bidirectional(self):
        start = self.inicialPos
        end = self.finalPos
        visited1 = []
        visited2 = []
        fila1 = []
        fila2 = []
        fila1.append(start)
        for c in end:
            fila2.append(c)
        path_found = False
        parent1 = dict()
        parent2 = dict()
        finalpos = (0, 0)
        while len(fila1) > 0 and len(fila2) > 0 and not path_found:
            c1 = fila1.pop()
            c2 = fila2.pop()
            if c2 in visited1:
                finalpos = c2
                path_found = True
            elif c1 in visited2:
                finalpos = c1
                path_found = True
            else:
                for adjacente in self.m_graph[c1]:
                    if adjacente not in visited1 and adjacente not in visited2:
                        fila1.append(adjacente)
                        parent1[adjacente] = c1
                        visited1.append(adjacente)
                for adjacente in self.m_graph[c2]:
                    if adjacente not in visited1 and adjacente not in visited2:
                        fila2.append(adjacente)
                        parent2[adjacente] = c2
                        visited2.append(adjacente)
        path = []
        if path_found:
            path.append(finalpos)
            intermedio = finalpos
            end = finalpos
            while end not in self.finalPos and parent2[end] is not None:
                path.append(parent2[end])
                end = parent2[end]
            path2 = []
            start = intermedio
            for c in parent1.keys():
                if parent1[c] == start:
                    start = c
            while start != self.inicialPos:
                path2.append(start)
                start = parent1[start]
            path2.append(start)
            path2.reverse()
            path = path2 + path
        return path, self.calcula_custo(path), visited1 + visited2

    # Custo Uniforme, ou algoritmo de dijkstra.
    def custoUniforme(self):
        start = self.inicialPos
        end = self.finalPos
        visited = set()
        fila = list()
        visited.add(start)
        fila.append((start, 0))
        parent = dict()
        parent[start] = None
        path_found = False
        finalpos = (0, 0)
        while len(fila) > 0 and path_found == False:
            nodo_atual, custo = min(fila, key=lambda elem: elem[1])
            fila.remove((nodo_atual, custo))
            if nodo_atual in end:
                finalpos = nodo_atual
                path_found = True
            else:
                for adjacente in self.m_graph[nodo_atual]:
                    if adjacente not in visited:
                        fila.append((adjacente, custo + self.m_nodes[adjacente].elem[1]))
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

    # PESQUISA INFORMADA

    def define_dis(self):
        for nodo in self.m_nodes.values():
            dist = inf
            for (x, y) in self.finalPos:
                d = sqrt((x - nodo.coords[0]) ** 2 + (y - nodo.coords[1]) ** 2)
                if dist > d:
                    dist = d
            nodo.heuristica = dist

    def calculaDist(self, c1, c2):
        x1 = c1[0]
        y1 = c1[1]
        x2 = c2[0]
        y2 = c2[1]
        dist = 0
        while x1 != x2 and y1 != y2:
            dist = dist + 1
            if x1 > x2:
                x1 = x1 - 1
                if y1 > y2:
                    y1 = y1 - 1
                else:
                    y1 = y1 + 1
            else:
                x2 = x2 - 1
                if y1 > y2:
                    y2 = y2 + 1
                else:
                    y2 = y2 - 1
        if x1 == x2:
            return dist + abs(y1 - y2)
        else:
            return dist + abs(x1 - x2)

    # Devolve a set de posições para uma velocidade
    def heuristica_pos(self, pos, velocity):
        la = self.m_graph[pos]
        l = list()
        if velocity > 1:
            for c in la:
                if self.m_nodes[c].heuristica < self.m_nodes[pos].heuristica:
                    aux = self.heuristica_pos(c, velocity - 1)
                    for path in aux:
                        if self.calculaDist(path[-1], pos) == velocity:
                            l.append([pos] + path)
        else:
            for c in la:
                if self.m_nodes[c].heuristica < self.m_nodes[pos].heuristica:
                    l.append([pos, c])
        return l

    def heuristica(self, pos, velocidade):
        if velocidade > 1:
            s1 = self.heuristica_pos(pos, velocidade - 1)
        else:
            s1 = list()
        s2 = self.heuristica_pos(pos, velocidade)
        s3 = self.heuristica_pos(pos, velocidade + 1)
        return s1, s2, s3

    def add_parent(self, s, parents):
        for i in range(1, len(s)):
            if not parents.keys().__contains__(s[i]) or parents[s[i]]:
                parents[s[i]] = s[i - 1]

    def rebuild_path(self, start, caminho, n, visited):
        parents = {start: start}
        reconst_path = []
        procura = True
        for l in caminho.values():
            visited.extend(l[0])
        while procura:
            if not parents.__contains__(n):
                self.add_parent(caminho[n][0], parents)
            if parents[n] == n:
                procura = False
            else:
                reconst_path.append(n)
                n = parents[n]
        reconst_path.append(start)
        reconst_path.reverse()
        return reconst_path, self.calcula_custo(reconst_path), visited

    def greedy_aux(self, s, caminho, open_list, visited, v):
        if len(s) > 0:
            s = min(s, key=lambda elem: self.m_nodes[elem[-1]].heuristica)
            m = s[-1]
            if m not in open_list and m not in visited:
                caux = self.m_nodes[m].heuristica
                if not caminho.__contains__(s[-1]) or caminho[s[-1]][1] > caux:
                    caminho[s[-1]] = (s, caux)
                open_list.append((m, v))

    # Procura Gulosa
    def greedy(self):
        start = self.inicialPos
        open_list = [(start, 1)]
        visited = []
        caminho = {}
        while len(open_list) > 0:
            n, v = min(open_list, key=lambda elem: self.m_nodes[elem[0]].heuristica)
            if n in self.finalPos:
                return self.rebuild_path(start, caminho, n, visited)
            s1, s2, s3 = self.heuristica(n, v)
            self.greedy_aux(s1, caminho, open_list, visited, v - 1)
            self.greedy_aux(s2, caminho, open_list, visited, v)
            self.greedy_aux(s3, caminho, open_list, visited, v + 1)
            open_list.remove((n, v))
            visited.append(n)
        return None

    def a_star_aux(self, s, caminho, open_list, visited, custo, v):
        if len(s) > 0:
            s = min(s, key=lambda elem: self.m_nodes[elem[-1]].heuristica + self.calcula_custo(elem))
            m = s[-1]
            if m not in open_list and m not in visited:
                c = self.calcula_custo(s)
                caux = c + custo
                if not caminho.__contains__(s[-1]) or caminho[s[-1]][1] > caux:
                    caminho[s[-1]] = (s, caux)
                open_list.append((m, v, caux))

    # Procura A*
    def a_star(self):
        start = self.inicialPos
        open_list = [(start, 1, 0)]
        visited = []
        caminho = {}
        while len(open_list) > 0:
            n, v, c = min(open_list, key=lambda elem: self.m_nodes[elem[0]].heuristica + elem[2])
            if n in self.finalPos:
                return self.rebuild_path(start, caminho, n, visited)
            s1, s2, s3 = self.heuristica(n, v)
            self.a_star_aux(s1, caminho, open_list, visited, c, v - 1)
            self.a_star_aux(s2, caminho, open_list, visited, c, v)
            self.a_star_aux(s3, caminho, open_list, visited, c, v + 1)
            open_list.remove((n, v, c))
            visited.append(n)
        return None

    def subs(self, ca, c, posicoes):
        posicoes[ca] = ' '
        posicoes[c] = '-'

    def adjacente_bool(self, c1, c2):
        return self.calculaDist(c1, c2) == 1

    def game(self, paths):
        vencedor = []
        i = 0
        jog = 0
        d = dict()
        posicoes = dict()
        for p in paths:
            d[jog] = p
            jog += 1
        for coords in self.m_nodes.keys():
            posicoes[coords] = ' '
        while len(vencedor) < len(paths):
            i += 1
            for j in d.keys():
                path = d[j]
                if i < len(path) and j not in vencedor:
                    cantigo = path[i - 1]
                    c = path[i]
                    k = i - 2
                    while cantigo == c:
                        cantigo = path[k]
                        k -= 1
                    e = posicoes[c]
                    if c in self.finalPos:
                        print("Chegou ao fim o jogador " + str(j))
                        vencedor.append(j)
                        posicoes[cantigo] = ' '
                    elif e[0] == '-':
                        b = True
                        adjacentes = self.m_graph[c]
                        for coords in adjacentes:
                            if path[i + 1] in self.m_graph[coords]:
                                e = self.m_nodes[coords].elem
                                if coords not in self.finalPos and e[0] != '-':
                                    self.subs(cantigo, c, posicoes)
                                    b = False
                                    break
                                elif coords in self.finalPos:
                                    b = False
                                    print("Chegou ao fim o jogador " + str(j))
                                    vencedor.append(j)
                                    posicoes[cantigo] = ' '
                                    break
                        if b:
                            k = len(path)
                            path.append(path[k - 1])
                            k -= 1
                            while k > i:
                                path[k + 1] = path[k]
                                k -= 1
                            path[i] = path[i - 1]
                    else:
                        self.subs(cantigo, c, posicoes)
        pos = dict()
        posicao = 1
        vencedores = []
        for v in vencedor:
            h = posicao + self.calcula_custo(d[v])
            while pos.__contains__(h):
                h += 1
            pos[h] = v
            posicao += 1
            vencedores.append(h)
        vencedores.sort()
        winner = pos[vencedores[0]]
        return winner

    # Desenha o grafo de uma forma muito básica. Para já não está apto para desenhar caminhos
    def draw_turtle(self, path, title):
        turtle.title(title)
        race = turtle.Turtle()
        race.color("white")
        race.right(180)
        race.forward(self.width * 10 / 2)
        race.right(90)
        race.forward(self.heigth * 10 / 2)
        race.left(270)
        n = 10
        for y in range(self.heigth):
            if y != 0:
                race.left(180)
            x = 0
            while x < self.width:
                if (x, y) in path:
                    race.color("gray")
                elif self.m_nodes[(x, y)].elem[0] == 'X':
                    race.color("brown")
                elif self.m_nodes[(x, y)].elem[0] == 'P':
                    race.color("black")
                elif self.m_nodes[(x, y)].elem[0] == 'F':
                    race.color("red")
                elif self.m_nodes[(x, y)].elem[0] == 'X':
                    race.color("brown")
                if self.m_nodes[(x, y)].elem[0] == ' ' and (x, y) not in path:
                    race.color("white")
                    race.forward(n + 1)
                    x += 1
                else:
                    if (x, y) in path:
                        b = True
                        c = 'k'
                    else:
                        b = False
                        c = self.m_nodes[(x, y)].elem[0]
                    xi = x
                    while x < self.width and (
                            (b and (x, y) in path) or (self.m_nodes[(x, y)].elem[0] == c and (x, y) not in path)):
                        x += 1
                    m = (n + 1) * (x - xi) - 1
                    race.begin_fill()
                    race.forward(m)
                    race.right(90)
                    race.forward(n)
                    race.right(90)
                    race.forward(m)
                    race.right(90)
                    race.forward(n)
                    race.right(90)
                    race.forward(m + 1)
                    race.end_fill()
            race.right(90)
            race.forward(n + 1)
            race.color('white')
            race.right(90)
            race.forward(self.width * (n + 1))
        race.forward(n)
        turtle.mainloop()
