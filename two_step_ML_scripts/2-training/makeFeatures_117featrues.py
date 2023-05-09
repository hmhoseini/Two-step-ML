import os
import sys
from pymatgen.core.composition import Composition
from pymatgen.core.periodic_table import Element

tolerance = 5
##############################################################################################################valence electrons
element_s_dic = {     'H' : 1,
                     'Li' : 1, 'Be' : 2,  'B' : 2,  'C' : 2,  'N' : 2,  'O' : 2,  'F' : 2,\
                     'Na' : 1, 'Mg' : 2, 'Al' : 2, 'Si' : 2,  'P' : 2,  'S' : 2, 'Cl' : 2,\
                      'K' : 1, 'Ca' : 2, 'Sc' : 2, 'Ti' : 2,  'V' : 2, 'Cr' : 1, 'Mn' : 2, 'Fe' : 2, 'Co' : 2, 'Ni' : 2, 'Cu' : 1, 'Zn' : 2, 'Ga' : 2, 'Ge' : 2, 'As' : 2, 'Se' : 2, 'Br' : 2, 'Kr' : 2,\
                     'Rb' : 1, 'Sr' : 2, 'Y' : 2,  'Zr' : 2, 'Nb' : 1, 'Mo' : 1, 'Tc' : 2, 'Ru' : 1, 'Rh' : 1, 'Pd' : 0, 'Ag' : 1, 'Cd' : 2, 'In' : 2, 'Sn' : 2, 'Sb' : 2, 'Te' : 2,  'I' : 2, 'Xe' : 2,\
                     'Cs' : 1, 'Ba' : 2,           'Hf' : 2, 'Ta' : 2,  'W' : 2, 'Re' : 2, 'Os' : 2, 'Ir' : 2, 'Pt' : 1, 'Au' : 1, 'Hg' : 2, 'Tl' : 2, 'Pb' : 2, 'Bi' : 2,\
                                         'La' : 2, 'Ce' : 2, 'Pr' : 2, 'Nd' : 2, 'Pm' : 2, 'Sm' : 2, 'Eu' : 2, 'Gd' : 2, 'Tb' : 2, 'Dy' : 2, 'Ho' : 2, 'Er' : 2, 'Tm' : 2, 'Yb' : 2, 'Lu' : 2,\
                                         'Ac' : 2, 'Th' : 2, 'Pa' : 2,  'U' : 2,  'Np' : 2, 'Pu' : 2, 'Am' : 2, 'Cm' : 2, 'Bk' : 2, 'Cf' : 2}


element_p_dic = {     'H' : 0,
                     'Li' : 0, 'Be' : 0,  'B' : 1,  'C' : 2,  'N' : 3,  'O' : 4,  'F' : 5,\
                     'Na' : 0, 'Mg' : 0, 'Al' : 1, 'Si' : 2,  'P' : 3,  'S' : 4, 'Cl' : 5,\
                      'K' : 0, 'Ca' : 0, 'Sc' : 0, 'Ti' : 0,  'V' : 0, 'Cr' : 0, 'Mn' : 0, 'Fe' : 0, 'Co' : 0, 'Ni' : 0, 'Cu' : 0, 'Zn' : 0, 'Ga' : 1, 'Ge' : 2, 'As' : 3, 'Se' : 4, 'Br' : 5, 'Kr' : 6,\
                     'Rb' : 0, 'Sr' : 0,  'Y' : 0, 'Zr' : 0, 'Nb' : 0, 'Mo' : 0, 'Tc' : 0, 'Ru' : 0, 'Rh' : 0, 'Pd' : 0, 'Ag' : 0, 'Cd' : 0, 'In' : 1, 'Sn' : 2, 'Sb' : 3, 'Te' : 4,  'I' : 5, 'Xe' : 6,\
                     'Cs' : 0, 'Ba' : 0,           'Hf' : 0, 'Ta' : 0,  'W' : 0, 'Re' : 0, 'Os' : 0, 'Ir' : 0, 'Pt' : 0, 'Au' : 0, 'Hg' : 0, 'Tl' : 1, 'Pb' : 2, 'Bi' : 3,\
                                         'La' : 0, 'Ce' : 0, 'Pr' : 0, 'Nd' : 0, 'Pm' : 0, 'Sm' : 0, 'Eu' : 0, 'Gd' : 0, 'Tb' : 0, 'Dy' : 0, 'Ho' : 0, 'Er' : 0, 'Tm' : 0, 'Yb' : 0, 'Lu' : 0,\
					 'Ac' : 0, 'Th' : 0, 'Pa' : 0,  'U' : 0, 'Np' : 0, 'Pu' : 0, 'Am' : 0, 'Cm' : 0, 'Bk' : 0, 'Cf' : 0}

element_d_dic = {     'H' : 0,
                     'Li' : 0, 'Be' : 0,  'B' : 0,  'C' : 0,  'N' : 0,  'O' : 0,  'F' : 0,\
                     'Na' : 0, 'Mg' : 0, 'Al' : 0, 'Si' : 0,  'P' : 0,  'S' : 0, 'Cl' : 0,\
                      'K' : 0, 'Ca' : 0, 'Sc' : 1, 'Ti' : 2,  'V' : 3, 'Cr' : 5, 'Mn' : 5, 'Fe' : 6, 'Co' : 7, 'Ni' : 8, 'Cu' :10, 'Zn' :10, 'Ga' :10, 'Ge' :10, 'As' :10, 'Se' :10, 'Br' :10, 'Kr' :10,\
                     'Rb' : 0, 'Sr' : 0,  'Y' : 1, 'Zr' : 2, 'Nb' : 4, 'Mo' : 5, 'Tc' : 5, 'Ru' : 7, 'Rh' : 8, 'Pd' :10, 'Ag' :10, 'Cd' :10, 'In' :10, 'Sn' :10, 'Sb' :10, 'Te' :10,  'I' :10, 'Xe' :10,\
                     'Cs' : 0, 'Ba' : 0,           'Hf' : 2, 'Ta' : 3,  'W' : 4, 'Re' : 5, 'Os' : 6, 'Ir' : 7, 'Pt' : 9, 'Au' :10, 'Hg' :10, 'Tl' :10, 'Pb' :10, 'Bi' :10,\
                                         'La' : 1, 'Ce' : 1, 'Pr' : 0, 'Nd' : 0, 'Pm' : 0, 'Sm' : 0, 'Eu' : 0, 'Gd' : 1, 'Tb' : 0, 'Dy' : 0, 'Ho' : 0, 'Er' : 0, 'Tm' : 0, 'Yb' : 0, 'Lu' : 1,\
                                         'Ac' : 1, 'Th' : 2, 'Pa' : 1,  'U' : 1, 'Np' : 1, 'Pu' : 0, 'Am' : 0, 'Cm' : 1, 'Bk' : 0, 'Cf' : 0}

element_f_dic = {     'H' : 0,
                     'Li' : 0, 'Be' : 0,  'B' : 0,  'C' : 0,  'N' : 0,  'O' : 0,  'F' : 0,\
                     'Na' : 0, 'Mg' : 0, 'Al' : 0, 'Si' : 0,  'P' : 0,  'S' : 0, 'Cl' : 0,\
                      'K' : 0, 'Ca' : 0, 'Sc' : 0, 'Ti' : 0,  'V' : 0, 'Cr' : 0, 'Mn' : 0, 'Fe' : 0, 'Co' : 0, 'Ni' : 0, 'Cu' : 0, 'Zn' : 0, 'Ga' : 0, 'Ge' : 0, 'As' : 0, 'Se' : 0, 'Br' : 0, 'Kr' : 0,\
                     'Rb' : 0, 'Sr' : 0,  'Y' : 0, 'Zr' : 0, 'Nb' : 0, 'Mo' : 0, 'Tc' : 0, 'Ru' : 0, 'Rh' : 0, 'Pd' : 0, 'Ag' : 0, 'Cd' : 0, 'In' : 0, 'Sn' : 0, 'Sb' : 0, 'Te' : 0,  'I' : 0, 'Xe' : 0,\
                     'Cs' : 0, 'Ba' : 0,           'Hf' :14, 'Ta' :14,  'W' :14, 'Re' :14, 'Os' :14, 'Ir' :14, 'Pt' :14, 'Au' :14, 'Hg' :14, 'Tl' :14, 'Pb' :14, 'Bi' :14,\
                                         'La' : 0, 'Ce' : 1, 'Pr' : 3, 'Nd' : 4, 'Pm' : 5, 'Sm' : 6, 'Eu' : 7, 'Gd' : 7, 'Tb' : 9, 'Dy' :10, 'Ho' :11, 'Er' :12, 'Tm' :13, 'Yb' :14, 'Lu' :14,\
                                         'Ac' : 0, 'Th' : 0, 'Pa' : 2,  'U' : 3, 'Np' : 4, 'Pu' : 6, 'Am' : 7, 'Cm' : 7, 'Bk' : 9, 'Cf' :10}


