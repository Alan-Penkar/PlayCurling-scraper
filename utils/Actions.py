import json
from json_minify import json_minify
import cv2
try:
    from .Objects import Region, State, DetectableObjects
except:
    from Objects import Region, State, DetectableObjects
try:
    from .parsing_helpers import build_instances, id_root_regions
except:
    from parsing_helpers import build_instances, id_root_regions

class Window(object):
    """
    Defines the Hierarchy of a Window with Regions, States, and Objects
    based on a json definition
    The Window is meant to encapsulate things that we are interested in tracking
    """
    def __init__(self, root_region):
        self.root_region = root_region
        self.active_images = {}

    def process_frame(self, image):
        self.active_images = dict()
        self._process_frame_node(image, self.root_region)

    def _process_frame_node(self, image, region):
        #Score all states in the region and set one to active
        cropped_image = region.set_active_state(image)
        #Store the image associated with this region
        self.active_images[region.name] = cropped_image
        #Recurse
        for subregion in region.active_state.regions:
            self._process_frame_node(cropped_image, subregion)

    @classmethod
    def create_from_config_file(cls, filename, single_root=True):
        conf = json.loads(json_minify(open(filename).read()))
        R, S = build_instances(conf)
        root_region_dict = id_root_regions(R, S)
        if len(root_region_dict)>1 and single_root:
            print(f"[WARNING] Too many root elements- please recheck your config file")
            return None
        return Window([x for x in root_region_dict.values()][0])

    def display_regions(self):
        for region_name, image in self.active_images.items():
            cv2.imshow(region_name, image)


if __name__=='__main__':
    o = Window.create_from_config_file('Window.json')
    print("None")