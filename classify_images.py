from pprint import pprint
import os

import numpy as np
import cv2
import progressbar

IMAGE_TYPES = ['Long', 'House', 'Long_House']
IMAGE_TYPES = {image:f"images/{image}_Template.png" for image in IMAGE_TYPES}

TEMPLATES = {name: cv2.imread(path) for name, path in IMAGE_TYPES.items()}
raw_images = len(os.listdir('images/Raw'))
widgets = ["Classifying and Cropping: ", progressbar.Percentage(), " ", progressbar.Bar(), " ", progressbar.ETA()]
pbar = progressbar.ProgressBar(maxval=raw_images, widgets=widgets).start()

def process_image(image, image_path, template_name, template_image):
    result = cv2.matchTemplate(image, template_image, cv2.TM_CCOEFF)
    minVal, maxVal, minLoc, (x, y) = cv2.minMaxLoc(result)
    h,w = template_image.shape[:2]
    cv2.imwrite(f"images/{template_name}/{file_name}", image[y:y+h, x:x+w])

result_list = {}
for i, file_name in enumerate(os.listdir('images/Raw')):
    image = cv2.imread(f"images/Raw/{file_name}")
    image_result = {}

    for template_name, template_image in TEMPLATES.items():
        result = cv2.matchTemplate(image, template_image, cv2.TM_CCOEFF)
        minVal, maxVal, minLoc, (x, y) = cv2.minMaxLoc(result)
        image_result.update({template_name:maxVal})

    result_list.update({file_name:image_result})

    if image_result['House'] > image_result['Long']:
        process_image(image, f"images/Raw/{file_name}", 'House', TEMPLATES['House'])
    else:
        process_image(image, f"images/Raw/{file_name}", 'Long', TEMPLATES['Long'])
        process_image(image, f"images/Raw/{file_name}", 'Long_House', TEMPLATES['Long_House'])
    pbar.update(i)

pprint(result_list)