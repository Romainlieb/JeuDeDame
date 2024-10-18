import pygame
import random

# Constantes
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
W_POWN = (255, 255, 255)
B_POWN = (57, 57, 56)
GOLD = (255, 215, 0)
HIGHLIGHT_COLOR = (0, 255, 0, 128)

# Initialiser Pygame
pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Jeu de Dame')

class JeuDeDame:
    def __init__(self):
        self.plateau = self.initialiser_plateau()
        self.selected_piece = None
        self.possible_moves = []
        self.joueur = 'Blanc'

    def initialiser_plateau(self):
        plateau = [[' ' for _ in range(8)] for _ in range(8)]
        for i in range(8):
            for j in range(8):
                if (i % 2 != j % 2):
                    if i < 3:
                        plateau[i][j] = 'B'
                    elif i > 4:
                        plateau[i][j] = 'N'
        return plateau

    def draw_board(self):
        WIN.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(WIN, WHITE, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def draw_pieces(self):
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.plateau[row][col]
                if piece != ' ':
                    color = W_POWN if piece in ['B', 'D'] else B_POWN
                    pygame.draw.circle(WIN, color, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 2 - 10)
                    if piece in ['D', 'd']:
                        self.draw_dame_triangles(row, col, color)

    def draw_dame_triangles(self, row, col, color):
        center_x = col * SQUARE_SIZE + SQUARE_SIZE // 2
        center_y = row * SQUARE_SIZE + SQUARE_SIZE // 2
        radius = SQUARE_SIZE // 2 - 10
        triangle_side = radius // 2

        def equilateral_triangle(center_x, center_y, side):
            height = (3 ** 0.5 / 2) * side
            return [
                (center_x - side / 2, center_y + height / 2),
                (center_x + side / 2, center_y + height / 2),
                (center_x, center_y - height / 2)
            ]

        triangle_center_y = center_y - radius // 2
        points1 = equilateral_triangle(center_x - triangle_side * 1.25, triangle_center_y, triangle_side)
        points2 = equilateral_triangle(center_x, triangle_center_y, triangle_side)
        points3 = equilateral_triangle(center_x + triangle_side * 1.25, triangle_center_y, triangle_side)

        pygame.draw.polygon(WIN, GOLD, points1)
        pygame.draw.polygon(WIN, GOLD, points2)
        pygame.draw.polygon(WIN, GOLD, points3)

    def draw_highlights(self):
        for move in self.possible_moves:
            row, col = move
            pygame.draw.circle(WIN, HIGHLIGHT_COLOR, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 2 - 10)

    def deplacer_piece(self, x1, y1, x2, y2, joueur):
        piece = self.plateau[x1][y1]
        if (joueur == 'Blanc' and piece not in ['B', 'D']) or (joueur == 'Noir' and piece not in ['N', 'd']):
            return False
        if self.mouvement_valide(x1, y1, x2, y2, joueur):
            self.plateau[x2][y2] = self.plateau[x1][y1]
            self.plateau[x1][y1] = ' '
            if abs(x2 - x1) >= 2 and abs(y2 - y1) >= 2:
                self.verifier_capture(x1, y1, x2, y2)
                self.promouvoir_dame(x2, y2, joueur)
                while self.capture_possible_depuis(x2, y2, joueur):
                    possible_captures = self.get_possible_captures(x2, y2)
                    if possible_captures:
                        nx, ny = possible_captures[0]
                        self.plateau[nx][ny] = self.plateau[x2][y2]
                        self.plateau[x2][y2] = ' '
                        self.verifier_capture(x2, y2, nx, ny)
                        x2, y2 = nx, ny
                    else:
                        break
            else:
                self.promouvoir_dame(x2, y2, joueur)
            return True
        return False

    def capture_possible_depuis(self, x, y, joueur):
        piece = self.plateau[x][y]
        if (joueur == 'Blanc' and piece in ['B', 'D']) or (joueur == 'Noir' and piece in ['N', 'd']):
            return bool(self.get_possible_captures(x, y))
        return False

    def mouvement_valide(self, x1, y1, x2, y2, joueur):
        if 0 <= x2 < 8 and 0 <= y2 < 8 and self.plateau[x2][y2] == ' ':
            piece = self.plateau[x1][y1]
            if piece in ['B', 'N']:
                if abs(x2 - x1) == 1 and abs(y2 - y1) == 1:
                    if (joueur == 'Blanc' and x2 > x1) or (joueur == 'Noir' and x2 < x1):
                        return not self.capture_possible(joueur)
                if abs(x2 - x1) == 2 and abs(y2 - y1) == 2:
                    x_capture = (x1 + x2) // 2
                    y_capture = (y1 + y2) // 2
                    if (piece == 'B' and self.plateau[x_capture][y_capture] in ['N', 'd']) or \
                    (piece == 'N' and self.plateau[x_capture][y_capture] in ['B', 'D']):
                        return True
            elif piece in ['D', 'd']:
                if abs(x2 - x1) == abs(y2 - y1):
                    x_step = 1 if x2 > x1 else -1
                    y_step = 1 if y2 > y1 else -1
                    x, y = x1 + x_step, y1 + y_step
                    enemy_piece_found = False
                    while x != x2 and y != y2:
                        if self.plateau[x][y] != ' ':
                            if enemy_piece_found or self.plateau[x][y] not in ['B', 'D', 'N', 'd']:
                                return False
                            enemy_piece_found = True
                        x += x_step
                        y += y_step
                    return enemy_piece_found
        return False

    def verifier_capture(self, x1, y1, x2, y2):
        if abs(x2 - x1) >= 2 and abs(y2 - y1) >= 2:
            x_step = 1 if x2 > x1 else -1
            y_step = 1 if y2 > y1 else -1
            x, y = x1 + x_step, y1 + y_step
            while x != x2 and y != y2:
                if self.plateau[x][y] in ['B', 'D', 'N', 'd']:
                    self.plateau[x][y] = ' '
                    break
                x += x_step
                y += y_step

    def promouvoir_dame(self, x, y, joueur):
        if self.plateau[x][y] == 'B' and x == 7:
            self.plateau[x][y] = 'D'
            print(f"Le joueur {joueur} a fait apparaître une dame blanche.")
        elif self.plateau[x][y] == 'N' and x == 0:
            self.plateau[x][y] = 'd'
            print(f"Le joueur {joueur} a fait apparaître une dame noire.")

    def partie_terminee(self):
        pieces_blanches = sum(ligne.count('B') + ligne.count('D') for ligne in self.plateau)
        pieces_noires = sum(line.count('N') + line.count('d') for line in self.plateau)
        return pieces_blanches == 0 or pieces_noires == 0

    def capture_possible(self, joueur):
        for x in range(8):
            for y in range(8):
                piece = self.plateau[x][y]
                if (joueur == 'Blanc' and piece in ['B', 'D']) or (joueur == 'Noir' and piece in ['N', 'd']):
                    if self.get_possible_captures(x, y):
                        return True
        return False

    def get_possible_captures(self, x, y):
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
                while 0 <= nx < 8 and 0 <= ny < 8:
                    if self.plateau[nx][ny] != ' ':
                        if self.plateau[nx][ny] in ['B', 'D', 'N', 'd'] and \
                        ((piece == 'D' and self.plateau[nx][ny] in ['N', 'd']) or \
                            (piece == 'd' and self.plateau[nx][ny] in ['B', 'D'])):
                            nx += dx
                            ny += dy
                            while 0 <= nx < 8 and 0 <= ny < 8 and self.plateau[nx][ny] == ' ':
                                captures.append((nx, ny))
                                nx += dx
                                ny += dy
                        break
                    nx += dx
                    ny += dy

        return captures

    def get_possible_moves(self, x, y, joueur):
        piece = self.plateau[x][y]
        if (joueur == 'Blanc' and piece not in ['B', 'D']) or (joueur == 'Noir' and piece not in ['N', 'd']):
            return []

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
                        if self.deplacer_piece(x1, y1, row, col, self.joueur):
                            self.joueur = 'Noir' if self.joueur == 'Blanc' else 'Blanc'
                        self.selected_piece = None
                        self.possible_moves = []
                    else:
                        self.selected_piece = (row, col)
                        self.possible_moves = self.get_possible_moves(row, col, self.joueur)

            self.draw_board()
            self.draw_pieces()
            self.draw_highlights()
            pygame.display.update()

        pygame.quit()

if __name__ == "__main__":
    jeu = JeuDeDame()
    jeu.jouer()