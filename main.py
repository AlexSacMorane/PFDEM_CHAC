# -*- coding: utf-8 -*-
"""
Created on 10/01/2021

@author: alsac
"""

#-------------------------------------------------------------------------------
#Librairy
#-------------------------------------------------------------------------------

import os
import shutil
from pathlib import Path
import numpy as np
import math
import pickle

#Own functions and classes
import Grain
import Owntools
import PF
import User

#-------------------------------------------------------------------------------
#Plan simulation
#-------------------------------------------------------------------------------

if Path('Input').exists():
    shutil.rmtree('Input')
os.mkdir('Input')
if Path('Output').exists():
    shutil.rmtree('Output')
os.mkdir('Output')
if Path('Data').exists():
    shutil.rmtree('Data')
os.mkdir('Data')
if Path('Debug').exists():
    shutil.rmtree('Debug')
os.mkdir('Debug')

#-------------------------------------------------------------------------------
#Create a simulation
#-------------------------------------------------------------------------------

#general parameters
dict_algorithm, dict_material, dict_sample, dict_sollicitation = User.All_parameters()

#create the two grains
User.Add_2grains(dict_sample,dict_material,dict_sollicitation)

#plot
Owntools.Plot_config(dict_sample)

#-------------------------------------------------------------------------------
#main
#-------------------------------------------------------------------------------

dict_algorithm['i_PFDEM'] = 0
while not User.Criteria_StopSimulation(dict_algorithm):

    dict_algorithm['i_PFDEM'] = dict_algorithm['i_PFDEM'] + 1

    #move grain
    Grain.Compute_overlap_2_grains(dict_sample)
    Grain.Apply_overlap_target(dict_material,dict_sample,dict_sollicitation)

    #plot
    Owntools.Plot_config(dict_sample)

    #write data
    PF.Write_eta_txt(dict_algorithm, dict_sample)
    PF.Write_c_txt(dict_algorithm, dict_sample)
    PF.Write_ep_txt(dict_algorithm, dict_sample)

    #create i
    Owntools.Create_i(dict_algorithm,dict_sample,dict_material)
    #run
    os.system('mpiexec -n '+str(dict_algorithm['np_proc'])+' ~/projects/moose/modules/combined/combined-opt -i '+dict_algorithm['namefile']+'_'+str(dict_algorithm['i_PFDEM'])+'.i')

    #sorting files
    j_str = Owntools.Sort_Files(dict_algorithm)

    raise ValueError('Stop !')

    #geometric_study

    #plot
    Owntools.Plot_config(dict_sample)


#-------------------------------------------------------------------------------
#Main
#-------------------------------------------------------------------------------


L_c_M = []
L_L_etai_M_g = []
j = 0
j_str = index_to_str(j)
folderpath = Path('Output/'+namefile+'_other_'+j_str+'.pvtu')
while folderpath.exists():
    L_etai_M_g, c_M = PFtoDEM_Multi('Output/'+namefile+'_other_'+j_str,x_L,y_L,L_g,np_proc)
    L_L_etai_M_g.append(L_etai_M_g)
    L_c_M.append(c_M)
    j = j + 1
    j_str = index_to_str(j)
    folderpath = Path('Output/'+namefile+'_other_'+j_str+'.pvtu')

for i in range(len(L_g)):
    before_sum = 0
    after_sum = 0
    for l in range(len(y_L)):
        for c in range(len(x_L)):
            before_sum = before_sum + max(L_g[i].etai_M[l][c],0)
            after_sum = after_sum + max(L_etai_M_g[i][l][c],0)
    print('eta',i+1,':',before_sum,'/',after_sum)

outfile = open('save','wb')
dict = {}
dict['L_c_M'] = L_c_M
dict['L_L_etai_M_g'] = L_L_etai_M_g
dict['x_L'] = x_L
dict['y_L'] = y_L
pickle.dump(dict,outfile)
outfile.close()


before_sum = 0
after_sum = 0
for l in range(len(y_L)):
    for c in range(len(x_L)):
        before_sum = before_sum + max(L_g[0].etai_M[l][c],0) + max(L_g[1].etai_M[l][c],0)
        after_sum = after_sum + c_M[l][c]
print('c :',before_sum,'/',after_sum)

#-------------------------------------------------------------------------------
#Save
#-------------------------------------------------------------------------------

if SaveData:

    shutil.copytree('../Test_2G_Box_CH_AC_EL','../Data_2G_Box_CH_AC_EL/'+name_folder)
