# User documentation

This documentation explains what is inside of the file User.py. Hence, all variables of the program is here. The variables are sorted in different dictionnaries.

## Units used

The lenght is in µm.

The time is in second.

The force is in µN.

The  mass is in kg.

## dict_algorithm

#### template
It is the template used to generate the name of the simulation. It should be a string.

#### np_proc
It is the number of processors used for the phase-field simulation. It should be an integer.

#### n_t_PFDEM
It is the number of iteration done during the PFDEM simulation. It should be an integer.

#### dt_PF
It is the base for the adaptive time step used during the phase-field simulation. It should be a float.

#### n_t_PF
It is approximatively the number of iteration done during the phase-field simulation. It should be an integer.

#### cut_etai
Description in coming...

#### SaveData
It is a boolean to save data.

#### template
It is the name of the folder where data is saved during the simulation. It should be a string.

## dict_material

#### w
It is the width interface used for the phase-field simulation. It should be several times the size of the mesh.

#### M
It is the mobility of the phase variables during the phase-field simulation. It should be an integer or a float.

#### kappa_eta
It is the gradient coefficient for the non conserved variables during the phase-field simulation. It should be an integer or a float.

#### kappa_c
It is the gradient coefficient for the conserved variable during the phase-field simulation. It should be an integer or a float.

#### Energy_barrier
It is the energy barrier used inside the free energy used during the phase-field simulation. It should be an integer or a float.

## dict_sample

#### x_L / y_L
It is the x / y coordinates of the domain mesh.

#### grain_discretisation
description in coming

## dict_sample

#### overlap_target
It is the target value for the overlap between the two grains before the phase-field simulation. It should be an integer or a float.
