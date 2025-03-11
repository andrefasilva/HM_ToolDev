# ----IMPORTS----
import hm
import hw
import hm.entities as ent
import numpy as np
import os

# Verifies if a Hypermesh model is detected
def detectmodel():
    global model    
    model = hm.Session.get_current_model()    
    if hm.Session.model_exists(model) is True:
        print("Valid model detected.")        
    else:
        print("Model not found!")
        exit

# Runs model detection and requests user to select elements and nodes
detectmodel()
elems = hm.CollectionByInteractiveSelection(hm.Model(model),ent.Element,"Select BEAM elements to orient.")
nodes = hm.CollectionByInteractiveSelection(hm.Model(model),ent.Node,"Select nodes for orientation reference.")
print(f'Number of selected elems: {len(elems)}' + f'|| Number os selected nodes:{len(nodes)}')

np.correspnodes = hm.Collection(hm.Model(model),ent.Node,elems)
# Print each element in the array 
for element in np.correspnodes: 
    print(element)

