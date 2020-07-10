import time
import os
import argparse
import cv2
from pprint import pprint
try:
    from .utils.Actions import Window
except:
    from utils.Actions import Window

IMAGE_TYPES = ['Long', 'House']
IMAGE_TYPES = {image:f"images/{image}_Template.png" for image in IMAGE_TYPES}
TEMPLATES = {name: cv2.imread(path) for name, path in IMAGE_TYPES.items()}

class Stream(object):

    def __init__(self, stream_id, window_conf_path, writers=None):
        self.id = stream_id
        self.cap = cv2.VideoCapture(stream_id)
        self.window = Window.create_from_config_file(window_conf_path)
        self.writers = [] if writers is None else writers

    def read(self):
        success, image = self.cap.read()
        if not success:
            print(f"Failed to read from cap with stream {self.id}")
            return False
        else:
            self.window.process_frame(image)
            return True

        #Write Stream if required
        for writer in self.writers:
            writer.write(self.window.active_images[writer.region_name])

    def show(self):
        self.window.display_regions()

class StreamWriter(object):

    def __init__(self, path, region_name):
        self.path = path
        self.region_name = region_name

    def write(self):
        pass


def watch_stream(stream_id, seconds, config_path):
    starttime = time.time()
    stream = Stream(stream_id, config_path)
    while time.time()-starttime < seconds:
        if stream.read():
            stream.show()
            cv2.waitKey(1)
        print(stream.window.active_images.keys())
    stream.cap.release()
    return True

ap = argparse.ArgumentParser()
ap.add_argument('--stream','-s',default=2, help='Stream ID - video read will be from /dev/video{stream}', type=int)
ap.add_argument('--time','-t',default=5, help='Number of Seconds to Record Stream', type=int)
ap.add_argument('--window','-w',default='Window.json', help='Path to the Window Config')

if __name__=='__main__':
    stream_id = 2
    time_to_watch = 5
    args = vars(ap.parse_args())
    watch_stream(args['stream'], args['time'], args['window'])