##############################################################################################################electron affinity  (eV)
element_electron_affinity_dic = {\
                      'H' : 0.754,
                     'Li' : 0.618, 'Be' : -0.500, 'B'  : 0.279,  'C' : 1.262,  'N' : -0.070,  'O' : 1.461,  'F' :  3.401,\
                     'Na' : 0.547, 'Mg' : -0.400, 'Al' : 0.432, 'Si' : 1.389,  'P' :  0.746,  'S' : 2.077, 'Cl' :  3.612,\
                      'K' : 0.501, 'Ca' :  0.024, 'Sc' : 0.188, 'Ti' : 0.075,  'V' :  0.527, 'Cr' : 0.675, 'Mn' : -0.500, 'Fe' :  0.153, 'Co' : 0.662, 'Ni' : 1.157, 'Cu' :  1.235, 'Zn' : -0.600, 'Ga' : 0.433, 'Ge' : 1.232, 'As' : 0.804, 'Se' :  2.020, 'Br' : 3.363, 'Kr' : -1.00,\
                     'Rb' : 0.485, 'Sr' : 0.052,   'Y' : 0.307, 'Zr' : 0.433, 'Nb' :  0.917, 'Mo' : 0.747, 'Tc' :  0.552, 'Ru' :  1.046, 'Rh' : 1.142, 'Pd' : 0.562, 'Ag' :  1.304, 'Cd' : -0.700, 'In' : 0.383, 'Sn' : 1.112, 'Sb' : 1.047, 'Te' :  1.970,  'I' : 3.059, 'Xe' : -0.800,\
                     'Cs' : 0.572, 'Ba' : 0.144,                'Hf' : 0.178, 'Ta' :  0.323,  'W' : 0.816, 'Re' :  0.060, 'Os' :  1.077, 'Ir' : 1.564, 'Pt' : 2.125, 'Au' :  2.308, 'Hg' : -0.500, 'Tl' : 0.377, 'Pb' : 0.356, 'Bi' : 0.942,\
                                                  'La' : 0.552, 'Ce' : 0.572, 'Pr' :  0.962, 'Nd' : 1.916, 'Pm' :  0.129, 'Sm' :  0.162, 'Eu' : 0.116, 'Gd' : 0.137, 'Tb' :  1.165, 'Dy' :  0.352, 'Ho' : 0.338, 'Er' : 0.312, 'Tm' : 1.029, 'Yb' : -0.020, 'Lu' : 0.346,\
                                                  'Ac' : 0.350, 'Th' : 1.170, 'Pa' :  0.550,  'U' : 0.530,  'Np' : 0.480, 'Pu' : -0.500, 'Am' : 0.100, 'Cm' : 0.280, 'Bk' : -1.720, 'Cf' : -1.010}

##############################################################################################################ionization energy (eV)
element_ionization_energy_dic = {\
                      'H' : [13.598],
                     'Li' : [24.58741], 'Be' : [9.3227, 18.21116], 'B'  : [8.29803, 25.15484, 37.93064],  'C' : [11.26030, 24.38332, 47.8878, 64.4939],  'N' : [14.53414, 29.6013, 47.44924, 77.4735, 97.8902],  'O' : [13.61806, 35.11730],  'F' :  [17.42282],\
                     'Na' : [5.13908], 'Mg' : [7.64624,	15.03528], 'Al' : [5.98577, 18.82856, 28.44765], 'Si' : [8.15169, 16.34585, 33.49302, 45.14181],  'P' :  [10.48669, 19.7694, 30.2027, 51.4439, 65.0251],  'S' : [10.36001, 23.3379, 34.79, 47.222, 72.5945, 88.0530], 'Cl' :  [12.96764],\
                      'K' : [4.34066], 'Ca' :  [6.11316, 11.87172], 'Sc' : [6.5615, 12.79967, 24.75666], 'Ti' : [6.8281, 13.5755, 27.4917, 43.2672],  'V' :  [6.7462, 14.66,29.311, 46.709, 65.2817], 'Cr' : [6.7665, 16.4857, 30.96, 49.16, 69.46, 90.6349], 'Mn' : [7.43402, 15.63999, 33.668, 51.2, 72.4, 95.6], 'Fe' : [7.9024, 16.1878, 30.652, 54.8, 75.0, 99.1, 124.98, 151.06], 'Co' : [7.8810, 17.083, 33.50, 51.3, 79.5, 102.0, 128.9, 157.8, 186.13], 'Ni' : [7.6398, 18.16884, 35.19, 54.9, 76.06, 108, 133, 162, 193, 224.6], 'Cu' :  [7.72638, 20.29240, 36.841, 57.38], 'Zn' : [9.3942, 17.96440, 39.723], 'Ga' : [5.99930, 20.5142, 30.71], 'Ge' : [7.8994, 15.93462], 'As' : [9.7886, 18.633], 'Se' :  [9.75238, 21.19], 'Br' : [11.81381, 21.8], 'Kr' : [13.99961],\
                     'Rb' : [4.17713], 'Sr' : [5.6949, 11.03013],   'Y' : [6.2171, 12.24, 20.52], 'Zr' : [6.63390, 13.13, 22.99], 'Nb' :  [6.75885, 14.32], 'Mo' : [7.09243, 16.16, 27.13], 'Tc' :  [7.28, 15.26], 'Ru' :  [7.36050, 16.76], 'Rh' : [7.45890, 18.08], 'Pd' : [8.3369, 19.43], 'Ag' :  [7.5762, 21.49], 'Cd' : [8.9938, 16.90832], 'In' : [5.78636, 18.8698], 'Sn' : [7.3439, 14.63225], 'Sb' : [8.6084, 16.53051], 'Te' :  [9.0096, 18.6],  'I' : [10.45126, 19.1313], 'Xe' : [12.1298, 21.20979],\
                     'Cs' : [3.89390], 'Ba' : [5.21170, 10.00390],                'Hf' : [6.82507, 14.9, 23.3], 'Ta' :  [7.5496],  'W' : [7.8640], 'Re' :  [7.8335 ], 'Os' :  [8.4382], 'Ir' : [8.9670], 'Pt' : [8.9587, 18.563], 'Au' :  [9.2255, 20.5], 'Hg' : [10.43750, 18.756], 'Tl' : [6.1082, 20.428, 29.83], 'Pb' : [7.41666, 15.0322, 31.9373, 42.32], 'Bi' : [7.2856, 16.69, 25.56],\
                                                  'La' : [5.5769, 11.060, 19.1773], 'Ce' : [5.5387, 10.85, 20.19], 'Pr' :  [5.473, 10.55, 21.624], 'Nd' : [5.5250, 10.73, 22.1], 'Pm' :  [5.582, 10.90, 22.3], 'Sm' :  [5.6436,	11.07, 23.4], 'Eu' : [5.6704, 11.241, 24.92], 'Gd' : [6.1501, 12.09, 20.63], 'Tb' :  [5.8638, 11.52, 21.91], 'Dy' :  [5.9389, 11.67, 22.8], 'Ho' : [6.0215, 11.80, 22.84], 'Er' : [ 	6.1077, 11.93, 22.74], 'Tm' : [6.18431, 12.05, 23.68], 'Yb' : [6.25416, 12.1761, 25.05], 'Lu' : [5.4259, 13.9, 20.9594],\
                                                  'Ac' : [5.17, 12.1], 'Th' : [6.3067, 11.5, 20.0], 'Pa' :  [5.89],  'U' : [6.194],  'Np' : [6.2657], 'Pu' : [6.02], 'Am' : [5.973], 'Cm' : [5.991], 'Bk' : [6.1979], 'Cf' : [6.2817]}



