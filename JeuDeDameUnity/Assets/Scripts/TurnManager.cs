using UnityEngine;

public class TurnManager : MonoBehaviour
{
    public enum Player { Blanc, Noir }
    public Player CurrentPlayer { get; private set; }
    public delegate void TurnEndHandler();
    public event TurnEndHandler OnTurnEnd;

    void Start()
    {
        CurrentPlayer = Player.Blanc;
    }

    public void EndTurn()
    {
        CurrentPlayer = (CurrentPlayer == Player.Blanc) ? Player.Noir : Player.Blanc;
        OnTurnEnd?.Invoke();
    }
}