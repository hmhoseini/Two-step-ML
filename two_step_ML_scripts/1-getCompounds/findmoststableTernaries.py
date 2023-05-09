import os
import json
from collections import Counter

abc_unique = []
abc_all = []
abc_tmp = []
abc_final = []
ehuls = []

with open('allTernaries_dict.dat', 'r') as ternary_file:
    ternaries = json.load(ternary_file)

for a_ternary in ternaries:
    compound = a_ternary["pretty_formula"]
    abc_all.append(compound)  
    if  not (compound in abc_unique):
       abc_unique.append(compound)

cnt = Counter()

for comp in abc_all:
    cnt[comp] += 1

for key, value in cnt.items():
    if (value == 1): 
        for a_ternary in ternaries:
            if (key == a_ternary["pretty_formula"]):
                abc_final.append(a_ternary)
    if (value > 1): 
        for a_ternary in ternaries:
            if (key == a_ternary["pretty_formula"]):
                abc_tmp.append(a_ternary)
        for n in range(0, len(abc_tmp)):
            ehuls.append(abc_tmp[n]["e_above_hull"])
        minehul = min(ehuls)
        ehuls = []
        for n in range(0, len(abc_tmp)):
            if (minehul == abc_tmp[n]["e_above_hull"]):
                abc_final.append(abc_tmp[n])
        abc_tmp = []
  
with open('stableTernaries_list.dat', 'w') as fhandle:
    for n in range (0, len(abc_final)):
        fhandle.write('{}, {} '.format(abc_final[n]['pretty_formula'], abc_final[n]["e_above_hull"])+'\n')

with open('stableTernaries_dict.json', 'w') as fhandle:
    json.dump(abc_final, fhandle)
