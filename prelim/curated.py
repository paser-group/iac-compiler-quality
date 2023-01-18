'''
Sample Python script 
to find out valid YAML manifests 
'''
import shutil 
import pandas as pd 
import numpy as np 
import os 

def findLegitFiles(i_, o_):
    cnt         = 0 
    df_         = pd.read_csv( i_ ) 
    valid_files = np.unique( df_['TARGET'].tolist() )
    for fil_ in valid_files: 
        if(os.path.exists( fil_ )):
            print(fil_)
            fil_siz = os.path.getsize(fil_) 
            if fil_siz >= 1000: 
                cnt = cnt + 1 
                shutil.copy(fil_, o_ + str(cnt) + '.yml' ) 
                print(cnt) 
        
        




if __name__ == '__main__': 
    inp_fil = '/Users/akondrahman/Documents/RESEARCH/IAC/COMPILER-WORK/valid-yaml-data-ansible.csv'
    out_dir = '../invalid/'

    findLegitFiles(inp_fil, out_dir) 