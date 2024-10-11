import re

class JeuDeDame:
    def __init__(self):
        self.plateau = self.initialiser_plateau()

    def initialiser_plateau(self):
        plateau = [[' ' for _ in range(8)] for _ in range(8)]
        for i in range(8):
            for j in range(8):
                if (i % 2 != j % 2):
                    if i < 3:
                        plateau[i][j] = 'B'  # Pièces blanches
                    elif i > 4:
                        plateau[i][j] = 'N'  # Pièces noires
        return plateau

    def afficher_plateau(self):
        print("  " + " ".join(str(i + 1) for i in range(8)))  # Numéros de colonnes
        for i, ligne in enumerate(self.plateau):
            print(chr(65 + i) + "|" + " ".join(ligne) + " ")  # Numéros de lignes en lettres et contenu du plateau
        print()

    def deplacer_piece(self, x1, y1, x2, y2, joueur):
        piece = self.plateau[x1][y1]
        if (joueur == 'Blanc' and piece not in ['B', 'D']) or (joueur == 'Noir' and piece not in ['N', 'd']):
            return False  # Empêcher de déplacer les pièces de l'adversaire
        if self.mouvement_valide(x1, y1, x2, y2):
            self.plateau[x2][y2] = self.plateau[x1][y1]
            self.plateau[x1][y1] = ' '
            self.verifier_capture(x1, y1, x2, y2)
            self.promouvoir_dame(x2, y2)
            # Vérifier les prises multiples
            while self.capture_possible(x2, y2):
                self.afficher_plateau()
                print(f"Prises multiples possibles pour {joueur}.")
                x1, y1 = x2, y2
                mouvement_valide = False
                while not mouvement_valide:
                    entree = input("Entrez les nouvelles coordonnées de déplacement (La Ca) : ")
                    match = re.match(r"([a-hA-H])\s*(\d)", entree.replace(" ", ""))
                    if match:
                        x2, y2 = match.groups()
                        x2 = ord(x2.upper()) - 65
                        y2 = int(y2) - 1
                        if self.mouvement_valide(x1, y1, x2, y2):
                            self.plateau[x2][y2] = self.plateau[x1][y1]
                            self.plateau[x1][y1] = ' '
                            self.verifier_capture(x1, y1, x2, y2)
                            self.promouvoir_dame(x2, y2)
                            mouvement_valide = True
                        else:
                            print("Mouvement invalide. Veuillez réessayer.")
                    else:
                        print("Format invalide. Veuillez réessayer.")
            return True
        return False

    def mouvement_valide(self, x1, y1, x2, y2):
        if 0 <= x2 < 8 and 0 <= y2 < 8 and self.plateau[x2][y2] == ' ':
            piece = self.plateau[x1][y1]
            if piece == 'B':
                if abs(x2 - x1) == 1 and abs(y2 - y1) == 1:
                    return True
                if abs(x2 - x1) == 2 and abs(y2 - y1) == 2:
                    x_capture = (x1 + x2) // 2
                    y_capture = (y1 + y2) // 2
                    if self.plateau[x_capture][y_capture] == 'N' and x2 > x1:
                        return True
            elif piece == 'N':
                if abs(x2 - x1) == 1 and abs(y2 - y1) == 1:
                    return True
                if abs(x2 - x1) == 2 and abs(y2 - y1) == 2:
                    x_capture = (x1 + x2) // 2
                    y_capture = (y1 + y2) // 2
                    if self.plateau[x_capture][y_capture] == 'B' and x2 < x1:
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
                    if abs(x2 - x1) == 2:
                        x_capture = (x1 + x2) // 2
                        y_capture = (y1 + y2) // 2
                        if (piece == 'D' and self.plateau[x_capture][y_capture] in ['N', 'd']) or \
                        (piece == 'd' and self.plateau[x_capture][y_capture] in ['B', 'D']):
                            return True
                    return True
        return False

    def verifier_capture(self, x1, y1, x2, y2):
        if abs(x2 - x1) == 2 and abs(y2 - y1) == 2:
            x_capture = (x1 + x2) // 2
            y_capture = (y1 + y2) // 2
            self.plateau[x_capture][y_capture] = ' '

    def promouvoir_dame(self, x, y):
        if self.plateau[x][y] == 'B' and x == 7:
            self.plateau[x][y] = 'D'  # Dame blanche
        elif self.plateau[x][y] == 'N' and x == 0:
            self.plateau[x][y] = 'd'  # Dame noire

    def capture_possible(self, x, y):
        piece = self.plateau[x][y]
        directions = [(-2, -2), (-2, 2), (2, -2), (2, 2)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 8 and 0 <= ny < 8 and self.plateau[nx][ny] == ' ':
                x_capture = (x + nx) // 2
                y_capture = (y + ny) // 2
                if (piece in ['B', 'D'] and self.plateau[x_capture][y_capture] in ['N', 'd']) or \
                   (piece in ['N', 'd'] and self.plateau[x_capture][y_capture] in ['B', 'D']):
                    # Empêcher les prises en arrière pour les pièces non-dames
                    if piece == 'B' and nx < x:
                        continue
                    if piece == 'N' and nx > x:
                        continue
                    return True
        return False

    def partie_terminee(self):
        pieces_blanches = sum(ligne.count('B') + ligne.count('D') for ligne in self.plateau)
        pieces_noires = sum(ligne.count('N') + ligne.count('d') for ligne in self.plateau)
        return pieces_blanches == 0 or pieces_noires == 0

    def jouer(self):
        joueur = 'Blanc'
        while not self.partie_terminee():
            self.afficher_plateau()
            print(f"Joueur {joueur}, à vous de jouer.")
            mouvement_valide = False
            while not mouvement_valide:
                entree = input("Entrez les coordonnées de déplacement (Ld Cd La Ca) : ")
                # Utiliser une expression régulière pour extraire les coordonnées
                match = re.match(r"([a-hA-H])\s*(\d)\s*([a-hA-H])\s*(\d)", entree.replace(" ", ""))
                if match:
                    x1, y1, x2, y2 = match.groups()
                    x1 = ord(x1.upper()) - 65
                    y1 = int(y1) - 1
                    x2 = ord(x2.upper()) - 65
                    y2 = int(y2) - 1
                    if self.deplacer_piece(x1, y1, x2, y2, joueur):
                        mouvement_valide = True
                    else:
                        print("Mouvement invalide. Veuillez réessayer.")
                else:
                    print("Format invalide. Veuillez réessayer.")
            joueur = 'Noir' if joueur == 'Blanc' else 'Blanc'
        print("Partie terminée!")

if __name__ == "__main__":
    jeu = JeuDeDame()
    jeu.jouer()