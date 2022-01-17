from utils.player import Player
import random


class Ia(Player):

    def __init__(self, couleur, niveau):
        self.couleur = couleur
        self.is_actif = False
        self.score = 0
        self.niveau = niveau

    def choix_niveau(self, board):
        if self.niveau == 1:
            return Ia.random_coup(board)
        elif self.niveau == 2:
            return Ia.premier_meilleur_coup(board)
        elif self.niveau == 3:
            return Ia.random_meilleur_coup(board)
        elif self.niveau == 4:
            return Ia.random_meilleur_coup_pondere(board)
        elif self.niveau == 103:
            return Ia.random_pire_coup(board)
        elif self.niveau == 104:
            return Ia.random_pire_coup_pondere(board)

    def random_coup(board):
        liste_coups_possibles = []
        for i in range(8):
            for j in range(8):
                if sum(board.table[i][j].poids) > 0:
                    liste_coups_possibles.append((i, j))
        return random.choice(liste_coups_possibles)

    def premier_meilleur_coup(board):
        max_value = 0
        ligne, col = 0, 0
        for i in range(8):
            for j in range(8):
                if sum(board.table[i][j].poids) > max_value:
                    max_value = sum(board.table[i][j].poids)
                    ligne, col = i, j
        return (ligne, col)

    def random_meilleur_coup(board):
        max_value = 0
        liste_coups_possibles = []
        for i in range(8):
            for j in range(8):
                if sum(board.table[i][j].poids) > max_value:
                    max_value = sum(board.table[i][j].poids)
        for i in range(8):
            for j in range(8):
                if sum(board.table[i][j].poids) == max_value:
                    liste_coups_possibles.append((i, j))
        return random.choice(liste_coups_possibles)

    def random_meilleur_coup_pondere(board):
        max_value = 0
        liste_coups_possibles = []
        ponderation = 1.25
        for i in range(8):
            for j in range(8):
                value = sum(board.table[i][j].poids)
                if i == 0 or i == 7:
                    value *= ponderation
                if j == 0 or j == 7:
                    value *= ponderation
                if value > max_value:
                    max_value = value
        for i in range(8):
            for j in range(8):
                value = sum(board.table[i][j].poids)
                if i == 0 or i == 7:
                    value *= ponderation
                if j == 0 or j == 7:
                    value *= ponderation
                if value == max_value:
                    liste_coups_possibles.append((i, j))
        return random.choice(liste_coups_possibles)

    def random_pire_coup(board):
        min_value = 64
        liste_coups_possibles = []
        for i in range(8):
            for j in range(8):
                if sum(board.table[i][j].poids) > 0 and sum(board.table[i][j].poids) < min_value:
                    min_value = sum(board.table[i][j].poids)
        for i in range(8):
            for j in range(8):
                if sum(board.table[i][j].poids) == min_value:
                    liste_coups_possibles.append((i, j))
        return random.choice(liste_coups_possibles)

    def random_pire_coup_pondere(board):
        min_value = 64
        liste_coups_possibles = []
        ponderation = 0.75
        for i in range(8):
            for j in range(8):
                value = sum(board.table[i][j].poids)
                if i == 0 or i == 7:
                    value *= ponderation
                if j == 0 or j == 7:
                    value *= ponderation
                if value > 0 and value < min_value:
                    min_value = value
        for i in range(8):
            for j in range(8):
                value = sum(board.table[i][j].poids)
                if i == 0 or i == 7:
                    value *= ponderation
                if j == 0 or j == 7:
                    value *= ponderation
                if value == min_value:
                    liste_coups_possibles.append((i, j))
        return random.choice(liste_coups_possibles)
