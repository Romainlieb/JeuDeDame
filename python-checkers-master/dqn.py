import torch
from torch import nn
import torch.nn.functional as torchFunctionnal

class DQN(nn.Module):
    """
    Deep Q-Network (DQN) model for reinforcement learning.
    Args:
        state_dimension (int): Dimension of the input state.
        action_dimension (int): Dimension of the output actions.
        hidden_dimension (int, optional): Dimension of the hidden layers. Default is 256.
    Attributes:
        fc1 (nn.Linear): First fully connected layer.
        fc2 (nn.Linear): Second fully connected layer.
        fc3 (nn.Linear): Third fully connected layer.
    Methods:
        forward(x):
            Defines the forward pass of the network.
            Args:
                x (torch.Tensor): Input tensor representing the state.
            Returns:
                torch.Tensor: Output tensor representing the action values.
    """

    def __init__(self,state_dimension,action_dimension,hidden_dimension = 256):
        super(DQN,self).__init__()
        self.fc1 = nn.Linear(state_dimension,hidden_dimension)
        self.fc2 = nn.Linear(hidden_dimension,hidden_dimension)
        self.fc3 = nn.Linear(hidden_dimension,action_dimension)

    def forward(self,x):
        x = torchFunctionnal.relu(self.fc1(x))
        x = torchFunctionnal.relu(self.fc2(x))
        x = self.fc3(x)
        return x
    
