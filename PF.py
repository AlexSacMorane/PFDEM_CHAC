# -*- coding: utf-8 -*-
"""
@author: Alexandre Sac--Morane
alexandre.sac-morane@uclouvain.be

??
"""

#-------------------------------------------------------------------------------
#Librairy
#-------------------------------------------------------------------------------

import math
import numpy as np

#-------------------------------------------------------------------------------

def Cosine_Profile(R,r,w):
  #r is the absolute value of the distance to the current point from the center
  if r<R-w/2:
    return 1
  elif r>R+w/2:
    return 0
  else :
    return 0.5*(1 + np.cos(math.pi*(r-R+w/2)/w))

#-------------------------------------------------------------------------------

def Write_eta_txt(dict_algorithm, dict_sample):

    grain1 = dict_sample['L_g'][0]
    grain2 = dict_sample['L_g'][1]

    file_to_write_1 = open('Data/etas_'+str(dict_algorithm['i_PFDEM'])+'.txt','w')
    file_to_write_1.write('AXIS X\n')
    line = ''
    for x in dict_sample['x_L']:
        line = line + str(x)+ ' '
    line = line + '\n'
    file_to_write_1.write(line)

    file_to_write_1.write('AXIS Y\n')
    line = ''
    for y in dict_sample['y_L']:
        line = line + str(y)+ ' '
    line = line + '\n'
    file_to_write_1.write(line)

    file_to_write_1.write('DATA\n')
    for l in range(len(dict_sample['y_L'])):
        for c in range(len(dict_sample['x_L'])):
            #grain 1
            if grain1.etai_M[-1-l][c] > dict_algorithm['cut_etai']:
                file_to_write_1.write(str(grain1.etai_M[-1-l][c])+'\n')
            else :
                if grain2.etai_M[-1-l][c] > dict_algorithm['cut_etai'] :
                    file_to_write_1.write(str(-grain2.etai_M[-1-l][c])+'\n')
                else :
                    file_to_write_1.write(str('0\n'))

    file_to_write_1.close()

#-------------------------------------------------------------------------------

def Write_c_txt(dict_algorithm, dict_sample):

    file_to_write = open('Data/c_'+str(dict_algorithm['i_PFDEM'])+'.txt','w')
    file_to_write.write('AXIS X\n')
    line = ''
    for x in dict_sample['x_L']:
        line = line + str(x)+ ' '
    line = line + '\n'
    file_to_write.write(line)

    file_to_write.write('AXIS Y\n')
    line = ''
    for y in dict_sample['y_L']:
        line = line + str(y)+ ' '
    line = line + '\n'
    file_to_write.write(line)

    file_to_write.write('DATA\n')
    for l in range(len(dict_sample['y_L'])):
        for c in range(len(dict_sample['x_L'])):
            sum_eta = 0
            for grain in dict_sample['L_g'] :
                sum_eta = sum_eta + max(grain.etai_M[-1-l][c],0)
            file_to_write.write(str(sum_eta)+'\n')

    file_to_write.close()

#-------------------------------------------------------------------------------

def Write_ep_txt(dict_algorithm, dict_sample):

    file_to_write = open('Data/ep_'+str(dict_algorithm['i_PFDEM'])+'.txt','w')
    file_to_write.write('AXIS X\n')
    line = ''
    for x in dict_sample['x_L']:
        line = line + str(x)+ ' '
    line = line + '\n'
    file_to_write.write(line)

    file_to_write.write('AXIS Y\n')
    line = ''
    for y in dict_sample['y_L']:
        line = line + str(y)+ ' '
    line = line + '\n'
    file_to_write.write(line)

    file_to_write.write('DATA\n')
    for l in range(len(dict_sample['y_L'])):
        for c in range(len(dict_sample['x_L'])):
            file_to_write.write(str(0.1*min(dict_sample['L_g'][0].etai_M[-1-l][c],dict_sample['L_g'][1].etai_M[-1-l][c]))+'\n')

    file_to_write.close()
