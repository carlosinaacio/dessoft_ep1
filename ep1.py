# EP - Design de Software
# Equipe: Carlos Andrade Inacio
# Data: 18/10/2020

def ascii_logo():
    print(" .----------------.  .----------------.  .----------------.  .----------------.  .----------------.  .----------------.")
    print("| .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. |")
    print("| |   ______     | || |      __      | || |     ______   | || |      __      | || |  _______     | || |      __      | |")
    print("| |  |_   _ \    | || |     /  \     | || |   .' ___  |  | || |     /  \     | || | |_   __ \    | || |     /  \     | |")
    print("| |    | |_) |   | || |    / /\ \    | || |  / .'   \_|  | || |    / /\ \    | || |   | |__) |   | || |    / /\ \    | |")
    print("| |    |  __'.   | || |   / ____ \   | || |  | |         | || |   / ____ \   | || |   |  __ /    | || |   / ____ \   | |")
    print("| |   _| |__) |  | || | _/ /    \ \_ | || |  \ `.___.'\  | || | _/ /    \ \_ | || |  _| |  \ \_  | || | _/ /    \ \_ | |")
    print("| |  |_______/   | || ||____|  |____|| || |   `._____.'  | || ||____|  |____|| || | |____| |___| | || ||____|  |____|| |")
    print("| |              | || |              | || |              | || |              | || |              | || |              | |")
    print("| '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' |")
    print(" '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------' ")
    print("\n")

# enumeração de estados de jogo
from enum import Enum
import random
import os

def limpar_terminal():
    # cls - windows
    # clear - os baseado em unix
    os.system('cls||clear')

# enumeração para estados de jogo
class ESTADOS(Enum):
    MENU = 0
    EMJOGO = 1

# variável global de estado de jogo
estado = ESTADOS.MENU

# definir uma variável global para as fichas iniciais
# essa variável é utilizada posteriormente para todos os jogadores cadastrados
fichas_iniciais = 20

# todas as cartas possíveis e seus valores
cartas_individuais = {"A" : 1, "2" : 2, "3" : 3, "4" : 4, "5" : 5, "6" : 6, "7" : 7, "8" : 8, "9" : 9, "10" : 0, "J" : 0, "Q" : 0, "K" : 0}
# tipos de aposta
apostas = ["Jogador", "Banco", "Empate"]
# taxas de comissão da casa para cada tipo de aposta
comissao_da_casa = { "Jogador" : [1.29, 1.29, 1.29, 1.29, 1.29, 1.24, 1.24, 1.24], "Banco" : [1.01, 1.01, 1.01, 1.01, 1.01, 1.06, 1.06, 1.06], "Empate" : [15.75, 15.75, 15.75, 15.75, 15.75, 14.44, 14.44, 14.36] }

# variáveis 'globais' que podem ser resetadas caso o usuário queria
baralho = []
jogadores = []
fichas = []

# variável global para número de baralhos
# justificável pois o número de baralhos é utilizado para calcular a taxa de comissão posteriormente
num_baralhos = 0

# variável que possibilita saída do jogo e finalização da execução do script
finalizar_execucao = False

# função para criar input de int e limpar o código poupando-o de ter as mesmas verficações várias vezes
def entrada_verificada(out, err, rejeitar_negativo):
    # out - string imprimido pelo input
    # err - string de texto caso o número seja negativo
    # rejeitar negativo - rejeita números negativos
    retorno = -1
    # continuar pedindo uma entrada do usuário até que a mesma seja válida
    while 1:
        entrada = input(out)
        # isdigit() - verifica se é um número
        if entrada.isdigit() == True:
            retorno = int(entrada)
            # caso a chama deca rejeitar negativos, rejeitamos negativos
            if retorno <= 0 and rejeitar_negativo:
                # imprimir o erro predefinido
                print(err)
            else: 
                return retorno
        else:
            print("Entrada inválida!")

    return retorno

