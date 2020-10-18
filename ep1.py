# EP - Design de Software
# Equipe: Carlos Andrade Inacio
# Data: 18/10/2020

# enumeração de estados de jogo
from enum import Enum

class ESTADOS(Enum):
    MENU = 0
    EMJOGO = 1

estado = ESTADOS.MENU

# definir uma variável global para as fichas iniciais
# essa variável é utilizada posteriormente para todos os jogadores cadastrados
fichas_iniciais = 20

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

def cadastro_jogadores(jogadores, fichas):
    quantidade_jogadores = 0
    while quantidade_jogadores <= 0:
        quantidade_jogadores = entrada_verificada("Quantos jogadores irão jogar? ", False)
        if quantidade_jogadores <= 0:
            print("Deve haver ao menos um jogador!")

    for j in range(quantidade_jogadores):
        jogadores.append(input("Nome do jogador {0}: ".format(j + 1)))
        fichas.append(fichas_iniciais)


# todas as cartas possíveis e seus valores
cartas_individuais = {"A" : 1, "2" : 2, "3" : 3, "4" : 4, "5" : 5, "6" : 6, "7" : 7, "8" : 8, "9" : 9, "10" : 0, "J" : 0, "Q" : 0, "K" : 0}

# definir um baralho completo de 52 cartas (13 cartas por naipe)
baralho = []
for c in cartas_individuais.keys():
    for i in range(4):
        baralho.append(c)

# cadastro de jogadores
jogadores = []
fichas = []
cadastro_jogadores(jogadores, fichas)

entrada_baralhos = 0
while entrada_baralhos <= 0:
    entrada_baralhos = entrada_verificada("Com quantos baralhos deseja jogar? ", False)
    if entrada_baralhos <= 0:
        print("Deve haver ao menos um baralho!")

baralho *= int(entrada_baralhos)
