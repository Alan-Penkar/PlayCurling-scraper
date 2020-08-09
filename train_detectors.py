from utils.Actions import train_detectors
import argparse
ap = argparse.ArgumentParser()
ap.add_argument('-c','--config', help='Path to configuration json', default='Window.json')

args = vars(ap.parse_args())
d = train_detectors(args['config'])
