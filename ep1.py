# EP - Design de Software
# Equipe: Carlos Andrade Inacio
# Data: 18/10/2020

# enumeração de estados de jogo
from enum import Enum
import random
import os

def limpar_terminal():
    os.system('cls||clear')

class ESTADOS(Enum):
    MENU = 0
    EMJOGO = 1

estado = ESTADOS.MENU

# definir uma variável global para as fichas iniciais
# essa variável é utilizada posteriormente para todos os jogadores cadastrados
fichas_iniciais = 20

# todas as cartas possíveis e seus valores
cartas_individuais = {"A" : 1, "2" : 2, "3" : 3, "4" : 4, "5" : 5, "6" : 6, "7" : 7, "8" : 8, "9" : 9, "10" : 0, "J" : 0, "Q" : 0, "K" : 0}
apostas = ["Jogador", "Banco", "Empate"]
comissao_da_casa = { "Jogador" : [1.29, 1.29, 1.29, 1.29, 1.29, 1.24, 1.24, 1.24], "Banco" : [1.01, 1.01, 1.01, 1.01, 1.01, 1.06, 1.06, 1.06], "Empate" : [15.75, 15.75, 15.75, 15.75, 15.75, 14.44, 14.44, 14.36] }

# variáveis 'globais' que podem ser resetadas caso o usuário queria
baralho = []
jogadores = []
fichas = []

num_baralhos = 0

# variável que possibilita saída do jogo e finalização da execução do script
finalizar_execucao = False

# função para criar input de int e limpar o código poupando-o de ter as mesmas verficações várias vezes
def entrada_verificada(out, err, rejeitar_negativo):
    # out - string imprimido pelo input
    # err - string de texto caso o número seja negativo
    # rejeitar negativo - rejeita números negativos
    retorno = -1
    while 1:
        entrada = input(out)
        if entrada.isdigit() == True:
            retorno = int(entrada)
            if retorno <= 0 and rejeitar_negativo:
                print(err)
            else: 
                return retorno
        else:
            print("Entrada inválida!")

    return retorno



def multipla_escolha(escolhas):
    print("")
    indice = 1
    for e in escolhas:
        print("{0} - {1}".format(indice, e))
        indice += 1
    
    entrada = 0
    while entrada > len(escolhas) or entrada <= 0:
        entrada = entrada_verificada("O que deseja fazer? ", "Entrada inválida!", True)
        if entrada > len(escolhas) or entrada <= 0:
            print("Entrada invalida!")
    
    return entrada

def cadastro_jogadores(jogadores, fichas):
    quantidade_jogadores = entrada_verificada("Quantos jogadores irão jogar? ", "Deve haver ao menos um jogador!", True)

    for j in range(quantidade_jogadores):
        jogadores.append(input("Nome do jogador {0}: ".format(j + 1)))
        fichas.append(fichas_iniciais)

def menu():
    global num_baralhos, baralho, jogadores, fichas, finalizar_execucao, estado

    limpar_terminal()

    baralho = []
    jogadores = []
    fichas = []
    num_baralhos = 0

    # definir um baralho completo de 52 cartas (13 cartas por naipe)
    for c in cartas_individuais.keys():
        for i in range(4):
            baralho.append(c)

    # cadastro de jogadores
    cadastro_jogadores(jogadores, fichas)

    entrada_baralhos = [1, 6, 8][multipla_escolha(["1 Baralho", "6 Baralhos", "8 Baralhos"]) - 1]

    baralho *= int(entrada_baralhos)
    num_baralhos = entrada_baralhos

    limpar_terminal()

    print("Jogadores:")
    for j in jogadores:
        print("  {0}".format(j))
    print("Baralho: {0} cartas, ou {1} {2}".format(len(baralho), num_baralhos, "baralhos" if num_baralhos > 1 else "baralho"))

    escolha = multipla_escolha(["Continuar", "Reconfigurar", "Sair"])
    if escolha == 1:
        estado = ESTADOS.EMJOGO
    elif escolha == 2:
        pass
    elif escolha == 3:
        finalizar_execucao = True

def carta_aleatoria():
    return baralho[random.randint(0, len(baralho) - 1)]

def terceira_carta(mao):
    soma = cartas_individuais[mao[0]] + cartas_individuais[mao[1]]

    # pegar carta aleatória
    # aqui pegamos a chave e não o dicionário
    carta = carta_aleatoria()
    valor = cartas_individuais[carta]

    # aqui verificamos os critérios para a terceira carta ser adicionada à mão do jogador
    cartas_n = [[], [], [], [8], [0, 1, 8, 9], [0, 1, 2, 3, 8, 9]]

    if soma >= 6:
        return
    else:
        for c in cartas_n[soma]:
            if c == valor:
                return

    mao.append(carta)

