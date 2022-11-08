# -*- coding: utf-8 -*-
"""
@author: Alexandre Sac--Morane
alexandre.sac-morane@uclouvain.be

The goal of this file is to define a new class.
The new class is about the grains
"""

#-------------------------------------------------------------------------------
#Libs
#-------------------------------------------------------------------------------

import numpy as np

#Own  functions and classes
import PF

#-------------------------------------------------------------------------------
#Class
#-------------------------------------------------------------------------------

class Grain:

    #---------------------------------------------------------------------------

    def __init__(self,id,radius,center,width_int,x_L,y_L):

        self.id = id
        self.etai_M = np.array(np.zeros((len(y_L),len(x_L))))
        for l in range(len(y_L)):
            for c in range(len(x_L)):
                y = y_L[-1-l]
                x = x_L[c]
                self.etai_M[l][c] = PF.Cosine_Profile(radius,np.linalg.norm(np.array(center)-np.array([x,y])),width_int)

    #---------------------------------------------------------------------------
