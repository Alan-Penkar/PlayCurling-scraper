from utils.easy import resize_folder
import cv2
import argparse

ap = argparse.ArgumentParser()
ap.add_argument('-d','--directory', required=True)
ap.add_argument('-s','--scale', required=True, type=int)
ap.add_argument('-i','--inter', default=cv2.INTER_CUBIC)
ap.add_argument('-p','--prefix', default='Resized_')
ap.add_argument('-e','--extensions', default=None)
args = vars(ap.parse_args())


resize_folder(args['directory'], factor_w=args['scale'], inter=args['inter'], file_prefix=args['prefix'], file_extensions=args['extensions'])