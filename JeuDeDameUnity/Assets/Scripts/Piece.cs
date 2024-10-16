using UnityEngine;

public class Piece : MonoBehaviour
{
    public enum PieceType { Pion, Dame }
    public enum PieceColor { Blanc, Noir }

    public PieceType Type { get; private set; }
    public PieceColor Color { get; private set; }

    // Initialise la pièce avec son type et sa couleur
    public void Initialize(PieceType type, PieceColor color)
    {
        Type = type;
        Color = color;
    }

    // Méthode pour bouger la pièce
    public void Move(Vector3 newPosition)
    {
        transform.position = newPosition;
    }

    // Start est appelé une fois avant la première exécution de Update après la création du MonoBehaviour
    void Start()
    {
        
    }

    // Update est appelé une fois par frame
    void Update()
    {
        
    }
}