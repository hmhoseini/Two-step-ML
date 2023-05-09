import os
import json
from collections import Counter

ab_unique = []
ab_all = []
ab_tmp = []
ab_final = []
ehuls = []

with open('allBinaries_dict.dat', 'r') as binary_file:
    binaries = json.load(binary_file)

for a_binary in binaries:
    compound = a_binary["pretty_formula"]
    ab_all.append(compound)  
    if  not (compound in ab_unique):
        ab_unique.append(compound)

cnt = Counter()

for comp in ab_all:
    cnt[comp] += 1

for key, value in cnt.items():
    if (value == 1): 
        for a_binary in binaries:
            if (key == a_binary["pretty_formula"]):
                ab_final.append(a_binary)
    if (value > 1): 
        for a_binary in binaries:
            if (key == a_binary["pretty_formula"]):
                ab_tmp.append(a_binary)
        for n in range(0, len(ab_tmp)):
            ehuls.append(ab_tmp[n]["e_above_hull"])
        minehul = min(ehuls)
        ehuls = []
        for n in range(0, len(ab_tmp)):
            if (minehul == ab_tmp[n]["e_above_hull"]):
                ab_final.append(ab_tmp[n])
        ab_tmp = []

with open('stableBinaries_list.dat', 'w') as fhandle:
    for n in range (0, len(ab_final)):
        fhandle.write('{}, {} '.format(ab_final[n]['pretty_formula'], ab_final[n]["e_above_hull"])+'\n')

with open('stableBinaries_dict.json', 'w') as fhandle:
    json.dump(ab_final, fhandle)
