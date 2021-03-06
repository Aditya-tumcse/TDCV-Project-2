import torch
import os
import numpy as np
import random
import configuration
from torch.utils.data import Dataset,DataLoader


class BalletDancer(Dataset):
    def __init__(self,transform=None):
        super(BalletDancer,self).__init__()
        np.random.seed(0)
        self.idx = 0
        self.data = self.load_patch()
        self.transform = transform

    def load_patch(self):
        rootdir = configuration.training_configuration.training_set_dir
        path, dirs, files = next(os.walk(rootdir))
        dirs = sorted(dirs)
        data_set = self.data_initializer()
        
        visible_key_point = np.load(rootdir + "/kp_visibility.npz",allow_pickle=True)['visibility']
        
        k = 0
        for i in range(int(min(dirs)),int(max(dirs)),configuration.Training_Data_Config.stride):
            cam_num = os.listdir(rootdir + str(i))
            
            for cam in range(len(cam_num)):
                visible_kp = visible_key_point[k][cam]
                for j in range(len(visible_kp)):
                    key_point = visible_kp[j]
                    data_set[key_point].append((i,cam))
                    
                    self.idx += 1
                
            k += 1
        print("Data loading complete")
        return data_set
        
    def data_initializer(self):
        data_set = {}
        for n in range(configuration.Training_Data_Config.number_keypoints):
            data_set[n] = []
        return data_set
        
    def _get_patch_path_(self,frame_num,cam_num,kp_num):
        rootdir = configuration.training_configuration.training_set_dir
        return(rootdir + str(frame_num) + "/" + str(frame_num) + "_" + str(cam_num) + "/tsdf_patch_" + str(kp_num) + ".npz")

    def _get_ground_truth_path(self,frame_num,kp_num):
        rootdir = configuration.training_configuration.training_gt_dir
        return (rootdir + str(frame_num) + "_gt_patches/tdf_patch_" + str(kp_num) + ".npz")

    def __len__(self):
        return configuration.Training_Data_Config.training_data_size

    def __getitem__(self,index):
        #get patch from same classs
        if(index % 2 == 1):
            label = 1
            kp = random.randint(0,configuration.Training_Data_Config.number_keypoints - 1)
            frame1,cam1 = random.choice(self.data[kp])
            patch1 = np.load(self._get_patch_path_(frame1,cam1,kp))['patch']
            patch1_gt = np.load(self._get_ground_truth_path(frame1,kp))['patch']
            frame2,cam2 = random.choice(self.data[kp])
            patch2 = np.load(self._get_patch_path_(frame2,cam2,kp))['patch']
            patch2_gt = np.load(self._get_ground_truth_path(frame2,kp))['patch']
        #get patch from different class
        else:
            label = 0
            kp_1 = random.randint(0,configuration.Training_Data_Config.number_keypoints - 1)
            kp_2 = random.randint(0,configuration.Training_Data_Config.number_keypoints - 1)
            while kp_1 == kp_2:
                kp_2 = random.randint(0,configuration.Training_Data_Config.number_keypoints - 1)
            frame1,cam1 = random.choice(self.data[kp_1])
            patch1 = np.load(self._get_patch_path_(frame1,cam1,kp_1))['patch']
            patch1_gt = np.load(self._get_ground_truth_path(frame1,kp_1))['patch']
            frame2,cam2 = random.choice(self.data[kp_2])
            patch2 = np.load(self._get_patch_path_(frame2,cam2,kp_2))['patch']
            patch2_gt = np.load(self._get_ground_truth_path(frame2,kp_2))['patch']

        if self.transform:
            patch1 = torch.tensor([patch1])
            patch1_gt = torch.tensor([patch1_gt])
            patch2 = torch.tensor([patch2])
            patch2_gt = torch.tensor([patch2_gt])
        
        return(patch1,patch2,label,patch1_gt,patch2_gt)

class GoalKeeper(Dataset):
    def __init__(self,transform=None):
        super(GoalKeeper,self).__init__
        self.transform = transform
        self.val_data = np.load(configuration.Validation_Data_Config.validation_set_dir + "validation_data.npz",allow_pickle=True)['data']
    
    def __len__(self):
        return configuration.Validation_Data_Config.validation_data_size
    
    def _get_file_number(self,file):
        if file < 100:
            file_num = "00" + str(file)
        else:
            file_num = "0" + str(file)
        return file_num

    def _get_val_patch_path(self,frame_num,cam_num,kp_num):
        rootdir = configuration.Validation_Data_Config.validation_set_dir
        return(rootdir + self._get_file_number(frame_num) + str(cam_num) + "/tsdf_patch_" + str(kp_num) + ".npz")

    def _get_val_patch_gt_path(self,frame_num,kp_num):
        rootdir = configuration.Validation_Data_Config.validation_gt_dir
        return(rootdir + self._get_file_number(frame_num) + "_gt_patches/tdf_patch_" + str(kp_num) + ".npz")

    def __getitem__(self,index):
        patch_1,patch_2,label = self.val_data[index]
        patch1 = np.load(self._get_val_patch_path(patch_1[0],patch_1[1],patch_1[2]))['patch']
        patch1_gt = np.load(self._get_val_patch_gt_path(patch_1[0],patch_1[2]))['patch']
        patch2 = np.load(self._get_val_patch_path(patch_2[0],patch_2[1],patch_2[2]))['patch']
        patch2_gt = np.load(self._get_val_patch_gt_path(patch_2[0],patch_2[2]))['patch']

        if self.transform:
            patch1 = torch.tensor([patch1])
            patch2 = torch.tensor([patch2])
            patch1_gt = torch.tensor([patch1_gt])
            patch2_gt = torch.tensor([patch2_gt])

        return patch1,patch2,label,patch_1,patch_2,patch1_gt,patch2_gt

        
"""
#Testing
if __name__ == '__main__':
    data = BalletDancer()
"""
