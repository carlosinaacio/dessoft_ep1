# EP - Design de Software
# Equipe: Carlos Andrade Inacio
# Data: 18/10/2020

# enumeração de estados de jogo
from enum import Enum
import random

class ESTADOS(Enum):
    MENU = 0
    EMJOGO = 1

estado = ESTADOS.MENU

# definir uma variável global para as fichas iniciais
# essa variável é utilizada posteriormente para todos os jogadores cadastrados
fichas_iniciais = 20

# todas as cartas possíveis e seus valores
cartas_individuais = {"A" : 1, "2" : 2, "3" : 3, "4" : 4, "5" : 5, "6" : 6, "7" : 7, "8" : 8, "9" : 9, "10" : 0, "J" : 0, "Q" : 0, "K" : 0}

comissao_da_casa = { "Jogador" : [1.29, 1.29, 1.29, 1.29, 1.29, 1.24, 1.24, 1.24], "Banco" : [1.01, 1.01, 1.01, 1.01, 1.01, 1.06, 1.06, 1.06], "Empate" : [15.75, 15.75, 15.75, 15.75, 15.75, 14.44, 14.44, 14.36] }

# variáveis 'globais' que podem ser resetadas caso o usuário queria
baralho = []
jogadores = []
fichas = []

# variável que possibilita saída do jogo e finalização da execução do script
finalizar_execucao = False

# função para criar input de int e limpar o código poupando-o de ter as mesmas verficações várias vezes
def entrada_verificada(out, ret_string):
    # out - string imprimido pelo input
    # ret_string - espera-se que um string seja retornado
    retorno = -1
    entrada = input(out)
    if ret_string == True:
        return entrada
    elif ret_string == False and entrada.isdigit() == True:
        retorno = int(entrada)
    else:
        print("Entrada inválida!")
    
    return retorno

def multipla_escolha(escolhas):
    indice = 1
    for e in escolhas:
        print("{0} - {1}".format(indice, e))
        indice += 1
    
    entrada = -1
    while entrada <= 0:
        entrada = entrada_verificada("O que deseja fazer? ", False)
        if entrada <= 0:
            print("Entrada inválida!")
    
    return entrada

def cadastro_jogadores(jogadores, fichas):
    quantidade_jogadores = 0
    while quantidade_jogadores <= 0:
        quantidade_jogadores = entrada_verificada("Quantos jogadores irão jogar? ", False)
        if quantidade_jogadores <= 0:
            print("Deve haver ao menos um jogador!")

    for j in range(quantidade_jogadores):
        jogadores.append(input("Nome do jogador {0}: ".format(j + 1)))
        fichas.append(fichas_iniciais)

def menu():
    global baralho, jogadores, fichas, finalizar_execucao, estado

    baralho = []
    jogadores = []
    fichas = []

    # definir um baralho completo de 52 cartas (13 cartas por naipe)
    for c in cartas_individuais.keys():
        for i in range(4):
            baralho.append(c)

    # cadastro de jogadores
    cadastro_jogadores(jogadores, fichas)

    entrada_baralhos = 0
    while entrada_baralhos <= 0:
        entrada_baralhos = entrada_verificada("Com quantos baralhos deseja jogar? ", False)
        if entrada_baralhos <= 0:
            print("Deve haver ao menos um baralho!")

    baralho *= int(entrada_baralhos)

    escolha = multipla_escolha(["Continuar", "Reconfigurar", "Sair"])
    print(escolha)
    if escolha == 1:
        estado = ESTADOS.EMJOGO
    elif escolha == 2:
        pass
    elif escolha == 3:
        finalizar_execucao = True

def carta_aleatoria():
    return baralho[random.randint(0, len(baralho) - 1)]

def terceira_carta(mao):
    soma = mao[0] + mao[1]

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
    mostrar_chaves = ""
    mostrar_valores = ""
    for c in mao:
        mostrar_chaves += "   {0}".format(c)
        mostrar_valores += "   {0}".format(cartas_individuais[c])
    print(mostrar_chaves)
    print(mostrar_valores)

def realizar_aposta():
    global baralho, jogadores, fichas, finalizar_execucao, estado
    
    print("Distribuindo cartas...")    
    
    mao_banco = distribuir_cartas()
    mao_jogadores = []
    print("--------------------------")
    for j in range(len(jogadores)):
        if len(jogadores) < 2:
            mao_jogadores = distribuir_cartas()
        else:
            mao_jogadores.append(distribuir_cartas())

        print("{0} com {1} fichas: ".format(jogadores[j], fichas[j]))
        imprimir_mao(mao_jogadores[j])
        print("--------------------------")
    
    print("Banco: ")
    imprimir_mao(mao_banco)
    print("--------------------------")
    

    
    

def jogo():
    global baralho, jogadores, fichas, finalizar_execucao, estado

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