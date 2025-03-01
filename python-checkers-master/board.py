
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
        self.lastMoveIsDame = False
        self.moves_dict = generate_moves()
        self.moves_dict[183] = (-1,-1)
        self.lastMoveIsPromote = False
        self.lastReward = 0

    def update_board(self):
        """
        Updates the internal representation of the board (self.board).
        0: empty, 1: white piece, 2: black piece 3: white king 4: Black king.
        """
        self.board = [0.0] * 32
        for piece in self.pieces:
            position = int(piece.get_position())
            if piece.is_king():
                self.board[position] = 3 if piece.get_color() == 'W' else 4
            else:
                self.board[position] = 1 if piece.get_color() == 'W' else 2

    
    
    def get_color_up(self):
        return self.color_up

    def get_pieces(self):
        return self.pieces
    def get_piecesByColor(self,color):
        colorPieces = []
        for piece in self.pieces:
            if piece.get_color() == color:
                colorPieces.append(piece)
        return colorPieces

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
        eaten_actions = []
        isEatingPiece = False
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
                    for offset in [-3- int(self.get_row_number(current_position)%2==0), -4- int(self.get_row_number(current_position)%2==0), 3 + int(self.get_row_number(current_position)%2==1), 4 + int(self.get_row_number(current_position)%2==1)]
                ]
            else:
                # Les pions avancent selon leur couleur
                if current_color.lower() == 'w':  # Blanc avance vers le haut
                    potential_moves = [current_position - 3- int(self.get_row_number(current_position)%2==0), current_position - 4 - int(self.get_row_number(current_position)%2==0)]
                elif current_color.lower() == 'b':  # Noir avance vers le bas
                    potential_moves = [current_position + 3 + int(self.get_row_number(current_position)%2==1), current_position + 4 + int(self.get_row_number(current_position)%2==1)]

            # Filtrer les mouvements valides
            for target in potential_moves:
                possible,eating,positionEaten = self.is_movement_possible(current_position, target)
                if possible:
                    if eating:
                        if not isEatingPiece:
                            isEatingPiece = True
                        eaten_actions.append((current_position, positionEaten))
                    else:
                        actions.append((current_position, target))
        if isEatingPiece:
            return eaten_actions
        else:
            return actions

    def isDiagonalEatingPossible(self,current_position,new_position):
        tupleLeftRight = ((0,8,16,24,7,15,23,31),(-5,3))
        distance = new_position-current_position
        if(current_position in tupleLeftRight[0]):
            if(distance not in tupleLeftRight[1]):
                return True
            else:
                return False
        elif(new_position in tupleLeftRight[0]):
            return False
        else:
            return True
    
    def is_movement_possible(self,current_position, new_position):

                eatingPiece = False
                opponentColor = "W" if self.get_pieces_by_coords((self.get_row_number(current_position),self.get_col_number(current_position)))[0].get_color() == "B" else "B"
                addOffset = 1
                if self.get_row_number(current_position) % 2 == 1:
                    addOffset = -1
                rowParity = self.get_row_number(current_position) % 2
                # Check if the new position is within the board limits
                if new_position < 0 or new_position >= 32:
                    return False, False, 0
                
                
                # Check if the new position is already occupied
                if self.has_piece(new_position):
                    posAfterEat = new_position+(new_position-current_position)+addOffset
                    isOutsideBoard = posAfterEat < 0 or posAfterEat >= 32
                    isNotPieceAfterEat = self.has_piece(new_position+(new_position-current_position)+addOffset)==False
                    isPieceAnOpps = self.get_pieces_by_coords((self.get_row_number(new_position),self.get_col_number(new_position)))[0].get_color() == opponentColor
                    isNotInBorder = self.isDiagonalEatingPossible(current_position,new_position)

                    if(isNotPieceAfterEat and isPieceAnOpps and isNotInBorder and not isOutsideBoard): #Verifie si la case d'apres est vide et si la piece est un opposant
                        eatingPiece = True
                    else:
                        return False, False, 0
                        
                
                # Check if the movement is diagonal
                current_row = self.get_row_number(current_position)
                new_row = self.get_row_number(new_position)
                current_col = self.get_col_number(current_position)
                new_col = self.get_col_number(new_position)
                
                if abs(current_row - new_row) != abs(current_col - new_col):
                    return False, False, 0
                if(eatingPiece):
                    return True,eatingPiece,new_position+(new_position-current_position)+addOffset
                return True,False,0

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
            eatenPiece = self.get_piece_by_index(get_eaten_index(int(piece_to_move.get_position())))
            isEatenPieceKing = eatenPiece.is_king()
            if isEatenPieceKing:
                self.lastReward = self.lastReward + 3 
            else: 
                self.lastReward = self.lastReward + 1
            self.pieces.pop(get_eaten_index(int(piece_to_move.get_position())))
            piece_to_move.set_has_eaten(True)
        else:
            piece_to_move.set_has_eaten(False)

        if is_king_movement(piece_to_move):
            piece_to_move.set_is_king(True)
            self.lastMoveIsPromote = True
            self.lastReward = self.lastReward + 2

        piece_to_move.set_position(new_position)
        self.lastMoveIsDame = piece_to_move.is_king()
        self.lastReward = self.lastReward + self.getMoveGood(new_position)
        return True
    
    def getMoveGood(self,new_position):

        def get_row_number(position):
            return position // 4
        def get_col_number(position,row):
            # There are four dark squares on each row where pieces can be placed.
            # The remainder of (position / 4) can be used to determine which of the four squares has the position.
            # We also take into account that odd rows on the board have a offset of 1 column.
            remainder = position % 4
            column_position = remainder * 2 # because the squares have a gap of one light square.
            is_row_odd = not (row % 2 == 0)
            return column_position + 1 if is_row_odd else column_position
        def getOpposite(index):
            if(index == 0):
                return 2
            elif(index == 1):
                return 3
            elif(index == 2):
                return 0
            else:
                return 1
        invinciblePos = (8,16,24,7,15,23,0,31,1,2,3,28,29,30)   
        reward = 0.5
        if(new_position in invinciblePos):
            return reward
        piece = self.get_pieces_by_coords((get_row_number(new_position),get_col_number(new_position,get_row_number(new_position))))[0]
        if piece.is_king():
            reward = 3
        potential_moves = [
                    new_position + offset
                    for offset in [-3- int(get_row_number(new_position)%2==0), -4- int(get_row_number(new_position)%2==0), 3 + int(get_row_number(new_position)%2==1), 4 + int(get_row_number(new_position)%2==1)]
                ]
        for i in range(len(potential_moves)):
            if(potential_moves[i] >= 0 and potential_moves[i] < 32):
                if(self.has_piece(potential_moves[i])):
                    OtherPiece = self.get_pieces_by_coords((get_row_number(potential_moves[i]),get_col_number(potential_moves[i],get_row_number(potential_moves[i]))))[0]
                    pieceColor = OtherPiece.get_color()
                    if (pieceColor != piece.get_color()):
                        if OtherPiece.is_king():
                            moveOtherPiece = OtherPiece.get_adjacent_squares(self)
                            for j in range(len(moveOtherPiece)):
                                if (moveOtherPiece[j]==new_position and not self.has_piece(potential_moves[j])):
                                    reward  = reward *-1
                                    return reward
                        else:
                            if pieceColor == 'W':
                                moveOtherPiece = OtherPiece.get_adjacent_squares(self)
                                moveOtherPiece = [0,0]+moveOtherPiece
                            else:
                                moveOtherPiece = OtherPiece.get_adjacent_squares(self)
                                moveOtherPiece = moveOtherPiece + [0,0]
                            for j in range(len(moveOtherPiece)):
                                if (moveOtherPiece[j]==new_position and not self.has_piece(potential_moves[j])):
                                    reward  = reward *-1
                                    return reward
        reward = 0.5
        return reward   
                            
        return True
    def move_pieceAgent(self, moved_index, new_position):
        self.move_piece(moved_index, new_position)
        self.update_board()
        return self.get_board_state_and_count_kings(),0,0

    def get_winner(self):
        # Returns the winning color or None if no player has won yet
        current_color = self.pieces[0].get_color()

        for piece in self.pieces:
            if piece.get_color() != current_color:
                break
        else:
            return current_color
        
        return None
    
    def get_board_state_and_count_kings(self):
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

        for piece in self.pieces:
            position = int(piece.get_position())
            is_king = piece.is_king()
            color = piece.get_color()

            if color == 'white':
                if is_king:
                    white_kings += 1
            elif color == 'black':
                if is_king:
                    black_kings += 1

        return self.board, white_kings, black_kings

    def is_piece_capturable(self, current_position, target_position, current_color): 
        """
        Vérifie si une pièce peut être capturée en se déplaçant de current_position à target_position.
        
        Args:
            current_position (int): Position actuelle de la pièce.
            target_position (int): Position cible après la capture.
            current_color (str): Couleur de la pièce actuelle ('W' pour blanc, 'B' pour noir).
        
        Returns:
            bool: True si la capture est possible, False sinon.
        """
        # Calculer la position intermédiaire
        middle_position = (current_position + target_position) // 2
        
        # Vérifier si la position intermédiaire contient une pièce adverse
        if not self.has_piece(middle_position):
            return False
        
        middle_piece = self.get_piece(middle_position)
        if middle_piece.get_color().lower() == current_color.lower():
            return False
        
        # Vérifier si la position cible est libre
        if self.has_piece(target_position):
            return False
        
        return True
    

