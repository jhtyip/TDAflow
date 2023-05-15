import numpy as np
from sklearn.neighbors import KernelDensity

import sys


def cleanPD(pd, cut, power=0.5):
    p0 = []
    p1 = []
    p2 = []
    for elm in pd:
        if elm[0] == 2 and elm[1][1] != elm[1][0] and elm[1][1] > (float(cut) / 2)**2:  # If it is a 2-cycle, birth != death and death > cut (= 0)
            p2.append([np.power(elm[1][0], power), np.power(elm[1][1] - elm[1][0], power)])  # [birth, persistence]
        
        elif elm[0] == 1 and elm[1][1] != elm[1][0] and elm[1][1] > (float(cut) / 2)**2:
            p1.append([np.power(elm[1][0], power), np.power(elm[1][1] - elm[1][0], power)])
        
        elif (np.isinf(elm[1][1])) == False and elm[1][1] != elm[1][0] and elm[1][1] > (float(cut) / 2)**2:  # If death is not infinite, birth != death and death > cut (= 0) 
            p0.append([np.power(elm[1][0], power), np.power(elm[1][1] - elm[1][0], power)])
    return np.array(p0), np.array(p1), np.array(p2)

def PI(sigma=None, pd=None, bounds=None, res=None):
    kde = KernelDensity(bandwidth=sigma, algorithm='kd_tree', kernel='gaussian').fit(pd, sample_weight=[np.sqrt(elm[1]) for elm in pd])
    
    x = np.linspace(bounds[0], bounds[1], res[0])
    y = np.linspace(bounds[2], bounds[3], res[1])
    xx, yy = np.meshgrid(x, y)
    xx = xx.ravel()
    yy = yy.ravel()
    xy_sample = np.array([[xx[j], yy[j]] for j in range(len(xx))])
    d = np.exp(kde.score_samples(xy_sample))
    
    return np.reshape(d, (res[1], res[0])) * sum([elm[1] for elm in pd])

def calcSavePI(p0, p1, p2, bounds_fileName, res_len, sigma):       
    # bound0=np.concatenate(([np.percentile(p0, 0.1, axis=0)[0], 0], np.percentile(p0, 99.9, axis=0), [np.percentile(p0[:,0]+p0[:,1], 0.1, axis=0)],[np.percentile(p0[:,0]+p0[:,1], 99.9, axis=0)]), axis=0)  # minbirth, minpersis, maxbirth, maxpersis, mindeath, maxdeath
    # bound1=np.concatenate(([np.percentile(p1, 0.1, axis=0)[0], 0], np.percentile(p1, 99.9, axis=0), [np.percentile(p1[:,0]+p1[:,1], 0.1, axis=0)],[np.percentile(p1[:,0]+p1[:,1], 99.9, axis=0)]), axis=0)
    # bound2=np.concatenate(([np.percentile(p2, 0.1, axis=0)[0], 0], np.percentile(p2, 99.9, axis=0), [np.percentile(p2[:,0]+p2[:,1], 0.1, axis=0)],[np.percentile(p2[:,0]+p2[:,1], 99.9, axis=0)]), axis=0)
    bounds = np.load(bounds_fileName)
    bound0 = bounds[0]
    bound1 = bounds[1]
    bound2 = bounds[2]
    
    img0=PI(sigma,p0,[0.9*bound0[0],1.1*bound0[2],0,1.1*bound0[3]],res=[res_len,res_len])  # res=higher the finer
    img1=PI(sigma,p1,[0.9*bound1[0],1.1*bound1[2],0,1.1*bound1[3]],res=[res_len,res_len])
    img2=PI(sigma,p2,[0.9*bound2[0],1.1*bound2[2],0,1.1*bound2[3]],res=[res_len,res_len]) 

    return [img0, img1, img2]

def stat1D(pd, bbounds, pbounds, dbounds, res_len):
    bvals = pd[:,0]
    pvals = pd[:,1]
    dvals = pd[:,0] + pd[:,1]

    bvec = np.histogram(bvals, bins=np.linspace(bbounds[0], bbounds[1], res_len+1))[0]
    pvec = np.histogram(pvals, bins=np.linspace(pbounds[0], pbounds[1], res_len+1))[0]
    dvec = np.histogram(dvals, bins=np.linspace(dbounds[0], dbounds[1], res_len+1))[0]

    return bvec, pvec, dvec

def calcSaveStat1D(p0, p1, p2, bounds_fileName, res_len):
    bounds = np.load(bounds_fileName)
    bound0 = bounds[0]
    bound1 = bounds[1]
    bound2 = bounds[2]

    bvec0, pvec0, dvec0 = stat1D(p0, [0.9*bound0[0],1.1*bound0[2]], [0,1.1*bound0[3]], [0.9*bound0[0]+0,1.1*bound0[2]+1.1*bound0[3]], res_len)
    bvec1, pvec1, dvec1 = stat1D(p1, [0.9*bound1[0],1.1*bound1[2]], [0,1.1*bound1[3]], [0.9*bound1[0]+0,1.1*bound1[2]+1.1*bound1[3]], res_len)
    bvec2, pvec2, dvec2 = stat1D(p2, [0.9*bound2[0],1.1*bound2[2]], [0,1.1*bound2[3]], [0.9*bound2[0]+0,1.1*bound2[2]+1.1*bound2[3]], res_len)

    return np.concatenate((bvec0, bvec1, bvec2, pvec0, pvec1, pvec2, dvec0, dvec1, dvec2))


om_input = sys.argv[1]
s8_input = sys.argv[2]
a0 = float(sys.argv[3])
z = float(sys.argv[4])
n_steps = int(sys.argv[5])
L = int(sys.argv[6])
N = int(sys.argv[7])
batch = int(sys.argv[8])
arg_k_ = int(sys.argv[9])
bounds_fileName = sys.argv[10]  # /staging/hyip2/TDAflow/PIGen/bounds.npy
res_len = int(sys.argv[11])
sigma = float(sys.argv[12])

i = int(sys.argv[13])

pd_fileName = "fs_{}_{}_{}_{}_{}_{}_{}_{}_swp_{}_{}".format(om_input, s8_input, a0, z, n_steps, L, N, batch, i, arg_k_)

pd = np.load("/staging/hyip2/TDAflow/PHGen/PD/{}.npy".format(pd_fileName))
pd = [[elm[0], [elm[1], elm[2]]] for elm in pd]  # [dimension, [birth, death]]
p0, p1, p2 = cleanPD(pd, 0, 1)
PIs = calcSavePI(p0, p1, p2, bounds_fileName, res_len, sigma)
vec = calcSaveStat1D(p0, p1, p2, bounds_fileName, res_len)

np.save("/staging/hyip2/TDAflow/PIGen/{}/{}_{}_{}_{}".format(0, pd_fileName, 0, res_len, sigma), PIs[0])
np.save("/staging/hyip2/TDAflow/PIGen/{}/{}_{}_{}_{}".format(1, pd_fileName, 1, res_len, sigma), PIs[1])
np.save("/staging/hyip2/TDAflow/PIGen/{}/{}_{}_{}_{}".format(2, pd_fileName, 2, res_len, sigma), PIs[2])
np.save("/staging/hyip2/TDAflow/vecGen/{}_{}".format(pd_fileName, res_len), vec)
