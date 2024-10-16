import pygame
import re

# Constantes
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
HIGHLIGHT_COLOR = (0, 255, 0, 128)  # Vert avec transparence

# Initialiser Pygame
pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Jeu de Dame')

class JeuDeDame:
    def __init__(self):
        self.plateau = self.initialiser_plateau()
        self.selected_piece = None
        self.possible_moves = []

    def initialiser_plateau(self):
        # Initialiser le plateau avec des pièces blanches et noires
        plateau = [[' ' for _ in range(8)] for _ in range(8)]
        for i in range(8):
            for j in range(8):
                if (i % 2 != j % 2):
                    if i < 3:
                        plateau[i][j] = 'B'  # Pièces blanches
                    elif i > 4:
                        plateau[i][j] = 'N'  # Pièces noires
        return plateau

    def draw_board(self):
        # Dessiner le plateau de jeu
        WIN.fill(WHITE)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(WIN, BLACK, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def draw_pieces(self):
        # Dessiner les pièces sur le plateau
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.plateau[row][col]
                if piece != ' ':
                    color = RED if piece in ['B', 'D'] else BLUE
                    pygame.draw.circle(WIN, color, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 2 - 10)
                    if piece in ['D', 'd']:
                        self.draw_dame_triangles(row, col, color)

    def draw_dame_triangles(self, row, col, color):
        # Dessiner des triangles pour différencier les dames des pions
        center_x = col * SQUARE_SIZE + SQUARE_SIZE // 2
        center_y = row * SQUARE_SIZE + SQUARE_SIZE // 2
        radius = SQUARE_SIZE // 2 - 10
        triangle_height = radius // 2

        # Dessiner deux petits triangles côte à côte
        points1 = [
            (center_x - triangle_height, center_y - triangle_height),
            (center_x, center_y - radius),
            (center_x + triangle_height, center_y - triangle_height)
        ]
        points2 = [
            (center_x - triangle_height, center_y + triangle_height),
            (center_x, center_y + radius),
            (center_x + triangle_height, center_y + triangle_height)
        ]
        pygame.draw.polygon(WIN, WHITE, points1)
        pygame.draw.polygon(WIN, WHITE, points2)

    def draw_highlights(self):
        # Dessiner les mouvements possibles en surbrillance
        for move in self.possible_moves:
            row, col = move
            pygame.draw.circle(WIN, HIGHLIGHT_COLOR, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 2 - 10)

    def deplacer_piece(self, x1, y1, x2, y2, joueur):
        # Déplacer une pièce si le mouvement est valide
        piece = self.plateau[x1][y1]
        if (joueur == 'Blanc' and piece not in ['B', 'D']) or (joueur == 'Noir' and piece not in ['N', 'd']):
            return False  # Empêcher de déplacer les pièces de l'adversaire
        if self.mouvement_valide(x1, y1, x2, y2, joueur):
            self.plateau[x2][y2] = self.plateau[x1][y1]
            self.plateau[x1][y1] = ' '
            self.verifier_capture(x1, y1, x2, y2)
            self.promouvoir_dame(x2, y2)
            return True
        return False

    def mouvement_valide(self, x1, y1, x2, y2, joueur):
        # Vérifier si un mouvement est valide
        if 0 <= x2 < 8 and 0 <= y2 < 8 and self.plateau[x2][y2] == ' ':
            piece = self.plateau[x1][y1]
            if piece == 'B':
                if x2 > x1 and abs(x2 - x1) == 1 and abs(y2 - y1) == 1:
                    return not self.capture_possible(joueur)
                if x2 > x1 and abs(x2 - x1) == 2 and abs(y2 - y1) == 2:
                    x_capture = (x1 + x2) // 2
                    y_capture = (y1 + y2) // 2
                    if self.plateau[x_capture][y_capture] in ['N', 'd']:
                        return True
            elif piece == 'N':
                if x2 < x1 and abs(x2 - x1) == 1 and abs(y2 - y1) == 1:
                    return not self.capture_possible(joueur)
                if x2 < x1 and abs(x2 - x1) == 2 and abs(y2 - y1) == 2:
                    x_capture = (x1 + x2) // 2
                    y_capture = (y1 + y2) // 2
                    if self.plateau[x_capture][y_capture] in ['B', 'D']:
                        return True
            elif piece in ['D', 'd']:  # Dame blanche ou noire
                if abs(x2 - x1) == abs(y2 - y1):
                    x_step = 1 if x2 > x1 else -1
                    y_step = 1 if y2 > y1 else -1
                    x, y = x1 + x_step, y1 + y_step
                    while x != x2 and y != y2:
                        if self.plateau[x][y] != ' ':
                            return False
                        x += x_step
                        y += y_step
                    # Vérifier la capture pour les dames
                    if abs(x2 - x1) >= 2:
                        x_capture = (x1 + x2) // 2
                        y_capture = (y1 + y2) // 2
                        if (piece == 'D' and self.plateau[x_capture][y_capture] in ['N', 'd']) or \
                        (piece == 'd' and self.plateau[x_capture][y_capture] in ['B', 'D']):
                            return True
                    return not self.capture_possible(joueur)
        return False

    def verifier_capture(self, x1, y1, x2, y2):
        # Vérifier et effectuer la capture d'une pièce
        if abs(x2 - x1) >= 2 and abs(y2 - y1) >= 2:
            x_capture = (x1 + x2) // 2
            y_capture = (y1 + y2) // 2
            self.plateau[x_capture][y_capture] = ' '

    def promouvoir_dame(self, x, y):
        # Promouvoir un pion en dame
        if self.plateau[x][y] == 'B' and x == 7:
            self.plateau[x][y] = 'D'  # Dame blanche
        elif self.plateau[x][y] == 'N' and x == 0:
            self.plateau[x][y] = 'd'  # Dame noire

    def partie_terminee(self):
        # Vérifier si la partie est terminée
        pieces_blanches = sum(ligne.count('B') + ligne.count('D') for ligne in self.plateau)
        pieces_noires = sum(ligne.count('N') + ligne.count('d') for ligne in self.plateau)
        return pieces_blanches == 0 or pieces_noires == 0

    def capture_possible(self, joueur):
        # Vérifier si une capture est possible pour le joueur actuel
        for x in range(8):
            for y in range(8):
                piece = self.plateau[x][y]
                if (joueur == 'Blanc' and piece in ['B', 'D']) or (joueur == 'Noir' and piece in ['N', 'd']):
                    if self.get_possible_captures(x, y):
                        return True
        return False

    def get_possible_captures(self, x, y):
        # Obtenir les captures possibles pour une pièce
        piece = self.plateau[x][y]
        captures = []
        directions = [(-2, -2), (-2, 2), (2, -2), (2, 2)]
        if piece in ['B', 'N']:
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if self.mouvement_valide(x, y, nx, ny, 'Blanc' if piece in ['B', 'D'] else 'Noir'):
                    captures.append((nx, ny))
        elif piece in ['D', 'd']:
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                while 0 <= nx < 8 and 0 <= ny < 8 and self.plateau[nx][ny] == ' ':
                    nx += dx
                    ny += dy
                if 0 <= nx < 8 and 0 <= ny < 8 and self.plateau[nx][ny] in ['B', 'D', 'N', 'd']:
                    nx += dx
                    ny += dy
                    if 0 <= nx < 8 and 0 <= ny < 8 and self.plateau[nx][ny] == ' ':
                        captures.append((nx, ny))
        return captures

    def get_possible_moves(self, x, y, joueur):
        # Obtenir les mouvements possibles pour une pièce
        piece = self.plateau[x][y]
        if (joueur == 'Blanc' and piece not in ['B', 'D']) or (joueur == 'Noir' and piece not in ['N', 'd']):
            return []  # Ne pas montrer les mouvements possibles pour les pièces de l'adversaire
        moves = []
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        if piece in ['B', 'N']:
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if self.mouvement_valide(x, y, nx, ny, joueur):
                    moves.append((nx, ny))
                nx, ny = x + 2 * dx, y + 2 * dy
                if self.mouvement_valide(x, y, nx, ny, joueur):
                    moves.append((nx, ny))
        elif piece in ['D', 'd']:
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                while 0 <= nx < 8 and 0 <= ny < 8 and self.plateau[nx][ny] == ' ':
                    moves.append((nx, ny))
                    nx += dx
                    ny += dy
                nx, ny = x + 2 * dx, y + 2 * dy
                if self.mouvement_valide(x, y, nx, ny, joueur):
                    moves.append((nx, ny))
        return moves

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