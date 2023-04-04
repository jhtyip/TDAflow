import quicklens as ql
import numpy as np
import torch
import torchvision.transforms as T
import torchvision.transforms
import random
import matplotlib.pyplot as plt

import flow_architecture

r2d = 180./np.pi
d2r = np.pi/180.
rad2arcmin = 180.*60./np.pi


def grab(var):
  return var.detach().cpu().numpy()


def plot_lists(list_1=None, list_2=[], idmin=0, trunc=0, ymin=None, ymax=None, offset=0, figsize=(5, 3),
               ylog=False, label1='', label2='', xlabel='', ylabel='', title='', file_name=None):
    idmax = len(list_1) - trunc
    fig=plt.figure(figsize=figsize)
    plt.plot(np.arange(idmin, idmax-offset, 1), list_1[idmin:idmax-offset], color='red', label=label1)
    if len(list_2) > 0: plt.plot(np.arange(idmin, idmax-offset, 1), list_2[idmin:idmax], label=label2)
    if not label1=='': plt.legend(loc=1, frameon=False, fontsize=14)
    plt.grid(True)
    plt.xlabel(xlabel, fontsize=14)
    plt.ylabel(ylabel, fontsize=14)
    plt.title(title)
    if ylog: ax.set_yscale('log')
    if not (ymin==None and ymax==None): plt.ylim([ymin, ymax])
    fig.tight_layout()
    if not file_name==None: plt.savefig(file_name)
    plt.show()
    

def imshow(array, vmin=None, vmax=None, figsize=(8, 8), title='', axis=True, colorbar=True, file_name=None):
    plt.figure(figsize=figsize)
    if (vmin==None and vmax==None): plt.imshow(array)
    else: plt.imshow(array, vmin=vmin, vmax=vmax)
    if not axis: plt.axis('off')
    if colorbar: plt.colorbar()
    plt.title(title)
    plt.tight_layout()
    if not file_name==None: plt.savefig(file_name)