def multipla_escolha(escolhas):
    # escolhas - lista de escolhas
    
    print("")
    indice = 1
    # imprimir no terminal as escolhas e seus índices
    for e in escolhas:
        print("{0} - {1}".format(indice, e))
        indice += 1
    
    # verificar se a entrada não vai além do número de escolhas
    entrada = 0
    while entrada > len(escolhas) or entrada <= 0:
        entrada = entrada_verificada("O que deseja fazer? ", "Entrada inválida!", True)
        if entrada > len(escolhas) or entrada <= 0:
            print("Entrada invalida!")
    
    return entrada

def cadastro_jogadores(jogadores, fichas):
    # jogadores - lista com nomes de jogadores
    # fichas - lista com fichas para cada jogador
    # talvez fosse melhor utilizar um dicionário (?)
    quantidade_jogadores = entrada_verificada("Quantos jogadores irão jogar? ", "Deve haver ao menos um jogador!", True)

    for j in range(quantidade_jogadores):
        jogadores.append(input("Nome do jogador {0}: ".format(j + 1)))
        fichas.append(fichas_iniciais)

def menu():
    # definir variáveis globais para que possamos modificá-las, se necessário
    global num_baralhos, baralho, jogadores, fichas, finalizar_execucao, estado

    limpar_terminal()

    # reinstanciar essas variáveis
    baralho = []
    jogadores = []
    fichas = []
    num_baralhos = 0

    # imprimir logo no terminal
    ascii_logo()

    # definir um baralho completo de 52 cartas (13 cartas por naipe)
    for c in cartas_individuais.keys():
        for i in range(4):
            baralho.append(c)

    # cadastro de jogadores
    cadastro_jogadores(jogadores, fichas)

    # escolher entre 1, 6 ou 8 baralhos
    entrada_baralhos = [1, 6, 8][multipla_escolha(["1 Baralho", "6 Baralhos", "8 Baralhos"]) - 1]

    # multiplicamos o baralho completo pelo número de baralhos
    baralho *= int(entrada_baralhos)
    # registramos o número de baralhos
    num_baralhos = entrada_baralhos

    limpar_terminal()

    # imprimir um resumo das configurações antes do usuário decidir se continua ou reconfigura
    print("Jogadores:")
    for j in jogadores:
        print("  {0}".format(j))
    print("Baralho: {0} cartas, ou {1} {2}".format(len(baralho), num_baralhos, "baralhos" if num_baralhos > 1 else "baralho"))

    escolha = multipla_escolha(["Continuar", "Reconfigurar", "Sair"])
    if escolha == 1:
        # continuar para o jogo
        estado = ESTADOS.EMJOGO
    elif escolha == 2:
        # a função menu será chamada mais uma vez
        pass
    elif escolha == 3:
        # o loop principal do programa quebra e o programa chega ao fim
        finalizar_execucao = True

def carta_aleatoria():
    # pegamos uma carta aleatória dentro dos baralhos ou baralho
    # retorna a chave dela
    # nós utilizamos a chave pois com ela podemos disponibilizar tanto o valor quanto uma representação visual para o usuário
    return baralho[random.randint(0, len(baralho) - 1)]

def terceira_carta(mao):
    # mao - lista de chaves
    soma = cartas_individuais[mao[0]] + cartas_individuais[mao[1]]

    # pegar carta aleatória
    # aqui pegamos a chave e não o dicionário
    carta = carta_aleatoria()
    valor = cartas_individuais[carta]

    # aqui verificamos os critérios para a terceira carta ser adicionada à mão do jogador
    cartas_n = [[], [], [], [8], [0, 1, 8, 9], [0, 1, 2, 3, 8, 9]]

    # paramos a função aqui se a soma ja for maior que ou igual a 6
    if soma >= 6:
        return
    else:
        # paramos a função aqui se a soma e a terceira carta não se adequarem aos critérios avançados
        for c in cartas_n[soma]:
            if c == valor:
                return

    # se a execução da função não for interrompida anteriormente, a carta pode ser adicionada à mão
    mao.append(carta)