def distribuir_cartas():
    mao = []

    mao.append(carta_aleatoria())
    mao.append(carta_aleatoria())
    terceira_carta(mao)        

    return mao

def imprimir_mao(mao):
    soma = 0
    mostrar_chaves = ""
    mostrar_valores = ""

    for c in mao:
        mostrar_chaves += "   {0}".format(c)
        mostrar_valores += "   {0}".format(cartas_individuais[c])
        soma += cartas_individuais[c]

    soma = soma - 10 if soma > 10 else soma

    print(mostrar_chaves)
    print(mostrar_valores)
    print("Soma: {0}".format(soma))

def verificar_aposta(soma_jogadores, soma_banco, aposta):
    global num_baralhos, jogadores, fichas

    limpar_terminal()
    indice = 0
    for a in aposta:
        ganho = int(round(a[0] * ((100 - comissao_da_casa[a[1]][num_baralhos - 1]) / 100)))
        if a[1] == "Jogador":
            if abs(soma_jogadores[indice] - 9) < abs(soma_banco - 9):
                # apostou em jogador e ganhou a aposta
                fichas[indice] += ganho
                print("{0} ganhou {1} fichas!".format(jogadores[indice], ganho))
            else:
                fichas[indice] -= a[0]
                print("{0} perdeu {1} fichas!".format(jogadores[indice], a[0]))
        elif a[1] == "Banco":
            if abs(soma_jogadores[indice] - 9) > abs(soma_banco - 9):
                # apostou no banco e ganhou a aposta
                fichas[indice] += ganho
                print("{0} ganhou {1} fichas!".format(jogadores[indice], ganho))
            else:
                fichas[indice] -= a[0]
                print("{0} perdeu {1} fichas!".format(jogadores[indice], a[0]))
        else:
            if soma_jogadores == soma_banco:
                # apostou em empate e ganhou a aposta
                fichas[indice] += ganho
                print("{0} ganhou {1} fichas!".format(jogadores[indice], ganho))
            else:
                fichas[indice] -= a[0]
                print("{0} perdeu {1} fichas!".format(jogadores[indice], a[0]))
        indice += 1

def realizar_aposta():
    global baralho, jogadores, fichas, finalizar_execucao, estado
    
    limpar_terminal()

    # aposta = [ [ valor, tipo ], [ valor, tipo ]  ]
    # matriz com uma lista de "valor, tipo" para cada jogador
    aposta = []
    for j in range(len(jogadores)):
        limpar_terminal()
        _aposta = [entrada_verificada("Quanto deseja apostar {0}? ".format(jogadores[j]), "Você tem que apostar um valor válido!", True)]
        _aposta.append(apostas[multipla_escolha(["Jogador", "Banco", "Empate"]) - 1])
        aposta.append(_aposta)

    limpar_terminal()
    for j in range(len(jogadores)):
        print("Aposta de {0}: {1} fichas em {2}".format(jogadores[j], aposta[j][0], aposta[j][1]))

    print("Distribuindo cartas...")
    input("Pressione enter para continuar")
    limpar_terminal()
    
    mao_banco = distribuir_cartas()
    mao_jogadores = []
    soma_jogadores = []
    soma_banco = 0

    print("--------------------------")
    
    for j in range(len(jogadores)):
        soma = 0

        mao_jogadores.append(distribuir_cartas())
        
        for c in mao_jogadores[j]:
            soma += cartas_individuais[c]
        
        soma_jogadores.append(soma)        
            
        print("{0} com {1} fichas: ".format(jogadores[j], aposta[j][0]))
        imprimir_mao(mao_jogadores[j])
        print("--------------------------")
    
    print("Banco: ")
    
    for c in mao_banco:
        soma_banco += cartas_individuais[c]

    imprimir_mao(mao_banco)
    print("--------------------------")
    
    input("Pressione enter para continuar")
    
    verificar_aposta(soma_jogadores, soma_banco, aposta)
    input("Pressione enter para continuar")

def jogo():
    global baralho, jogadores, fichas, finalizar_execucao, estado

    limpar_terminal()

    for j in range(len(jogadores)):
        print("{0}: {1} fichas".format(jogadores[j], fichas[j]))
    
    escolha = multipla_escolha(["Fazer apostas", "Reconfigurar", "Sair"])
    if escolha == 1:
        realizar_aposta()
    elif escolha == 2:
        estado = ESTADOS.MENU
    elif escolha == 3:
        finalizar_execucao = True


while finalizar_execucao == False:
    if estado == ESTADOS.MENU:
        menu()
    elif estado == ESTADOS.EMJOGO:
        jogo()

print("Até mais!")