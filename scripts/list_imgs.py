# helpful for creating a testing .txt file to visualize only some of yolo/darknet predictions
# writes paths of only every x-th specified testing image for later visualization

import os
from os import path as osp

def list_imgs(img_dir, x, out):
    # only writes the path of every x-th image in dir to file out, which is created in dir script is run from
    f = open(out, 'w+')
    
    count = 0
    imgs = 0
    for n in os.listdir(img_dir):
        if osp.splitext(n)[1] == '.jpg':
            if count % x == 0:
                f.write(osp.join(img_dir, n) + '\n')
                imgs += 1
            count += 1
    print('%d image paths written of total %d images' % (imgs,count))
    print('File saved as %s' % out)
        

def main():
    # main for file to be called "list_imgs.py" 
    out = 'visual_test.txt' # if want to save directly to darknet data set out='PATH_TO_DARKNET/data/NAME.txt'
    list_imgs('PATH_TO_IMAGES', 10, out)

if __name__ == '__main__':
    main()
