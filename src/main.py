from datetime import datetime

from Grafo import Grafo
import threading


def getAlgoritmo():
    b = True
    p = []
    alg = ""
    delta = datetime.now()
    while (b):
        b = False
        print("Qual o algoritmo?")
        print("1 - Largura")
        print("2 - Profundidade")
        print("3 - Iterativo")
        print("4 - Bidirecional")
        print("5 - Uniforme")
        print("6 - Gulosa")
        print("7 - A Estrela")
        alg = int(input())
        init = datetime.now()
        if alg == 1:
            alg = "Largura"
            p = grafo.procura_BFS()
        elif alg == 2:
            alg = "Profundidade"
            p = grafo.procura_DFS()
        elif alg == 3:
            alg = "Iterativo"
            print("Quantas iterações?")
            ite = int(input())
            init = datetime.now()
            p = grafo.procura_iterativa(ite)
        elif alg == 4:
            alg = "Bidirecional"
            p = grafo.bidirectional()
        elif alg == 5:
            alg = "Uniforme"
            p = grafo.custoUniforme()
        elif alg == 6:
            alg = "Gulosa"
            p = grafo.greedy()
        elif alg == 7:
            alg = "A Estrela"
            p = grafo.a_star()
        else:
            print("Opção Inválida")
            b = True
        fim = datetime.now()
        delta = fim - init
    print("Tempo: " + str(delta.total_seconds()))
    return p, alg


grafo = Grafo()
grafo.add_info("../nossapista")

print("Bem vindo ao Simulador RACE-TRACK!!")
print("Escolha uma das seguintes opções:")
print("1 - Multijogador")
print("2 - Jogar sozinho")
n = int(input())
if n == 2:
    p, alg = getAlgoritmo()
    if p is None:
        print("Solução não encontrada")
    else:
        print("1-Formato textual")
        print("2-Representação Gráfica")
        op = int(input())
        if op == 1:
            print(grafo.toMatrizPath(p[0],p[1],'.'))
        else:
            grafo.draw_turtle(p[0], "Solução algoritmo " + alg)
else:
    print("Quando jogadores (1-7)?")
    jog = int(input())
    while jog > 7 or jog < 1:
        print("Número de jogadores inválido")
        jog = int(input())
    l = []
    alg = []
    for i in range(jog):
        b = True
        while b:
            print("Jogador " + str(i))
            p, _ = getAlgoritmo()
            if _ in alg:
                print("Algoritmo já escolhido")
            else:
                alg.append(_)
                l.append(p[0])
                b = False
    winner = grafo.game(l)
    print("Ganhou jogador: " + str(winner))
