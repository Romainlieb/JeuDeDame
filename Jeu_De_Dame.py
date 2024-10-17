import pygame  # Importer la bibliothèque Pygame pour la gestion graphique et des événements
import re  # Importer la bibliothèque re pour les expressions régulières (non utilisé dans ce code)

# Constantes
WIDTH, HEIGHT = 800, 800  # Définir la largeur et la hauteur de la fenêtre de jeu
ROWS, COLS = 8, 8  # Définir le nombre de lignes et de colonnes du plateau de jeu
SQUARE_SIZE = WIDTH // COLS  # Calculer la taille d'une case du plateau

# Couleurs
WHITE = (255, 255, 255)  # Définir la couleur blanche en RGB
BLACK = (0, 0, 0)  # Définir la couleur noire en RGB
RED = (255, 0, 0)  # Définir la couleur rouge en RGB
BLUE = (0, 0, 255)  # Définir la couleur bleue en RGB
HIGHLIGHT_COLOR = (0, 255, 0, 128)  # Définir la couleur verte avec transparence pour les surbrillances

# Initialiser Pygame
pygame.init()  # Initialiser toutes les fonctionnalités de Pygame
WIN = pygame.display.set_mode((WIDTH, HEIGHT))  # Créer une fenêtre de jeu avec les dimensions spécifiées
pygame.display.set_caption('Jeu de Dame')  # Définir le titre de la fenêtre de jeu

