import numpy as np
from sklearn.neighbors import KernelDensity
import sys
import os


param = sys.argv[1] + "/"

def cleanPD(pd, cut, power=0.5):  # Apply cuts onto PDs?
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

def PI(sigma=None, pd=None, bounds=None, res=[30, 30]):
    #nbrs = NearestNeighbors(n_neighbors=nn).fit(pd)
    #kde = KernelDensity(bandwidth=sigma, algorithm='kd_tree', kernel='epanechnikov').fit(pd, sample_weight=np.log([1 + abs(elm[1]) for elm in pd]))
    kde = KernelDensity(bandwidth=sigma, algorithm='kd_tree', kernel='epanechnikov').fit(pd, sample_weight=[elm[1] for elm in pd])
    
    x = np.linspace(bounds[0], bounds[1], res[0])
    y = np.linspace(bounds[2], bounds[3], res[1])
    xx, yy = np.meshgrid(x, y)
    xx = xx.ravel()
    yy = yy.ravel()
    xy_sample = np.array([[xx[i], yy[i]] for i in range(len(xx))])
    d = np.exp(kde.score_samples(xy_sample))
    #distances, indices = nbrs.kneighbors(xy_sample)
    #d = np.array([np.sum([np.log(1 + pd[indices[i][j]][1]) * np.exp(-0.5 * (distances[i][j])**2 / sigma**2) for j in range(len(distances[i]))]) for i in range(len(distances))])
    
    return np.reshape(d, (res[1], res[0])) * sum([elm[1] for elm in pd])

def calcSavePI(diag, sample=None):       
    dimPow = 1
    power = float(dimPow)
    p0, p1, p2 = cleanPD(diag, 0, power)  # pX = [[birth, persistence], [item 2], [item 3]]

    # bound0=np.concatenate(([np.percentile(p0, 0.1, axis=0)[0], 0], np.percentile(p0, 99.9, axis=0), [np.percentile(p0[:,0]+p0[:,1], 0.1, axis=0)],[np.percentile(p0[:,0]+p0[:,1], 99.9, axis=0)]), axis=0)  # minbirth, minpersis, maxbirth, maxpersis, mindeath, maxdeath
    # bound1=np.concatenate(([np.percentile(p1, 0.1, axis=0)[0], 0], np.percentile(p1, 99.9, axis=0), [np.percentile(p1[:,0]+p1[:,1], 0.1, axis=0)],[np.percentile(p1[:,0]+p1[:,1], 99.9, axis=0)]), axis=0)
    # bound2=np.concatenate(([np.percentile(p2, 0.1, axis=0)[0], 0], np.percentile(p2, 99.9, axis=0), [np.percentile(p2[:,0]+p2[:,1], 0.1, axis=0)],[np.percentile(p2[:,0]+p2[:,1], 99.9, axis=0)]), axis=0)
    bounds = np.load("bounds.npy")
    bound0 = bounds[0]
    bound1 = bounds[1]
    bound2 = bounds[2]
        
    res_len = 200
    img0=PI(5*min([(bound0[2]-bound0[0])/res_len,(bound0[3])/res_len]),p0,[0.9*bound0[0],1.1*bound0[2],0,1.1*bound0[3]],res=[res_len,res_len])  # res=higher the finer
    img1=PI(5*min([(bound1[2]-bound1[0])/res_len,(bound1[3])/res_len]),p1,[0.9*bound1[0],1.1*bound1[2],0,1.1*bound1[3]],res=[res_len,res_len])
    img2=PI(5*min([(bound2[2]-bound2[0])/res_len,(bound2[3])/res_len]),p2,[0.9*bound2[0],1.1*bound2[2],0,1.1*bound2[3]],res=[res_len,res_len]) 

    return [img0, img1, img2]


mvFolder = "/staging/hyip2/PIcal_5/"
for folderNum in [0, 25, 50, 75]:
    toSaveImg = []
    dir = param.replace("/", "")+"_"+str(folderNum)+"_"+str(folderNum+25)+"_5"
    for file in os.listdir(dir):
        print(dir+"/"+file)
        diag = np.load(dir+"/"+file)
        diag = [[elm[0], [elm[1], elm[2]]] for elm in diag]  # [dimension, [birth, death]]
        imgs = calcSavePI(diag)
        toSaveImg.append(imgs)
    np.save(param.replace("/", "")+"_"+str(folderNum)+"_"+str(folderNum+25)+"_img", np.array(toSaveImg))
    os.system("mv "+param.replace("/", "")+"_"+str(folderNum)+"_"+str(folderNum+25)+"_img.npy"+" "+mvFolder)
