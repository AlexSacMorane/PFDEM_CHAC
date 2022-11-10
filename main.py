# -*- coding: utf-8 -*-
"""
@author: Alexandre Sac--Morane
alexandre.sac-morane@uclouvain.be

This is the main file.
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
if not Path('../'+dict_algorithm['foldername']).exists():
    os.mkdir('../'+dict_algorithm['foldername'])

#create the two grains
User.Add_2grains(dict_sample,dict_material)

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
    Owntools.Write_eta_txt(dict_algorithm, dict_sample)
    Owntools.Write_c_txt(dict_algorithm, dict_sample)
    Owntools.Write_ep_txt(dict_algorithm, dict_sample)

    #create i
    Owntools.Create_i(dict_algorithm,dict_sample,dict_material)
    #run
    os.system('mpiexec -n '+str(dict_algorithm['np_proc'])+' ~/projects/moose/modules/combined/combined-opt -i '+dict_algorithm['namefile']+'_'+str(dict_algorithm['i_PFDEM'])+'.i')

    #sorting files
    j_str = Owntools.Sort_Files(dict_algorithm)

    for grain in dict_sample['L_g']:
        grain.PFtoDEM_Multi('Output/'+dict_algorithm['namefile']+'_'+str(dict_algorithm['i_PFDEM'])+'_other_'+j_str,dict_algorithm,dict_sample)
        grain.geometric_study(dict_sample)

    #plot
    Owntools.Plot_config(dict_sample)

#-------------------------------------------------------------------------------
#Main
#-------------------------------------------------------------------------------

raise ValueError('Stop !')
