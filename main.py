# -*- coding: utf-8 -*-
"""
@author: Alexandre Sac--Morane
alexandre.sac-morane@uclouvain.be

This is the main file.
"""

#-------------------------------------------------------------------------------
#Librairy
#-------------------------------------------------------------------------------

from pathlib import Path
from datetime import datetime
import numpy as np
import os
import shutil
import math

#Own functions and classes
import Grain
import Owntools
import User
import Report

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

#create a simulation report
simulation_report = Report.Report('Debug/Report',datetime.now())
simulation_report.tic_tempo(datetime.now())

#general parameters
dict_algorithm, dict_material, dict_sample, dict_sollicitation = User.All_parameters()
if dict_algorithm['SaveData']:
    if not Path('../'+dict_algorithm['foldername']).exists():
        os.mkdir('../'+dict_algorithm['foldername'])
    #tempo save of the user file
    shutil.copy('User.py','../'+dict_algorithm['foldername']+'/User_'+dict_algorithm['namefile']+'_tempo.txt')

#create the two grains
User.Add_2grains(dict_sample,dict_material)

#plot
Owntools.Plot_config(dict_sample)

simulation_report.tac_tempo(datetime.now(),'Initialisation')

#-------------------------------------------------------------------------------
#main
#-------------------------------------------------------------------------------

dict_algorithm['i_PFDEM'] = 0
while not User.Criteria_StopSimulation(dict_algorithm):

    simulation_report.tic_tempo(datetime.now())
    dict_algorithm['i_PFDEM'] = dict_algorithm['i_PFDEM'] + 1
    simulation_report.write_and_print(f"\nITERATION {dict_algorithm['i_PFDEM']} / {dict_algorithm['n_t_PFDEM']}\n\n",f"\nITERATION {dict_algorithm['i_PFDEM']} / {dict_algorithm['n_t_PFDEM']}\n")

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

    simulation_report.tac_tempo(datetime.now(),f"Iteration {dict_algorithm['i_PFDEM']}: preparation of the pf simulation")
    simulation_report.tic_tempo(datetime.now())

    #run
    os.system('mpiexec -n '+str(dict_algorithm['np_proc'])+' ~/projects/moose/modules/combined/combined-opt -i '+dict_algorithm['namefile']+'_'+str(dict_algorithm['i_PFDEM'])+'.i')

    simulation_report.tac_tempo(datetime.now(),f"Iteration {dict_algorithm['i_PFDEM']}: pf simulation")
    simulation_report.tic_tempo(datetime.now())

    #sorting files
    j_str = Owntools.Sort_Files(dict_algorithm)

    for grain in dict_sample['L_g']:
        grain.PFtoDEM_Multi('Output/'+dict_algorithm['namefile']+'_'+str(dict_algorithm['i_PFDEM'])+'_other_'+j_str,dict_algorithm,dict_sample)
        grain.geometric_study(dict_sample)

    #plot
    Owntools.Plot_config(dict_sample)

    #tempo save
    if dict_algorithm['SaveData']:
        Owntools.save_dicts_tempo(dict_algorithm, dict_material, dict_sample, dict_sollicitation)
        shutil.copy('Debug/Report.txt','../'+dict_algorithm['foldername']+'/Report_'+dict_algorithm['namefile']+'_tempo.txt')

    simulation_report.tac_tempo(datetime.now(),f"Iteration {dict_algorithm['i_PFDEM']}: from pf to dem")

#-------------------------------------------------------------------------------
#postprocess
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#close simulation
#-------------------------------------------------------------------------------

simulation_report.end(datetime.now())

#final save
if dict_algorithm['SaveData']:
    Owntools.save_dicts_final(dict_algorithm, dict_material, dict_sample, dict_sollicitation)
    name_actual_folder = os.path.dirname(os.path.realpath(__file__))
    shutil.copytree(name_actual_folder, '../'+dict_algorithm['foldername']+'/'+dict_algorithm['namefile'])
    os.remove('../'+dict_algorithm['foldername']+'/User_'+dict_algorithm['namefile']+'_tempo.txt')
    os.remove('../'+dict_algorithm['foldername']+'/Report_'+dict_algorithm['namefile']+'_tempo.txt')
