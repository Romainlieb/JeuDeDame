using UnityEngine;

public class BoardManager : MonoBehaviour
{
    public GameObject tilePrefab; // Prefab for the tile
    private Tile[,] plateau = new Tile[8, 8];

    void Start()
    {
        InitialiserPlateau();
        AfficherPlateau();
    }

    void InitialiserPlateau()
    {
        for (int i = 0; i < 8; i++)
        {
            for (int j = 0; j < 8; j++)
            {
                // Instantiate the tile prefab
                GameObject tileObject = Instantiate(tilePrefab, new Vector3(j, 0, i), Quaternion.identity);
                Tile tile = tileObject.GetComponent<Tile>();
                // Determine if the tile should be black or white
                bool isBlack = (i + j) % 2 == 1;
                Piece.PieceColor pieceColor = Piece.PieceColor.Blanc;
                Piece.PieceType pieceType = Piece.PieceType.Pion;
                bool hasPiece = false;
    
                // Place les pièces blanches et noires
                if ((i % 2) != (j % 2))
                {
                    if (i < 3)
                    {
                        pieceColor = Piece.PieceColor.Blanc;
                        hasPiece = true;
                    }
                    else if (i > 4)
                    {
                        pieceColor = Piece.PieceColor.Noir;
                        hasPiece = true;
                    }
                }
    
                // Initialize the tile
                tile.Initialize(isBlack, hasPiece ? pieceColor.ToString()[0] : ' ');
    
                // Initialize the piece if there is one
                if (hasPiece)
                {
                    GameObject pieceObject = new GameObject("Piece");
                    Piece piece = pieceObject.AddComponent<Piece>();
                    piece.Initialize(pieceType, pieceColor);
                    pieceObject.transform.SetParent(tileObject.transform);
                    pieceObject.transform.localPosition = Vector3.zero;
                }
    
                // Store the tile in the array
                plateau[i, j] = tile;
            }
        }
    }

    void AfficherPlateau()
    {
        // Affiche le plateau dans la console pour le moment (à adapter pour l'UI)
        string affichage = "  1 2 3 4 5 6 7 8\n";
        for (int i = 0; i < 8; i++)
        {
            affichage += (char)(65 + i) + "|";
            for (int j = 0; j < 8; j++)
            {
                affichage += plateau[i, j].Piece + " ";
            }
            affichage += "\n";
        }
        Debug.Log(affichage);
    }

    public void DeplacerPiece(string coord1, string coord2, string joueur)
    {
        (int x1, int y1) = ConvertCoordToIndex(coord1);
        (int x2, int y2) = ConvertCoordToIndex(coord2);

        Tile tile1 = plateau[x1, y1];
        Tile tile2 = plateau[x2, y2];
        char piece = tile1.Piece;

        if ((joueur == "Blanc" && (piece != 'B' && piece != 'D')) ||
            (joueur == "Noir" && (piece != 'N' && piece != 'd')))
        {
            Debug.Log("Mouvement invalide pour le joueur " + joueur);
            return;
        }

        // Effectue le déplacement
        tile2.SetPiece(piece);
        tile1.SetPiece(' ');
        Debug.Log($"Déplacement de {piece} de {coord1} à {coord2}");
        AfficherPlateau();
    }

    private (int, int) ConvertCoordToIndex(string coord)
    {
        int x = coord[0] - 'A';
        int y = int.Parse(coord[1].ToString()) - 1;
        return (x, y);
    }

    private string ConvertIndexToCoord(int x, int y)
    {
        char letter = (char)('A' + x);
        int number = y + 1;
        return $"{letter}{number}";
    }
}