##############################################################################################################empty dictionary for element ratio is ternary compound
element_vdw_radii = { 'H' : 1.20,
                     'Li' : 2.12, 'Be' : 1.98,  'B' : 1.91,  'C' : 1.77,  'N' : 1.66,  'O' : 1.50,  'F' : 1.46,\
                     'Na' : 2.50, 'Mg' : 2.51, 'Al' : 2.25, 'Si' : 2.19,  'P' : 1.90,  'S' : 1.89, 'Cl' : 1.82,\
                      'K' : 2.73, 'Ca' : 2.62, 'Sc' : 2.58, 'Ti' : 2.46,  'V' : 2.42, 'Cr' : 2.45, 'Mn' : 2.45, 'Fe' : 2.44, 'Co' : 2.40, 'Ni' : 2.40, 'Cu' : 2.38, 'Zn' : 2.39, 'Ga' : 2.32, 'Ge' : 2.29, 'As' : 1.88, 'Se' : 1.82, 'Br' : 1.86, 'Kr' : 2.25,\
                     'Rb' : 3.21, 'Sr' : 2.84, 'Y' : 2.75,  'Zr' : 2.52, 'Nb' : 2.56, 'Mo' : 2.45, 'Tc' : 2.44, 'Ru' : 2.46, 'Rh' : 2.44, 'Pd' : 2.15, 'Ag' : 2.53, 'Cd' : 2.49, 'In' : 2.43, 'Sn' : 2.42, 'Sb' : 2.47, 'Te' : 1.99,  'I' : 2.04, 'Xe' : 2.06,\
                     'Cs' : 3.48, 'Ba' : 3.03,           'Hf' : 2.63, 'Ta' : 2.53,  'W' : 2.57, 'Re' : 2.49, 'Os' : 2.48, 'Ir' : 2.41, 'Pt' : 2.29, 'Au' : 2.32, 'Hg' : 2.45, 'Tl' : 2.47, 'Pb' : 2.60, 'Bi' : 2.54,\
                                         'La' : 2.93, 'Ce' : 2.88, 'Pr' : 2.92, 'Nd' : 2.95, 'Pm' : 2.90, 'Sm' : 2.90, 'Eu' : 2.87, 'Gd' : 2.83, 'Tb' : 2.79, 'Dy' : 2.870, 'Ho' : 2.81, 'Er' : 2.83, 'Tm' : 2.79, 'Yb' : 2.80, 'Lu' : 2.74,\
                                         'Ac' : 2.80, 'Th' : 2.93, 'Pa' : 2.88,  'U' : 2.71,  'Np' : 2.82, 'Pu' : 2.81, 'Am' : 2.83, 'Cm' : 3.05, 'Bk' : 3.4, 'Cf' : 3.05}

##############################################################################################################empty dictionary for element ratio is ternary compound
element_ratio_dic = { 'H' : 0,
                     'Li' : 0, 'Be' : 0,  'B' : 0,  'C' : 0,  'N' : 0,  'O' : 0,  'F' : 0,\
                     'Na' : 0, 'Mg' : 0, 'Al' : 0, 'Si' : 0,  'P' : 0,  'S' : 0, 'Cl' : 0,\
                      'K' : 0, 'Ca' : 0, 'Sc' : 0, 'Ti' : 0,  'V' : 0, 'Cr' : 0, 'Mn' : 0, 'Fe' : 0, 'Co' : 0, 'Ni' : 0, 'Cu' : 0, 'Zn' : 0, 'Ga' : 0, 'Ge' : 0, 'As' : 0, 'Se' : 0, 'Br' : 0, 'Kr' : 0,\
                     'Rb' : 0, 'Sr' : 0, 'Y' : 0,  'Zr' : 0, 'Nb' : 0, 'Mo' : 0, 'Tc' : 0, 'Ru' : 0, 'Rh' : 0, 'Pd' : 0, 'Ag' : 0, 'Cd' : 0, 'In' : 0, 'Sn' : 0, 'Sb' : 0, 'Te' : 0,  'I' : 0, 'Xe' : 0,\
                     'Cs' : 0, 'Ba' : 0,           'Hf' : 0, 'Ta' : 0,  'W' : 0, 'Re' : 0, 'Os' : 0, 'Ir' : 0, 'Pt' : 0, 'Au' : 0, 'Hg' : 0, 'Tl' : 0, 'Pb' : 0, 'Bi' : 0,\
                                         'La' : 0, 'Ce' : 0, 'Pr' : 0, 'Nd' : 0, 'Pm' : 0, 'Sm' : 0, 'Eu' : 0, 'Gd' : 0, 'Tb' : 0, 'Dy' : 0, 'Ho' : 0, 'Er' : 0, 'Tm' : 0, 'Yb' : 0, 'Lu' : 0,\
                                         'Ac' : 0, 'Th' : 0, 'Pa' : 0,  'U' : 0,  'Np' : 0, 'Pu' : 0, 'Am' : 0, 'Cm' : 0, 'Bk' : 0, 'Cf' : 0}


############################################header of arff file##################################################################
print('{}'.format("@relation 10percent"))

for i in range(1, 38):
  print ('{} {}{} {}'.format("@attribute","ternary_", i, "numeric"))
#for i in range(42, 46):
#  print ('{} {}{} {}'.format("@attribute","ternary_", i, "{1, 2, 3, 4}"))
for i in range(1, 41):
  print ('{} {}{} {}'.format("@attribute","first_comp_", i, "numeric"))
for i in range(1, 41):
  print ('{} {}{} {}'.format("@attribute","second_comp_", i, "numeric"))

print('{}'.format("@attribute EFoff_s {0,1}"))

print('{}'.format("@data"))
##############################################################################################################

element_ratio = []

with open('ternaries-from-binaries.dat', 'r') as fhandle:
    lines = fhandle.readlines()
for line in lines:
    line = line.strip()
    line = line.split(",")
    tc = Composition(line[0])
    ternary_comp = Composition(tc.formula)
    fc = Composition(line[2])
    first_comp   = Composition(fc.formula)
    sc = Composition(line[5])
    second_comp  = Composition(sc.formula)

    first_comp_weight  = line[1]
    first_comp_energy = line[3]

    second_comp_weight = line[4]
    second_comp_energy = line[6]

    E_DFT        = line[7]
    E_heuristic  = line[8]

    # calculate atomic ratios for the ternary compound [0]
    for key, val in element_ratio_dic.items():
        element_ratio_dic[key] = ternary_comp.get_atomic_fraction(key)
    element_ratio.append(element_ratio_dic)
    element_ratio_dic = dict.fromkeys(element_ratio_dic, 0)

    # calculate atomic ratios for the first binary compound [1]
    for key, val in element_ratio_dic.items():
        element_ratio_dic[key] = first_comp.get_atomic_fraction(key)
    element_ratio.append(element_ratio_dic)
    element_ratio_dic = dict.fromkeys(element_ratio_dic, 0)

    # calculate atomic ratios for the second binary compound [2]
    for key, val in element_ratio_dic.items():
        element_ratio_dic[key] = second_comp.get_atomic_fraction(key)
    element_ratio.append(element_ratio_dic)
    element_ratio_dic = dict.fromkeys(element_ratio_dic, 0)

##########################################################################################ternary
#########ternary elements##########
    a_in_ternary = ternary_comp.elements[0]
    b_in_ternary = ternary_comp.elements[1]
    c_in_ternary = ternary_comp.elements[2]

    a_in_ternary_sym = a_in_ternary.symbol
    b_in_ternary_sym = b_in_ternary.symbol 
    c_in_ternary_sym = c_in_ternary.symbol
    
#########ternary elements ratio##########
    a_in_ternary_ratio = element_ratio[0][a_in_ternary_sym]
    b_in_ternary_ratio = element_ratio[0][b_in_ternary_sym]
    c_in_ternary_ratio = element_ratio[0][c_in_ternary_sym]

#########electronegativity of ternary compound##########
    a_in_ternary_X = a_in_ternary.X
    b_in_ternary_X = b_in_ternary.X
    c_in_ternary_X = c_in_ternary.X
    average_X_ternary = a_in_ternary_ratio * a_in_ternary_X + b_in_ternary_ratio * b_in_ternary_X + c_in_ternary_ratio * c_in_ternary_X 
    
#########group of ternary compound##########
    a_in_ternary_group = a_in_ternary.group
    b_in_ternary_group = b_in_ternary.group
    c_in_ternary_group = c_in_ternary.group
    average_group_ternary = a_in_ternary_ratio * a_in_ternary_group + b_in_ternary_ratio * b_in_ternary_group + c_in_ternary_ratio * c_in_ternary_group 
 
#########row of ternary compound##########
    a_in_ternary_row = a_in_ternary.row
    b_in_ternary_row = b_in_ternary.row
    c_in_ternary_row = c_in_ternary.row
    average_row_ternary = a_in_ternary_ratio * a_in_ternary_row + b_in_ternary_ratio * b_in_ternary_row + c_in_ternary_ratio * c_in_ternary_row

