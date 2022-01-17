from utils.cell import Cell
from utils.ia import Ia


class Board(Cell):
    def __init__(self):
        self.trigger = 0
        self.table = []
        for i in range(8):
            self.table.append([])
            for j in range(8):
                if (i == 3 and j == 3) or (i == 4 and j == 4):
                    self.table[i].append(Cell((i, j), "noir"))
                elif (i == 3 and j == 4) or (i == 4 and j == 3):
                    self.table[i].append(Cell((i, j), "blanc"))
                else:
                    self.table[i].append(Cell((i, j), "vide"))

    def next_joueur(self, joueur1, joueur2):
        if joueur1.is_actif:
            joueur1.is_actif = False
            joueur2.is_actif = True
            return joueur2, joueur1
        else:
            joueur2.is_actif = False
            joueur1.is_actif = True
            return joueur1, joueur2

    def calcul_poids(self, joueur):
        """Calcul le poids de chaque cellules composant le plateau"""
        offsets = [(-1, 0), (1, 0), (0, 1), (0, -1),
                   (1, 1), (1, -1), (-1, 1), (-1, -1)]
        for ligne in range(8):
            for col in range(8):
                current_cell = self.table[ligne][col]
                if current_cell.couleur == "vide":
                    # print(current_cell.coordonnee)  # to test
                    i = 0
                    current_cell.poids[i] = 0
                    for offset in offsets:
                        # print("offset", offset)  # to test
                        count = 1
                        do_i_continue = True
                        while do_i_continue:
                            try:
                                voisin = self.table[ligne + count *
                                                    offset[0]][col + count * offset[1]]
                                if ligne + count * offset[0] < 0 or col + count * offset[1] < 0:
                                    raise IndexError
            # 3 cas: soit il est vide -> on arrete, soit il est de la même couleur -> on arrete, soit il est de la couleur opposée -> on continue
                                elif voisin.couleur == joueur.couleur:
                                    do_i_continue = False
                                elif voisin.couleur == "vide":
                                    do_i_continue = False
                                    count = 1
                                else:  # couleur adverse
                                    count += 1
                            except IndexError:
                                do_i_continue = False
                                count = 1
                        # print(count)
                        current_cell.poids[i] = count - 1
                        i += 1
                else:
                    current_cell.poids = [0, 0, 0, 0, 0, 0, 0, 0]

    def joueur_actif_peut_jouer(self, joueur):
        # trigger=0 -> un joueur vient de jouer
        # trigger=1 -> le joueur précédent n'a pas pu jouer
        # trigger=2 -> le joueur actif n'a pas pu jouer alors que trigger était à 1
        # Si pas de coup possible trigger +=1 et return False
        # si au moins un coup possible trigger = 0  et return True
        for i in range(8):
            for j in range(8):
                if sum(self.table[i][j].poids) > 0:
                    self.trigger = 0
                    return True
        self.trigger += 1
        print("Vous ne pouvez pas jouer")
        return False

    def choix_joueur(self, joueur):
        # input et check validité
        # while is_coup_valide:
        # Demande d'input et vérification de la validité et du format de l'input
        if isinstance(joueur, Ia):
            print("L'IA est en train réfléchir.")
            (ligne, col) = joueur.choix_niveau(self)
            print("L'IA joue le coup :", (ligne, col))
        else:
            is_wrong = True
            set_col = {"A", "B", "C", "D", "E", "F", "G", "H"}
            set_ligne = {"1", "2", "3", "4", "5", "6", "7", "8"}
            while is_wrong:
                case_jouer_brut = input(
                    'Sur quelle case voulez vous jouer ? (Colonne + Ligne : "G5")')
                if len(case_jouer_brut) != 2:
                    print("Mauvaise entrée...recommencez...")
                    continue
                elif not case_jouer_brut[0].upper() in set_col:
                    print("Colonne inexistante...recommencez...")
                    continue
                elif not case_jouer_brut[1] in set_ligne:
                    print("Ligne inexistante...recommencez...")
                    continue
                # Conversion de l'input en ligne et colonne
                col_brut = case_jouer_brut[0].upper()
                if col_brut == "A":
                    col = 0
                elif col_brut == "B":
                    col = 1
                elif col_brut == "C":
                    col = 2
                elif col_brut == "D":
                    col = 3
                elif col_brut == "E":
                    col = 4
                elif col_brut == "F":
                    col = 5
                elif col_brut == "G":
                    col = 6
                elif col_brut == "H":
                    col = 7
                ligne = int(case_jouer_brut[1])-1
                # Vérification de la validité du coup
                if sum(self.table[ligne][col].poids) == 0:
                    print("Ce coup n'est pas valide, choisissez-en un autre.")
                else:
                    is_wrong = False
        return (ligne, col)

    def maj_board(self, coup, joueur_actif, joueur_inactif):
        # met a jour le plateau de
        # modifie le score
        # On récupère une lsite de direction avec le poids pour chaque direction
        # (ligne, colonne)
        current_cell = self.table[coup[0]][coup[1]]
        current_cell.couleur = joueur_actif.couleur
        offsets = [(-1, 0), (1, 0), (0, 1), (0, -1),
                   (1, 1), (1, -1), (-1, 1), (-1, -1)]
        for i, offset in enumerate(offsets):
            for j in range(current_cell.poids[i]):
                self.table[coup[0] + (j+1)*offset[0]][coup[1]
                                                      + (j+1)*offset[1]].couleur = joueur_actif.couleur
        self.calcul_score(joueur_actif, joueur_inactif)

    def calcul_score(self, joueur1, joueur2):
        score_blanc = 0
        score_noir = 0
        for ligne in range(8):
            for col in range(8):
                if self.table[ligne][col].couleur == "noir":
                    score_noir += 1
                elif self.table[ligne][col].couleur == "blanc":
                    score_blanc += 1
        if joueur1.couleur == "noir":
            joueur1.score = score_noir
            joueur2.score = score_blanc
        else:
            joueur2.score = score_blanc
            joueur1.score = score_noir

    def afficher_board(self):
        map = f"    A   B   C   D   E   F   G   H\n"
        map += f"  +---+---+---+---+---+---+---+---+\n"
        for i in range(8):
            map += f"{int(i+1)} | "
            for j in range(8):
                if self.table[i][j].couleur == "noir":
                    value = "X"
                elif self.table[i][j].couleur == "blanc":
                    value = "O"
                else:
                    value = " "
                map += f"{value} | "
            map += f"\n  +---+---+---+---+---+---+---+---+\n"
        print(map)

    def fin_du_jeu(self, joueur1, joueur2):
        # Merci d'avoir joué
        # affiche le score
        self.calcul_score(joueur1, joueur2)

        if joueur1.score > joueur2.score:
            joueur_win = f"Le joueur {joueur1.couleur} a gagné ! Félicitation"
        elif joueur1.score < joueur2.score:
            joueur_win = f"Le joueur {joueur2.couleur} a gagné ! Félicitation"
        else:
            joueur_win = f"Les joueurs {joueur1.couleur} et {joueur2.couleur} sont execo. Félicitation à vous deux"
        message = f"""
        Partie terminé
        Score :
        {joueur1.couleur} -> {joueur1.score}
        {joueur2.couleur} -> {joueur2.score}
        """
        message += joueur_win

        print(message)

    def afficher_board_debug(self):
        map = f"    A   B   C   D   E   F   G   H\n"
        map += f"  +---+---+---+---+---+---+---+---+\n"
        for i in range(8):
            map += f"{int(i+1)} | "
            for j in range(8):
                value = sum(self.table[i][j].poids)
                map += f"{value} | "
            map += f"\n  +---+---+---+---+---+---+---+---+\n"
        print(map)
