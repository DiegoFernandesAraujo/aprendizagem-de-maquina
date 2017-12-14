#autor: Diego Fernandes de Araújo

from numpy import *

def regressao_formula_fechada(pontos):
    aux_x = 0
    aux_y = 0
    a = 0
    b = 0
    n = len(pontos)

    for i in range(0, n):
        aux_x += pontos[i, 0]
        aux_y += pontos[i, 1]
    media_x = aux_x / n
    media_y = aux_y / n

    for i in range(0, n):
        a += (pontos[i, 0] - media_x) * (pontos[i, 1] - media_y)
        b += (pontos[i, 0] - media_x) ** 2

    w1 = a / b
    w0 = media_y - w1 * media_x

    return(w0, w1)

def computa_erro_medio(w0, w1, pontos):
    erroTotal = 0
    for i in range(0, len(pontos)):
        x = pontos[i, 0]
        y = pontos[i, 1]
        erroTotal += (y - (w0 + w1*x)) **2

    return erroTotal/float(len(pontos))

def calcula_passo_gradiente(w0_atual, w1_atual, pontos, taxa_aprend):
    w0_gradiente = 0
    w1_gradiente = 0
    N = float(len(pontos))
    rss = 0

    for i in range(0, len(pontos)):
        x = pontos[i, 0]
        y = pontos[i, 1]

        w0_gradiente += -(2 / N) * (y - (w0_atual + (w1_atual * x)))
        w1_gradiente += -(2 / N) * x * (y - (w0_atual + (w1_atual * x)))

        rss += (y - (w0_atual + w1_atual * x)) ** 2

    print("RSS: %f" % (rss))

    new_w0 = w0_atual - (taxa_aprend * w0_gradiente)
    new_w1 = w1_atual - (taxa_aprend * w1_gradiente)

    return [new_w0, new_w1]

#Executa o gradiente descendente com quantidade pré-estabelecida de iterações	
def executa_gradiente_descendente2(pontos, starting_w0, starting_w1, taxa_aprend, num_iteracoes):
    w0 = starting_w0
    w1 = starting_w1

    for i in range(num_iteracoes):
        w0, w1 = calcula_passo_gradiente(w0, w1, array(pontos), taxa_aprend)

    return [w0, w1]


#Executa o gradiente descendente com critério de tolerância
def executa_gradiente_descendente(w0_atual, w1_atual, pontos, taxa_aprend, crit_tolerancia):
    w0_gradiente = 0
    w1_gradiente = 0
    iteracao = 1


    while ((sqrt(w0_gradiente ** 2 + w1_gradiente ** 2)) >= crit_tolerancia) or iteracao == 1:

        w0_gradiente = 0
        w1_gradiente = 0
        N = float(len(pontos))
        iteracao = 0
        rss = 0

        for i in range(0, len(pontos)):
            x = pontos[i, 0]
            y = pontos[i, 1]

            w0_gradiente += -(2 / N) * (y - (w0_atual + (w1_atual * x)))
            w1_gradiente += -(2 / N) * x * (y - (w0_atual + (w1_atual * x)))

            rss += (y - (w0_atual + w1_atual * x)) ** 2

        print("RSS: %f" % (rss))

        w0_atual -= (taxa_aprend * w0_gradiente)
        w1_atual -= (taxa_aprend * w1_gradiente)

    return [w0_atual, w1_atual]

def run():
    pontos = genfromtxt('income.csv', delimiter=',')
    taxa_aprend = 0.001
    #taxa_aprend = 0.0001
    
    #y = w0 + w1x
    w0_inicial = 0
    w1_inicial = 0
    opcao = 0

    while((opcao != 'f') and (opcao != 'g')):
        opcao = input("Gostaria de executar a regressão através de gradiente descendente (g) ou da fórmula fechada (f)?")

        if opcao == 'f':

            print("Executando...")

            [w0, w1] = regressao_formula_fechada(pontos)

            print(
                "Depois da execução, w0 = %f, w1 = %f, erro médio = %f" % (w0, w1, computa_erro_medio(w0, w1, pontos)))

        elif opcao == 'g':

            while ((opcao != 1) and (opcao != 2)):

                opcao = input(
                    "Gostaria de executar a regressão através de um critério de tolerância (1) ou a partir de iterações fixas(2)?")

                if (int(opcao) == 1):
                    tolerancia = input("Informe o critério de tolerância: ")

                    print("Iniciando gradiente descendente com w0 = %f, w1 = %f, erro médio = %f" % (
                        w0_inicial, w1_inicial, computa_erro_medio(w0_inicial, w0_inicial, pontos)))
                    print("Executando...")

                    [w0, w1] = executa_gradiente_descendente(w0_inicial, w1_inicial, array(pontos), taxa_aprend,
                                                             float(tolerancia))

                    print("Depois da execução, w0 = %f, w1 = %f, erro médio = %f" % (
                        w0, w1, computa_erro_medio(w0, w1, pontos)))

                    break

                elif (int(opcao) == 2):
                    num_iteracoes = input("Informe a quantidade de iterações: ")

                    print("Iniciando gradiente descendente com w0 = %f, w1 = %f, e erro = %f" % (
                        w0_inicial, w1_inicial, computa_erro_medio(w0_inicial, w0_inicial, pontos)))
                    print("Executando...")

                    [w0, w1] = executa_gradiente_descendente2(pontos, w0_inicial, w1_inicial, taxa_aprend,
                                                              int(num_iteracoes))

                    print("Depois da execução, w0 = %f, w1 = %f, error = %f" % (
                        w0, w1, computa_erro_medio(w0, w1, pontos)))

                    break

            else:
                print(
                    "Digite 1 para informar o critério de tolerância ou 2 para informar a quantidade de iterações")


        else:

            print("Digite \"g\" para gradiente descendente ou \"f\" para fórmula fechada")




if __name__ == '__main__':
    run()