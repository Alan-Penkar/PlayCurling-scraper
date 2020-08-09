from __future__ import print_function
import os
import json
from imutils import paths
from skimage import io
import dlib
import sys

if sys.version_info > (3,):
    long = int

IMAGE_PATH = ''
ANNOTATION_PATH = ''
OUTPUT_PATH = ''

options = dlib.simple_object_detector_training_options()

def make_abs_path(path, directory=True):
    if path[0] != '/':
        path = os.getcwd() + '/' + path
    if directory and path[-1] != '/':
        path += '/'
    return path

def parse_labelbox_boxes(IMAGE_PATH, ANNOTATION_FILEPATH, CLASS_NAMES):
    """
    Parses a labelbox JSON of annotations and returns the image and bounding box
    arrays that are required for training by dlib
    :parameter: IMAGE_PATH - path to the directory holding all images for training
    :parameter: ANNOTATION_PATH - Path to the annotation json file
    :parameter: CLASS_NAMES - list of object names to detect (lowercased)
    :return: list(images), dict(object_name : list(boxes))
    """
    IMAGE_PATH = make_abs_path(IMAGE_PATH)
    annotation_data = json.loads(open(ANNOTATION_FILEPATH).read())
    images = []
    boxes = {name:[] for name in CLASS_NAMES}
    for image_data in annotation_data:
        image_file = image_data.get('External ID')
        images.append(io.imread(IMAGE_PATH + image_file))
        image_boxes = {name: [] for name in CLASS_NAMES}
        for obj in image_data.get("Label",{}).get("objects",[]):
            object_name = obj.get('title','').lower()
            if object_name not in CLASS_NAMES:
                continue
            label_box = obj.get('bbox',{})
            image_boxes[object_name].append(
                dlib.rectangle(left=long(label_box.get("left")), top=long(label_box.get("top")), right=long(label_box.get("width")), bottom=long(label_box.get("height")))
            )
        for class_name in CLASS_NAMES:
            boxes[class_name].append(image_boxes[class_name])

    return images, boxes


if __name__=='__main__':
    IMAGE_PATH = '/home/alan/Documents/PythonProjects/DataScience/pyimagesearchgurus/PlayCurling/images/Long/'
    ANNOTATION_FILEPATH = '/home/alan/Documents/PythonProjects/DataScience/pyimagesearchgurus/PlayCurling/annotations/Long/all_stones.json'
    CLASS_NAMES = ['stone']
    print(parse_labelbox_boxes(IMAGE_PATH, ANNOTATION_FILEPATH, CLASS_NAMES))