#########mass of ternary compound##########
    a_in_ternary_mass = a_in_ternary.atomic_mass
    b_in_ternary_mass = b_in_ternary.atomic_mass
    c_in_ternary_mass = c_in_ternary.atomic_mass
    average_mass_ternary = a_in_ternary_ratio * a_in_ternary_mass + b_in_ternary_ratio * b_in_ternary_mass +  c_in_ternary_ratio * c_in_ternary_mass 

#########ionic radius of ternary compound##########
    a_in_ternary_average_ionic_radius = a_in_ternary.average_ionic_radius
    if (a_in_ternary == 'H'): 
        a_in_ternary_average_ionic_radius = 0.01
    b_in_ternary_average_ionic_radius = b_in_ternary.average_ionic_radius
    if (b_in_ternary == 'H'):
        b_in_ternary_average_ionic_radius = 0.01
    c_in_ternary_average_ionic_radius = c_in_ternary.average_ionic_radius
    if (c_in_ternary == 'H'):
        c_in_ternary_average_ionic_radius = 0.01
    average_ionic_radius_ternary = a_in_ternary_ratio * a_in_ternary_average_ionic_radius + b_in_ternary_ratio * b_in_ternary_average_ionic_radius + c_in_ternary_ratio * c_in_ternary_average_ionic_radius

#########vdw radius of ternary compound##########
    a_in_ternary_vdw_radius = element_vdw_radii[a_in_ternary_sym]
    b_in_ternary_vdw_radius = element_vdw_radii[b_in_ternary_sym]
    c_in_ternary_vdw_radius = element_vdw_radii[c_in_ternary_sym]
    average_vdw_radius_ternary = a_in_ternary_ratio * a_in_ternary_vdw_radius + b_in_ternary_ratio * b_in_ternary_vdw_radius + c_in_ternary_ratio * c_in_ternary_vdw_radius

#########electron affinity of ternary compound##########
    a_in_ternary_electron_affinity = element_electron_affinity_dic[a_in_ternary_sym]
    b_in_ternary_electron_affinity = element_electron_affinity_dic[b_in_ternary_sym]
    c_in_ternary_electron_affinity = element_electron_affinity_dic[c_in_ternary_sym]
    average_electron_affinity_ternary = a_in_ternary_ratio * a_in_ternary_electron_affinity + b_in_ternary_ratio * b_in_ternary_electron_affinity + c_in_ternary_ratio * c_in_ternary_electron_affinity

#########ioniztion energy of ternary compound##########
    a_in_ternary_1_ionization_energy = element_ionization_energy_dic[a_in_ternary_sym][0]
    b_in_ternary_1_ionization_energy = element_ionization_energy_dic[b_in_ternary_sym][0]
    c_in_ternary_1_ionization_energy = element_ionization_energy_dic[c_in_ternary_sym][0]
    average_1_ionization_energy_ternary = a_in_ternary_ratio * a_in_ternary_1_ionization_energy + b_in_ternary_ratio * b_in_ternary_1_ionization_energy + c_in_ternary_ratio * c_in_ternary_1_ionization_energy

#########block of ternary compound##########
    a_in_ternary_block =  a_in_ternary.block
    if a_in_ternary_block == 's':
       a_in_ternary_block = '1'
    if a_in_ternary_block == 'p':
       a_in_ternary_block = '2'
    if a_in_ternary_block == 'd':
       a_in_ternary_block = '3'
    if a_in_ternary_block == 'f':
       a_in_ternary_block = '4'

    b_in_ternary_block = b_in_ternary.block
    if b_in_ternary_block == 's':
       b_in_ternary_block = '1'
    if b_in_ternary_block == 'p':
       b_in_ternary_block = '2'
    if b_in_ternary_block == 'd':
       b_in_ternary_block = '3'
    if b_in_ternary_block == 'f':
       b_in_ternary_block = '4'

    c_in_ternary_block = c_in_ternary.block
    if c_in_ternary_block == 's':
       c_in_ternary_block = '1'
    if c_in_ternary_block == 'p':
       c_in_ternary_block = '2'
    if c_in_ternary_block == 'd':
       c_in_ternary_block = '3'
    if c_in_ternary_block == 'f':
       c_in_ternary_block = '4'

#########total valence elecrons for ternary compound#########
    s_in_v_e_ternary = a_in_ternary_ratio * element_s_dic[a_in_ternary_sym] + b_in_ternary_ratio * element_s_dic[b_in_ternary_sym] + c_in_ternary_ratio * element_s_dic[c_in_ternary_sym]
    p_in_v_e_ternary = a_in_ternary_ratio * element_p_dic[a_in_ternary_sym] + b_in_ternary_ratio * element_p_dic[b_in_ternary_sym] + c_in_ternary_ratio * element_p_dic[c_in_ternary_sym]
    d_in_v_e_ternary = a_in_ternary_ratio * element_d_dic[a_in_ternary_sym] + b_in_ternary_ratio * element_d_dic[b_in_ternary_sym] + c_in_ternary_ratio * element_d_dic[c_in_ternary_sym]
    f_in_v_e_ternary = a_in_ternary_ratio * element_f_dic[a_in_ternary_sym] + b_in_ternary_ratio * element_f_dic[b_in_ternary_sym] + c_in_ternary_ratio * element_f_dic[c_in_ternary_sym]

    total_v_e_ternary = s_in_v_e_ternary + p_in_v_e_ternary + d_in_v_e_ternary + f_in_v_e_ternary

#########orbital fraction of valence elecrons for ternary compound##########

    s_frac_ternary = s_in_v_e_ternary / total_v_e_ternary
    p_frac_ternary = p_in_v_e_ternary / total_v_e_ternary
    d_frac_ternary = d_in_v_e_ternary / total_v_e_ternary
    f_frac_ternary = f_in_v_e_ternary / total_v_e_ternary

############################################################################################first binary
#########first binary elements##########
    a_in_first_comp = first_comp.elements[0]
    b_in_first_comp = first_comp.elements[1]

    a_in_first_comp_sym = a_in_first_comp.symbol
    b_in_first_comp_sym = b_in_first_comp.symbol

#########first binary elements ratio##########
    a_in_first_comp_ratio = element_ratio[1][a_in_first_comp_sym]
    b_in_first_comp_ratio = element_ratio[1][b_in_first_comp_sym]

    if Element(a_in_first_comp).X >= Element(b_in_first_comp).X :  #a is the anion
        anion_over_cation_first_comp = a_in_first_comp_ratio/b_in_first_comp_ratio

    if Element(b_in_first_comp).X > Element(a_in_first_comp).X :   # b is the anion
        anion_over_cation_first_comp = b_in_first_comp_ratio/a_in_first_comp_ratio

#########electronegativity of first binary compound##########
    a_in_first_comp_X = a_in_first_comp.X
    b_in_first_comp_X = b_in_first_comp.X
    average_X_first_comp = a_in_first_comp_ratio * a_in_first_comp_X + b_in_first_comp_ratio * b_in_first_comp_X
    abs_diff_X_first_comp = abs((a_in_first_comp_X - b_in_first_comp_X)/(a_in_first_comp_X + b_in_first_comp_X))

    if Element(a_in_first_comp).X >= Element(b_in_first_comp).X :  #a is the anion
        diff_X_first_comp = (a_in_first_comp_X - b_in_first_comp_X)/(a_in_first_comp_X + b_in_first_comp_X) 
        ratio_X_first_comp = a_in_first_comp_X/b_in_first_comp_X

    if Element(b_in_first_comp).X > Element(a_in_first_comp).X :   # b is the anion
        diff_X_first_comp = (b_in_first_comp_X - a_in_first_comp_X)/(a_in_first_comp_X + b_in_first_comp_X)
        ratio_X_first_comp = b_in_first_comp_X/a_in_first_comp_X

#########group of first binary compound##########
    a_in_first_comp_group = a_in_first_comp.group
    b_in_first_comp_group = b_in_first_comp.group
    average_group_first_comp = a_in_first_comp_ratio * a_in_first_comp_group + b_in_first_comp_ratio * b_in_first_comp_group
    abs_diff_group_first_comp = abs((a_in_first_comp_group - b_in_first_comp_group)/(a_in_first_comp_group + b_in_first_comp_group))

    if Element(a_in_first_comp).X >= Element(b_in_first_comp).X :  #a is the anion
        diff_group_first_comp = (a_in_first_comp_group - b_in_first_comp_group)/(a_in_first_comp_group + b_in_first_comp_group)
        ratio_group_first_comp = a_in_first_comp_group/b_in_first_comp_group

    if Element(b_in_first_comp).X > Element(a_in_first_comp).X :   # b is the anion
        diff_group_first_comp = (b_in_first_comp_group - a_in_first_comp_group)/(a_in_first_comp_group + b_in_first_comp_group)
        ratio_group_first_comp = b_in_first_comp_group/a_in_first_comp_group

