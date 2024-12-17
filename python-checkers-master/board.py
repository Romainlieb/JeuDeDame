from utils import get_position_with_row_col

class Board:
    """
    Class representing a checkers board.
    Attributes:
        pieces (list): List of Piece objects on the board.
        color_up (str): Color of the pieces that are moving up.
    Methods:
        __init__(pieces, color_up):
            Initializes the board with pieces and the color moving up.
        get_color_up():
            Returns the color of the pieces moving up.
        get_pieces():
            Returns the list of pieces on the board.
        get_piece_by_index(index):
            Returns the piece at the specified index.
        has_piece(position):
            Checks if there is a piece at the given position.
        get_row_number(position):
            Returns the row number for the given position.
        get_col_number(position):
            Returns the column number for the given position.
        get_row(row_number):
            Returns a set of pieces in the specified row.
        get_pieces_by_coords(*coords):
            Returns a list of pieces at the specified (row, column) coordinates.
        move_piece(moved_index, new_position):
            Moves a piece to a new position and handles eating and king movements.
        get_winner():
            Returns the winning color or None if no player has won yet.
    """
    def __init__(self, pieces, color_up):
        self.pieces = pieces
        self.color_up = color_up  # Defines which of the colors is moving up.
        self.board = [0] * 32  # Initialize the board as empty.
        self.update_board()

    def update_board(self):
        """
        Updates the internal representation of the board (self.board).
        0: empty, 1: white piece, 2: black piece.
        """
        self.board = [0] * 32
        for piece in self.pieces:
            position = int(piece.get_position())
            self.board[position] = 1 if piece.get_color() == 'white' else 2
    
    def get_color_up(self):
        return self.color_up

    def get_pieces(self):
        return self.pieces

    def get_piece_by_index(self, index):
        return self.pieces[index]

    def has_piece(self, position):
        # Receives position (e.g.: 28), returns True if there's a piece in that position
        string_pos = str(position)

        for piece in self.pieces:
            if piece.get_position() == string_pos:
                return True

        return False
    
    def get_row_number(self, position):
        # Receives position (e.g.: 1), returns the row this position is on the board.
        return position // 4
    
    def get_col_number(self, position):
        # There are four dark squares on each row where pieces can be placed.
        # The remainder of (position / 4) can be used to determine which of the four squares has the position.
        # We also take into account that odd rows on the board have a offset of 1 column.
        remainder = position % 4
        column_position = remainder * 2 # because the squares have a gap of one light square.
        is_row_odd = not (self.get_row_number(position) % 2 == 0)
        return column_position + 1 if is_row_odd else column_position
    
    def get_row(self, row_number):
        # Receives a row number, returns a set with all pieces contained in it.
        # [0, 1, 2, 3] represents the first row of the board. All rows contain four squares.
        # row_pos needs to contain strings on it because Piece.get_position() returns a number in type string.

        row_pos = [0, 1, 2, 3]
        row_pos = list(map((lambda pos: str(pos + (4 * row_number))), row_pos))
        row = []

        for piece in self.pieces:
            if piece.get_position() in row_pos:
                row.append(piece)

        return set(row)
    
    def get_pieces_by_coords(self, *coords):
        # Receives a variable number of (row, column) pairs.
        # Returns a ordered list of same length with a Piece if found, otherwise None.
        row_memory = dict() # Used to not have to keep calling get_row().
        results = []

        for coord_pair in coords:
            if coord_pair[0] in row_memory:
                current_row = row_memory[coord_pair[0]]
            else:
                current_row = self.get_row(coord_pair[0])
                row_memory[coord_pair[0]] = current_row
            
            for piece in current_row:
                if self.get_col_number(int(piece.get_position())) == coord_pair[1]:
                    results.append(piece)
                    break
            else:
                # This runs if 'break' isn't called on the for loop above.
                results.append(None)
        
        return results
    def get_valid_actions(self, current_color):
        """
        Génère une liste de toutes les actions valides dans l'état actuel du plateau,
        en prenant en compte la couleur des pièces qui jouent.
        
        Args:
            current_color (str): Couleur des pièces jouant actuellement ('W' pour blanc, 'B' pour noir).
        
        Returns:
            list: Liste des actions valides sous forme de paires (source, target).
        """
        actions = []
        has_jump_restraint = False
        for index, piece in enumerate(self.pieces):
            # Vérifie si la pièce appartient au joueur actuel
            if piece.get_color().lower() != current_color.lower():
                continue

            current_position = int(piece.get_position())
            # Calculer les positions cibles possibles en diagonale
            # Les mouvements dépendent de la direction selon la couleur des pièces
            if piece.is_king():
                # Les dames peuvent se déplacer dans toutes les directions diagonales
                potential_moves = [
                    current_position + offset
                    for offset in [-3, -4, 3, 4]
                ]
            else:
                # Les pions avancent selon leur couleur
                if current_color.lower() == 'w':  # Blanc avance vers le haut


                    potential_moves = [current_position - 3, current_position - 4]
                elif current_color.lower() == 'b':  # Noir avance vers le bas
                    potential_moves = [current_position + 3, current_position + 4]

            # Filtrer les mouvements valides
            for target in potential_moves:
                if self.is_movement_possible(current_position, target):  # Vérifie si le mouvement est valide
                    actions.append((current_position, target))

            
        for piece in self.pieces:
        #Verifie si une piece peut manger une autre piece
            for move in piece.get_moves(self.board):
                if move["eats_piece"]:
                    if piece.get_color() == piece_clicked["piece"]["color"]:
                        has_jump_restraint = True
            else:
                continue
            break
        
        piece_moves = board_pieces[piece_clicked["index"]].get_moves(self.board)

        if has_jump_restraint:
            piece_moves = list(filter(lambda move: move["eats_piece"] == True, piece_moves))


        return actions

    
    def is_movement_possible(self,current_position, new_position):
                # Check if the new position is within the board limits
                if new_position < 0 or new_position >= 32:
                    return False
                
                # Check if the new position is already occupied
                if self.has_piece(new_position):
                    return False
                
                # Check if the movement is diagonal
                current_row = self.get_row_number(current_position)
                new_row = self.get_row_number(new_position)
                current_col = self.get_col_number(current_position)
                new_col = self.get_col_number(new_position)
                
                if abs(current_row - new_row) != abs(current_col - new_col):
                    return False
                
                return True

    def move_piece(self, moved_index, new_position):
        

        def is_eat_movement(current_position):
            return abs(self.get_row_number(current_position) - self.get_row_number(new_position)) != 1

        def get_eaten_index(current_position):
            current_coords = [self.get_row_number(current_position), self.get_col_number(current_position)]
            new_coords = [self.get_row_number(new_position), self.get_col_number(new_position)]
            eaten_coords = [current_coords[0], current_coords[1]]

            eaten_coords[0] += (new_coords[0] - current_coords[0]) // 2
            eaten_coords[1] += (new_coords[1] - current_coords[1]) // 2

            eaten_position = str(get_position_with_row_col(eaten_coords[0], eaten_coords[1]))

            for index, piece in enumerate(self.pieces):
                if piece.get_position() == eaten_position:
                    return index

        def is_king_movement(piece):
            if piece.is_king():
                return False
            
            end_row = self.get_row_number(new_position)
            piece_color = piece.get_color()
            king_row = 0 if self.color_up == piece_color else 7

            return end_row == king_row

        for piece in self.pieces:
            if piece.get_position() == str(moved_index):
                piece_to_move = piece


        def is_movement_possible(current_position, new_position):
                # Check if the new position is within the board limits
                if new_position < 0 or new_position >= 32:
                    return False
                
                # Check if the new position is already occupied
                if self.has_piece(new_position):
                    return False
                
                # Check if the movement is diagonal
                current_row = self.get_row_number(current_position)
                new_row = self.get_row_number(new_position)
                current_col = self.get_col_number(current_position)
                new_col = self.get_col_number(new_position)
                
                if abs(current_row - new_row) != abs(current_col - new_col):
                    return False
                
                return True

        if not is_movement_possible(int(piece_to_move.get_position()), new_position):
            return False

        if is_eat_movement(int(piece_to_move.get_position())):
            self.pieces.pop(get_eaten_index(int(piece_to_move.get_position()))) 
            piece_to_move.set_has_eaten(True)
        else:
            piece_to_move.set_has_eaten(False)

        if is_king_movement(piece_to_move):
            piece_to_move.set_is_king(True)

        piece_to_move.set_position(new_position)
        return True
    
    def get_winner(self):
        # Returns the winning color or None if no player has won yet
        current_color = self.pieces[0].get_color()

        for piece in self.pieces:
            if piece.get_color() != current_color:
                break
        else:
            return current_color
        
        return None
    
    def get_board_state_and_count_kings(pieces):
        """
        Retourne l'état du plateau sous forme de liste et compte le nombre de dames.
        
        Args:
            pieces (list): Liste des pièces sur le plateau.

        Returns:
            tuple:
                - board_state (list): Liste de 32 entiers représentant l'état du plateau.
                - white_kings (int): Nombre de dames blanches.
                - black_kings (int): Nombre de dames noires.
        """
        # Initialisation de l'état du plateau et des compteurs de dames
        board_state = [0] * 32
        white_kings = 0
        black_kings = 0

        for piece in pieces:
            position = int(piece.get_position())
            is_king = piece.is_king()
            color = piece.get_color()

            if color == 'white':
                board_state[position] = 3 if is_king else 1
                if is_king:
                    white_kings += 1
            elif color == 'black':
                board_state[position] = 4 if is_king else 2
                if is_king:
                    black_kings += 1

        return board_state, white_kings, black_kings