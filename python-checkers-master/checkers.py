import pygame as pg
from sys import exit, argv
from pygame.locals import *
from board_gui import BoardGUI
from game_control import GameControl

def display_board_console(board):
    """
    Affiche le plateau de jeu dans la console avec toutes les cases entourées par des |.
    Les cases jouables affichent leur contenu (pièce ou vide), et les non jouables sont vides.
    """
    print("\nPlateau de jeu :")
    for row in range(8):
        row_display = []
        for col in range(8):
            # Calcul de la position sur un plateau de 32 cases
            if (col//2)+(row*8) % 2 != 0:  # Case jouable (sombre)
                #position = row * 4 + (col // 2)
                piece = board.get_pieces_by_coords((col,row))
                row_display.append(f" {piece[0]} ")
            else:  # Case non jouable (claire)
                row_display.append("    ")

        # Afficher la ligne avec des séparateurs
        print("|" + "|".join(row_display) + "|")
        print("-" * 65)  # Ligne de séparation


def play_without_gui(game_control):
    """
    Mode de jeu sans interface graphique.
    Gère les mouvements des joueurs et de l'IA via la console.
    """
    while game_control.get_winner() is None:
        display_board_console(game_control.board)
        
        turn = game_control.get_turn()
        print(f"Tour de {'Blancs' if turn == 'W' else 'Noirs'}")

        # Définir les actions possibles
        valid_actions = game_control.board.get_valid_actions()
        if not valid_actions:
            print(f"Pas d'actions possibles pour {'Blancs' if turn == 'W' else 'Noirs'}.")
            break

        # Simulation pour l'IA (exemple : choix aléatoire pour l'instant)
        from random import choice
        action = choice(valid_actions)
        print(f"Action choisie par {'IA Blancs' if turn == 'W' else 'IA Noirs'} : {action}")

        # Effectuer le mouvement
        game_control.board.move_piece(*action)
        game_control.switch_turn(game_control.board.get_piece_by_index(action[1]))

    # Fin du jeu
    display_board_console(game_control.board)
    winner = game_control.get_winner()
    print(f"Le gagnant est : {'Blancs' if winner == 'W' else 'Noirs' if winner == 'B' else 'Aucun'}")

def main():
    # Choisir le mode avec ou sans GUI
    use_gui = '--gui' in argv

    if use_gui:
        # Mode graphique
        pg.init()
        FPS = 165
        DISPLAYSURF = pg.display.set_mode((700, 500))
        pg.display.set_caption('Checkers in Python')
        fps_clock = pg.time.Clock()
        game_control = GameControl()

        # Font setup
        main_font = pg.font.SysFont("Arial", 25)
        turn_rect = (509, 26)
        winner_rect = (509, 152)

        while True:
            # GUI
            DISPLAYSURF.fill((0, 0, 0))
            game_control.draw_screen(DISPLAYSURF)

            turn_display_text = "White's turn" if game_control.get_turn() == "W" else "Black's turn"
            DISPLAYSURF.blit(main_font.render(turn_display_text, True, (255, 255, 255)), turn_rect)

            if game_control.get_winner() is not None:
                winner_display_text = "White wins!" if game_control.get_winner() == "W" else "Black wins!"
                DISPLAYSURF.blit(main_font.render(winner_display_text, True, (255, 255, 255)), winner_rect)

            # Event handling
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    return

                if event.type == MOUSEBUTTONUP:
                    game_control.hold_piece(event.pos)

                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        game_control.board.move_piece(8, 12)  # Bouge la pièce

                if event.type == MOUSEBUTTONDOWN:
                    game_control.release_piece()

            pg.display.update()
            fps_clock.tick(FPS)

    else:
        # Mode console
        print("Lancement en mode console...")
        game_control = GameControl()
        play_without_gui(game_control)

if __name__ == '__main__':
    main()
    exit()
