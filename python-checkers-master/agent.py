import torch
from torch import nn
from dqn import DQN 
from experience_replay import ReplayMemory
from itertools import count
import random
import os
import numpy as np
os.environ["CUDA_LAUNCH_BLOCKING"] = "1"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
os.environ['TORCH_USE_CUDA_DSA'] = '1'
from game_control import GameControl
from Graphique import Graphics
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
    def __init__(self):
        self.loss_fn = torch.nn.MSELoss()
        self.optimizer = None
        self.nbDameMove = 0
        self.discount_factor_g = 0.99
    def display_board_console(self,board):
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
        

        #self.display_board_console(game_control.board)
        reward = 0
        game_control.board.lastReward = 0
        turn = game_control.get_turn()
        oppositeTurn = 'W' if turn == 'B' else 'B'
        #print(f"Tour de {'Blancs' if turn == 'W' else 'Noirs'}")

        exitList = (-1,-1)

        noMove = all(x == y for x, y in zip(action, exitList))

        # Définir les actions possibles
        if not action or noMove:
            #print(f"Pas d'actions possibles pour {'Blancs' if turn == 'W' else 'Noirs'}.")
            game_control.winner = 'W' if turn == 'B' else 'B'
            #print(game_control.get_winner())
            terminated = True
            enemiePieces = game_control.board.get_piecesByColor(oppositeTurn)
            allyPieces = game_control.board.get_piecesByColor(turn)
            if(len(allyPieces)!=0 and len(allyPieces)>len(enemiePieces)):
                reward = -50
            elif(len(allyPieces)!=0 and len(allyPieces)<len(enemiePieces)):
                reward = 50
            else:
                reward = -100

        #print(f"Action choisie par {'IA Blancs' if turn == 'W' else 'IA Noirs'} : {action}")

        # Effectuer le mouvement
        isDameMove = False
        if not terminated:
            game_control.board.move_piece(*action)
            isDameMove =  game_control.board.lastMoveIsDame
            if game_control.get_all_possible_moves(oppositeTurn) == []:
                enemiePieces = game_control.board.get_piecesByColor(oppositeTurn)
                allyPieces = game_control.board.get_piecesByColor(turn)
                if(len(enemiePieces)!=0 and len(enemiePieces)>len(allyPieces)):
                    reward = 50
                elif(len(enemiePieces)!=0 and len(enemiePieces)<len(allyPieces)):
                    reward = -50
                else:
                    reward = 100
                #print("No more possible moves for the opponent")
        
        
        if(isDameMove):
            self.nbDameMove += 1
        else:
            self.nbDameMove = 0
        if (self.nbDameMove>=25):
            #print("DAME MOVE EXCEEDED")
            reward = -50
            terminated = True

        
        if terminated:
            #self.display_board_console(game_control.board)
            winner = game_control.get_winner()
            #print(f"{bcolors.OKCYAN}Le gagnant est : {'Blancs' if winner == 'W' else 'Noirs' if winner == 'B' else 'Aucun'}{bcolors.ENDC}")

        reward = game_control.board.lastReward + reward
        game_control.switch_turn()
        return game_control.GetState(),reward, terminated #state, reward, terminated


    def run(self, is_training = True, render = False):
        num_state = 32+1
        num_action = 183+1

        policy_net = DQN(num_state, num_action).to(device)

        epsilonHistory = []
        reward_per_episode = []
        if is_training:
            memory = ReplayMemory(maxlen = 10000)
            epsilon = 1.0
            epsilon_decay = 0.999995
            epsilon_min = 0.01
            target_net = DQN(num_state, num_action).to(device)
            target_net.load_state_dict(policy_net.state_dict())
            syncRate = 10
            step_count = 0  # Compteur de pas pour la mise à jour du réseau cible
            learning_rate = 0.001
            self.optimizer = torch.optim.Adam(policy_net.parameters(), lr = learning_rate)
       
        for episode in range(10000):
            terminated = False
            episode_reward = 0.0
            gameControl = GameControl()
            oGstate = gameControl.GetState()
            state = torch.tensor(oGstate, dtype = torch.float32, device = device)
            
            while not terminated:
                action = gameControl.get_all_possible_moves(gameControl.get_turn()) # action = (ancienne position , nouvelle position)
                if (gameControl.get_turn() == 'B'):
                    if len(action) != 0:
                        action = random.choice(action)
                    else:
                        action = (-1,-1)
                    new_state, reward, terminated = self.step(gameControl,oGstate,action)
                    if not terminated:
                        continue
                    else:
                        break

                if is_training and random.random() < epsilon:
                    if len(action) != 0:
                        action = random.choice(action)
                    else:
                        action = (-1,-1)
                    original_action = action
                    action = [key for key, value in gameControl.board.moves_dict.items() if value == action]
                    if len(action)<=0:
                        testAction = gameControl.get_all_possible_moves(gameControl.get_turn())
                    action = action[0]
                    
                    action = torch.tensor(action, dtype = torch.int64, device = device)
                else:
                    with torch.no_grad():
                        actionPossibilities = action.copy()

                        if len(actionPossibilities)<=0:
                            actionPossibilities.append((-1,-1))
                            action = (-1,-1)

                        index = [key for move in actionPossibilities for key, value in gameControl.board.moves_dict.items() if value == move]
                        actionChosen = policy_net(state.unsqueeze(dim=0)).squeeze()
                        actionQList = actionChosen.tolist()
                        actionQvalueXIndex = actionQList.copy()

                        for i in range(len(actionQList)):
                            actionQvalueXIndex[i] = (actionQList[i],i)
                        actionQvalueXIndex.sort()
                        actionQvalueXIndex.reverse()

                        for i in range(len(actionQvalueXIndex)):
                            if actionQvalueXIndex[i][1] in index:
                                action = torch.tensor(actionQvalueXIndex[i][1], dtype = torch.int64, device = device)
                                original_action = gameControl.board.moves_dict[actionQvalueXIndex[i][1]]
                                break
                        
                #Processing 
                #gameControl.board.move_pieceAgent(*original_action)
                new_state, reward, terminated = self.step(gameControl,oGstate,original_action) #FAIRE LA REWARD ET LE TERMINATED
                episode_reward += reward
                new_state = torch.tensor(new_state, dtype = torch.float32, device = device)
                reward = torch.tensor(reward, dtype = torch.float32, device = device)
                if is_training:
                    memory.append((state, action, new_state, reward, terminated))   
                    step_count += 1
                
                state = new_state

            reward_per_episode.append(episode_reward)
            epsilon = max(epsilon_min, epsilon *epsilon_decay)
            epsilonHistory.append(epsilon)

            if is_training and len(memory) >= 32:
                batch = memory.sample(32)
                self.optimize(policy_net, target_net, batch)

                if step_count > syncRate:
                    target_net.load_state_dict(policy_net.state_dict())
                    step_count = 0
                # actionChosen = policy_net(state.unsqueeze(dim=0)).squeeze()
                # actionQList = actionChosen.tolist()
                #print(f"Episode {episode} : Reward = {episode_reward}, Epsilon = {epsilon}, Action Q-Values = {actionQList}")
            if episode % 500 == 0:    
                print("Iteration: "+str(episode),"Epsilon: "+str(epsilon))

                mean_reward = np.zeros(len(reward_per_episode))
                for x in range(len(mean_reward)):
                    mean_reward[x] = np.mean(reward_per_episode[max(0,x-99):x+1])
                mean_reward = mean_reward.tolist()
                Graphics(mean_reward, 'W',epsilonHistory).save_plot_as_image("Epsilon","Reward")
                policy_net.save_model('dqn_model.pth')

        return reward_per_episode 
     # Optimize policy network
    def optimize(self, policy_dqn, target_dqn, mini_batch,):

        # Transpose the list of experiences and separate each element
        states, actions, new_states, rewards, terminations = zip(*mini_batch)

        # Stack tensors to create batch tensors
        # tensor([[1,2,3]])
        states = torch.stack(states)

        actions = torch.stack(actions)

        new_states = torch.stack(new_states)

        rewards = torch.stack(rewards)
        terminations = torch.tensor(terminations).float().to(device)

        with torch.no_grad():
            # if self.enable_double_dqn:
            #     best_actions_from_policy = policy_dqn(new_states).argmax(dim=1)

            #     target_q = rewards + (1-terminations) * self.discount_factor_g * \
            #                     target_dqn(new_states).gather(dim=1, index=best_actions_from_policy.unsqueeze(dim=1)).squeeze()
            # else:
                # Calculate target Q values (expected returns)
                target_q = rewards + (1-terminations) * self.discount_factor_g * target_dqn(new_states).max(dim=1)[0]
                '''
                    target_dqn(new_states)  ==> tensor([[1,2,3],[4,5,6]])
                        .max(dim=1)         ==> torch.return_types.max(values=tensor([3,6]), indices=tensor([3, 0, 0, 1]))
                            [0]             ==> tensor([3,6])
                '''

        # Calcuate Q values from current policy


        # print(f"actions: {actions}")
        # print(f"actions min: {actions.min()}, actions max: {actions.max()}")
        # print(f"policy_dqn(states) shape: {policy_dqn(states).shape}")
        # print("Actions shape before unsqueeze:", actions.shape)
        # print("Actions shape after unsqueeze:", actions.unsqueeze(1).shape)

        current_q = policy_dqn(states).gather(1, actions.unsqueeze(1)).squeeze()
        '''
            policy_dqn(states)  ==> tensor([[1,2,3],[4,5,6]])
                actions.unsqueeze(dim=1)
                .gather(1, actions.unsqueeze(dim=1))  ==>
                    .squeeze()                    ==>
        '''
        # Afficher la forme de current_q et target_q
        # print("Shape of current_q:", current_q.shape)
        # print("Shape of target_q:", target_q.shape)

        # Compute loss
        loss = self.loss_fn(current_q, target_q)

        # Optimize the model (backpropagation)
        self.optimizer.zero_grad()  # Clear gradients
        loss.backward()             # Compute gradients
        self.optimizer.step()       # Update network parameters i.e. weights and biases

        
if __name__ == "__main__":
    agent = Agent()
    rewardFinal = agent.run()
    graphics = Graphics(rewardFinal, 'W')
    graphics.show_plot()