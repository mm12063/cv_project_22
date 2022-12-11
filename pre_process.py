import file_locs
from os import listdir
from os.path import isfile, join
import os
from PIL import Image
import PIL
import numpy as np
from os.path import exists
from tqdm import tqdm

DATASETS_TO_UPDATE = [
    file_locs.TRAIN_DS,
    file_locs.VAL_DS
    file_locs.TEST_DS
]

def resize_large_images(ds_loc):
    print("Resizing the large images...")
    DIR = f"{ds_loc}resized/"
    if not os.path.exists(DIR):
        os.makedirs(DIR)

    files = [f for f in listdir(DIR) if isfile(join(DIR, f))]

    large_img_size = (4288, 2848)

    for filename in tqdm(files):
        full_loc = ds_loc + filename
        if (filename == ".DS_Store") or exists(DIR+filename):
            continue
        im = Image.open(full_loc)
        if im.size == large_img_size:
            resizedImage = im.resize((int(large_img_size[0]*.5), int(large_img_size[1]*.5)), Image.Resampling.LANCZOS)
            resizedImage.save(f"{DIR}{filename}", 'png')


def crop_to_remove_border(image):
    thresh = 80
    im = np.array(image)
    im[im < thresh] = 0
    y_nonzero, x_nonzero, _ = np.nonzero(im)
    cropped = image.crop((np.min(x_nonzero), np.min(y_nonzero), np.max(x_nonzero), np.max(y_nonzero)))
    if cropped.size != (0,0):
        return cropped
    else:
        return image


def auto_cropping(ds_loc):
    print("Auto cropping to remove the black border...")
    DIR = f"{ds_loc}resized/auto_crop/"

    if not os.path.exists(DIR):
        os.makedirs(DIR)

    files = [f for f in listdir(DIR) if isfile(join(DIR, f))]

    for filename in tqdm(files):
        full_loc = ds_loc+filename
        if (filename == ".DS_Store") or exists(DIR+filename):
            continue
        im = Image.open(full_loc)
        cropped_image = crop_to_remove_border(im)
        cropped_image.save(f"{DIR}{filename}", 'png')


def update_bad_crops(ds_loc):
    print("Checking for bad crops and reverting to original image...")
    DIR = f"{ds_loc}resized/auto_crop/"

    files = [f for f in listdir(DIR) if isfile(join(DIR, f))]

    for filename in tqdm(files):
        full_loc = DIR + filename
        if (filename == ".DS_Store"):
            continue
        im = Image.open(full_loc)
        MIN = 1200
        width, height = im.size
        if width < MIN or height < MIN:
            print(f"Bad crop: {full_loc} = {im.size} Reverting to original...")
            orig = Image.open(ds_loc + filename)
            orig.save(f"{DIR}{filename}", 'png')



def crop_all_to_same_size(ds_loc):
    print("Cropping all images to same size...")
    START_DIR = f"{ds_loc}resized/auto_crop/"
    DIR = f"{START_DIR}same_size/"
    CROP_SIZE = 1350

    if not os.path.exists(DIR):
        os.makedirs(DIR)

    files = [f for f in listdir(START_DIR) if isfile(join(START_DIR, f))]

    for filename in tqdm(files):
        full_loc = START_DIR + filename
        if (filename == ".DS_Store") or exists(DIR+filename):
            continue
        im = Image.open(full_loc)
        width, height = im.size

        left = (width - CROP_SIZE) / 2
        top = (height - CROP_SIZE) / 2
        right = (width + CROP_SIZE) / 2
        bottom = (height + CROP_SIZE) / 2

        cropped = im.crop((left, top, right, bottom))
        cropped.save(f"{DIR}{filename}", 'png')



def resize_all(ds_loc):
    print("Resizing all images to similar size...")
    DIR = f"{ds_loc}resized/auto_crop/same_size/"
    RESIZE_SIZE = 1000

    files = [f for f in listdir(DIR) if isfile(join(DIR, f))]

    for filename in tqdm(files):
        full_loc = DIR + filename
        if (filename == ".DS_Store"):
            continue
        im = Image.open(full_loc)
        resized = im.resize((int(RESIZE_SIZE), int(RESIZE_SIZE)), Image.Resampling.LANCZOS)
        resized.save(f"{DIR}{filename}", 'png')



for ds_loc in DATASETS_TO_UPDATE:
    print(f"Updating DS: {ds_loc}")
    resize_large_images(ds_loc)
    auto_cropping(ds_loc)
    update_bad_crops(ds_loc)
    crop_all_to_same_size(ds_loc)
    resize_all(ds_loc)
    print("*"*20)















