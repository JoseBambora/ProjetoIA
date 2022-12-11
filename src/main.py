from Grafo import Grafo
import threading

def getAlgoritmo():
    b = True
    p = []
    alg = ""
    while(b):
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
        if alg == 1:
            alg = "Largura"
            p = grafo.procura_BFS()[0]
        elif alg == 2:
            alg = "Profundidade"
            p = grafo.procura_DFS()[0]
        elif alg == 3:
            alg = "Iterativo"
            print("Quantas iterações?")
            ite = input()
            p = grafo.procura_iterativa(ite)[0]
        elif alg == 4:
            alg = "Bidirecional"
            p = grafo.bidirectional()[0]
        elif alg == 5:
            alg = "Uniforme"
            p = grafo.custoUniforme()[0]
        elif alg == 6:
            alg = "Gulosa"
            p = grafo.greedy()[0]
        elif alg == 7:
            alg = "A Estrela"
            p = grafo.a_star()[0]
        else:
            print("Opção Inválida")
            b = True
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
    grafo.draw_turtle(p,"Solução algoritmo " + alg)
else:
    print("Quando jogadores (1-7)?")
    jog = int(input())
    l = []
    for i in range(jog):
        b = True
        while b:
            print("Jogador " + str(i))
            p, _ = getAlgoritmo()
            if p in l:
                print("Algoritmo já escolhido")
            else:
                l.append(p)
                b = False
    winner = grafo.game(l)
    print("Ganhou jogador: " + str(winner))
