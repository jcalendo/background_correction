"""
This program will iterate through image files (specimen images) in a folder and
save new image files of background corrected images given brightfield and
darkfield input images in a new "Corrected" folder for analysis
"""
import cv2
import os
import numpy as np


def correct_background(input_img, brightfield_img, darkfield_img):
    """Correct background of source image given brightfield and darkfield.
    Returns corrected image."""
    specimen = cv2.imread(input_img)
    brightfield = cv2.imread(brightfield_img)
    darkfield = cv2.imread(darkfield_img)

    numerator = cv2.subtract(specimen, darkfield)
    divisor = cv2.subtract(brightfield, darkfield)

    C = np.mean(specimen) * (1 / np.mean(cv2.divide(numerator, divisor)))

    corrected = numerator / divisor * C

    return corrected


def process_folder(src_dir, bright, dark, out_dir):
    """Iterate through folder producing background corrected images and saving
    in new location."""
    for filename in os.listdir(src_dir):
        if filename.endswith(".tif"):
            f_name = (os.path.join(src_dir, filename))
            print("Processing: {}".format(f_name))
            output = correct_background(f_name,
                                        brightfield_img=bright,
                                        darkfield_img=dark)
            os.chdir(out_dir)
            print("Corrected {} written to {}".format(f_name, out_dir))
            cv2.imwrite(filename, output)
