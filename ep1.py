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

def cadastro_jogadores(jogadores, fichas):
    quantidade_jogadores = int(input("Quantos jogadores vão jogar? "))
    for j in range(quantidade_jogadores):
        jogadores.append(input("Nome do jogador {0}: ".format(j + 1)))
        fichas.append(fichas_iniciais)


# todas as cartas possíveis e seus valores
cartas = {"A" : 1, "2" : 2, "3" : 3, "4" : 4, "5" : 5, "6" : 6, "7" : 7, "8" : 8, "9" : 9, "10" : 0, "J" : 0, "Q" : 0, "K" : 0}

# cadastro de jogadores
jogadores = []
fichas = []
cadastro_jogadores(jogadores)

