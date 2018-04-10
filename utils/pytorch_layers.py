import torch
import torch.nn as nn
import torch.nn.init as init
import numpy as np


class Identity(nn.Module):
    def __init__(self):
        super(Identity,self).__init__()

    def forward(self,x):
        return x


def get_activation(name):
    if name=='ReLU':
        return nn.ReLU(inplace=True)
    elif name=='Tanh':
        return nn.Tanh()
    elif name=='Identity':
        return Identity()
    elif name=='Sigmoid':
        return nn.Sigmoid()
    elif name=='LeakyReLU':
        return nn.LeakyReLU(0.2,inplace=True)
    else:
        assert(False), 'Not Implemented'


def create_mlp(const):
    out_activation = pytorch_layers.get_activation(const['out_activation'])
    activation = pytorch_layers.get_activation(const['activation'])
    mlp = MLP(
        in_dim=const['in_dim'],
        out_dim=const['out_dim'],
        out_activation=out_activation,
        activation=activation,
        layer_units=const['layer_units'],
        use_out_bn=const['use_out_bn'],
        use_bn=const['use_bn'])
    return mlp

class MLP(nn.Module):
    def __init__(
            self,
            in_dim,
            out_dim,
            out_activation,
            layer_units=[],
            activation=nn.ReLU(inplace=True),
            use_out_bn=True,
            use_bn=True):
        super(MLP,self).__init__()
        self.layers = nn.ModuleList()
        in_units = in_dim 
        for num_units in layer_units:
            out_units = num_units
            fc_layer = self.linear_with_bn_and_activations(
                in_units,
                out_units,
                activation,
                use_bn)
            self.layers.append(fc_layer)
            in_units = out_units

        fc_layer = self.linear_with_bn_and_activations(
            in_units,
            out_dim,
            out_activation,
            use_out_bn)
        self.layers.append(fc_layer)

    def linear_with_bn_and_activations(
            self,
            in_dim,
            out_dim,
            activation,
            use_bn=True):
        linear = nn.Linear(in_dim,out_dim)
        if use_bn:
            bn = nn.BatchNorm1d(out_dim)
            block = nn.Sequential(linear,bn,activation)
        else:
            block = nn.Sequential(linear,activation)
            
        return block

    def forward(self,x):
        for layer in self.layers:
            x = layer(x)

        return x