from pprint import pprint
from collections import defaultdict
import json
from json_minify import json_minify
import numpy as np
import cv2
try:
    from .Objects import Region, State, DetectableObjects
except:
    from Objects import Region, State, DetectableObjects

def build_instances(conf_data):
    """
    Takes the parsed json config and creates the associated states and regions
    :param conf_data:
    :return:
    """
    Regions = dict() #Tracks {region name: Region object}
    States = dict() #Tracks {state name: State object}
    State_Region_map = {} #Tracks {state: parent_region}

    #Create all the Regions while tracking what states are associated with each region
    for reg_conf in conf_data['Regions']:
        name = reg_conf.get('name',"UNKNOWN_REGION")
        needs_dummy_state = reg_conf.get('states') is None
        Regions[name] = Region(name, reg_conf.get('x',None), reg_conf.get('y',None),
                        reg_conf.get('width',None), reg_conf.get('height',None),
                               dummy_state=needs_dummy_state)
        if not needs_dummy_state:
            for state_name in reg_conf.get('states', []):
                State_Region_map[state_name] = name

    #Creates all States
    for state_conf in conf_data['States']:
        name = state_conf.get("name","UNKNOWN_STATE")
        template_image = state_conf.get("template_image", None)
        regions = state_conf.get("regions")
        if regions is None:
            regions = list()
        regions = [Regions.get(reg) for reg in regions]
        States[name] = State(name, Regions[State_Region_map[name]], template_image, regions=regions)

        #Add State to its parent region
        state = States[name]
        region_name = State_Region_map[name]
        region = Regions[region_name]
        region.add_state(state)
        #check sizes match
        if region.width is None or region.height is None:
            region.width, region.height = state.width, state.height
        elif region.width!=state.width or region.height !=state.height:
            print(f"[WARNING] Size Doesn't match for Region: {region.name} and related State:{state.name}\n"
                  f"Region '{region.name}' has size ({region.width},{region.height}) and State '{state.name}' has size ({state.width},{state.height})")

    print("DONE")
    return Regions, States

def id_root_regions(Regions, States):
    non_root_regions = []
    [non_root_regions.extend(x.regions) for x in States.values()]
    root_regions = {name:obj for name, obj in Regions.items() if obj not in non_root_regions}
    return root_regions

if __name__=='__main__':
    filename = 'Window.json'
    conf = json.loads(json_minify(open(filename).read()))
    pprint(conf)
    R, S = build_instances(conf)
    print(id_root_regions(R, S))
    #R, S = check_sizes(R,S)