#########row of first binary compound##########
    a_in_first_comp_row = a_in_first_comp.row
    b_in_first_comp_row = b_in_first_comp.row
    average_row_first_comp = a_in_first_comp_ratio * a_in_first_comp_row + b_in_first_comp_ratio * b_in_first_comp_row
    abs_diff_row_first_comp = abs((a_in_first_comp_row - b_in_first_comp_row)/(a_in_first_comp_row + b_in_first_comp_row))

    if Element(a_in_first_comp).X >= Element(b_in_first_comp).X :  #a is the anion
        diff_row_first_comp = (a_in_first_comp_row - b_in_first_comp_row)/(a_in_first_comp_row + b_in_first_comp_row)
        ratio_row_first_comp = a_in_first_comp_row/b_in_first_comp_row

    if Element(b_in_first_comp).X > Element(a_in_first_comp).X :   # b is the anion
        diff_row_first_comp = (b_in_first_comp_row - a_in_first_comp_row)/(a_in_first_comp_row + b_in_first_comp_row)
        ratio_row_first_comp = b_in_first_comp_row/a_in_first_comp_row

#########mass of first binary compound##########
    a_in_first_comp_mass = a_in_first_comp.atomic_mass
    b_in_first_comp_mass = b_in_first_comp.atomic_mass
    average_mass_first_comp = a_in_first_comp_ratio * a_in_first_comp_mass + b_in_first_comp_ratio * b_in_first_comp_mass
    abs_diff_mass_first_comp = abs((a_in_first_comp_mass - b_in_first_comp_mass)/(a_in_first_comp_mass + b_in_first_comp_mass))

    if Element(a_in_first_comp).X >= Element(b_in_first_comp).X :  #a is the anion
        diff_mass_first_comp = (a_in_first_comp_mass - b_in_first_comp_mass)/(a_in_first_comp_mass + b_in_first_comp_mass)
        ratio_mass_first_comp = a_in_first_comp_mass/b_in_first_comp_mass

    if Element(b_in_first_comp).X > Element(a_in_first_comp).X :   # b is the anion
        diff_mass_first_comp = (b_in_first_comp_mass - a_in_first_comp_mass)/(a_in_first_comp_mass + b_in_first_comp_mass)
        ratio_mass_first_comp = b_in_first_comp_mass/a_in_first_comp_mass

#########ionic radius of first binary compound##########
    a_in_first_comp_average_ionic_radius = a_in_first_comp.average_ionic_radius
    if (a_in_first_comp_sym == 'H'): 
        a_in_first_comp_average_ionic_radius = 0.01
    b_in_first_comp_average_ionic_radius = b_in_first_comp.average_ionic_radius
    if (b_in_first_comp_sym == 'H'):
        b_in_first_comp_average_ionic_radius = 0.01

    average_ionic_radius_first_comp = a_in_first_comp_ratio * a_in_first_comp_average_ionic_radius + b_in_first_comp_ratio * b_in_first_comp_average_ionic_radius
    abs_diff_ionic_radius_first_comp = abs((a_in_first_comp_average_ionic_radius - b_in_first_comp_average_ionic_radius)/(a_in_first_comp_average_ionic_radius + b_in_first_comp_average_ionic_radius))

    if Element(a_in_first_comp).X >= Element(b_in_first_comp).X :  #a is the anion
        diff_ionic_radius_first_comp = (a_in_first_comp_average_ionic_radius - b_in_first_comp_average_ionic_radius)/(a_in_first_comp_average_ionic_radius + b_in_first_comp_average_ionic_radius)
        ratio_ionic_radius_first_comp = a_in_first_comp_average_ionic_radius / b_in_first_comp_average_ionic_radius

    if Element(b_in_first_comp).X > Element(a_in_first_comp).X :   # b is the anion
        diff_ionic_radius_first_comp = (b_in_first_comp_average_ionic_radius - a_in_first_comp_average_ionic_radius)/(a_in_first_comp_average_ionic_radius + b_in_first_comp_average_ionic_radius)
        ratio_ionic_radius_first_comp = b_in_first_comp_average_ionic_radius / a_in_first_comp_average_ionic_radius

#########vdw radius of first binary compound##########
    a_in_first_comp_vdw_radius = element_vdw_radii[a_in_first_comp_sym]
    b_in_first_comp_vdw_radius = element_vdw_radii[b_in_first_comp_sym]

    average_vdw_radius_first_comp = a_in_first_comp_ratio * a_in_first_comp_vdw_radius + b_in_first_comp_ratio * b_in_first_comp_vdw_radius
    abs_diff_vdw_radius_first_comp = abs((a_in_first_comp_vdw_radius - b_in_first_comp_vdw_radius)/(a_in_first_comp_vdw_radius + b_in_first_comp_vdw_radius))

    if Element(a_in_first_comp).X >= Element(b_in_first_comp).X :  #a is the anion
        diff_vdw_radius_first_comp = (a_in_first_comp_vdw_radius - b_in_first_comp_vdw_radius)/(a_in_first_comp_vdw_radius + b_in_first_comp_vdw_radius)
        ratio_vdw_radius_first_comp = a_in_first_comp_vdw_radius / b_in_first_comp_vdw_radius

    if Element(b_in_first_comp).X > Element(a_in_first_comp).X :   # b is the anion
        diff_vdw_radius_first_comp = (b_in_first_comp_vdw_radius - a_in_first_comp_vdw_radius)/(a_in_first_comp_vdw_radius + b_in_first_comp_vdw_radius)
        ratio_vdw_radius_first_comp = b_in_first_comp_vdw_radius / a_in_first_comp_vdw_radius

#########electron affinity of first binary compound##########
    a_in_first_comp_electron_affinity = element_electron_affinity_dic[a_in_first_comp_sym]
    b_in_first_comp_electron_affinity = element_electron_affinity_dic[b_in_first_comp_sym]

    average_electron_affinity_first_comp = a_in_first_comp_ratio * a_in_first_comp_electron_affinity + b_in_first_comp_ratio * b_in_first_comp_electron_affinity
#    abs_diff_electron_affinity_first_comp = abs((a_in_first_comp_electron_affinity - b_in_first_comp_electron_affinity)/(a_in_first_comp_electron_affinity + b_in_first_comp_electron_affinity))
    abs_diff_electron_affinity_first_comp = abs(a_in_first_comp_electron_affinity - b_in_first_comp_electron_affinity)

    if Element(a_in_first_comp).X >= Element(b_in_first_comp).X :  #a is the anion
        diff_electron_affinity_first_comp = (a_in_first_comp_electron_affinity - b_in_first_comp_electron_affinity)
        ratio_electron_affinity_first_comp = a_in_first_comp_electron_affinity / b_in_first_comp_electron_affinity
 
    if Element(b_in_first_comp).X > Element(a_in_first_comp).X :   # b is the anion
        diff_electron_affinity_first_comp = (b_in_first_comp_electron_affinity - a_in_first_comp_electron_affinity)
        ratio_electron_affinity_first_comp = b_in_first_comp_electron_affinity / a_in_first_comp_electron_affinity

#########ioniztion energy of first binary compound##########
    a_in_first_comp_1_ionization_energy = element_ionization_energy_dic[a_in_first_comp_sym][0]
    b_in_first_comp_1_ionization_energy = element_ionization_energy_dic[b_in_first_comp_sym][0]

    average_1_ionization_energy_first_comp = a_in_first_comp_ratio * a_in_first_comp_1_ionization_energy + b_in_first_comp_ratio * b_in_first_comp_1_ionization_energy
    abs_diff_1_ionization_energy_first_comp = abs((a_in_first_comp_1_ionization_energy - b_in_first_comp_1_ionization_energy)/(a_in_first_comp_1_ionization_energy + b_in_first_comp_1_ionization_energy))

    if Element(a_in_first_comp).X >= Element(b_in_first_comp).X :  #a is the anion
        diff_1_ionization_energy_first_comp = (a_in_first_comp_1_ionization_energy - b_in_first_comp_1_ionization_energy)/(a_in_first_comp_1_ionization_energy + b_in_first_comp_1_ionization_energy)
        ratio_1_ionization_energy_first_comp = a_in_first_comp_1_ionization_energy / b_in_first_comp_1_ionization_energy

    if Element(b_in_first_comp).X > Element(a_in_first_comp).X :   # b is the anion
        diff_1_ionization_energy_first_comp = (b_in_first_comp_1_ionization_energy - a_in_first_comp_1_ionization_energy)/(a_in_first_comp_1_ionization_energy + b_in_first_comp_1_ionization_energy)
        ratio_1_ionization_energy_first_comp = b_in_first_comp_1_ionization_energy / a_in_first_comp_1_ionization_energy

