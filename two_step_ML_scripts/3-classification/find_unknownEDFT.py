import os
import json


compounds = []

with open("../1-getCompounds/stableTernaries_dict.json", 'r') as ternary_file:
    ternarycompounds_fromMP = json.load(ternary_file)
for a_ternary_fromMP in ternarycompounds_fromMP:
    compounds.append(a_ternary_fromMP["pretty_formula"])

with open("A3B3C3_ternaries-from-binaries_notclassified.dat", 'r') as fhandle:
    lines = fhandle.readlines()
for aline in lines:
    acomposition = aline.split(',')[0]
    if acomposition not in compounds:
        print(aline,end = '')

