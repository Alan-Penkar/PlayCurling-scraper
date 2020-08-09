import json
from json_minify import json_minify
from os.path import exists
import cv2
import dlib
try:
    from .Objects import Region, State, DetectableObjects
except:
    from Objects import Region, State, DetectableObjects
try:
    from .parsing_helpers import build_instances, id_root_regions
except:
    from parsing_helpers import build_instances, id_root_regions

try:
    from .detection_helpers import parse_labelbox_boxes
except:
    from detection_helpers import parse_labelbox_boxes


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

###
#
# Detector Stuff
#
###

def train_detectors(filename, force=True):
    conf = json.loads(json_minify(open(filename).read()))
    train_options = dlib.simple_object_detector_training_options()
    validate_detectable_conf(conf)
    for detectable in conf.get("Objects", []):
        if not force:
            detector_path = detectable['detector_filepath']
            if exists(detector_path):
                continue
        images, box_dict = parse_labelbox_boxes(detectable["image_path"], detectable["annotation_filepath"], [detectable["name"]])
        detector = dlib.train_simple_object_detector(images, box_dict.get(detectable.get("name")), train_options)
        detector.save(detectable['detector_filepath'])
    return True

REQUIRED_DETECTABLE_FIELDS = ["name", "image_path", "annotation_filepath", "detector_filepath"]
def validate_detectable_conf(conf):
    for detectable in conf.get("Objects", []):
        for field in REQUIRED_DETECTABLE_FIELDS:
            if detectable.get(field) is None:
                raise ValueError(f"{field} is a required field for an Object")


if __name__=='__main__':
    o = Window.create_from_config_file('Window.json')
    #d = train_detectors('Window.json')
    print("None")