#########total valence elecrons for first binary compound##########
    s_in_v_e_first_comp = a_in_first_comp_ratio * element_s_dic[a_in_first_comp_sym] + b_in_first_comp_ratio * element_s_dic[b_in_first_comp_sym]
    p_in_v_e_first_comp = a_in_first_comp_ratio * element_p_dic[a_in_first_comp_sym] + b_in_first_comp_ratio * element_p_dic[b_in_first_comp_sym]
    d_in_v_e_first_comp = a_in_first_comp_ratio * element_d_dic[a_in_first_comp_sym] + b_in_first_comp_ratio * element_d_dic[b_in_first_comp_sym]
    f_in_v_e_first_comp = a_in_first_comp_ratio * element_f_dic[a_in_first_comp_sym] + b_in_first_comp_ratio * element_f_dic[b_in_first_comp_sym]

    total_v_e_first_comp = s_in_v_e_first_comp + p_in_v_e_first_comp + d_in_v_e_first_comp + f_in_v_e_first_comp

#########orbital fraction of valence elecrons for first binary compound##########

    s_frac_first_comp = s_in_v_e_first_comp / total_v_e_first_comp
    p_frac_first_comp = p_in_v_e_first_comp / total_v_e_first_comp
    d_frac_first_comp = d_in_v_e_first_comp / total_v_e_first_comp
    f_frac_first_comp = f_in_v_e_first_comp / total_v_e_first_comp


############################################################################################second binary
#########second binary elements##########
    a_in_second_comp = second_comp.elements[0]
    b_in_second_comp = second_comp.elements[1]

    a_in_second_comp_sym = a_in_second_comp.symbol
    b_in_second_comp_sym = b_in_second_comp.symbol

#########second binary elements ratio##########
    a_in_second_comp_ratio = element_ratio[2][a_in_second_comp_sym]
    b_in_second_comp_ratio = element_ratio[2][b_in_second_comp_sym]

    if Element(a_in_second_comp).X >= Element(b_in_second_comp).X :  #a is the anion
        anion_over_cation_second_comp = a_in_second_comp_ratio/b_in_second_comp_ratio

    if Element(b_in_second_comp).X > Element(a_in_second_comp).X :   # b is the anion
        anion_over_cation_second_comp = b_in_second_comp_ratio/a_in_second_comp_ratio

#########electronegativity of second binary compound##########
    a_in_second_comp_X = a_in_second_comp.X
    b_in_second_comp_X = b_in_second_comp.X

    average_X_second_comp = a_in_second_comp_ratio * a_in_second_comp_X + b_in_second_comp_ratio * b_in_second_comp_X
    abs_diff_X_second_comp = abs((a_in_second_comp_X - b_in_second_comp_X)/(a_in_second_comp_X + b_in_second_comp_X))

    if Element(a_in_second_comp).X >= Element(b_in_second_comp).X :  #a is the anion
        diff_X_second_comp = (a_in_second_comp_X - b_in_second_comp_X)/(a_in_second_comp_X + b_in_second_comp_X)
        ratio_X_second_comp = a_in_second_comp_X/b_in_second_comp_X

    if Element(b_in_second_comp).X > Element(a_in_second_comp).X :   # b is the anion
        diff_X_second_comp = (b_in_second_comp_X - a_in_second_comp_X)/(a_in_second_comp_X + b_in_second_comp_X)
        ratio_X_second_comp = b_in_second_comp_X/a_in_second_comp_X

#########group of second binary compound##########
    a_in_second_comp_group = a_in_second_comp.group
    b_in_second_comp_group = b_in_second_comp.group

    average_group_second_comp = a_in_second_comp_ratio * a_in_second_comp_group + b_in_second_comp_ratio * b_in_second_comp_group
    abs_diff_group_second_comp = abs((a_in_second_comp_group - b_in_second_comp_group)/(a_in_second_comp_group + b_in_second_comp_group))

    if Element(a_in_second_comp).X >= Element(b_in_second_comp).X :  #a is the anion
        diff_group_second_comp = (a_in_second_comp_group - b_in_second_comp_group)/(a_in_second_comp_group + b_in_second_comp_group)
        ratio_group_second_comp = a_in_second_comp_group /b_in_second_comp_group

    if Element(b_in_second_comp).X > Element(a_in_second_comp).X :   # b is the anion
        diff_group_second_comp = (b_in_second_comp_group - a_in_second_comp_group)/(a_in_second_comp_group + b_in_second_comp_group)
        ratio_group_second_comp = b_in_second_comp_group /a_in_second_comp_group

#########row of second binary compound##########
    a_in_second_comp_row = a_in_second_comp.row
    b_in_second_comp_row = b_in_second_comp.row

    average_row_second_comp = a_in_second_comp_ratio * a_in_second_comp_row + b_in_second_comp_ratio * b_in_second_comp_row
    abs_diff_row_second_comp = abs((a_in_second_comp_row - b_in_second_comp_row)/(a_in_second_comp_row + b_in_second_comp_row))

    if Element(a_in_second_comp).X >= Element(b_in_second_comp).X :  #a is the anion
        diff_row_second_comp = (a_in_second_comp_row - b_in_second_comp_row)/(a_in_second_comp_row + b_in_second_comp_row)
        ratio_row_second_comp = a_in_second_comp_row / b_in_second_comp_row

    if Element(b_in_second_comp).X > Element(a_in_second_comp).X :   # b is the anion
        diff_row_second_comp = (b_in_second_comp_row - a_in_second_comp_row)/(a_in_second_comp_row + b_in_second_comp_row)
        ratio_row_second_comp = b_in_second_comp_row / a_in_second_comp_row

#########mass of second binary compound##########
    a_in_second_comp_mass = a_in_second_comp.atomic_mass
    b_in_second_comp_mass = b_in_second_comp.atomic_mass

    average_mass_second_comp = a_in_second_comp_ratio * a_in_second_comp_mass + b_in_second_comp_ratio * b_in_second_comp_mass
    abs_diff_mass_second_comp = abs((a_in_second_comp_mass - b_in_second_comp_mass)/(a_in_second_comp_mass + b_in_second_comp_mass))

    if Element(a_in_second_comp).X >= Element(b_in_second_comp).X :  #a is the anion
        diff_mass_second_comp = (a_in_second_comp_mass - b_in_second_comp_mass)/(a_in_second_comp_mass + b_in_second_comp_mass)
        ratio_mass_second_comp = a_in_second_comp_mass / b_in_second_comp_mass

    if Element(b_in_second_comp).X > Element(a_in_second_comp).X :   # b is the anion
        diff_mass_second_comp = (b_in_second_comp_mass - a_in_second_comp_mass)/(a_in_second_comp_mass + b_in_second_comp_mass)
        ratio_mass_second_comp = b_in_second_comp_mass / a_in_second_comp_mass

#########ionic radius of second binary compound##########
    a_in_second_comp_average_ionic_radius = a_in_second_comp.average_ionic_radius
    if (a_in_second_comp_sym == 'H'):
        a_in_second_comp_average_ionic_radius = 0.01
    b_in_second_comp_average_ionic_radius = b_in_second_comp.average_ionic_radius
    if (b_in_second_comp_sym == 'H'):
        b_in_second_comp_average_ionic_radius = 0.01

    average_ionic_radius_second_comp = a_in_second_comp_ratio * a_in_second_comp_average_ionic_radius + b_in_second_comp_ratio * b_in_second_comp_average_ionic_radius
    abs_diff_ionic_radius_second_comp = abs((a_in_second_comp_average_ionic_radius - b_in_second_comp_average_ionic_radius)/(a_in_second_comp_average_ionic_radius + b_in_second_comp_average_ionic_radius))
   
    if Element(a_in_second_comp).X >= Element(b_in_second_comp).X :  #a is the anion
        diff_ionic_radius_second_comp = (a_in_second_comp_average_ionic_radius - b_in_second_comp_average_ionic_radius)/(a_in_second_comp_average_ionic_radius + b_in_second_comp_average_ionic_radius)
        ratio_ionic_radius_second_comp = a_in_second_comp_average_ionic_radius / b_in_second_comp_average_ionic_radius

    if Element(b_in_second_comp).X > Element(a_in_second_comp).X :   # b is the anion
        diff_ionic_radius_second_comp = (b_in_second_comp_average_ionic_radius - a_in_second_comp_average_ionic_radius)/(a_in_second_comp_average_ionic_radius + b_in_second_comp_average_ionic_radius)
        ratio_ionic_radius_second_comp = b_in_second_comp_average_ionic_radius / a_in_second_comp_average_ionic_radius

