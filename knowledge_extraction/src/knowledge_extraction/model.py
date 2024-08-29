from math import prod
import torch
import torch.nn as nn
import torch.nn.functional as F


# Dense model:
class DenseModel(nn.Module):
    def __init__(self, input_shape, num_classes):
        """
        An MLP to be trained as a classifier.


        Parameters
        ----------
        input_shape: tuple
            A tuple representing the sizes of the input along all dimensions.
        num_classes: int
            The number of classes
        """
        super().__init__()
        input_size = prod(input_shape)
        self.fc0 = nn.Linear(input_size, 256)
        self.fc1 = nn.Linear(256, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, num_classes)  # output

    def forward(self, x):
        x = torch.flatten(x, 1)  # flatten all dimensions except batch
        x = F.relu(self.fc0(x))
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x