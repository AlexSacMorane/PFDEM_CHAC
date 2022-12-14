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
import math
import random

#Own  functions and classes
import Owntools

#-------------------------------------------------------------------------------
#Class
#-------------------------------------------------------------------------------

class Grain:

    #---------------------------------------------------------------------------

    def __init__(self,id,radius,center,dict_material,dict_sample):

        self.id = id
        self.center = center
        L_r = []
        L_theta_r = []
        L_border = []
        L_border_x = []
        L_border_y = []
        for i in range(dict_sample['grain_discretisation']):
            theta = 2*math.pi*i/dict_sample['grain_discretisation']
            L_r.append(radius)
            L_theta_r.append(theta)
            L_border.append(np.array([center[0]+radius*math.cos(theta),center[1]+radius*math.sin(theta)]))
            L_border_x.append(center[0]+radius*math.cos(theta))
            L_border_y.append(center[1]+radius*math.sin(theta))
        L_border.append(L_border[0])
        L_border_x.append(L_border_x[0])
        L_border_y.append(L_border_y[0])
        #save description
        self.l_r = L_r
        self.l_theta_r = L_theta_r
        self.l_border = L_border
        self.l_border_x = L_border_x
        self.l_border_y = L_border_y

        self.build_etai_M(dict_material,dict_sample)

    #---------------------------------------------------------------------------

    def build_etai_M(self,dict_material,dict_sample):

        #initilization
        self.etai_M = np.array(np.zeros((len(dict_sample['y_L']),len(dict_sample['x_L']))))

        #extract a spatial zone
        x_min = min(self.l_border_x)-dict_material['w']
        x_max = max(self.l_border_x)+dict_material['w']
        y_min = min(self.l_border_y)-dict_material['w']
        y_max = max(self.l_border_y)+dict_material['w']

        #look for this part inside the global mesh
        #create search list
        x_L_search_min = abs(np.array(dict_sample['x_L'])-x_min)
        x_L_search_max = abs(np.array(dict_sample['x_L'])-x_max)
        y_L_search_min = abs(np.array(dict_sample['y_L'])-y_min)
        y_L_search_max = abs(np.array(dict_sample['y_L'])-y_max)

        #get index
        i_x_min = list(x_L_search_min).index(min(x_L_search_min))
        i_x_max = list(x_L_search_max).index(min(x_L_search_max))
        i_y_min = list(y_L_search_min).index(min(y_L_search_min))
        i_y_max = list(y_L_search_max).index(min(y_L_search_max))


        for l in range(i_y_min,i_y_max+1):
            for c in range(i_x_min,i_x_max+1):
                y = dict_sample['y_L'][-1-l]
                x = dict_sample['x_L'][c]
                p = np.array([x,y])
                r = np.linalg.norm(self.center - p)
                #look for the radius on this direction
                if p[1]>self.center[1]:
                    theta = math.acos((p[0]-self.center[0])/np.linalg.norm(self.center-p))
                else :
                    theta= 2*math.pi - math.acos((p[0]-self.center[0])/np.linalg.norm(self.center-p))
                L_theta_R_i = list(abs(np.array(self.l_theta_r)-theta))
                R = self.l_r[L_theta_R_i.index(min(L_theta_R_i))]
                #build etai_M
                self.etai_M[l][c] = Owntools.Cosine_Profile(R,r,dict_material['w'])

    #---------------------------------------------------------------------------

    def geometric_study(self,dict_sample):
      #Searching limits
      #Not best method but first approach
      #We iterate on y constant, we look for a value under and over 0.5
      #If both conditions are verified, there is a limit at this y
      #Same with iteration on x constant

      #-------------------------------------------------------------------------
      #load data needed
      n = dict_sample['grain_discretisation']
      x_L = dict_sample['x_L']
      y_L = dict_sample['y_L']
      #-------------------------------------------------------------------------

      L_border_old = []
      for y_i in range(len(y_L)):
          L_extract_x = self.etai_M[y_i][:]
          if id == 1:
              L_extract_x = list(L_extract_x)
              L_extract_x.reverse()
          if max(L_extract_x)>0.5 and min(L_extract_x)<0.5:
              y_intersect = y_L[len(y_L)-1-y_i]
              for x_i in range(len(x_L)-1):
                  if (L_extract_x[x_i]-0.5)*(L_extract_x[x_i+1]-0.5)<0:
                      x_intersect = (0.5-L_extract_x[x_i])/(L_extract_x[x_i+1]-L_extract_x[x_i])*\
                                  (x_L[x_i+1]-x_L[x_i]) + x_L[x_i]
                      L_border_old.append(np.array([x_intersect,y_intersect]))

      for x_i in range(len(x_L)):
          L_extract_y = []
          for y_i in range(len(y_L)):
              L_extract_y.append(self.etai_M[y_i][x_i])
          if max(L_extract_y)>0.5 and min(L_extract_y)<0.5:
              x_intersect = x_L[x_i]
              for y_i in range(len(y_L)-1):
                  if (L_extract_y[y_i]-0.5)*(L_extract_y[y_i+1]-0.5)<0:
                      y_intersect = (0.5-L_extract_y[y_i])/(L_extract_y[y_i+1]-L_extract_y[y_i])*\
                                  (y_L[len(y_L)-1-y_i-1]-y_L[len(y_L)-1-y_i]) + y_L[len(y_L)-1-y_i]
                      L_border_old.append(np.array([x_intersect,y_intersect]))

      #Adaptating
      L_id_used = [0]
      L_border = [L_border_old[0]]
      HighValue = 100000000 #Large

      current_node = L_border_old[0]
      for j in range(1,len(L_border_old)):
          L_d = list(np.zeros(len(L_border_old)))
          for i in range(0,len(L_border_old)):
              node = L_border_old[i]
              if  i not in L_id_used:
                  d = np.linalg.norm(node - current_node)
                  L_d[i] = d
              else :
                  L_d[i] = HighValue #Value need to be larger than potential distance between node

          index_nearest_node = L_d.index(min(L_d))
          nearest_node = L_border_old[index_nearest_node]
          current_node = nearest_node
          L_border.append(nearest_node)
          L_id_used.append(index_nearest_node)

      #Correcting
      L_d_final = []
      for i in range(len(L_border)-1):
          L_d_final.append(np.linalg.norm(L_border[i+1] - L_border[i]))

      #look for really far points, we assume the first point is accurate
      d_final_mean = np.mean(L_d_final)
      while np.max(L_d_final) > 5 * d_final_mean : #5 here is an user choixe value
          i_error = L_d_final.index(np.max(L_d_final))+1
          simulation_report.write('Point '+str(L_border[i_error])+' is deleted because it is detected as an error\n')
          L_border.pop(i_error)
          L_id_used.pop(i_error)
          L_d_final = []
          for i in range(len(L_border)-1):
              L_d_final.append(np.linalg.norm(L_border[i+1] - L_border[i]))

      #-------------------------------------------------------------------------------
      #Reduce the number of nodes for a grain
      #-------------------------------------------------------------------------------

      Perimeter = 0
      for i_p in range(len(L_border)-1):
          Perimeter = Perimeter + np.linalg.norm(L_border[i_p+1]-L_border[i_p])
      Perimeter = Perimeter + np.linalg.norm(L_border[-1]-L_border[0])
      distance_min = Perimeter/n
      L_border_adapted = [L_border[0]]
      for p in L_border[1:]:
          distance = np.linalg.norm(p-L_border_adapted[-1])
          if distance >= distance_min:
              L_border_adapted.append(p)
      L_border = L_border_adapted
      L_border.append(L_border[0])
      self.l_border = L_border

      #-------------------------------------------------------------------------------
      #Searching Surface, Center of mass and Inertia.
      #Monte Carlo Method
      #A box is defined, we take a random point and we look if it is inside or outside the grain
      #Properties are the statistic times the box properties
      #-------------------------------------------------------------------------------

      min_max_defined = False
      for p in L_border[:-1] :
          if not min_max_defined:
              box_min_x = p[0]
              box_max_x = p[0]
              box_min_y = p[1]
              box_max_y = p[1]
              min_max_defined = True
          else:
              if p[0] < box_min_x:
                  box_min_x = p[0]
              elif p[0] > box_max_x:
                  box_max_x = p[0]
              if p[1] < box_min_y:
                  box_min_y = p[1]
              elif p[1] > box_max_y:
                  box_max_y = p[1]

      N_MonteCarlo = 3000 #The larger it is, the more accurate it is
      sigma = 1
      M_Mass = 0
      M_Center_Mass = np.array([0,0])

      for i in range(N_MonteCarlo):
          P = np.array([random.uniform(box_min_x,box_max_x),random.uniform(box_min_y,box_max_y)])
          if self.P_is_inside(P):
              M_Mass = M_Mass + sigma
              M_Center_Mass = M_Center_Mass + sigma*P

      Mass = (box_max_x-box_min_x)*(box_max_y-box_min_y)/N_MonteCarlo*M_Mass
      Center_Mass = (box_max_x-box_min_x)*(box_max_y-box_min_y)/N_MonteCarlo*M_Center_Mass/Mass

      #-------------------------------------------------------------------------------
      #Updating the grain geometry and properties
      #-------------------------------------------------------------------------------

      L_R = []
      L_theta_R = []
      L_border_x = []
      L_border_y = []
      for p in L_border[:-1]:
          L_R.append(np.linalg.norm(p-Center_Mass))
          L_border_x.append(p[0])
          L_border_y.append(p[1])
          if (p-Center_Mass)[1] > 0:
              theta = math.acos((p-Center_Mass)[0]/np.linalg.norm(p-Center_Mass))
          else :
              theta = 2*math.pi - math.acos((p-Center_Mass)[0]/np.linalg.norm(p-Center_Mass))
          L_theta_R.append(theta)
      L_border_x.append(L_border_x[0])
      L_border_y.append(L_border_y[0])
      #reorganize lists
      L_R.reverse()
      L_theta_R.reverse()
      i_min_theta = L_theta_R.index(min(L_theta_R))
      L_R = L_R[i_min_theta:]+L_R[:i_min_theta]
      L_theta_R = L_theta_R[i_min_theta:]+L_theta_R[:i_min_theta]

      self.r_min = np.min(L_R)
      self.r_max = np.max(L_R)
      self.r_mean = np.mean(L_R)
      self.l_r = L_R
      self.l_theta_r = L_theta_R
      self.surface = Mass/sigma
      self.center = Center_Mass
      self.l_border_x = L_border_x
      self.l_border_y = L_border_y

    #-------------------------------------------------------------------------------

    def P_is_inside(self,P):
      #Franklin 1994, see Alonso-Marroquin 2009
      #determine if a point P is inside of a grain
      #slide on y constant

      counter = 0
      for i_p_border in range(len(self.l_border)-1):
          #consider only points if the coordinates frame the y-coordinate of the point
          if (self.l_border[i_p_border][1]-P[1])*(self.l_border[i_p_border+1][1]-P[1]) < 0 :
            x_border = self.l_border[i_p_border][0] + (self.l_border[i_p_border+1][0]-self.l_border[i_p_border][0])*(P[1]-self.l_border[i_p_border][1])/(self.l_border[i_p_border+1][1]-self.l_border[i_p_border][1])
            if x_border > P[0] :
                counter = counter + 1
      if counter % 2 == 0:
        return False
      else :
        return True

    #---------------------------------------------------------------------------

    def PFtoDEM_Multi(self,FileToRead,dict_algorithm,dict_sample):

        #---------------------------------------------------------------------------
        #Global parameters
        #---------------------------------------------------------------------------

        self.etai_M = np.array(np.zeros((len(dict_sample['y_L']),len(dict_sample['x_L']))))

        id_L = None
        eta_selector_len = len('        <DataArray type="Float64" Name="etai')
        end_len = len('        </DataArray>')
        XYZ_selector_len = len('        <DataArray type="Float64" Name="Points"')
        data_jump_len = len('          ')

        for i_proc in range(dict_algorithm['np_proc']):

            L_Work = [[], #X
                      [], #Y
                      []] #etai

        #---------------------------------------------------------------------------
        #Reading file
        #---------------------------------------------------------------------------

            f = open(f'{FileToRead}_{i_proc}.vtu','r')
            data = f.read()
            f.close
            lines = data.splitlines()

            #iterations on line
            for line in lines:

                if line[0:eta_selector_len] == '        <DataArray type="Float64" Name="eta'+str(self.id):
                    id_L = 2

                elif line[0:XYZ_selector_len] == '        <DataArray type="Float64" Name="Points"':
                    id_L = 0

                elif (line[0:end_len] == '        </DataArray>' or  line[0:len('          <InformationKey')] == '          <InformationKey') and id_L != None:
                    id_L = None

                elif line[0:data_jump_len] == '          ' and id_L == 2: #Read etai
                    line = line[data_jump_len:]
                    c_start = 0
                    for c_i in range(0,len(line)):
                        if line[c_i]==' ':
                            c_end = c_i
                            L_Work[id_L].append(float(line[c_start:c_end]))
                            c_start = c_i+1
                    L_Work[id_L].append(float(line[c_start:]))

                elif line[0:data_jump_len] == '          ' and id_L == 0: #Read [X, Y, Z]
                    line = line[data_jump_len:]
                    XYZ_temp = []
                    c_start = 0
                    for c_i in range(0,len(line)):
                        if line[c_i]==' ':
                            c_end = c_i
                            XYZ_temp.append(float(line[c_start:c_end]))
                            if len(XYZ_temp)==3:
                                L_Work[0].append(XYZ_temp[0])
                                L_Work[1].append(XYZ_temp[1])
                                XYZ_temp = []
                            c_start = c_i+1
                    XYZ_temp.append(float(line[c_start:]))
                    L_Work[0].append(XYZ_temp[0])
                    L_Work[1].append(XYZ_temp[1])

            #Adaptating data and update of etai_M
            for i in range(len(L_Work[0])):
                #Interpolation method
                L_dy = []
                for y_i in dict_sample['y_L'] :
                    L_dy.append(abs(y_i - L_Work[1][i]))
                L_dx = []
                for x_i in dict_sample['x_L'] :
                    L_dx.append(abs(x_i - L_Work[0][i]))
                if L_Work[2][i] > 0 : #do not consider etai < 0 because it is etaj
                    self.etai_M[-1-list(L_dy).index(min(L_dy))][list(L_dx).index(min(L_dx))] = L_Work[2][i]

    #---------------------------------------------------------------------------

    def move_grain_rebuild(self,displacement,dict_material,dict_sample):

        self.center = self.center + displacement
        for i in range(len(self.l_border)):
            self.l_border[i] = self.l_border[i] + displacement
            self.l_border_x[i] = self.l_border_x[i] + displacement[0]
            self.l_border_y[i] = self.l_border_y[i] + displacement[1]
        self.build_etai_M(dict_material,dict_sample)

    #---------------------------------------------------------------------------

    def move_grain_interpolation(self,displacement,dict_material,dict_sample):

        self.center = self.center + displacement
        for i in range(len(self.l_border)):
            self.l_border[i] = self.l_border[i] + displacement
            self.l_border_x[i] = self.l_border_x[i] + displacement[0]
            self.l_border_y[i] = self.l_border_y[i] + displacement[1]

        #displacement over x
        dx = dict_sample['x_L'][1]-dict_sample['x_L'][0]
        n_dx_disp_x = int(abs(displacement[0])//dx)
        disp_x_remainder = abs(displacement[0])%dx
        etai_M_old = self.etai_M.copy()

        if np.sign(displacement[0]) > 0 : # +x direction
            #dx*n_dx_disp_x translation
            if n_dx_disp_x > 0:
                for l in range(len(dict_sample['y_L'])):
                    self.etai_M[l][:n_dx_disp_x] = 0 #no information to translate so put equal to 0
                    self.etai_M[l][n_dx_disp_x:] = etai_M_old[l][:-n_dx_disp_x]
            #disp_x_remainder translation
            etai_M_old = self.etai_M.copy()
            for l in range(len(dict_sample['y_L'])):
                for c in range(1,len(dict_sample['x_L'])):
                    self.etai_M[l][c] = (etai_M_old[l][c]*(dx-disp_x_remainder) + etai_M_old[l][c-1]*disp_x_remainder)/dx
                self.etai_M[l][0] = 0 #no information to translate so put equal to 0

        else : # -x direction
            #dx*n_dx_disp_x translation
            if n_dx_disp_x > 0:
                for l in range(len(dict_sample['y_L'])):
                    self.etai_M[l][-n_dx_disp_x:] = 0 #no information to translate so put equal to 0
                    self.etai_M[l][:-n_dx_disp_x] = etai_M_old[l][n_dx_disp_x:]
            #disp_x_remainder translation
            etai_M_old = self.etai_M.copy()
            for l in range(len(dict_sample['y_L'])):
                for c in range(len(dict_sample['x_L'])-1):
                    self.etai_M[l][c] = (etai_M_old[l][c]*(dx-disp_x_remainder) + etai_M_old[l][c+1]*disp_x_remainder)/dx
                self.etai_M[l][0] = 0 #no information to translate so put equal to 0

#-------------------------------------------------------------------------------
#Functions
#-------------------------------------------------------------------------------

def Compute_overlap_2_grains(dict_sample):

    #2 grains
    g1 = dict_sample['L_g'][0]
    g2 = dict_sample['L_g'][1]

    #compute overlap
    #assume the normal n12 is +x axis
    overlap = max(g1.l_border_x) - min(g2.l_border_x)

    #Add element in dict
    dict_sample['overlap'] = overlap

#-------------------------------------------------------------------------------

def Apply_overlap_target(dict_material,dict_sample,dict_sollicitation):

    #compute the difference between real overlap and target value
    delta_overlap = dict_sollicitation['overlap_target'] - dict_sample['overlap']

    #move grains to apply target overlap
    dict_sample['L_g'][0].move_grain_interpolation(np.array([ delta_overlap/2,0]),dict_material,dict_sample)
    dict_sample['L_g'][1].move_grain_interpolation(np.array([-delta_overlap/2,0]),dict_material,dict_sample)