#########vdw radius of second binary compound##########
    a_in_second_comp_vdw_radius = element_vdw_radii[a_in_second_comp_sym]
    b_in_second_comp_vdw_radius = element_vdw_radii[b_in_second_comp_sym]

    average_vdw_radius_second_comp = a_in_second_comp_ratio * a_in_second_comp_vdw_radius + b_in_second_comp_ratio * b_in_second_comp_vdw_radius
    abs_diff_vdw_radius_second_comp = abs((a_in_second_comp_vdw_radius - b_in_second_comp_vdw_radius)/(a_in_second_comp_vdw_radius + b_in_second_comp_vdw_radius))

    if Element(a_in_second_comp).X >= Element(b_in_second_comp).X :  #a is the anion
        diff_vdw_radius_second_comp = (a_in_second_comp_vdw_radius - b_in_second_comp_vdw_radius)/(a_in_second_comp_vdw_radius + b_in_second_comp_vdw_radius)
        ratio_vdw_radius_second_comp = a_in_second_comp_vdw_radius / b_in_second_comp_vdw_radius

    if Element(b_in_second_comp).X > Element(a_in_second_comp).X :   # b is the anion
        diff_vdw_radius_second_comp = (b_in_second_comp_vdw_radius - a_in_second_comp_vdw_radius)/(a_in_second_comp_vdw_radius + b_in_second_comp_vdw_radius)
        ratio_vdw_radius_second_comp = b_in_second_comp_vdw_radius / a_in_second_comp_vdw_radius

#########electron affinity of second binary compound##########
    a_in_second_comp_electron_affinity = element_electron_affinity_dic[a_in_second_comp_sym]
    b_in_second_comp_electron_affinity = element_electron_affinity_dic[b_in_second_comp_sym]

    average_electron_affinity_second_comp = a_in_second_comp_ratio * a_in_second_comp_electron_affinity + b_in_second_comp_ratio * b_in_second_comp_electron_affinity
#    abs_diff_electron_affinity_second_comp = abs((a_in_second_comp_electron_affinity - b_in_second_comp_electron_affinity)/(a_in_second_comp_electron_affinity + b_in_second_comp_electron_affinity))
    abs_diff_electron_affinity_second_comp = (a_in_second_comp_electron_affinity - b_in_second_comp_electron_affinity)

    if Element(a_in_second_comp).X >= Element(b_in_second_comp).X :  #a is the anion
        diff_electron_affinity_second_comp = (a_in_second_comp_electron_affinity - b_in_second_comp_electron_affinity)
        ratio_electron_affinity_second_comp = a_in_second_comp_electron_affinity / b_in_second_comp_electron_affinity

    if Element(b_in_second_comp).X > Element(a_in_second_comp).X :   # b is the anion
        diff_electron_affinity_second_comp = (b_in_second_comp_electron_affinity - a_in_second_comp_electron_affinity)
        ratio_electron_affinity_second_comp = b_in_second_comp_electron_affinity / a_in_second_comp_electron_affinity

#########ioniztion energy of second binary compound##########
    a_in_second_comp_1_ionization_energy = element_ionization_energy_dic[a_in_second_comp_sym][0]
    b_in_second_comp_1_ionization_energy = element_ionization_energy_dic[b_in_second_comp_sym][0]

    average_1_ionization_energy_second_comp = a_in_second_comp_ratio * a_in_second_comp_1_ionization_energy + b_in_second_comp_ratio * b_in_second_comp_1_ionization_energy
    abs_diff_1_ionization_energy_second_comp = abs((a_in_second_comp_1_ionization_energy - b_in_second_comp_1_ionization_energy)/(a_in_second_comp_1_ionization_energy + b_in_second_comp_1_ionization_energy))

    if Element(a_in_second_comp).X >= Element(b_in_second_comp).X :  #a is the anion
        diff_1_ionization_energy_second_comp = (a_in_second_comp_1_ionization_energy - b_in_second_comp_1_ionization_energy)/(a_in_second_comp_1_ionization_energy + b_in_second_comp_1_ionization_energy)
        ratio_1_ionization_energy_second_comp = a_in_second_comp_1_ionization_energy / b_in_second_comp_1_ionization_energy

    if Element(b_in_second_comp).X > Element(a_in_second_comp).X :   # b is the anion
        diff_1_ionization_energy_second_comp = (b_in_second_comp_1_ionization_energy - a_in_second_comp_1_ionization_energy)/(a_in_second_comp_1_ionization_energy + b_in_second_comp_1_ionization_energy)
        ratio_1_ionization_energy_second_comp = b_in_second_comp_1_ionization_energy / a_in_second_comp_1_ionization_energy


#########total valence elecrons for second binary compound##########
    s_in_v_e_second_comp = a_in_second_comp_ratio * element_s_dic[a_in_second_comp_sym] + b_in_second_comp_ratio * element_s_dic[b_in_second_comp_sym]
    p_in_v_e_second_comp = a_in_second_comp_ratio * element_p_dic[a_in_second_comp_sym] + b_in_second_comp_ratio * element_p_dic[b_in_second_comp_sym]
    d_in_v_e_second_comp = a_in_second_comp_ratio * element_d_dic[a_in_second_comp_sym] + b_in_second_comp_ratio * element_d_dic[b_in_second_comp_sym]
    f_in_v_e_second_comp = a_in_second_comp_ratio * element_f_dic[a_in_second_comp_sym] + b_in_second_comp_ratio * element_f_dic[b_in_second_comp_sym]

    total_v_e_second_comp = s_in_v_e_second_comp + p_in_v_e_second_comp + d_in_v_e_second_comp + f_in_v_e_second_comp

#########orbital fraction of valence elecrons for ternary compound##########
    s_frac_second_comp = s_in_v_e_second_comp / total_v_e_second_comp
    p_frac_second_comp = p_in_v_e_second_comp / total_v_e_second_comp
    d_frac_second_comp = d_in_v_e_second_comp / total_v_e_second_comp
    f_frac_second_comp = f_in_v_e_second_comp / total_v_e_second_comp

#######################################################print##############################################
    print('{}, {}, {},'.format(ternary_comp.reduced_formula, first_comp.reduced_formula, second_comp.reduced_formula)),

#######################################################print ternary values##############################################
#    for key, values in element_ratio[0].items():
#      print('{:.2f},'.format(values)),
#    print('X'),
    print('{:.3f},'.format(float(E_heuristic)), end='')
#   print averages 
    print('{:.3f}, {:.3f}, {:.3f}, {:.3f}, {:.3f}, {:.3f}, {:.3f}, {:.3f},'.format(average_X_ternary, average_group_ternary, average_row_ternary, average_mass_ternary, average_ionic_radius_ternary, average_electron_affinity_ternary, average_1_ionization_energy_ternary, average_vdw_radius_ternary), end =' ')
#    print('X'), 
    print('{:.3f}, {:.3f}, {:.3f},'.format(a_in_ternary_X/average_X_ternary, b_in_ternary_X/average_X_ternary, c_in_ternary_X/average_X_ternary), end = '')
#    print('group'),
    print('{:.3f}, {:.3f}, {:.3f},'.format(a_in_ternary_group/average_group_ternary, b_in_ternary_group/average_group_ternary, c_in_ternary_group/average_group_ternary), end = '')
#    print('row'),
    print('{:.3f}, {:.3f}, {:.3f},'.format(a_in_ternary_row/average_row_ternary, b_in_ternary_row/average_row_ternary, c_in_ternary_row/average_row_ternary), end = '')
#    print('mass')   ,
    print('{:.3f}, {:.3f}, {:.3f},'.format(float(a_in_ternary_mass)/average_mass_ternary, float(b_in_ternary_mass)/average_mass_ternary, float(c_in_ternary_mass)/average_mass_ternary), end = '')
#    print('ionic radius'),
    print('{:.3f}, {:.3f}, {:.3f},'.format(float(a_in_ternary_average_ionic_radius)/average_ionic_radius_ternary, float(b_in_ternary_average_ionic_radius)/average_ionic_radius_ternary, float(c_in_ternary_average_ionic_radius)/average_ionic_radius_ternary), end = '')
