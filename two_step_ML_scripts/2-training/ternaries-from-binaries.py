import os
import json
from pymatgen.core.composition import Composition

with open("../1-getCompounds/stableTernaries_dict.json", 'r') as ternary_file:
    ternarycompounds_fromMP = json.load(ternary_file)

with open("../1-getCompounds/stableBinaries_dict.json", 'r') as binary_file:
    binariescompounds_fromMP = json.load(binary_file)

compound = []
abc = []

for a_ternary_fromMP in ternarycompounds_fromMP:
    compound = a_ternary_fromMP["pretty_formula"]

    ABC_comp = Composition(compound)
    ABC = a_ternary_fromMP

    ab = []
    AB = []
    AB_list = []
    # find all AB binary compounds 
    for a_binary_fromMP in binariescompounds_fromMP:
        AB_comp=Composition(a_binary_fromMP['pretty_formula'])
        if ABC_comp.elements[0] in AB_comp.keys() and ABC_comp.elements[1] in AB_comp.keys():
            AB.append(a_binary_fromMP)

    ac = []
    AC = []
    AC_list = []
    # find all AC binary compounds 
    for a_binary_fromMP in binariescompounds_fromMP:
        AC_comp=Composition(a_binary_fromMP['pretty_formula'])
        if ABC_comp.elements[0] in AC_comp.keys() and ABC_comp.elements[2] in AC_comp.keys():
            AC.append(a_binary_fromMP)

    bc = []
    BC = []
    BC_list = []
    # find all BC binary compounds 
    for a_binary_fromMP in binariescompounds_fromMP:
        BC_comp=Composition(a_binary_fromMP['pretty_formula'])
        if ABC_comp.elements[1] in BC_comp.keys() and ABC_comp.elements[2] in BC_comp.keys():
            BC.append(a_binary_fromMP)

#A_XB_YC_Z compound
    X = ABC_comp.get_atomic_fraction(ABC_comp.elements[0].symbol)
    Y = ABC_comp.get_atomic_fraction(ABC_comp.elements[1].symbol)
    Z = ABC_comp.get_atomic_fraction(ABC_comp.elements[2].symbol)

#a*A_xB_y+b*A_xpC_z  
    if len(AB) > 0 and len(AC) > 0:
        for n in range (0, len(AB)):
            for m in range (0, len(AC)):
                AB_compound = Composition(AB[n]['pretty_formula'])
                AB_id = AB[n]['material_id']
                AC_compound = Composition(AC[m]['pretty_formula'])
                AC_id = AC[m]['material_id']

                x  = AB_compound.get_atomic_fraction(ABC_comp.elements[0].symbol)
                y  = AB_compound.get_atomic_fraction(ABC_comp.elements[1].symbol)
                xp = AC_compound.get_atomic_fraction(ABC_comp.elements[0].symbol)
                z  = AC_compound.get_atomic_fraction(ABC_comp.elements[2].symbol)

                a = Y/y
                b = Z/z

                if   (X-0.01)< a*x+b*xp < (X+0.01):
                    AB_energy = AB[n]['formation_energy_per_atom']
                    AC_energy = AC[m]['formation_energy_per_atom']
                    E_heuristic = a * AB_energy + b * AC_energy
                    E_modified = 1.5 * E_heuristic - 0.02
                    print ('{}, {:.3f}, {}, {:.3f}, {:.3f}, {}, {:.3f}, {:.3f}, {:.3f}'.format(\
                           ABC['pretty_formula'], a, AB_compound.reduced_formula, AB_energy,\
                                           b, AC_compound.reduced_formula, AC_energy, ABC['formation_energy_per_atom'], E_heuristic))

#a*A_xB_y+b*B_zpC_z
    if len(AB) > 0 and len(BC) > 0:
        for n in range (0, len(AB)):
            for m in range (0, len(BC)):
                AB_compound = Composition(AB[n]['pretty_formula'])
                AB_id = AB[n]['material_id']
                BC_compound = Composition(BC[m]['pretty_formula'])
                BC_id = BC[m]['material_id']

                x  = AB_compound.get_atomic_fraction(ABC_comp.elements[0].symbol)
                y  = AB_compound.get_atomic_fraction(ABC_comp.elements[1].symbol)
                yp = BC_compound.get_atomic_fraction(ABC_comp.elements[1].symbol)
                z  = BC_compound.get_atomic_fraction(ABC_comp.elements[2].symbol)

                a = X/x
                b = Z/z

                if   (Y-0.01)< a*y+b*yp < (Y+0.01):
                    AB_energy = AB[n]['formation_energy_per_atom']
                    BC_energy = BC[m]['formation_energy_per_atom']
                    E_heuristic = a * AB_energy + b * BC_energy
                    E_modified = 1.5 * E_heuristic - 0.02
                    print ('{}, {:.3f}, {}, {:.3f}, {:.3f}, {}, {:.3f}, {:.3f}, {:.3f}'.format(\
                           ABC['pretty_formula'], a, AB_compound.reduced_formula, AB_energy,\
                                          b, BC_compound.reduced_formula, BC_energy, ABC['formation_energy_per_atom'], E_heuristic))

#aA_xC_z*+b*B_yC_zp
    if len(AC) > 0 and len(BC) > 0:
        for n in range (0, len(AC)):
            for m in range (0, len(BC)):
                AC_compound = Composition(AC[n]['pretty_formula'])
                AC_id = AC[n]['material_id']
                BC_compound = Composition(BC[m]['pretty_formula'])
                BC_id = BC[m]['material_id']

                x  = AC_compound.get_atomic_fraction(ABC_comp.elements[0].symbol)
                z  = AC_compound.get_atomic_fraction(ABC_comp.elements[2].symbol)
                y  = BC_compound.get_atomic_fraction(ABC_comp.elements[1].symbol)
                zp = BC_compound.get_atomic_fraction(ABC_comp.elements[2].symbol)

                a = X/x
                b = Y/y

                if   (Z-0.01)< a*z+b*zp < (Z+0.01):
                    AC_energy = AC[n]['formation_energy_per_atom']
                    BC_energy = BC[m]['formation_energy_per_atom']
                    E_heuristic = a * AC_energy + b * BC_energy
                    E_modified = 1.5 * E_heuristic - 0.02
                    print ('{}, {:.3f}, {}, {:.3f}, {:.3f}, {}, {:.3f}, {:.3f}, {:.3f}'.format(\
                           ABC['pretty_formula'], a, AC_compound.reduced_formula, AC_energy,\
                                                  b, BC_compound.reduced_formula, BC_energy, ABC['formation_energy_per_atom'], E_heuristic))
