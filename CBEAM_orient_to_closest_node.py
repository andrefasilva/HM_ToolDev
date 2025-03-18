##################################################
#              Author: André Silva               #
##################################################
#
################ Version history #################
# v1.0 - First version
# v2.0 - Calculated distance from node A of CBEAM
# to closest node (instead of node A and B)
#_________________________________________________

# ----IMPORTS----
import hm
import hm.entities as ent
import sys

# Verifies if a Hypermesh model is detected
def detectmodel():
    global model    
    model = hm.Session.get_current_model()    
    if hm.Session.model_exists(model) is True:
        print("Valid Hypermesh model detected.")        
    else:
        print("Model not found!")
        exit

# Runs model detection and requests user to select elements and nodes
detectmodel()
elems = hm.CollectionByInteractiveSelection(hm.Model(model),ent.Element,"Select BEAM elements to orient.")
nodes = hm.CollectionByInteractiveSelection(hm.Model(model),ent.Node,"Select nodes for orientation reference.")
print(f'Number of selected elems: {len(elems)}' + f' || Number of selected nodes:{len(nodes)}')
print("-------------------------")
# Checks if all selected elements are CBEAM, otherwise stops the code
for element in elems:
    if element.typename != "CBEAM":
        print('Selected elements contain non CBEAM elements. Review selection.')
        sys.exit('Terminated with errors.')

#Initialization of variables    
stored1 = 1000.0
stored2 = stored1

# Find the distance between node A of CBEAM and finding the closest node from the reference list
for element in elems:
    for node in nodes:
        distance1 = hm.Model(model).hm_getdistance(ent.Node,element.node1.id,node.id,element.node1.outputsystemid.id)
        if stored1 > distance1[1].distanceTotal:
            stored1 = distance1[1].distanceTotal
            nodeid1 = node
            temp1 = stored1
    stored1 = 1000.0

    # Orients beam based on distance -> node A of CBEAM with closest node
    hm.Model(model).bardirectionupdate(hm.Collection(hm.Model(),ent.Element,[element.id]),nodeid1,0)
    print("Successfully oriented element " + str(element.id) + " with respect to node " + str(nodeid1.id))  
    print("-------------------------")
print("-------- FINISHED -------")