class JeuDeDame:
    def __init__(self):
        self.plateau = self.initialiser_plateau()  # Initialiser le plateau de jeu
        self.selected_piece = None  # Initialiser la pièce sélectionnée à None
        self.possible_moves = []  # Initialiser la liste des mouvements possibles à vide

    def initialiser_plateau(self):
        # Initialiser le plateau avec des pièces blanches et noires
        plateau = [[' ' for _ in range(8)] for _ in range(8)]  # Créer un plateau vide de 8x8
        for i in range(8):  # Parcourir les lignes du plateau
            for j in range(8):  # Parcourir les colonnes du plateau
                if (i % 2 != j % 2):  # Placer les pièces sur les cases noires uniquement
                    if i < 3:  # Placer les pièces blanches sur les trois premières lignes
                        plateau[i][j] = 'B'  # Pièces blanches
                    elif i > 4:  # Placer les pièces noires sur les trois dernières lignes
                        plateau[i][j] = 'N'  # Pièces noires
        return plateau  # Retourner le plateau initialisé

    def draw_board(self):
        # Dessiner le plateau de jeu
        WIN.fill(WHITE)  # Remplir la fenêtre de jeu avec la couleur blanche
        for row in range(ROWS):  # Parcourir les lignes du plateau
            for col in range(row % 2, COLS, 2):  # Parcourir les colonnes du plateau en alternant les cases noires
                pygame.draw.rect(WIN, BLACK, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))  # Dessiner une case noire

    def draw_pieces(self):
        # Dessiner les pièces sur le plateau
        for row in range(ROWS):  # Parcourir les lignes du plateau
            for col in range(COLS):  # Parcourir les colonnes du plateau
                piece = self.plateau[row][col]  # Obtenir la pièce à la position (row, col)
                if piece != ' ':  # Si la case n'est pas vide
                    color = RED if piece in ['B', 'D'] else BLUE  # Déterminer la couleur de la pièce (rouge pour blanc, bleu pour noir)
                    pygame.draw.circle(WIN, color, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 2 - 10)  # Dessiner la pièce
                    if piece in ['D', 'd']:  # Si la pièce est une dame
                        self.draw_dame_triangles(row, col, color)  # Dessiner les triangles pour différencier les dames

    def draw_dame_triangles(self, row, col, color):
        # Dessiner des triangles pour différencier les dames des pions
        center_x = col * SQUARE_SIZE + SQUARE_SIZE // 2  # Calculer la position x du centre de la case
        center_y = row * SQUARE_SIZE + SQUARE_SIZE // 2  # Calculer la position y du centre de la case
        radius = SQUARE_SIZE // 2 - 10  # Calculer le rayon du cercle de la pièce
        triangle_height = radius // 2  # Calculer la hauteur des triangles

        # Dessiner deux petits triangles côte à côte
        points1 = [
            (center_x - triangle_height, center_y - triangle_height),  # Point gauche du premier triangle
            (center_x, center_y - radius),  # Point supérieur du premier triangle
            (center_x + triangle_height, center_y - triangle_height)  # Point droit du premier triangle
        ]
        points2 = [
            (center_x - triangle_height, center_y + triangle_height),  # Point gauche du deuxième triangle
            (center_x, center_y + radius),  # Point inférieur du deuxième triangle
            (center_x + triangle_height, center_y + triangle_height)  # Point droit du deuxième triangle
        ]
        pygame.draw.polygon(WIN, WHITE, points1)  # Dessiner le premier triangle en blanc
        pygame.draw.polygon(WIN, WHITE, points2)  # Dessiner le deuxième triangle en blanc

    def draw_highlights(self):
        # Dessiner les mouvements possibles en surbrillance
        for move in self.possible_moves:  # Parcourir les mouvements possibles
            row, col = move  # Obtenir la position du mouvement
            pygame.draw.circle(WIN, HIGHLIGHT_COLOR, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 2 - 10)  # Dessiner un cercle en surbrillance

    def deplacer_piece(self, x1, y1, x2, y2, joueur):
        # Déplacer une pièce si le mouvement est valide
        piece = self.plateau[x1][y1]  # Obtenir la pièce à la position de départ
        if (joueur == 'Blanc' and piece not in ['B', 'D']) or (joueur == 'Noir' and piece not in ['N', 'd']):  # Vérifier si la pièce appartient au joueur
            return False  # Empêcher de déplacer les pièces de l'adversaire
        if self.mouvement_valide(x1, y1, x2, y2, joueur):  # Vérifier si le mouvement est valide
            self.plateau[x2][y2] = self.plateau[x1][y1]  # Déplacer la pièce à la nouvelle position
            self.plateau[x1][y1] = ' '  # Vider la case de départ
            if abs(x2 - x1) == 2 and abs(y2 - y1) == 2:  # Si le mouvement est une capture
                self.verifier_capture(x1, y1, x2, y2)  # Vérifier et effectuer la capture
                self.promouvoir_dame(x2, y2, joueur)  # Promouvoir en dame si applicable
                
                # Vérifier si une capture supplémentaire est possible
                while self.capture_possible_depuis(x2, y2, joueur):  # Tant qu'une capture supplémentaire est possible
                    possible_captures = self.get_possible_captures(x2, y2)  # Obtenir les captures possibles
                    if possible_captures:  # Si des captures sont possibles
                        nx, ny = possible_captures[0]  # Prendre la première capture possible
                        self.plateau[nx][ny] = self.plateau[x2][y2]  # Déplacer la pièce à la nouvelle position
                        self.plateau[x2][y2] = ' '  # Vider la case précédente
                        self.verifier_capture(x2, y2, nx, ny)  # Vérifier et effectuer la capture
                        x2, y2 = nx, ny  # Mettre à jour la position de la pièce
                    else:
                        break  # Sortir de la boucle si aucune capture n'est possible
            else:
                self.promouvoir_dame(x2, y2, joueur)  # Promouvoir en dame si applicable
            
            return True  # Retourner True si le déplacement est réussi
        return False  # Retourner False si le déplacement est invalide
    
    def capture_possible_depuis(self, x, y, joueur):
        # Vérifier si une capture est possible à partir de la position (x, y)
        piece = self.plateau[x][y]  # Obtenir la pièce à la position (x, y)
        if (joueur == 'Blanc' and piece in ['B', 'D']) or (joueur == 'Noir' and piece in ['N', 'd']):  # Vérifier si la pièce appartient au joueur
            return bool(self.get_possible_captures(x, y))  # Retourner True si des captures sont possibles, sinon False
        return False  # Retourner False si la pièce n'appartient pas au joueur

    def mouvement_valide(self, x1, y1, x2, y2, joueur):
        # Vérifier si un mouvement est valide
        if 0 <= x2 < 8 and 0 <= y2 < 8 and self.plateau[x2][y2] == ' ':  # Vérifier si la destination est dans les limites du plateau et la case est vide
            piece = self.plateau[x1][y1]  # Obtenir la pièce à la position de départ
            if piece in ['B', 'N']:  # Si la pièce est un pion (blanc ou noir)
                if abs(x2 - x1) == 1 and abs(y2 - y1) == 1:  # Mouvement simple en diagonale d'une case
                    return not self.capture_possible(joueur)  # Valide si aucune capture n'est possible
                if abs(x2 - x1) == 2 and abs(y2 - y1) == 2:  # Mouvement de capture en diagonale de deux cases
                    x_capture = (x1 + x2) // 2  # Calculer la position de la pièce capturée
                    y_capture = (y1 + y2) // 2
                    if (piece == 'B' and self.plateau[x_capture][y_capture] in ['N', 'd']) or \
                    (piece == 'N' and self.plateau[x_capture][y_capture] in ['B', 'D']):  # Valide si la pièce capturée est une pièce ennemie
                        return True
            elif piece in ['D', 'd']:  # Si la pièce est une dame (blanche ou noire)
                if abs(x2 - x1) == abs(y2 - y1):  # Mouvement en diagonale
                    x_step = 1 if x2 > x1 else -1  # Déterminer la direction du mouvement en x
                    y_step = 1 if y2 > y1 else -1  # Déterminer la direction du mouvement en y
                    x, y = x1 + x_step, y1 + y_step
                    enemy_piece_found = False  # Indicateur pour savoir si une pièce ennemie a été trouvée
                    while x != x2 and y != y2:
                        if self.plateau[x][y] != ' ':
                            if enemy_piece_found or self.plateau[x][y] not in ['B', 'D', 'N', 'd']:
                                return False  # Mouvement invalide si une case intermédiaire n'est pas vide ou contient une pièce alliée
                            enemy_piece_found = True  # Marquer qu'une pièce ennemie a été trouvée
                        x += x_step
                        y += y_step
                    return enemy_piece_found  # Mouvement valide si une capture est possible
        return False  # Mouvement invalide si aucune des conditions ci-dessus n'est remplie

    def verifier_capture(self, x1, y1, x2, y2):
        # Vérifier et effectuer la capture d'une pièce
        if abs(x2 - x1) == 2 and abs(y2 - y1) == 2:  # Si le mouvement est une capture en diagonale de deux cases
            x_capture = (x1 + x2) // 2  # Calculer la position de la pièce capturée
            y_capture = (y1 + y2) // 2
            self.plateau[x_capture][y_capture] = ' '  # Enlever la pièce capturée
        elif abs(x2 - x1) > 2 and abs(y2 - y1) > 2:  # Capture multiple pour les dames
            x_step = 1 if x2 > x1 else -1  # Déterminer la direction du mouvement en x
            y_step = 1 if y2 > y1 else -1  # Déterminer la direction du mouvement en y
            x, y = x1 + x_step, y1 + y_step
            while x != x2 and y != y2:
                if self.plateau[x][y] in ['B', 'D', 'N', 'd']:
                    self.plateau[x][y] = ' '  # Enlever la pièce capturée
                    break
                x += x_step
                y += y_step

    def promouvoir_dame(self, x, y, joueur):
        # Promouvoir un pion en dame
        if self.plateau[x][y] == 'B' and x == 7:  # Si un pion blanc atteint la dernière ligne
            self.plateau[x][y] = 'D'  # Promouvoir en dame blanche
            print(f"Le joueur {joueur} a fait apparaître une dame blanche.")
        elif self.plateau[x][y] == 'N' and x == 0:  # Si un pion noir atteint la première ligne
            self.plateau[x][y] = 'd'  # Promouvoir en dame noire
            print(f"Le joueur {joueur} a fait apparaître une dame noire.")

    def partie_terminee(self):
        # Vérifier si la partie est terminée
        pieces_blanches = sum(ligne.count('B') + ligne.count('D') for ligne in self.plateau)  # Compter les pièces blanches
        pieces_noires = sum(line.count('N') + line.count('d') for line in self.plateau)  # Compter les pièces noires
        return pieces_blanches == 0 or pieces_noires == 0  # Retourner True si l'un des joueurs n'a plus de pièces

    def capture_possible(self, joueur):
        # Vérifier si une capture est possible pour le joueur actuel
        for x in range(8):  # Parcourir les lignes du plateau
            for y in range(8):  # Parcourir les colonnes du plateau
                piece = self.plateau[x][y]  # Obtenir la pièce à la position (x, y)
                if (joueur == 'Blanc' and piece in ['B', 'D']) or (joueur == 'Noir' and piece in ['N', 'd']):  # Vérifier si la pièce appartient au joueur
                    if self.get_possible_captures(x, y):  # Vérifier si des captures sont possibles
                        return True  # Retourner True si une capture est possible
        return False  # Retourner False si aucune capture n'est possible

    def get_possible_captures(self, x, y):
        # Obtenir les captures possibles pour une pièce
        piece = self.plateau[x][y]  # Obtenir la pièce à la position (x, y)
        captures = []  # Liste pour stocker les captures possibles
        directions = [(-2, -2), (-2, 2), (2, -2), (2, 2)]  # Directions pour les captures en diagonale

        if piece in ['B', 'N']:  # Si la pièce est un pion (blanc ou noir)
            for dx, dy in directions:  # Pour chaque direction diagonale possible
                nx, ny = x + dx, y + dy  # Calculer la prochaine position en diagonale
                if self.mouvement_valide(x, y, nx, ny, 'Blanc' if piece in ['B', 'D'] else 'Noir'):  # Vérifier si le mouvement est valide pour le joueur correspondant
                    captures.append((nx, ny))  # Ajouter la position de capture possible à la liste

        elif piece in ['D', 'd']:  # Si la pièce est une dame (blanche ou noire)
            for dx, dy in directions:  # Pour chaque direction diagonale possible
                nx, ny = x + dx, y + dy  # Calculer la prochaine position en diagonale
                while 0 <= nx < 8 and 0 <= ny < 8:
                    if self.plateau[nx][ny] != ' ':
                        if self.plateau[nx][ny] in ['B', 'D', 'N', 'd'] and \
                           ((piece == 'D' and self.plateau[nx][ny] in ['N', 'd']) or \
                            (piece == 'd' and self.plateau[nx][ny] in ['B', 'D'])):
                            nx += dx
                            ny += dy
                            if 0 <= nx < 8 and 0 <= ny < 8 and self.plateau[nx][ny] == ' ':
                                captures.append((nx, ny))
                        break
                    nx += dx
                    ny += dy

        return captures  # Retourner la liste des captures possibles

    def get_possible_moves(self, x, y, joueur):
        # Obtenir les mouvements possibles pour une pièce
        piece = self.plateau[x][y]  # Obtenir la pièce à la position (x, y)
        if (joueur == 'Blanc' and piece not in ['B', 'D']) or (joueur == 'Noir' and piece not in ['N', 'd']):
            return []  # Ne pas montrer les mouvements possibles pour les pièces de l'adversaire

        moves = []  # Liste pour stocker les mouvements possibles
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # Directions pour les mouvements en diagonale

        if piece in ['B', 'N']:  # Si la pièce est un pion (blanc ou noir)
            for dx, dy in directions:  # Pour chaque direction diagonale possible
                nx, ny = x + dx, y + dy  # Calculer la prochaine position en diagonale
                if self.mouvement_valide(x, y, nx, ny, joueur):
                    # Vérifier si le mouvement est valide pour le joueur correspondant
                    moves.append((nx, ny))  # Ajouter la position de mouvement possible à la liste
                nx, ny = x + 2 * dx, y + 2 * dy  # Calculer la position pour un mouvement de capture
                if self.mouvement_valide(x, y, nx, ny, joueur):
                    # Vérifier si le mouvement de capture est valide pour le joueur correspondant
                    moves.append((nx, ny))  # Ajouter la position de mouvement de capture possible à la liste

        elif piece in ['D', 'd']:  # Si la pièce est une dame (blanche ou noire)
            for dx, dy in directions:  # Pour chaque direction diagonale possible
                nx, ny = x + dx, y + dy  # Calculer la prochaine position en diagonale
                while 0 <= nx < 8 and 0 <= ny < 8 and self.plateau[nx][ny] == ' ':
                    moves.append((nx, ny))
                    nx += dx
                    ny += dy
                nx, ny = x + 2 * dx, y + 2 * dy  # Calculer la position pour un mouvement de capture
                if self.mouvement_valide(x, y, nx, ny, joueur):
                    # Vérifier si le mouvement de capture est valide pour le joueur correspondant
                    moves.append((nx, ny))  # Ajouter la position de mouvement de capture possible à la liste

        return moves  # Retourner la liste des mouvements possibles

    def jouer(self):
        # Boucle principale du jeu
        joueur = 'Blanc'
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    row, col = pos[1] // SQUARE_SIZE, pos[0] // SQUARE_SIZE
                    if self.selected_piece:
                        x1, y1 = self.selected_piece
                        if self.deplacer_piece(x1, y1, row, col, joueur):
                            joueur = 'Noir' if joueur == 'Blanc' else 'Blanc'
                        self.selected_piece = None
                        self.possible_moves = []
                    else:
                        self.selected_piece = (row, col)
                        self.possible_moves = self.get_possible_moves(row, col, joueur)

            self.draw_board()
            self.draw_pieces()
            self.draw_highlights()
            pygame.display.update()

        pygame.quit()

if __name__ == "__main__":
    jeu = JeuDeDame()
    jeu.jouer()