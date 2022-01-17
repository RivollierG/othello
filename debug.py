from utils.board import Board
from utils.player import Player
from utils.ia import Ia

# Initialisation

joueur1 = Ia("noir")
joueur2 = Player("blanc")
plateau = Board()

joueur1.is_actif = True
print(type(joueur1))

if isinstance(joueur1, Ia):
    print("ça marche !!!")

# plateau.calcul_poids(joueur1)
# for i in range(8):
#     for j in range(8):
#         print(i, j, plateau.table[i][j].poids)
