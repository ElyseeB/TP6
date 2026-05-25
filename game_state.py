from enum import Enum

class GameState(Enum):
    NOT_STARTED = 0   # Le jeu commence dans cet état (écran d'accueil)
    ROUND_ACTIVE = 1  # Le joueur choisit son attaque
    ROUND_DONE = 2    # Une ronde vient de se terminer, on affiche le gagnant de la ronde
    GAME_OVER = 3     # Un joueur a atteint 3 points, la partie est finie