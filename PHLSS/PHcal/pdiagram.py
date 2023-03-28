import numpy as np
import gudhi

import fclaux as fc
import param as par

from sklearn.neighbors import KDTree


class DIAG:
    def __init__(self, dat=None, npool=None, outfile=None, N_min=None, savePrefix=None, k_=None):
        self.dat = dat
        self.npool = npool
        self.outfile = outfile
        self.nhalo = N_min
        self.savePrefix = savePrefix
        self.k_ = k_

        self.box = par.box  # Length of box
        self.smallbox = par.smallbox
        self.method = par.method

        if par.box % par.smallbox != 0:
             print("Incorrect value for the sub box size. Please choose an integer dividend of the box size.\n")
             raise SystemExit
        
        self.nsub = self.box // self.smallbox  # Integer division
        
        xx, yy, zz = np.mgrid[0:self.nsub, 0:self.nsub, 0:self.nsub]
        self.xyz_sample = np.vstack([xx.ravel(), yy.ravel(), zz.ravel()]).T  # Transpose. All coordinates
        
        self.parallelPD()


    # Adapted from Chazal code
    def Filtration_value(self, p, fx, fy, d, n=10):  # Filtration value of an edge for alphaDTMl
        # p can only be 1, 2, or np.inf
        if p == np.inf:  # Basically then r of ball = v
            value = max([fx, fy, d/2])  # If fx or fy is so large, once v > fx then the edge appears
        else:
            fmax = max([fx, fy])
            if d < (abs(fx**p - fy**p))**(1 / p):
                value = fmax
            elif p == 1:
                value = (fx + fy + d) / 2
            elif p == 2:
                value = np.sqrt(((fx + fy)**2 + d**2)*((fx - fy)**2 + d**2)) / (2 * d)  # Solution for v for alphaDTMl          
            else:
                Imin = fmax; Imax = (d**p + fmax**p)**(1 / p)
                for i in range(n):
                    I = (Imin + Imax) / 2
                    g = (I**p - fx**p)**(1 / p) + (I**p - fy**p)**(1 / p)
                    if g < d:
                        Imin = I
                    else:
                        Imax = I
                value = I
        
        return value
        

    # Using implementation from Chazal et al.
    def DTM(self, X, query_pts, m):  # X=[x, y, z], m=15/minH
        N_tot = X.shape[0]  # Total number of halos=minH
        k = int(np.floor(m * N_tot)) + 1  # Number of neighbors, i.e. k=15

        kdt = KDTree(X, leaf_size=30, metric='euclidean')
        NN_Dist, NN = kdt.query(query_pts, k+1, return_distance=True)  # NN_Dist = [[query pt1_dist_to_self (=0), pt1_dist_to_1st_neighb, pt1_dist_to_2nd, ..., pt1_dist_to_kth], [pt2_, ...], ...]

        DTM_result = np.sqrt(np.sum(NN_Dist * NN_Dist, axis=1) / k)
    
        return(DTM_result)
        
    
    # Evaluates sublevel filtration of F on alpha complex -- modified from Chazal et al.
    # alphaDTMl-filtration
    def AlphaWeightedFiltration(self, X, m, lDTMmix=False, filtration_max=np.inf):  # F=DTM_values
        p = 2

        alphaComplex = gudhi.AlphaComplex(points=X)
        st_alpha = alphaComplex.create_simplex_tree()

        X_reordered = np.array([alphaComplex.get_point(N) for N in range(X.shape[0])])
        F = self.DTM(X_reordered, X_reordered, m)

        # f = open(self.savePrefix+"_DTMvalues.txt", "a")
        # np.savetxt(f, F, newline=" ")
        # f.write("\n")
        # f.close()

        st = gudhi.SimplexTree()  # Create an empty simplex tree
    
        for simplex in st_alpha.get_filtration():  # Add vertices with corresponding filtration value
            if len(simplex[0]) == 1:
                i = simplex[0][0]
                st.insert([i], filtration=F[i])
            if len(simplex[0]) == 2:  # Add edges with corresponding filtration value
                i = simplex[0][0]
                j = simplex[0][1]
                if lDTMmix == True: 
                    value = self.Filtration_value(p, F[i], F[j], np.linalg.norm(X_reordered[i] - X_reordered[j]))
                else: 
                    value = max([F[i], F[j]])
                st.insert([i, j], filtration=value)
            if len(simplex[0]) == 3:
                i = simplex[0][0]
                j = simplex[0][1]
                k = simplex[0][2]
                value = max([st.filtration([i, j]), st.filtration([j, k]), st.filtration([i, k])])
                st.insert([i, j, k], filtration=value)
            if len(simplex[0]) == 4:
                i = simplex[0][0]
                j = simplex[0][1]
                k = simplex[0][2]
                l = simplex[0][3]
                value=max([st.filtration([i, j, k]), st.filtration([j, k, l]),
                           st.filtration([i, k, l]), st.filtration([i, j, l])])
                st.insert([i, j, k, l], filtration=value)
        
        return st


    # Inspired by Chazal et al.
    # alphaDTMl-filtration
    def AlphaDTMFiltration(self, X, m, lDTMmix=True, filtration_max=np.inf):  # X=[x, y, z], m=15/minH
        st = self.AlphaWeightedFiltration(X, m, lDTMmix, filtration_max)

        return st
        

    def computeSavePDalphaDTM(self, sample=None, lDTMmix=None, dat=None, nsub=None, smallbox=None, outfile=None, k_=None):
        x0,y0,z0=sample[0],sample[1],sample[2]  # No sub-box => x0,y0,z0=0,0,0
        dat_slice=dat[(dat[:,3]>=smallbox*z0)*(dat[:,3]<smallbox*(z0+1))]
        dat_slice=dat_slice[(dat_slice[:,2]>=smallbox*y0)*(dat_slice[:,2]<smallbox*(y0+1))]
        dat_slice=dat_slice[(dat_slice[:,1]>=smallbox*x0)*(dat_slice[:,1]<smallbox*(x0+1))]
        
        # minH=int(self.nhalo)
        # ind=np.random.choice(range(np.shape(dat_slice)[0]),minH,replace=False)
        # dat_slice=dat_slice[ind,:]
        
        m=k_/np.shape(dat_slice)[0]  # = 15/number of halos = 15/minH
        st=self.AlphaDTMFiltration(dat_slice[:,1:],m,lDTMmix)  # Return simplex tree
        
        diag_alpha=st.persistence(min_persistence=0.01)
        fc.savePD(diag_alpha,outfile,self.savePrefix)
	

    def computeSavePDalpha(self, sample=None, lDTMmix=None, dat=None, nsub=None, smallbox=None, outfile=None, k_=None):
        x0,y0,z0=sample[0],sample[1],sample[2]
        dat_slice=dat[(dat[:,3]>=smallbox*z0)*(dat[:,3]<smallbox*(z0+1))]
        dat_slice=dat_slice[(dat_slice[:,2]>=smallbox*y0)*(dat_slice[:,2]<smallbox*(y0+1))]
        dat_slice=dat_slice[(dat_slice[:,1]>=smallbox*x0)*(dat_slice[:,1]<smallbox*(x0+1))]

        # minH=int(self.nhalo)
        # ind=np.random.choice(range(np.shape(dat_slice)[0]),minH,replace=False)
        # dat_slice=dat_slice[ind,:]
        
        ac=gudhi.AlphaComplex(points=dat_slice[:,1:])
        st=ac.create_simplex_tree()
        
        diag_alpha=st.persistence(min_persistence=0.01)
        fc.savePD(diag_alpha,outfile,self.savePrefix)


    '''
    def computeSavePDsub(self, sample=None, dat=None, nsub=None, smallbox=None, outfile=None):  # Compute and save persistence diagram?
        x0, y0, z0 = sample[0], sample[1], sample[2]  # Single numbers
        dat_slice = dat[(dat[:, 3] > smallbox * z0) * (dat[:, 3] < smallbox * (z0 + 1))]  # x0, y0, z0 should be < 1 and in the unit of smallbox
        dat_slice = dat_slice[(dat_slice[:, 2] > smallbox * y0) * (dat_slice[:, 2] < smallbox * (y0 + 1))]
        dat_slice = dat_slice[(dat_slice[:, 1] > smallbox * x0) * (dat_slice[:, 1] < smallbox * (x0 + 1))]
        minH = 60000  # The minimum number of halos to be matched
        ind = np.random.choice(range(np.shape(dat_slice)[0]), minH, replace=False)  # Pick 60000 halos without replacement
        dat_slice = dat_slice[ind, :]  # Select the picked "rows"
        #print("Done slicing\n")
        
        nbrs = NearestNeighbors(n_neighbors=15, algorithm='ball_tree').fit(dat_slice[:, 1:])  # Now it's a class. Number of nearest neighb = 15
        xx, yy, zz = np.mgrid[smallbox * x0:smallbox * (x0 + 1):4, smallbox * y0:smallbox * (y0 + 1):4, smallbox * z0:smallbox * (z0 + 1):4]  # Why use 4 as the separation?
        xyz_sample = np.vstack([xx.ravel(), yy.ravel(), zz.ravel()]).T
        distances, indices = nbrs.kneighbors(xyz_sample)  # Query set contains the sample coordinates (grid points)
        
        DTM = np.array([np.sqrt(np.sum([((distances[i][j]) / np.log10(dat_slice[indices[i][j]][0]))**2 for j in range(len(distances[i]))])) for i in range(len(distances))])
        # For every query point, find 15 nearest neighbour halos
        # dat (or dat_slice) is [[some halo prop, x-coor, y, z], [], [], ...]
        # For each of the neighbours, compute value = sqrt(sum((distance / something)**2))
        # DTM = [value1, value2, value3, ...] for the query pt set

        #DTM = np.reshape(DTM, xx.shape)
        dim = smallbox // 4
        cc = gudhi.CubicalComplex(dimensions=[dim, dim, dim], top_dimensional_cells=DTM)
        diag_cc = cc.persistence(min_persistence=0.01)
        #print('persistent homology computed\n')
        
        outfile = outfile.replace("000", str(x0) + str(y0) + str(z0))
        outfile = outfile.replace("PD.gz", "PD_sub.gz")
        #print('Now saving file %s' %outfile)
        fc.savePD(diag_cc, outfile,self.savePrefix)
    '''


    # Parallelization
    def parallelPD(self):
        if self.method == 0:  # alpha
            self.computeSavePDalpha([0,0,0], self.dat, self.nsub, self.smallbox, self.outfile)
        if self.method == 2:  # alpha-DTM
            self.computeSavePDalphaDTM([0,0,0], False, self.dat, self.nsub, self.smallbox, self.outfile, self.k_)
        if self.method == 3:  # alpha-DTM with length-DTM mixing
            self.computeSavePDalphaDTM([0,0,0], True, self.dat, self.nsub, self.smallbox, self.outfile, self.k_)
