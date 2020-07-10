import json
import pickle

import cv2
import numpy as np


class Region(object):

    def __init__(self, name, x, y, w, h, dummy_state=True):
        self.name = name
        self.x, self.y = x, y
        self.width, self.height = w, h
        self.states = list() if not dummy_state else [self.create_dummy_state()]
        self.active_state = None

    def add_state(self, state):
        self.states.append(state)

    def remove_state(self, state_name):
        rem_states = [x for x in self.states if x.name==state_name]
        for rem_state in rem_states:
            self.states.remove(rem_state)

    def create_dummy_state(self):
        dummy_state = State(f"{self.name}-state", self, None)
        return dummy_state

    @property
    def region_found(self):
        return self.x is not None and self.y is not None and self.width is not None and self.height is not None

    def _get_cropped_region(self, image, copy=True):
        if not self.region_found:
            self._score_states(image, source_image=True)
        if copy:
            return image[self.y:self.y+self.height, self.x:self.x+self.width].copy()
        else:
            return image[self.y: self.y+self.height, self.x: self.x+self.width]

    def _score_states(self, image, source_image=True):
        best_score = -1
        for state in self.states:
            score, (x,y) = state.score_image(image)
            if score > best_score:
                best_score = score
                if source_image:
                    self.x, self.y = x, y
                self.active_state = state
        if best_score < 0:
            print(f"[WARNING] Best State for Region:{self.name} is {self.active_state} with score={best_score}")


    def set_active_state(self, image, relocate=False):
        if not self.region_found or relocate:
            self._score_states(image, source_image=True)
            return self._get_cropped_region(image)
        else:
            img = self._get_cropped_region(image)
            self._score_states(img, source_image=False)
            return img


class State(object):

    def __init__(self, name, parent_region, template_path, regions=None, objects=None):
        self.name = name
        self.parent_region = parent_region
        self.template_path = template_path
        self._set_template(template_path)
        self.regions = list() if regions is None else regions
        self.objects = list() if objects is None else objects

    def _set_template(self, path):
        if path is not None:
            image = cv2.imread(path)
            self.height, self.width = image.shape[:2]
            self.template_image = image
            return True
        else:
            self.width, self.height = None, None
            return False

    def score_image(self, image):
        result = cv2.matchTemplate(image, self.template_image, cv2.TM_CCOEFF_NORMED)
        minVal, maxVal, minLoc, (x, y) = cv2.minMaxLoc(result)
        return maxVal, (x,y)

    @property
    def size(self):
        return self.width, self.height

    def add_region(self, region):
        self.regions.append(region)

    def remove_region(self, region_name):
        rem_regions = [x for x in self.regions if x.name == region_name]
        for rem_region in rem_regions:
            self.regions.remove(rem_region)

    def add_object(self, _object):
        self.objects.append(_object)

    def remove_object(self, object_name):
        rem_objects = [x for x in self.objects if x.name == object_name]
        for rem_object in rem_objects:
            self.objects.remove(rem_object)

class DetectableObjects(object):

    def __init__(self, name, detector):
        self.name = name
        self.detector = detector


if __name__ == '__main__':
    import pickle
    from pprint import pprint
    rootRegion = Region('Root', 0, 0, 960, 600)

    pprint(rootRegion.__dict__)
    with open('temp.pkl','wb') as f:
        pickle.dump(rootRegion, f)
