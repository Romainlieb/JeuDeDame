import torch
from dqn import DQN 
from experience_replay import ReplayMemory
from itertools import count
import random
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
from game_control import GameControl
class bcolors:
        HEADER = '\033[95m'
        OKBLUE = '\033[94m'
        OKCYAN = '\033[96m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'


class Agent : 
    
    def display_board_console(board):
        """
        Affiche le plateau de jeu dans la console avec toutes les cases entourées par des |.
        Les cases jouables affichent leur contenu (pièce ou vide), et les non jouables sont vides.
        """
        print("\nPlateau de jeu :")
        for row in range(8):
            row_display = []
            for col in range(8):
                # Calcul de la position sur un plateau de 32 cases
                if col  * 4 + (row // 2) != 0 or (col == 0 and row == 0):  # Case jouable (sombre)
                    #position = row * 4 + (col // 2)
                    piece = board.get_pieces_by_coords((row,col))
                    if piece[0] != None:
                        if(not piece[0].is_king()):
                            row_display.append(f" {piece[0].get_color()} ")
                        else:
                            row_display.append(f"{bcolors.OKGREEN} {piece[0].get_color()} {bcolors.ENDC}")
                    else:
                        row_display.append("   ")
                else:  # Case non jouable (claire)
                    row_display.append("   ")

            # Afficher la ligne avec des séparateurs
            print("|" + "|".join(row_display) + "|")
            print("-" * 65)  # Ligne de séparation

    def step(self, game_control,state, action):
        terminated = False
        nbDameMove = 0

        self.display_board_console(game_control.board)
        
        turn = game_control.get_turn()
        print(f"Tour de {'Blancs' if turn == 'W' else 'Noirs'}")

        # Définir les actions possibles
        if not action :
            print(f"Pas d'actions possibles pour {'Blancs' if turn == 'W' else 'Noirs'}.")
            game_control.winner = 'W' if turn == 'B' else 'B'
            print(game_control.get_winner())
            terminated = True

        print(f"Action choisie par {'IA Blancs' if turn == 'W' else 'IA Noirs'} : {action}")

        # Effectuer le mouvement
        if not terminated:
            game_control.board.move_piece(*action)
            isDameMove =  game_control.board.lastMoveIsDame

        if(isDameMove):
            nbDameMove += 1
        else:
            nbDameMove = 0
        if (nbDameMove>=25):
            print("DAME MOVE EXCEEDED")
            terminated = True

        game_control.switch_turn()
        game_control.switch_turn()
        if terminated:
            # Fin du jeu
            self.display_board_console(game_control.board)
            winner = game_control.get_winner()
            print(f"{bcolors.OKCYAN}Le gagnant est : {'Blancs' if winner == 'W' else 'Noirs' if winner == 'B' else 'Aucun'}{bcolors.ENDC}")
        return game_control.GetState(), game_control.board.get_reward(), terminated


    def run(self, is_training = True, render = False):
        num_state = 32
        num_action = 4*32

        policy_net = DQN(num_state, num_action).to(device)

        epsilonHistory = []
        reward_per_episode = []
        if is_training:
            memory = ReplayMemory(maxlen = 10000)
            epsilon = 1.0
            epsilon_decay = 0.995
            epsilon_min = 0.01
       
        for episode in count():
            terminated = False
            episode_reward = 0.0
            gameControl = GameControl()
            state = gameControl.GetState()
            state = torch.tensor(state, dtype = torch.int32, device = device)
             
            while not terminated:
                action = gameControl.get_all_possible_moves(gameControl.get_turn())
                if is_training and random.random() < epsilon:
                    action = random.choice(action)
                    action = torch.tensor(action, dtype = torch.int32, device = device)
                else:
                    with torch.no_grad():
                        action = policy_net(state.unsqueeze(dim=0)).squeeze().argmax()
                #Processing 
                new_state, reward, terminated = gameControl.board.move_piece(*action)
                episode_reward += reward
                new_state = torch.tensor(new_state, dtype = torch.int32, device = device)
                reward = torch.tensor(reward, dtype = torch.float32, device = device)
                if is_training:
                    memory.append((state, action, new_state, reward, terminated))   
                
                state = new_state
            reward_per_episode.append(episode_reward)
            espilon = max(epsilon_min, epsilon *epsilon_decay)
            epsilonHistory.append(epsilon)
if __name__ == "__main__":
    agent = Agent()
    agent.run()