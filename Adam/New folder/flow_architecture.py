import utilities

import numpy as np
import torch
import torch.nn as nn


######################## Real NVP flow


def make_checker_mask(shape, parity,torch_device):
    checker = torch.ones(shape, dtype=torch.uint8) - parity
    checker[::2, ::2] = parity
    checker[1::2, 1::2] = parity
    return checker.to(torch_device)



class AffineCoupling(nn.Module):
    def __init__(self, net0, net1, net2, *, mask_shape, mask_parity, torch_device, lattice_shape):
        super().__init__()
        self.mask = make_checker_mask(mask_shape, mask_parity, torch_device)
        
        #A separate network for each 0, 1, and 2-cycle
        self.net0 = net0
        self.net1 = net1
        self.net2 = net2
        
        #Images have global patterns, so parameters to multiply each s and t by
        self.s0_factor = nn.Parameter(torch.ones((mask_shape[0], mask_shape[1])))
        self.t0_factor = nn.Parameter(torch.ones((mask_shape[0], mask_shape[1])))
        self.s1_factor = nn.Parameter(torch.ones((mask_shape[0], mask_shape[1])))
        self.t1_factor = nn.Parameter(torch.ones((mask_shape[0], mask_shape[1])))
        self.s2_factor = nn.Parameter(torch.ones((mask_shape[0], mask_shape[1])))
        self.t2_factor = nn.Parameter(torch.ones((mask_shape[0], mask_shape[1])))
    
    
    def forward(self, x, m1, m2):
        #Mask images
        x_frozen = self.mask*x      
        x_active = (1 - self.mask)*x
        
        #Combine data to input into network
        m1_repeat = m1.unsqueeze(-1).unsqueeze(-1).repeat(1, 1, x.shape[-2], x.shape[-1])
        m2_repeat = m2.unsqueeze(-1).unsqueeze(-1).repeat(1, 1, x.shape[-2], x.shape[-1])
        
        net_in0 = torch.concat((x_frozen[:, 0].unsqueeze(1), m1_repeat, m2_repeat), dim=1)
        net_in1 = torch.concat((x_frozen[:, 1].unsqueeze(1), m1_repeat, m2_repeat), dim=1)
        net_in2 = torch.concat((x_frozen[:, 2].unsqueeze(1), m1_repeat, m2_repeat), dim=1)
        
        #Networks
        net_out0 = self.net0(net_in0)
        net_out1 = self.net1(net_in1)
        net_out2 = self.net2(net_in2)

        s0i, t0i = net_out0[:, 0], net_out0[:, 1]
        s1i, t1i = net_out1[:, 0], net_out1[:, 1]
        s2i, t2i = net_out2[:, 0], net_out2[:, 1]
        
        s0, t0 = torch.tanh(self.s0_factor * s0i), torch.tanh(self.t0_factor * t0i)
        s1, t1 = torch.tanh(self.s1_factor * s1i), torch.tanh(self.t1_factor * t1i)
        s2, t2 = torch.tanh(self.s2_factor * s2i), torch.tanh(self.t2_factor * t2i)
        
        #Affine transformation
        fx0 = (1 - self.mask)*t0 + x_active[:, 0]*torch.exp(s0) + x_frozen[:, 0]
        fx1 = (1 - self.mask)*t1 + x_active[:, 1]*torch.exp(s1) + x_frozen[:, 1]
        fx2 = (1 - self.mask)*t2 + x_active[:, 2]*torch.exp(s2) + x_frozen[:, 2]
        fx = torch.stack((fx0, fx1, fx2), 1)
        
        #Log probability
        logJ = torch.sum((1 - self.mask)*(-s0-s1-s2), dim=tuple(range(1, len(s0.size()))))
        return fx, logJ
    
    
    def reverse(self, fx, m1, m2):
        #Mask images
        fx_frozen = self.mask*fx
        fx_active = (1 - self.mask)*fx
        
        #Combine data to input into network
        m1_repeat = m1.unsqueeze(-1).unsqueeze(-1).repeat(1, 1, fx.shape[-2], fx.shape[-1])
        m2_repeat = m2.unsqueeze(-1).unsqueeze(-1).repeat(1, 1, fx.shape[-2], fx.shape[-1])
        
        net_in0 = torch.concat((fx_frozen[:, 0].unsqueeze(1), m1_repeat, m2_repeat), dim=1)
        net_in1 = torch.concat((fx_frozen[:, 1].unsqueeze(1), m1_repeat, m2_repeat), dim=1)
        net_in2 = torch.concat((fx_frozen[:, 2].unsqueeze(1), m1_repeat, m2_repeat), dim=1)
        
        #Networks
        net_out0 = self.net0(net_in0)
        net_out1 = self.net1(net_in1)
        net_out2 = self.net2(net_in2)

        s0i, t0i = net_out0[:, 0], net_out0[:, 1]
        s1i, t1i = net_out1[:, 0], net_out1[:, 1]
        s2i, t2i = net_out2[:, 0], net_out2[:, 1]
        
        s0, t0 = torch.tanh(self.s0_factor * s0i), torch.tanh(self.t0_factor * t0i)
        s1, t1 = torch.tanh(self.s1_factor * s1i), torch.tanh(self.t1_factor * t1i)
        s2, t2 = torch.tanh(self.s2_factor * s2i), torch.tanh(self.t2_factor * t2i)
        
        #Affine transformation
        x0 = (fx_active[:, 0] - (1 - self.mask)*t0)*torch.exp(-s0) + fx_frozen[:, 0]
        x1 = (fx_active[:, 1] - (1 - self.mask)*t1)*torch.exp(-s1) + fx_frozen[:, 1]
        x2 = (fx_active[:, 2] - (1 - self.mask)*t2)*torch.exp(-s2) + fx_frozen[:, 2]
        x = torch.stack((x0, x1, x2), 1)
        
        #Log probability
        logJ = torch.sum((1 - self.mask)*(-s0-s1-s2), dim=tuple(range(1, len(s0.size()))))
        return x, logJ


    