def generate_moves():
    moves = {}
    move_id = 0
    board_size = 8
    playable_squares = [
        0, 1, 2, 3,
        4, 5, 6, 7,
        8, 9, 10, 11,
        12, 13, 14, 15,
        16, 17, 18, 19,
        20, 21, 22, 23,
        24, 25, 26, 27,
        28, 29, 30, 31
    ]
    tupleLeftRight = (8,16,24,7,15,23)
    tulpeCorner = (0,31)    
    def get_row_number(position):
        return position // 4
    def get_col_number(position,row):
        # There are four dark squares on each row where pieces can be placed.
        # The remainder of (position / 4) can be used to determine which of the four squares has the position.
        # We also take into account that odd rows on the board have a offset of 1 column.
        remainder = position % 4
        column_position = remainder * 2 # because the squares have a gap of one light square.
        is_row_odd = not (row % 2 == 0)
        return column_position + 1 if is_row_odd else column_position

    for square in playable_squares:
        row = get_row_number(square)
        col = get_col_number(square,row)
        addOffset = 1
        if get_row_number(square) % 2 == 1:
            addOffset = -1
        if (square in tupleLeftRight):
            bLeft = 0 if col == 0 else 1
            bRight = 0 if col == 7 else 1
            potential_moves = [
                    square + offset
                    for offset in [(-3- int(get_row_number(square)%2==0))*bRight, (-4- int(get_row_number(square)%2==0)) *bLeft , (3 + int(get_row_number(square)%2==1))*bLeft, (4 + int(get_row_number(square)%2==1))*bRight]
            ]
            potential_movesJump = []
            for new_position in potential_moves:
                if new_position != square:
                    potential_movesJump.append(new_position+(new_position-square)+addOffset)
            potential_moves = potential_moves + potential_movesJump
            for action in potential_moves:
                if(action >= 0 and action < 32 and action != square):
                    moves[move_id] = (square,action)
                    move_id += 1
                    
        elif square not in tulpeCorner:
            potential_moves = [
                    square + offset
                    for offset in [-3- int(get_row_number(square)%2==0), -4- int(get_row_number(square)%2==0), 3 + int(get_row_number(square)%2==1), 4 + int(get_row_number(square)%2==1)]
                ]
            potential_movesJump = []
            for new_position in potential_moves:
                potential_movesJump.append(new_position+(new_position-square)+addOffset)
            potential_moves = potential_moves + potential_movesJump
            for action in potential_moves:
                if(action >= 0 and action < 32):
                    moves[move_id] = (square,action)
                    move_id += 1
    moves[move_id+1] = (0,4)
    moves[move_id+2] = (0,9)
    moves[move_id+3] = (31,27)
    moves[move_id+4] = (31,22)

    return moves
