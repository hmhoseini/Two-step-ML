import os
import json


with open("allTernaries_dict.dat", 'r') as ternary_file:
    ternaries = json.load(ternary_file)
compositions = []
for a_ternary in ternaries:
    if a_ternary['e_above_hull'] != None:
        if not (a_ternary['pretty_formula'] in compositions) and a_ternary['e_above_hull'] < 0.2:
            compositions.append(a_ternary['pretty_formula'])
    else:
        print(a_ternary['pretty_formula'])

with open('uniqueTernaries_list.dat', 'w') as fhandle:
    for a_composition in compositions:
        fhandle.write(a_composition+'\n')


with open("allBinaries_dict.dat", 'r') as binary_file:
    binaries = json.load(binary_file)

compositions = []
for a_binary in binaries:
    if a_binary['e_above_hull'] != None:
        if not (a_binary['pretty_formula'] in compositions) and a_binary['e_above_hull'] < 0.2:
            compositions.append(a_binary['pretty_formula'])
    else:
        print(a_binary['pretty_formula'])

with open('uniqueBinaries_list.dat', 'w') as fhandle:
    for a_composition in compositions:
        fhandle.write(a_composition+'\n')