def distribuir_cartas():
    mao = []

    # adicionamos 2 cartas aleatórias à mão e, logo após, verificamos e adicionamos a terceira carta se necessário
    mao.append(carta_aleatoria())
    mao.append(carta_aleatoria())
    terceira_carta(mao)        

    # retornamos uma lista de chaves
    return mao

def imprimir_mao(mao):
    # mao - lista de chaves

    soma = 0
    mostrar_chaves = ""
    mostrar_valores = ""

    for c in mao:
        mostrar_chaves += "   {0}".format(c)
        mostrar_valores += "   {0}".format(cartas_individuais[c])
        soma += cartas_individuais[c]

    # caso a soma seja maior que ou igual a 10, somente o último dígito é considerado
    soma = soma - 10 if soma > 10 else soma

    print(mostrar_chaves)
    print(mostrar_valores)
    print("Soma: {0}".format(soma))

def verificar_aposta(soma_jogadores, soma_banco, aposta):
    # soma_jogadores - lista de somas
    # soma banco - número inteiro
    # aposta - matriz com listas contendo os valores e tipos de aposta para cada jogador

    global num_baralhos, jogadores, fichas

    limpar_terminal()
    indice = 0
    for a in aposta:
        # subtraímos a taxa de comissão
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
        # para cada jogador, adicionamos uma lista de [valor, aposta] para a matriz 'aposta'
        limpar_terminal()
        _aposta = [entrada_verificada("Quanto deseja apostar {0}? ".format(jogadores[j]), "Você tem que apostar um valor válido!", True)]
        _aposta.append(apostas[multipla_escolha(["Jogador", "Banco", "Empate"]) - 1])
        aposta.append(_aposta)

    limpar_terminal()

    # imprimimos um resumo das apostas
    for j in range(len(jogadores)):
        print("Aposta de {0}: {1} fichas em {2}".format(jogadores[j], aposta[j][0], aposta[j][1]))

    print("Distribuindo cartas...")
    input("Pressione enter para continuar")

    limpar_terminal()
    
    # instaciamos essas variáveis para podermos executar essa função quantas vezes quisermos
    mao_banco = distribuir_cartas()
    mao_jogadores = []
    soma_jogadores = []
    soma_banco = 0

    # decoração
    print("--------------------------")
    
    for j in range(len(jogadores)):
        soma = 0
        # adicionar a lista de cartas à matriz 'mao_jogadores'
        mao_jogadores.append(distribuir_cartas())
        
        for c in mao_jogadores[j]:
            soma += cartas_individuais[c]
        
        # adicionamos a soma para a lista 'soma_jogadores'
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
    
    # executamos a validação da aposta e realizamos a redução ou aumento de fichas de acordo
    verificar_aposta(soma_jogadores, soma_banco, aposta)
    input("Pressione enter para continuar")

def jogo():
    # variáveis globais que podemos modificar, se necessário
    global baralho, jogadores, fichas, finalizar_execucao, estado

    limpar_terminal()

    # imprimimos um resumo sobre os jogadores antes de realizarem suas apostas
    for j in range(len(jogadores)):
        print("{0}: {1} fichas".format(jogadores[j], fichas[j]))
    
    escolha = multipla_escolha(["Fazer apostas", "Reconfigurar", "Sair"])
    if escolha == 1:
        # continuar para apostas
        realizar_aposta()
    elif escolha == 2:
        # voltar ao menu e reconfigurar o jogo
        estado = ESTADOS.MENU
    elif escolha == 3:
        # finalizar o programa
        finalizar_execucao = True

# caso 'finalizar_execucao' seja True, o programa chega ao fim
while finalizar_execucao == False:
    # verificação de estados e execução de funções de acordo
    if estado == ESTADOS.MENU:
        menu()
    elif estado == ESTADOS.EMJOGO:
        jogo()

# se esse código for executado, o programa chega ao fim, por isso deixamos uma mensagem de adeus
limpar_terminal()
print("Até mais!")