# Générer le dictionnaire de mouvements possibles

def TestDico(dico):
    def get_row_number(coord):
        return coord//4
    def isDiagonalEatingPossible(current_position,new_position):
        tupleLeftRight = ((0,8,16,24,7,15,23,31),(-5,3))
        distance = new_position-current_position
        if(current_position in tupleLeftRight[0]):
            if(distance not in tupleLeftRight[1]):
                return True
            else:
                return False
        elif(new_position in tupleLeftRight[0]):
            return False
        else:
            return True
        
    isCorrect = True
    falseArray = []
    
    for current_position,newCoord in dico.values():
        addOffset = 1
        if get_row_number(current_position) % 2 == 1:
            addOffset = -1
        rowNb = get_row_number(current_position)
        potential_moves = []
        potential_moves = [
                    current_position + offset
                    for offset in [-3- int(get_row_number(current_position)%2==0), -4- int(get_row_number(current_position)%2==0), 3 + int(get_row_number(current_position)%2==1), 4 + int(get_row_number(current_position)%2==1)]
                ]
        potential_movesJump = []
        for new_position in potential_moves:
           potential_movesJump.append(new_position+(new_position-current_position)+addOffset)
        

        distance = newCoord-current_position
        if(not isDiagonalEatingPossible(current_position,newCoord) and (distance<-5 and distance>5 )):
            isCorrect = False
            falseArray.append((current_position,newCoord))

        potential_moves = potential_moves + potential_movesJump 
        if not(newCoord in potential_moves):
            isCorrect = False
            falseArray.append((current_position,newCoord))
    if(not isCorrect):
        print("Dico pas bon, voila les galère : ",falseArray)
    else:
        print("Dico good")


# generate_moves()
TestDico(generate_moves())
