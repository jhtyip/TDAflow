import os
import numpy as np
import h5py
import utilities
import random



class TrainingDataPersistentImages_64px_2p0_Om_s8():
    
    def __init__(self):
        
        base_path  = '/home/adamrouhiainen/homology/data/'
        
        self.trainset = np.load(base_path + 'train/train_samples.npy')
        self.valset   = np.load(base_path + 'train/val_samples.npy')
        self.testset  = np.load(base_path + 'test/test_samples.npy')
        
        self.train_om = np.load(base_path + 'train/om_train.npy')
        self.val_om   = np.load(base_path + 'train/om_val.npy')
        self.test_om  = np.ones((self.testset.shape[0]))*0.3089
        
        self.train_s8 = np.load(base_path + 'train/s8_train.npy')
        self.val_s8   = np.load(base_path + 'train/s8_val.npy')
        self.test_s8  = np.ones((self.testset.shape[0]))*0.8159
        
        
    def draw_samples_of_px(self, batch_size):
        idx = np.random.randint(33000, size=batch_size)
        
        samples = self.trainset[idx]
        om = self.train_om[idx]
        s8 = self.train_s8[idx]
        
        return samples, om, s8
    
    
    def draw_samples_of_pv(self, batch_size):
        idx = np.random.randint(3000, size=batch_size)
        
        samples = self.valset[idx]
        om = self.val_om[idx]
        s8 = self.val_s8[idx]
        
        return samples, om, s8
    
    
    def draw_samples_of_pt(self, batch_size):
        #idx = np.random.randint(1000, size=batch_size)
        
        samples = self.testset[:batch_size]
        om = self.test_om[:batch_size]
        s8 = self.test_s8[:batch_size]
        
        return samples, om, s8
    

    

class TrainingDataPersistentImages_64px_10ave_2p0_Om_s8():
    
    def __init__(self):
        
        base_path  = '/home/adamrouhiainen/homology/data/'
        
        self.trainset = np.load(base_path + 'train_ave/train_samples.npy')
        self.valset   = np.load(base_path + 'train_ave/val_samples.npy')
        self.testset  = np.load(base_path + 'test_ave/test_samples_2.npy')
        
        self.train_om = np.load(base_path + 'train_ave/om_train.npy')
        self.val_om   = np.load(base_path + 'train_ave/om_val.npy')
        self.test_om  = np.ones((self.testset.shape[0]))*0.3089
        
        self.train_s8 = np.load(base_path + 'train_ave/s8_train.npy')
        self.val_s8   = np.load(base_path + 'train_ave/s8_val.npy')
        self.test_s8  = np.ones((self.testset.shape[0]))*0.8159
        
        
    def draw_samples_of_px(self, batch_size):
        idx = np.random.randint(3300, size=batch_size)
        
        samples = self.trainset[idx]
        om = self.train_om[idx]
        s8 = self.train_s8[idx]
        
        return samples, om, s8
    
    
    def draw_samples_of_pv(self, batch_size):
        idx = np.random.randint(300, size=batch_size)
        
        samples = self.valset[idx]
        om = self.val_om[idx]
        s8 = self.val_s8[idx]
        
        return samples, om, s8
    
    
    def draw_samples_of_pt(self, batch_size):
        #idx = np.random.randint(1000, size=batch_size)
        
        samples = self.testset[:batch_size]
        om = self.test_om[:batch_size]
        s8 = self.test_s8[:batch_size]
        
        return samples, om, s8
    
    
    
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