import torch
from dqn import DQN 

class Agent : 
    def run(self, is_training = True, render = False):
        num_state = 32
        num_action = 0

        policy_net = DQN(num_state, num_action)

        while True:
            break