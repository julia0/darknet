import shutil
import json
import os
from os import path as osp
from PIL import Image, ImageDraw


def process_signs(label_dir, imgs_dir, output_dir, out_imgs):
    # Inspired by label2det.py from https://github.com/ucbdrive/bdd-data
    """Process BDD dataset given the original json labels and images. Record
    data about which images contain signs and the number of sign annotations.
    Write paths of images containing signs to text file in output directory. 
    Create copy of images containing signs and save to image output directory 
    after drawing bounding boxes for visualization of signs.
    
    Args:
        label_dir -- abs. path to directory with .json label files
        imgs_dir -- abs. path to directory with CORRESPONDING image files
        output_dir -- abs. path to directory where 'signs.txt' will be stored,
                        containing paths of images with signs
        out_imgs -- abs. path to directory where image copies with sign box
                    visualizations will be stored 
    
    """
    
    if not osp.exists(label_dir):
        print('Can not find', label_dir)
        return
    print('Processing', label_dir)
    input_names = [n for n in os.listdir(label_dir)
                   if osp.splitext(n)[1] == '.json']
    
    count = 0
    total_signs = 0
    signs_file = open(output_dir + 'signs.txt', 'w+')
    for name in input_names:
        label_path = osp.join(label_dir, name)
        img_name = os.path.splitext(name)[0] + '.jpg'
        img_path = imgs_dir + img_name
        json_file = json.load(open(label_path, 'r'))
        
        count = 0
        num_signs = 0
        for frame in json_file['frames']:
            for obj in frame['objects']:
                if 'box2d' not in obj:
                    continue
                xy = obj['box2d']
                if xy['x1'] >= xy['x2'] and xy['y1'] >= xy['y2']:
                    continue
                
                if (obj['category'] == 'traffic sign'):
                    num_signs += 1
                    
                    # write image path to text file, but no duplicates
                    if num_signs == 1:
                        signs_file.write(img_path + '\n')
                    
                    # make copy of image in output dir 
                    new_im = out_imgs + img_name
                    if (new_im != img_path):
                        shutil.copy(img_path, new_im)
                    
                    # box coordinates: convert floats to ints with round()
                    x1 = round(xy['x1'])
                    x2 = round(xy['x2'])
                    y1 = round(xy['y1'])
                    y2 = round(xy['y2'])
                    
                    # draw bounding box on copy image
                    im = Image.open(new_im)
                    draw = ImageDraw.Draw(im)
                    draw.rectangle([x1,y1,x2,y2], fill=None, outline=(0,0,255)) # blue outline
                    im.save(new_im)
                    
                    if (num_signs > 0):
                        # change image path 
                        img_path = new_im
                        
        print('Number of signs in', img_name, ':', num_signs)
        total_signs += num_signs                
         
        count += 1
        if count % 100 == 0:
            print('Finished processing', count, 'files')
                
    print('Total number of signs:', total_signs)
    
    
def main():
    label_dir = 'PATH_TO_LABELS'
    imgs_dir = 'PATH_TO_IMAGES'
    out_dir = 'TXT_OUT_DIR'  
    out_imgs = 'IMGS_OUT_DIR'
    process_signs(label_dir, imgs_dir, out_dir, out_imgs)


if __name__ == '__main__':
    main()
