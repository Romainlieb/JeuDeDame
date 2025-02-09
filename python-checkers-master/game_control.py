from piece import Piece
"""
GameControl class manages the game state, player turns, and interactions with the board and pieces.
Methods:
    __init__():
        Initializes the game control, setting up the initial game state.
    get_turn():
        Returns the current player's turn.
    get_winner():
        Returns the winner of the game, if any.
    setup():
        Sets up the initial game state with pieces and board.
    draw_screen(display_surface):
        Draws the game board and pieces on the given display surface.
    hold_piece(mouse_pos):
        Handles the logic for picking up a piece with the mouse, including determining possible moves.
    release_piece():
        Handles the logic for releasing a held piece, including moving the piece if the release position is valid.
    set_held_piece(index, piece, mouse_pos):
        Creates a HeldPiece object to follow the mouse when a piece is picked up.
    get_all_possible_moves(color):
        Returns a dictionary of all possible moves for all pieces of the given color.
"""
from board import Board
from board_gui import BoardGUI
from held_piece import HeldPiece
from utils import get_surface_mouse_offset, get_piece_position

class GameControl:
    """
    Contrôle le flux du jeu de dames, y compris les tours, les mouvements et l'affichage.
    Attributs:
    ----------
    turn : str
        Indique le tour actuel ("W" pour blanc, "B" pour noir).
    winner : str ou None
        Indique le gagnant du jeu, ou None si le jeu est toujours en cours.
    board : Board
        L'objet représentant le plateau de jeu et ses pièces.
    board_draw : BoardGUI
        L'objet responsable de l'affichage graphique du plateau et des pièces.
    held_piece : HeldPiece ou None
        La pièce actuellement tenue par le joueur, ou None si aucune pièce n'est tenue.
    Méthodes:
    ---------
    __init__():
        Initialise les attributs et configure le jeu.
    get_turn():
        Retourne le tour actuel.
    get_winner():
        Retourne le gagnant du jeu.
    setup():
        Configure le plateau de jeu initial avec les pièces.
    draw_screen(display_surface):
        Dessine le plateau et les pièces sur la surface d'affichage.
    hold_piece(mouse_pos):
        Sélectionne une pièce à tenir en fonction de la position de la souris.
    release_piece():
        Relâche la pièce tenue et effectue un mouvement si possible.
    set_held_piece(index, piece, mouse_pos):
        Crée un objet HeldPiece pour suivre la souris.
    get_all_possible_moves(color):
        Retourne tous les mouvements possibles pour une couleur donnée.
    """
    def __init__(self):
        self.turn = "W"
        self.winner = None
        self.board = None
        self.board_draw = None
        self.held_piece = None

        self.setup()

    def switch_turn(self, piece_moved=None):
        """
        Change le tour de jeu en alternant entre les joueurs "W" (blanc) et "B" (noir).
        Si la pièce déplacée a mangé une autre pièce, vérifie si le joueur doit continuer son tour.
        
        Args:
            piece_moved (Piece): La pièce qui a été déplacée lors du dernier mouvement.
        """
        if piece_moved and piece_moved.get_has_eaten():
            # Vérifie si la pièce peut encore manger
            jump_moves = list(filter(lambda move: move["eats_piece"], piece_moved.get_moves(self.board)))
            if jump_moves:
                return  # Le joueur garde son tour pour continuer à jouer avec la même pièce.
        
        # Change de tour si aucune condition spéciale n'est remplie
        self.turn = "B" if self.turn == "W" else "W"


    def get_turn(self):
        return self.turn

    def get_winner(self):
        return self.winner

    def setup(self):
        # Initial setup
        pieces = []

        for opponent_piece in range(0, 12):
            pieces.append(Piece(str(opponent_piece) + 'BN')) 
        
        for player_piece in range(20, 32):
            pieces.append(Piece(str(player_piece) + 'WN'))
        
        self.board = Board(pieces, self.turn)
        self.board_draw = BoardGUI(self.board)        
        pass
    
    def draw_screen(self, display_surface):
        self.board_draw.draw_board(display_surface)
        self.board_draw.draw_pieces(display_surface)

        if self.held_piece is not None:
            self.held_piece.draw_piece(display_surface)

    def hold_piece(self, mouse_pos):
        piece_clicked = self.board_draw.get_piece_on_mouse(mouse_pos)
        board_pieces = self.board.get_pieces()
        has_jump_restraint = False # True if any piece can jump in one of its moves, forcing the player to jump

        if piece_clicked is None:
            return
        
        if piece_clicked["piece"]["color"] != self.turn:
            return
        
        # Determines if player has a jump restraint
        for piece in board_pieces:
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

        move_marks = []

        # Gets possible moving positions and tells BoardGUI to draw them
        for possible_move in piece_moves:
            row = self.board.get_row_number(int(possible_move["position"]))
            column = self.board.get_col_number(int(possible_move["position"]))
            move_marks.append((row, column))

        self.board_draw.set_move_marks(move_marks)

        self.board_draw.hide_piece(piece_clicked["index"])
        self.set_held_piece(piece_clicked["index"], board_pieces[piece_clicked["index"]], mouse_pos)

    def release_piece(self):
        if self.held_piece is None:
            return

        position_released = self.held_piece.check_collision(self.board_draw.get_move_marks())
        moved_index = self.board_draw.show_piece()
        piece_moved = self.board.get_piece_by_index(moved_index)

        # Effectue le mouvement si la pièce est lâchée sur une marque valide
        if position_released is not None:
            self.board.move_piece(moved_index, self.board_draw.get_position_by_rect(position_released))
            self.board_draw.set_pieces(self.board_draw.get_piece_properties(self.board))
            self.winner = self.board.get_winner()

            # Change de tour en passant la pièce déplacée à switch_turn
            self.switch_turn(piece_moved)

        self.held_piece = None
        self.board_draw.set_move_marks([])


    def set_held_piece(self, index, piece, mouse_pos):
        # Creates a HeldPiece object to follow the mouse
        surface = self.board_draw.get_surface(piece)
        offset = get_surface_mouse_offset(self.board_draw.get_piece_by_index(index)["rect"], mouse_pos)
        self.held_piece = HeldPiece(surface, offset)

    def get_all_possible_moves(self, color):
        return self.board.get_valid_actions(color) #Faire ceci pou n'avoir que des coup légaux
    
    def GetState(self):
        self.board.update_board()
        state ,b,c = self.board.get_board_state_and_count_kings()
        return state
    def GetIsTerminated(self):
        
        return True if self.get_all_possible_moves(self.turn) == [] else False