import torch.nn.functional as F
import torch.nn as nn
import torch
import torch.optim as optim
import math
import numpy as np
from torch.nn import init
#from torch.nn.modules import Flatten


class RNDModel(nn.Module):
    def __init__(self, input_size, output_size):
        super(RNDModel, self).__init__()

        self.input_size = input_size
        self.output_size = output_size

        feature_output = 7 * 7 * 64
        self.predictor = nn.Sequential(
            nn.Conv2d(
                in_channels=1,
                out_channels=32,
                kernel_size=8,
                stride=4),
            nn.LeakyReLU(),
            nn.Conv2d(
                in_channels=32,
                out_channels=64,
                kernel_size=4,
                stride=2),
            nn.LeakyReLU(),
            nn.Conv2d(
                in_channels=64,
                out_channels=64,
                kernel_size=3,
                stride=1),
            nn.LeakyReLU(),
            Flatten(),
            nn.Linear(feature_output, 512),
            nn.ReLU(),
            nn.Linear(512, 512),
            nn.ReLU(),
            nn.Linear(512, 512)
        )

        self.target = nn.Sequential(
            nn.Conv2d(
                in_channels=1,
                out_channels=32,
                kernel_size=8,
                stride=4),
            nn.LeakyReLU(),
            nn.Conv2d(
                in_channels=32,
                out_channels=64,
                kernel_size=4,
                stride=2),
            nn.LeakyReLU(),
            nn.Conv2d(
                in_channels=64,
                out_channels=64,
                kernel_size=3,
                stride=1),
            nn.LeakyReLU(),
            Flatten(),
            nn.Linear(feature_output, 512)
        )

        for p in self.modules():
            if isinstance(p, nn.Conv2d):
                init.orthogonal_(p.weight, np.sqrt(2))
                p.bias.data.zero_()

            if isinstance(p, nn.Linear):
                init.orthogonal_(p.weight, np.sqrt(2))
                p.bias.data.zero_()

        for param in self.target.parameters():
            param.requires_grad = False

    def forward(self, next_obs):
        target_feature = self.target(next_obs)
        predict_feature = self.predictor(next_obs)

        return predict_feature, target_feature