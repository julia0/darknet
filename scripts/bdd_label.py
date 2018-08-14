# Adapted label2det.py from https://github.com/ucbdrive/bdd-data to prepare annotations for YOLO v3 training via Darknet

import json
import os
from os import path as osp
from PIL import Image

def cat_int_id(cat):
    # new function
    """Map string category to integer id. Return id."""
    cats = {'bike': 0,'bus': 1,'car': 2,'motor': 3,'person': 4,'rider': 5, 
            'traffic light': 6, 'traffic sign': 7, 'train': 8, 'truck': 9}
    id = cats[cat]
    return id
    
def convert(label, w_i, h_i):
    # adapted function from label2det.py
    """ Creates annotation, adjusting to input width,height size. 
    1. Adds class id and box coordinates 
    2. Concatenates as string 
    """
    
    box = ''
    for frame in label['frames']:
        for obj in frame['objects']:
            if 'box2d' not in obj:
                continue
            xy = obj['box2d']
            if xy['x1'] >= xy['x2'] and xy['y1'] >= xy['y2']:
                continue
            
            # adaption for YOLO annotation
            cat = obj['category']
            cat_id = cat_int_id(cat)
            box += str(cat_id)
            
            # get coords
            x1 = xy['x1']
            x2 = xy['x2']
            y1 = xy['y1']
            y2 = xy['y2']
            
            # calculate image width and height
            width = x2 - x1 + 1
            height = y2 - y1 + 1
            
            # find center coords
            x_center = x1 + width / 2
            y_center = y1 + height / 2 
            
            # find relative (0-1] values and round to 6 decimal places
            x = round(x_center / w_i, 6)
            y = round(y_center / h_i, 6)
            w = round(width / w_i, 6)
            h = round(height / h_i, 6)
            
            box += ' ' + str(x) + ' ' + str(y) + ' ' + str(w) + ' ' + str(h) + '\n'
    return box


def make_annotations(label_dir, imgs_dir, darknet_dir, file):
    # adapted change_dir function from label2d.py
    """Prepare text files for Darknet YOLO training. 
    1. Creates and writes to file with paths to images. Saved in .../darknet/data dir.  
    2. Creates corresponding '.txt' file for each image with the annotations. Saved in same dir as images.
    
    Args:
        label_dir -- abs. path to json labels (corresponding to images)
        imgs_dir -- abs. path to jpg images (corresponding to labels)
        darknet_dir -- abs. path to darknet directory
        file -- either 'train.txt' or 'test.txt'
        
    """
    
    if not osp.exists(label_dir):
        print('Can not find', label_dir)
        return
    print('Processing', label_dir)
    input_names = [n for n in os.listdir(label_dir)
                   if osp.splitext(n)[1] == '.json']
    
    count = 0
    train_file = open(osp.join(darknet_dir,'data', file), 'w+')
    for name in input_names:
        root_name = os.path.splitext(name)[0]
        
        # get current image size
        img = osp.join(imgs_dir, root_name + '.jpg')
        image = Image.open(img)
        w_i, h_i, = image.size
        
        # create new file to write to
        f_name = osp.join(imgs_dir, root_name + '.txt')
        f = open(f_name, 'w+')
        
        # read label and convert to annotation, writing to file
        in_path = osp.join(label_dir, name)
        out = convert(json.load(open(in_path, 'r')), w_i, h_i)
        f.write(out) 
        
        # write image path to train.txt
        train_file.write(img + '\n')
        
        count += 1
        if count % 1000 == 0:
            print('Finished', count)


def main():
    label_dir = 'PATH_TO_LABELS'
    imgs_dir = 'PATH_TO_IMAGES'
    darknet_dir = 'PATH_TO_DARKNET'
    file = 'train.txt' # either 'train.txt' or 'test.txt'
    make_annotations(label_dir, imgs_dir, darknet_dir, file)


if __name__ == '__main__':
    main()