#    print('electron affinity'),
#    print('{:.3f}, {:.3f}, {:.3f},'.format(float(a_in_ternary_electron_affinity)/average_electron_affinity_ternary, float(b_in_ternary_electron_affinity)/average_electron_affinity_ternary, float(c_in_ternary_electron_affinity)/average_electron_affinity_ternary)),

    print('{:.3f}, {:.3f}, {:.3f},'.format(float(a_in_ternary_electron_affinity), float(b_in_ternary_electron_affinity), float(c_in_ternary_electron_affinity)), end = '')
#    print('ionization energy'),
    print('{:.3f}, {:.3f}, {:.3f},'.format(float(a_in_ternary_1_ionization_energy)/average_1_ionization_energy_ternary, float(b_in_ternary_1_ionization_energy)/average_1_ionization_energy_ternary, float(c_in_ternary_1_ionization_energy)/average_1_ionization_energy_ternary), end = '')
#    print ("vdw radius')
    print('{:.3f}, {:.3f}, {:.3f},'.format(a_in_ternary_vdw_radius/average_vdw_radius_ternary, b_in_ternary_vdw_radius/average_vdw_radius_ternary, c_in_ternary_vdw_radius/average_vdw_radius_ternary), end = '')
#    print('orbital fraction'),
    print('{:.3f}, {:.3f}, {:.3f}, {:.3f},'.format(s_frac_ternary, p_frac_ternary, d_frac_ternary, f_frac_ternary), end = '')
#    print('{:.3f}, {:.3f}, {:.3f}, {:.3f},'.format(s_in_v_e_ternary, p_in_v_e_ternary, d_in_v_e_ternary, f_in_v_e_ternary)),

#    print('block'),
#    print('{}, {}, {},'.format(a_in_ternary_block, b_in_ternary_block, c_in_ternary_block)),

#######################################################print first compound values##############################################
    print('{:.2f},'.format(float(first_comp_weight)), end = '')
    print('{:.3f},'.format(float(first_comp_energy)), end = '')
#ratio of anion/cation for the first binary
    print('{:.3f},'.format(anion_over_cation_first_comp), end = '')
#ratio of A/a and B/b for the first binary 
    print('{:.3f},'.format(element_ratio[0][a_in_first_comp_sym]/element_ratio[1][a_in_first_comp_sym]), end = '')
    print('{:.3f},'.format(element_ratio[0][b_in_first_comp_sym]/element_ratio[1][b_in_first_comp_sym]), end = '')


#    for key, values in element_ratio[1].items():
#      print('{:.2f},'.format(values)),
    print('{:.3f}, {:.3f}, {:.3f}, {:.3f}, {:.3f}, {:.3f}, {:.3f}, {:.3f},'.format(average_X_first_comp, average_group_first_comp, average_row_first_comp, average_mass_first_comp, average_ionic_radius_first_comp, average_electron_affinity_first_comp, average_1_ionization_energy_first_comp, average_vdw_radius_first_comp), end = '')

#abs_diff_X_first_comp = diff_X_first_comp
    print('{:.3f}, {:.3f}, {:.3f}, {:.3f}, {:.3f}, {:.3f}, {:.3f},'.format(abs_diff_group_first_comp, abs_diff_row_first_comp, abs_diff_mass_first_comp, abs_diff_ionic_radius_first_comp, abs_diff_electron_affinity_first_comp, abs_diff_1_ionization_energy_first_comp, abs_diff_vdw_radius_first_comp), end = '')
    print('{:.3f}, {:.3f}, {:.3f}, {:.3f}, {:.3f}, {:.3f}, {:.3f}, {:.3f},'.format(diff_X_first_comp, diff_group_first_comp, diff_row_first_comp, diff_mass_first_comp, diff_ionic_radius_first_comp, diff_electron_affinity_first_comp, diff_1_ionization_energy_first_comp, diff_vdw_radius_first_comp), end = '')
    print('{:.3f}, {:.3f}, {:.3f}, {:.3f}, {:.3f}, {:.3f}, {:.3f}, {:.3f},'.format(ratio_X_first_comp, ratio_group_first_comp, ratio_row_first_comp, ratio_mass_first_comp, ratio_ionic_radius_first_comp, ratio_electron_affinity_first_comp, ratio_1_ionization_energy_first_comp, ratio_vdw_radius_first_comp), end = '')

    print('{:.3f}, {:.3f}, {:.3f}, {:.3f},'.format(s_frac_first_comp, p_frac_first_comp, d_frac_first_comp, f_frac_first_comp), end = '')
#    print('{:.3f}, {:.3f}, {:.3f}, {:.3f},'.format(s_in_v_e_first_comp, p_in_v_e_first_comp, d_in_v_e_first_comp, f_in_v_e_first_comp)),


#only for charge neutral compounds
#    print('{:.3f},'.format(ternary_comp.oxi_state_guesses()[0][a_in_first_comp]/first_comp.oxi_state_guesses()[0][a_in_first_comp])),
#    print('{:.3f},'.format(ternary_comp.oxi_state_guesses()[0][b_in_first_comp]/first_comp.oxi_state_guesses()[0][b_in_first_comp])),

#######################################################print second compound values##############################################
    print('{:.2f},'.format(float(second_comp_weight)), end = '')
    print('{:.3f},'.format(float(second_comp_energy)), end = '')
#ratio of anion/cation for the second binary
    print('{:.3f},'.format(anion_over_cation_second_comp), end = '')
#ratio of A/a and B/b for the second binary 
    print('{:.3f},'.format(element_ratio[0][a_in_second_comp_sym]/element_ratio[2][a_in_second_comp_sym]), end = '')
    print('{:.3f},'.format(element_ratio[0][b_in_second_comp_sym]/element_ratio[2][b_in_second_comp_sym]), end = '')

#    for key, values in element_ratio[2].items():
#      print('{:.2f},'.format(values)),
    print('{:.3f}, {:.3f}, {:.3f}, {:.3f}, {:.3f}, {:.3f}, {:.3f}, {:.3f},'.format(average_X_second_comp, average_group_second_comp, average_row_second_comp, average_mass_second_comp, average_ionic_radius_second_comp, average_electron_affinity_second_comp, average_1_ionization_energy_second_comp, average_vdw_radius_second_comp), end = '')

#abs_diff_X_second_comp = diff_X_second_comp
    print('{:.3f}, {:.3f}, {:.3f}, {:.3f}, {:.3f}, {:.3f}, {:.3f},'.format(abs_diff_group_second_comp, abs_diff_row_second_comp, abs_diff_mass_second_comp, abs_diff_ionic_radius_second_comp, abs_diff_electron_affinity_second_comp, abs_diff_1_ionization_energy_second_comp, abs_diff_vdw_radius_second_comp), end = '')
    print('{:.3f}, {:.3f}, {:.3f}, {:.3f}, {:.3f}, {:.3f}, {:.3f}, {:.3f},'.format(diff_X_second_comp, diff_group_second_comp, diff_row_second_comp, diff_mass_second_comp, diff_ionic_radius_second_comp, diff_electron_affinity_second_comp, diff_1_ionization_energy_second_comp, diff_vdw_radius_second_comp), end = '')
    print('{:.3f}, {:.3f}, {:.3f}, {:.3f}, {:.3f}, {:.3f}, {:.3f}, {:.3f},'.format(ratio_X_second_comp, ratio_group_second_comp, ratio_row_second_comp, ratio_mass_second_comp, ratio_ionic_radius_second_comp, ratio_electron_affinity_second_comp, ratio_1_ionization_energy_second_comp, ratio_vdw_radius_second_comp), end = '')

    print('{:.3f}, {:.3f}, {:.3f}, {:.3f},'.format(s_frac_second_comp, p_frac_second_comp, d_frac_second_comp, f_frac_second_comp), end = '')
#    print('{:.3f}, {:.3f}, {:.3f}, {:.3f},'.format(s_in_v_e_second_comp, p_in_v_e_second_comp, d_in_v_e_second_comp, f_in_v_e_second_comp)),

#only for charge neutral compounds
#    print('{:.3f},'.format(ternary_comp.oxi_state_guesses()[0][a_in_second_comp]/second_comp.oxi_state_guesses()[0][a_in_second_comp])),
#    print('{:.3f},'.format(ternary_comp.oxi_state_guesses()[0][b_in_second_comp]/second_comp.oxi_state_guesses()[0][b_in_second_comp])),


#######################################################print class##############################################
    if (float(E_DFT) == 0): 
        E_DFT = 0.0001
    E_off = (float(E_heuristic)/float(E_DFT)-1)*100
    E_off_s = 1
    if E_off > int(tolerance) or E_off < -1 * int(tolerance):
        E_off_s = 0
    print('{}'.format(E_off_s)),
    #print("\n"),
    
#############################################################################################################
    element_ratio = []