def make_conv_net(*, hidden_sizes, kernel_size, in_channels, out_channels, use_final_tanh, padding_mode):
    sizes = [in_channels] + hidden_sizes + [out_channels]
    net = []
    for i in range(len(sizes) - 1):
        padding_size = (kernel_size[i]//2)
        net.append(nn.Conv2d(sizes[i], sizes[i+1], kernel_size[i],
                             padding=padding_size, stride=1, padding_mode=padding_mode))
        if i != len(sizes) - 2:
            net.append(nn.LeakyReLU())
        else:
            if use_final_tanh: net.append(nn.Tanh())
    return nn.Sequential(*net)


def make_flow1_affine_layers(*, n_layers, lattice_shape, hidden_sizes, kernel_size, torch_device, padding_mode, bias=False):
    layers = []
    
    for i in range(n_layers):
        parity = i % 2
        
        #A separate network for each 0, 1, and 2-cycle; tanh is applied later
        net0 = make_conv_net(in_channels=3, out_channels=2, hidden_sizes=hidden_sizes,
                             kernel_size=kernel_size, use_final_tanh=False, padding_mode=padding_mode)
        net1 = make_conv_net(in_channels=3, out_channels=2, hidden_sizes=hidden_sizes,
                             kernel_size=kernel_size, use_final_tanh=False, padding_mode=padding_mode)
        net2 = make_conv_net(in_channels=3, out_channels=2, hidden_sizes=hidden_sizes,
                             kernel_size=kernel_size, use_final_tanh=False, padding_mode=padding_mode)
        
        coupling = AffineCoupling(net0, net1, net2, mask_shape=lattice_shape, mask_parity=parity,
                                  torch_device=torch_device, lattice_shape=lattice_shape)
            
        layers.append(coupling)
        
    return nn.ModuleList(layers)


######################## Prior


class SimpleNormal:
    def __init__(self, loc, var):
        self.dist = torch.distributions.normal.Normal(torch.flatten(loc), torch.flatten(var))
        self.shape = loc.shape
        
        
    def log_prob(self, x):
        logp = self.dist.log_prob(x.reshape(x.shape[0], -1))
        return torch.sum(logp, dim=1)
    
    
    def sample_n(self, batch_size):
        x = self.dist.sample((batch_size,))
        return x.reshape(batch_size, *self.shape)


######################## Flow generalities


def apply_flow_to_prior(prior, coupling_layers, batch_size=None, m1=None, m2=None, u=None):
    #Draws from the prior (base distribution) and flows them
    if u == None: u = torch.stack((prior.sample_n(batch_size),
                                   prior.sample_n(batch_size),
                                   prior.sample_n(batch_size)), 1)
    
    log_pu = prior.log_prob(u[:, 0]) + prior.log_prob(u[:, 1]) + prior.log_prob(u[:, 2])
    z = u.clone()
    #log_pz = log_pu.clone()
    log_pz = prior.log_prob(u[:, 0]) + prior.log_prob(u[:, 1]) + prior.log_prob(u[:, 2])
    log_pz.requires_grad_(requires_grad=True)
    for layer in coupling_layers:
        z, logJ = layer.forward(z, m1, m2)
        log_pz -= logJ
    return u, log_pu, z, log_pz


def apply_reverse_flow_to_sample(z, prior, coupling_layers, m1=None, m2=None):
    #Takes samples and calculates their representation in base distribution space and their density 
    log_J_Tinv = 0
    n_layers = len(coupling_layers)
    for layer_id in reversed(range(n_layers)):
        layer = coupling_layers[layer_id]
        z, logJ = layer.reverse(z, m1, m2)
        log_J_Tinv = log_J_Tinv + logJ 
    u = z
    log_pu = prior.log_prob(u[:, 0])+prior.log_prob(u[:, 1])+prior.log_prob(u[:, 2])
    return u, log_pu, log_J_Tinv