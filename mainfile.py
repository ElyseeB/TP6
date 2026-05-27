import random
import arcade
from game_state import GameState
from attack_anim import AttackType, AttackAnimation

# Constantes de la fenêtre
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 750
SCREEN_TITLE = "Roche, papier, ciseaux"


class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Définition de la couleur de fond (gris foncé comme dans les captures d'écran)
        arcade.set_background_color((54, 54, 54))

        # Variables de pointage
        self.player_score = 0
        self.computer_score = 0

        # État initial du jeu
        self.game_state = GameState.NOT_STARTED

        # Variables pour stocker les choix d'attaques
        self.player_attack_type = None
        self.computer_attack_type = None

        # Sprites d'attaques pour le joueur
        self.rock = None
        self.paper = None
        self.scissors = None

        # Sprite dynamique pour l'attaque choisie par l'ordinateur
        self.computer_attack_sprite = None

        # Chaîne de texte pour afficher le résultat d'une ronde
        self.round_result_text = ""

        # Chargement des avatars statiques du joueur et de l'ordinateur
        # (Ajustez les chemins ou noms de fichiers si nécessaire)
        self.player_avatar = arcade.Sprite("assets/faceBeard.png", scale=0.6)
        self.player_avatar.center_x = 250
        self.player_avatar.center_y = 380

        self.computer_avatar = arcade.Sprite("assets/compy.png", scale=0.6)
        self.computer_avatar.center_x = 750
        self.computer_avatar.center_y = 380

        # Initialisation des éléments de jeu
        self.setup()

    def setup(self):
        """ Initialise ou réinitialise les positions des sprites d'attaque """
        self.rock = AttackAnimation(AttackType.ROCK)
        self.rock.center_x = 150
        self.rock.center_y = 200

        self.paper = AttackAnimation(AttackType.PAPER)
        self.paper.center_x = 250
        self.paper.center_y = 200

        self.scissors = AttackAnimation(AttackType.SCISSORS)
        self.scissors.center_x = 350
        self.scissors.center_y = 200

    def on_draw(self):
        """ Rendu graphique de l'écran """
        self.clear()

        # --- 1. AFFICHAGE DES ÉLÉMENTS STATIQUES ---
        # Titre principal du jeu
        arcade.draw_text("Roche, papier, ciseaux", SCREEN_WIDTH / 2, 660,
                         arcade.color.RED_DEVIL, font_size=50, bold=True, anchor_x="center")

        # Dessiner les avatars du joueur et de l'ordinateur
        self.player_avatar.draw()
        self.computer_avatar.draw()


        arcade.draw_rectangle_outline(150, 200, 90, 90, arcade.color.PINK, border_width=2)
        arcade.draw_rectangle_outline(250, 200, 90, 90, arcade.color.PINK, border_width=2)
        arcade.draw_rectangle_outline(350, 200, 90, 90, arcade.color.PINK, border_width=2)


        arcade.draw_rectangle_outline(750, 200, 90, 90, arcade.color.PINK, border_width=2)



        arcade.draw_text(f"Le pointage du joueur est {self.player_score}", 250, 100,
                         arcade.color.WHITE, font_size=20, anchor_x="center")
        arcade.draw_text(f"Le pointage de l'ordinateur est {self.computer_score}", 750, 100,
                         arcade.color.WHITE, font_size=20, anchor_x="center")


        if self.game_state == GameState.NOT_STARTED:
            arcade.draw_text("Appuyer sur 'ESPACE' pour débuter une ronde!", SCREEN_WIDTH / 2, 570,
                             arcade.color.LIGHT_BLUE, font_size=24, anchor_x="center")

        elif self.game_state == GameState.ROUND_ACTIVE:
            arcade.draw_text("Appuyer sur une image pour faire une attaque!", SCREEN_WIDTH / 2, 570,
                             arcade.color.LIGHT_BLUE, font_size=24, anchor_x="center")

            self.rock.draw()
            self.paper.draw()
            self.scissors.draw()

        elif self.game_state == GameState.ROUND_DONE:
            arcade.draw_text("Appuyer sur 'ESPACE' pour commencer une nouvelle ronde!", SCREEN_WIDTH / 2, 570,
                             arcade.color.LIGHT_BLUE, font_size=24, anchor_x="center")
            # Affiche le résultat texte au centre
            arcade.draw_text(self.round_result_text, SCREEN_WIDTH / 2, 480,
                             arcade.color.LIGHT_GREEN, font_size=26, anchor_x="center")

            # Affiche uniquement l'attaque sélectionnée par le joueur dans son carré respectif
            if self.player_attack_type == AttackType.ROCK:
                self.rock.draw()
            elif self.player_attack_type == AttackType.PAPER:
                self.paper.draw()
            elif self.player_attack_type == AttackType.SCISSORS:
                self.scissors.draw()

            # Affiche l'attaque choisie par l'ordinateur
            if self.computer_attack_sprite:
                self.computer_attack_sprite.draw()

        elif self.game_state == GameState.GAME_OVER:
            # Détermination du grand gagnant de la partie (premier à 3 points)
            if self.player_score >= 3:
                final_msg = "Vous avez gagné la partie!"
            else:
                final_msg = "L'ordinateur a gagné la partie!"

            arcade.draw_text(final_msg, SCREEN_WIDTH / 2, 500, arcade.color.GOLD, font_size=30, anchor_x="center")
            arcade.draw_text("La partie est terminée.", SCREEN_WIDTH / 2, 450, arcade.color.WHITE, font_size=22,
                             anchor_x="center")
            arcade.draw_text("Appuyer sur 'ESPACE' pour débuter une nouvelle partie", SCREEN_WIDTH / 2, 380,
                             arcade.color.LIGHT_BLUE, font_size=20, anchor_x="center")

    def on_update(self, delta_time):
        """ Logique d'animation et mise à jour des sprites """
        # On met à jour l'animation des sprites selon l'état actuel pour qu'ils s'animent de façon fluide
        if self.game_state == GameState.ROUND_ACTIVE:
            self.rock.on_update(delta_time)
            self.paper.on_update(delta_time)
            self.scissors.on_update(delta_time)

        elif self.game_state in [GameState.ROUND_DONE, GameState.GAME_OVER]:
            # Garder animé uniquement l'attaque choisie par le joueur
            if self.player_attack_type == AttackType.ROCK:
                self.rock.on_update(delta_time)
            elif self.player_attack_type == AttackType.PAPER:
                self.paper.on_update(delta_time)
            elif self.player_attack_type == AttackType.SCISSORS:
                self.scissors.on_update(delta_time)

            # Garder animé l'attaque choisie par l'ordinateur
            if self.computer_attack_sprite:
                self.computer_attack_sprite.on_update(delta_time)

    def on_key_press(self, key, key_modifiers):
        """ Gestion des touches du clavier """
        if key == arcade.key.SPACE:
            if self.game_state == GameState.NOT_STARTED:
                self.game_state = GameState.ROUND_ACTIVE

            elif self.game_state == GameState.ROUND_DONE:
                # Nettoyage des flags et variables de validation de la ronde précédente
                self.player_attack_type = None
                self.computer_attack_type = None
                self.computer_attack_sprite = None
                self.game_state = GameState.ROUND_ACTIVE

            elif self.game_state == GameState.GAME_OVER:
                # Remise à zéro complète pour une toute nouvelle partie
                self.player_score = 0
                self.computer_score = 0
                self.player_attack_type = None
                self.computer_attack_type = None
                self.computer_attack_sprite = None
                self.game_state = GameState.ROUND_ACTIVE

    def on_mouse_press(self, x, y, button, key_modifiers):
        """ Gestion des clics de souris pour sélectionner une attaque """
        if self.game_state == GameState.ROUND_ACTIVE:
            # Vérification du clic sur l'un des trois sprites à l'aide de collides_with_point
            clicked = False
            if self.rock.collides_with_point((x, y)):
                self.player_attack_type = AttackType.ROCK
                clicked = True
            elif self.paper.collides_with_point((x, y)):
                self.player_attack_type = AttackType.PAPER
                clicked = True
            elif self.scissors.collides_with_point((x, y)):
                self.player_attack_type = AttackType.SCISSORS
                clicked = True

            if clicked:
                # 1. Génération de l'attaque aléatoire de l'ordinateur
                pc_attack = random.randint(0, 2)
                if pc_attack == 0:
                    self.computer_attack_type = AttackType.ROCK
                    self.computer_attack_sprite = AttackAnimation(AttackType.ROCK)
                elif pc_attack == 1:
                    self.computer_attack_type = AttackType.PAPER
                    self.computer_attack_sprite = AttackAnimation(AttackType.PAPER)
                else:
                    self.computer_attack_type = AttackType.SCISSORS
                    self.computer_attack_sprite = AttackAnimation(AttackType.SCISSORS)

                # Positionnement du sprite de l'ordinateur dans son carré (à droite)
                self.computer_attack_sprite.center_x = 750
                self.computer_attack_sprite.center_y = 200

                # 2. Validation des règles pour déterminer le vainqueur de la ronde
                if self.player_attack_type == self.computer_attack_type:
                    self.round_result_text = "Égalité !"
                elif (
                        self.player_attack_type == AttackType.ROCK and self.computer_attack_type == AttackType.SCISSORS) or \
                        (
                                self.player_attack_type == AttackType.PAPER and self.computer_attack_type == AttackType.ROCK) or \
                        (
                                self.player_attack_type == AttackType.SCISSORS and self.computer_attack_type == AttackType.PAPER):
                    self.round_result_text = "Le joueur a gagné la ronde !"
                    self.player_score += 1
                else:
                    self.round_result_text = "L'ordinateur à gagné la ronde !"
                    self.computer_score += 1

                # 3. Vérification si un joueur a atteint le score maximal de 3 victoires
                if self.player_score >= 3 or self.computer_score >= 3:
                    self.game_state = GameState.GAME_OVER
                else:
                    self.game_state = GameState.ROUND_DONE


def main():
    window = MyGame()
    arcade.run()


if __name__ == "__main__":
    main()