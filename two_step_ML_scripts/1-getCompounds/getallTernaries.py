import os
import json
from pymatgen.core.composition import Composition
from pymatgen.ext.matproj import MPRester

# Make sure that you have the Materials API key. Put the key in the call to MPRester if needed, e.g, MPRester("MY_API_KEY")
mpr = MPRester('')

results = mpr.query(criteria={'nelements':3, 'is_hubbard':False, 'is_compatible': True},\
                    properties=['pretty_formula', 'formation_energy_per_atom', 'material_id', 'e_above_hull', 'is_hubbard', 'is_compatible']
                    )
with open('allTernaries_list.dat', 'w') as fhandle:
    for a_result in results:
        fhandle.write(a_result['pretty_formula']+'\n')
with open('allTernaries_dict.dat', 'w') as fhandle:
    json.dump(results, fhandle)
