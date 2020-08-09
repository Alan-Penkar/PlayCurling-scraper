import cv2
import os
from .detection_helpers import make_abs_path


def resize_folder(path, factor_w=None, factor_h=None, inter=cv2.INTER_AREA, file_prefix=None, file_extensions=None):
    assert factor_h is not None or factor_w is not None, "A multiplying factor for height or width is required"

    path = make_abs_path(path)
    files = os.listdir(path)
    if file_prefix is None:
        file_prefix = 'resized_'

    if file_extensions is None:
        file_extensions = ['.png', '.jpg']

    for file in files:
        if not file[-4:] in file_extensions:
            continue
        image = cv2.imread(path+file)
        print(file)
        if factor_w is not None:
            options = {"width": image.shape[1]*factor_w}
        if factor_h is not None:
            options = {"height": image.shape[0]*factor_h}
        if inter is not None:
            options.update({"inter":inter})
        image2 = resize(image, **options)
        cv2.imwrite(path+file_prefix+file, image2)

def resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation=inter)

    # return the resized image
    return resized
