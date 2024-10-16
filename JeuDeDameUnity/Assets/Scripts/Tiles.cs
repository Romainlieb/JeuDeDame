using UnityEngine;

public class Tile : MonoBehaviour
{
    public bool IsBlack { get; private set; }
    public bool IsOccupied { get; private set; }
    public char Piece { get; private set; }

    public void Initialize(bool isBlack, char piece)
    {
        IsBlack = isBlack;
        Piece = piece;
        IsOccupied = piece != ' ';
    }

    public void SetPiece(char piece)
    {
        Piece = piece;
        IsOccupied = piece != ' ';
    }
}