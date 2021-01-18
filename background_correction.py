"""
This program will iterate through image files (specimen images) in a folder and
save new image files of background corrected images given brightfield and
darkfield input images in a new "Corrected" folder for analysis
"""
import cv2
import os
import numpy as np
from gooey import Gooey
from gooey import GooeyParser


def correct_background(input_img, brightfield_img, darkfield_img):
    """Correct background of source image given brightfield and darkfield.
    Returns corrected image."""
    specimen = cv2.imread(input_img)
    brightfield = cv2.imread(brightfield_img)
    darkfield = cv2.imread(darkfield_img)

    numerator = cv2.subtract(specimen, darkfield)
    divisor = cv2.subtract(brightfield, darkfield)

    # Calculated constant that can be applied in place of 255
    # C = np.mean(specimen) * (1 / np.mean(cv2.divide(numerator, divisor)))
    corrected = numerator / divisor * 255

    return corrected.astype('float32')


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


@Gooey(program_name="A Priori Background Correction", default_size=(700, 530))
def main():
    parser = GooeyParser(description="Perform a priori Background Correction. Written by Gennaro Calendo")
    parser.add_argument("Brightfield", help="Select the Brightfiled image", widget='FileChooser')
    parser.add_argument("Darkfield", help="Select the Darkfield image", widget="FileChooser")
    parser.add_argument("Specimen_images", help="Choose the image set to be corrected", widget="DirChooser")
    args = parser.parse_args()

    bf = args.Brightfield
    df = args.Darkfield
    img_dir = args.Specimen_images

    if not os.path.exists(os.path.join(img_dir, "corrected_images")):
            os.makedirs(os.path.join(img_dir, "corrected_images"))
    
    out_dir = os.path.join(img_dir, "corrected_images")
    
    np.seterr(divide='ignore', invalid='ignore')

    process_folder(img_dir, bf, df, out_dir)


if __name__ == '__main__':
    main()