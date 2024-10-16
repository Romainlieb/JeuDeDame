using UnityEngine;

public class PieceMovement : MonoBehaviour
{
    public Piece piece;
    public BoardManager boardManager;

    private Vector2Int[] directions = new Vector2Int[]
    {
        new Vector2Int(1, 1), new Vector2Int(-1, 1), // Diagonales pour les pions blancs
        new Vector2Int(1, -1), new Vector2Int(-1, -1) // Diagonales pour les pions noirs
    };

    void Start()
    {
        piece = GetComponent<Piece>();
        boardManager = FindObjectOfType<BoardManager>();
    }

    void Update()
    {
        // Logique de déplacement à implémenter
    }

    public bool IsValidMove(Vector2Int start, Vector2Int end)
    {
        if (!boardManager.IsWithinBounds(end))
            return false;

        if (boardManager.GetPieceAt(end) != null)
            return false;

        Vector2Int direction = end - start;
        if (piece.Type == Piece.PieceType.Pion)
        {
            if (piece.Color == Piece.PieceColor.Blanc && direction.y != 1)
                return false;
            if (piece.Color == Piece.PieceColor.Noir && direction.y != -1)
                return false;
        }

        return true;
    }

    public void MovePiece(Vector2Int start, Vector2Int end)
    {
        if (IsValidMove(start, end))
        {
            boardManager.MovePiece(start, end);
            if ((piece.Color == Piece.PieceColor.Blanc && end.y == 7) || 
                (piece.Color == Piece.PieceColor.Noir && end.y == 0))
            {
                piece.PromoteToDame();
            }
        }
    }
}