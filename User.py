# -*- coding: utf-8 -*-
"""
@author: Alexandre Sac--Morane
alexandre.sac-morane@uclouvain.be

This is the file where the user can change the different parameters for the simulation.
"""

#-------------------------------------------------------------------------------
#Librairy
#-------------------------------------------------------------------------------

import math
import numpy as np
from pathlib import Path

#Own functions and classes
import Grain

#-------------------------------------------------------------------------------
#User
#-------------------------------------------------------------------------------

def All_parameters():
    #this function is called in main.py to have all the parameters needed in the simulation

    #---------------------------------------------------------------------------
    #Sample parameters

    #spatial discretisation
    x_min = -27
    x_max = 27
    nx = 180
    x_L = np.linspace(x_min,x_max,nx)
    y_min = -17
    y_max = 17
    ny = 100
    y_L = np.linspace(y_min,y_max,ny)

    #approximatively the number of vertices for one grain during DEM simulation
    grain_discretisation = 20

    dict_sample = {
    'x_L' : x_L,
    'y_L' : y_L,
    'grain_discretisation' : grain_discretisation
    }

    #---------------------------------------------------------------------------
    #Algorithm parameters

    template = 'PF_CH_AC' #template of the name of the simulation
    np_proc = 4 #number of processor used

    n_t_PFDEM = 1 #number of cycle PF-DEM

    #Time step for phase field
    dt_PF = 0.01
    n_t_PF = 100

    cut_etai = 0.1 #????

    SaveData = True #Save data or not
    foldername = 'Data_2G_Box_CH_AC_EL' #name of the folder where data are saved
    if SaveData :
        i_run = 1
        folderpath = Path('../'+foldername+'/'+template+'_'+str(i_run))
        while folderpath.exists():
            i_run = i_run + 1
            folderpath = Path('../'+foldername+'/'+template+'_'+str(i_run))
        namefile = template+'_'+str(i_run)
    else :
        namefile = template

    dict_algorithm = {
    'np_proc' : np_proc,
    'SaveData' : SaveData,
    'namefile' : namefile,
    'dt_PF' : dt_PF,
    'n_t_PF' : n_t_PF,
    'foldername' : foldername,
    'n_t_PFDEM' : n_t_PFDEM,
    'cut_etai' : cut_etai
    }

    #---------------------------------------------------------------------------
    #External sollicitation parameters

    overlap_target = 1

    dict_sollicitation = {
    'overlap_target' : overlap_target
    }

    #---------------------------------------------------------------------------
    #Material parameters

    #phase field
    width_int = math.sqrt((x_L[4]-x_L[0])**2+(y_L[4]-y_L[0])**2)
    Mobility = 5 #M, L1, L2 in .i
    kappa_eta = 0.1
    kappa_c = 0.1
    Energy_barrier = 20*kappa_eta/(width_int)**2

    dict_material = {
    'w' : width_int,
    'M' : Mobility,
    'kappa_eta' : kappa_eta,
    'kappa_c' : kappa_c,
    'Energy_barrier' : Energy_barrier
    }

    #---------------------------------------------------------------------------

    return dict_algorithm, dict_material, dict_sample, dict_sollicitation

#-------------------------------------------------------------------------------

def Add_2grains(dict_sample,dict_material,dict_sollicitation):

    #grain 1
    radius = 10
    center = np.array([np.mean(dict_sample['x_L'])-radius,np.mean(dict_sample['y_L'])])
    grain_1 = Grain.Grain(1,radius,center,dict_material,dict_sample)

    #grain 2
    radius = 10
    center = np.array([np.mean(dict_sample['x_L'])+radius,np.mean(dict_sample['y_L'])])
    grain_2 = Grain.Grain(1,radius,center,dict_material,dict_sample)

    #add element in dict
    dict_sample['L_g'] = [grain_1, grain_2]

#-------------------------------------------------------------------------------

def Criteria_StopSimulation(dict_algorithm):
    #Criteria to stop simulation (PF and DEM)

    Criteria_Verified = False
    if dict_algorithm['i_PFDEM'] >= dict_algorithm['n_t_PFDEM']:
        Criteria_Verified = True
    return Criteria_Verified
