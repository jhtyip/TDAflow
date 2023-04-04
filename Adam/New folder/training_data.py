import os
import numpy as np
import h5py
import utilities
import random



class TrainingDataPersistentImages0_Om_s8():
    
    def __init__(self):
        
        base_path  = '/home/adamrouhiainen/data/persistent_images_Om_s8/PIGen_32px/'
        path_train = base_path + '012_train/'
        path_val   = base_path + '012_val/'
        path_test  = base_path + '012_test/'
        
        self.trainset = np.load(path_train + 'train_samples.npy')
        self.valset   = np.load(path_val   + 'val_samples.npy')
        self.testset  = np.load(path_test  + 'test_samples.npy')
        
        self.train_om = np.load(path_train + 'om_train.npy')
        self.val_om   = np.load(path_val   + 'om_val.npy')
        self.test_om  = np.load(path_test  + 'om_test.npy')
        
        self.train_s8 = np.load(path_train + 's8_train.npy')
        self.val_s8   = np.load(path_val   + 's8_val.npy')
        self.test_s8  = np.load(path_test  + 's8_test.npy')
        
        
    def draw_samples_of_px(self, batch_size):
        idx = np.random.randint(8000, size=batch_size)
        
        samples = self.trainset[idx]
        om = self.train_om[idx]
        s8 = self.train_s8[idx]
        
        return samples, om, s8
    
    
    def draw_samples_of_pv(self, batch_size):
        idx = np.random.randint(1000, size=batch_size)
        
        samples = self.valset[idx]
        om = self.val_om[idx]
        s8 = self.val_s8[idx]
        
        return samples, om, s8
    
    
    def draw_samples_of_pt(self, batch_size):
        idx = np.random.randint(1000, size=batch_size)
        
        samples = self.testset[idx]
        om = self.test_om[idx]
        s8 = self.test_s8[idx]
        
        return samples, om, s8



class TrainingDataPersistentImages0_Om_s8_old():
    
    def __init__(self, nx=32, n_patchfiles=10000, n_trainfiles=8000, n_valfiles=1000, n_testfiles=1000, normalize=True, test=False):
        self.n_trainfiles = n_trainfiles
        self.n_valfiles = n_valfiles
        self.n_testfiles = n_testfiles
        
        base_path_0 = '/home/adamrouhiainen/data/persistent_images_Om_s8/PIGen_32px/0/'
        base_path_1 = '/home/adamrouhiainen/data/persistent_images_Om_s8/PIGen_32px/1/'
        base_path_2 = '/home/adamrouhiainen/data/persistent_images_Om_s8/PIGen_32px/2/'
            
        fnames_train_0 = os.listdir(base_path_0)
        fnames_train_1 = os.listdir(base_path_1)
        fnames_train_2 = os.listdir(base_path_2)
        
        fnames_train_0.sort()
        fnames_train_1.sort()
        fnames_train_2.sort()

        dataset_0 = np.zeros((len(fnames_train_0), nx, nx))
        self.Om_list = np.zeros((len(fnames_train_0)))
        self.s8_list = np.zeros((len(fnames_train_0)))
        i = 0
        for fname in fnames_train_0:
            path = '/home/adamrouhiainen/data/persistent_images_Om_s8/PIGen_32px/0/'+fname
            dataset_0[i] = np.load(path)
            self.Om_list[i] = float(fname.split('_')[1])
            self.s8_list[i] = float(fname.split('_')[2])
            i += 1
            
        dataset_1 = np.zeros((len(fnames_train_1), nx, nx))
        i = 0
        for fname in fnames_train_1:
            path = '/home/adamrouhiainen/data/persistent_images_Om_s8/PIGen_32px/1/'+fname
            dataset_1[i] = np.load(path)
            i += 1
            
        dataset_2 = np.zeros((len(fnames_train_2), nx, nx))
        i = 0
        for fname in fnames_train_2:
            path = '/home/adamrouhiainen/data/persistent_images_Om_s8/PIGen_32px/2/'+fname
            dataset_2[i] = np.load(path)
            i += 1

        #Resize training set
        self.dataset_0 = dataset_0[:n_trainfiles, :nx, :nx]
        self.dataset_1 = dataset_1[:n_trainfiles, :nx, :nx]
        self.dataset_2 = dataset_2[:n_trainfiles, :nx, :nx]
        
        #Resize validation set
        self.valset_0 = dataset_0[n_trainfiles:n_trainfiles+n_valfiles, :nx, :nx]
        self.valset_1 = dataset_1[n_trainfiles:n_trainfiles+n_valfiles, :nx, :nx]
        self.valset_2 = dataset_2[n_trainfiles:n_trainfiles+n_valfiles, :nx, :nx]
        
        #Resize test set
        self.testset_0 = dataset_0[n_trainfiles+n_valfiles:, :nx, :nx]
        self.testset_1 = dataset_1[n_trainfiles+n_valfiles:, :nx, :nx]
        self.testset_2 = dataset_2[n_trainfiles+n_valfiles:, :nx, :nx]

        print("Dataset shape:", np.shape(self.dataset_0))
        
        
    def draw_samples_of_px(self, batch_size):
        idx = np.random.randint(self.n_trainfiles, size=batch_size)
        
        samples_0 = self.dataset_0[idx]
        samples_1 = self.dataset_1[idx]
        samples_2 = self.dataset_2[idx]
        samples = np.stack((samples_0, samples_1, samples_2), axis=1)
                           
        Om = self.Om_list[idx]
        s8 = self.s8_list[idx]
        
        return samples, Om, s8
    
    
    def draw_samples_of_pv(self, batch_size):
        idx = np.random.randint(self.n_valfiles, size=batch_size)
        
        samples_0 = self.valset_0[idx]
        samples_1 = self.valset_1[idx]
        samples_2 = self.valset_2[idx]
        samples = np.stack((samples_0, samples_1, samples_2), axis=1)
                           
        Om = self.Om_list[idx]
        s8 = self.s8_list[idx]
        
        return samples, Om, s8
    
    
    def draw_samples_of_pt(self, batch_size):
        idx = np.random.randint(self.n_testfiles, size=batch_size)
        
        samples_0 = self.testset_0[idx]
        samples_1 = self.testset_1[idx]
        samples_2 = self.testset_2[idx]
        samples = np.stack((samples_0, samples_1, samples_2), axis=1)
                           
        Om = self.Om_list[idx]
        s8 = self.s8_list[idx]
        
        return samples, Om, s8