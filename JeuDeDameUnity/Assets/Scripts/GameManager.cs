using UnityEngine;

public class GameManager : MonoBehaviour
{
    public enum GameState { Playing, GameOver }
    public GameState CurrentState { get; private set; }
    public TurnManager turnManager;

    void Start()
    {
        CurrentState = GameState.Playing;
        turnManager = FindObjectOfType<TurnManager>();
        turnManager.OnTurnEnd += HandleTurnEnd;
    }

    void Update()
    {
        if (CurrentState == GameState.Playing)
        {
            CheckVictoryConditions();
        }
    }

    void HandleTurnEnd()
    {
        // Logique pour gérer la fin d'un tour
        CheckVictoryConditions();
    }

    void CheckVictoryConditions()
    {
        // Logique pour vérifier les conditions de victoire
        // Exemple : Si un joueur n'a plus de pièces ou ne peut plus bouger
        bool isVictory = false;

        if (isVictory)
        {
            CurrentState = GameState.GameOver;
            Debug.Log("Game Over!");
        }
    }
}