from random import random
import cv2,time,os,sys
from tqdm import tqdm
from glob import glob
import numpy as np
import pandas as pd
from pathlib import Path
import logging
import getopt
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def main(argv):
    help_str = 'yolo_aug.py -i <input_dir> -t <aug_type (hflip,vflip,hvflip,bright)> -e <image extension (jpg,jpeg,png ...)> -o <output_dir>'

    try:
        opts, args = getopt.getopt(
            argv,"hi:t:e:o:",["input_dir=","aug_type=", "image extension=" ,"output_dir="])
    except getopt.GetoptError:
        log.exception(help_str)
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            log.info(help_str)
            sys.exit()
        elif opt in ("-i", "--input_dir"):
            input_dir = arg
        elif opt in ("-t", "--aug_type"):
            aug_type = arg
        elif opt in ("-e", "--image extension"):
            image_ext = arg
        elif opt in ("-o", "--output_dir"):
            output_dir = arg

    
    if aug_type == 'hflip':
        output_dir = output_dir + '/hflip_'+ time.strftime("%H%M%S")
        out_dir = Path(output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
    elif aug_type == 'vflip':
        output_dir = output_dir + '/vflip_'+ time.strftime("%H%M%S")
        out_dir = Path(output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
    elif aug_type == 'hvflip':
        output_dir = output_dir + '/hvflip_'+ time.strftime("%H%M%S")
        out_dir = Path(output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
    elif aug_type == 'bright':
        output_dir = output_dir + '/bright_'+ time.strftime("%H%M%S")
        out_dir = Path(output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
    else:
        log.error('Invalid augmentation type')
        log.exception(help_str)
        sys.exit(2)
            

    log.info('Input directory: {}'.format(input_dir))
    log.info('Augmentation type: {}'.format(aug_type))
    log.info('Output directory: {}'.format(output_dir))

    # --------- read yolo format label file -------------
    def boxesFromYOLO(imagePath,labelPath):
        image = cv2.imread(imagePath)
        (hI, wI) = image.shape[:2]
        lines = [line.rstrip('\n') for line in open(labelPath)]
        boxes = []
        if lines != ['']:
            for line in lines:
                components = line.split(" ")
                category = components[0]
                x  = int(float(components[1])*wI - float(components[3])*wI/2)
                y = int(float(components[2])*hI - float(components[4])*hI/2)
                h = int(float(components[4])*hI)
                w = int(float(components[3])*wI)
                boxes.append((category, (x, y, w, h)))
        return (hI, wI,image,boxes)

    # -------- vertical flip function --------
    def flip_ver(image,boxes,H,W):
        txt_yolo = []
        img= cv2.flip(image,1)
        (H,W) = img.shape[:2]
        for box in boxes:
            class_name = int(box[0])
            (x, y, w, h) = box[1]
            x2 = ((W - x -w)+w/2)/W
            h2 = h/H
            w2 = w/W
            y2 = (y+(h/2))/H
            txt_yolo.append((class_name,round(x2,4),round(y2,4),round(w2,4),round(h2,4)))
        return img,txt_yolo
    # -------- horizontal and vertical flip function --------
    def flip_hor_ver(image,boxes,H,W):
        txt_yolo = []
        img= cv2.flip(image,-1)
        (H,W) = img.shape[:2]
        for box in boxes:
            class_name =int(box[0])
            (x, y, w, h) = box[1]
            x2 = ((W - x -w)+w/2)/W
            h2 = h/H
            w2 = w/W
            y2 =((H -y -h)+h/2)/H
            txt_yolo.append((class_name,round(x2,4),round(y2,4),round(w2,4),round(h2,4)))
        return img,txt_yolo

    # -------- Horizontal flip function --------
    def flip_hor(image,boxes,H,W):
        txt_yolo = []
        img= cv2.flip(image,0)
        (H,W) = img.shape[:2]
        for box in boxes:
            class_name =int(box[0])
            (x, y, w, h) = box[1]
            x2 = (x+(w/2))/W
            h2 = h/H
            w2 = w/W
            y2 =((H -y -h)+h/2)/H
            txt_yolo.append((class_name,round(x2,4),round(y2,4),round(w2,4),round(h2,4)))
        return img,txt_yolo
    
    # -------- Brightness function --------
    def brightness_augment(img,boxes,H,W):
        hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV) #convert to hsv
        hsv = np.array(hsv, dtype=np.float64)
        factor = random()
        hsv[:, :, 2] = hsv[:, :, 2] * (factor + np.random.uniform()) #scale channel V uniformly
        hsv[:, :, 2][hsv[:, :, 2] > 255] = 255 #reset out of range values
        rgb = cv2.cvtColor(np.array(hsv, dtype=np.uint8), cv2.COLOR_HSV2RGB)
        (H,W) = img.shape[:2]
        txt_yolo = []
        for box in boxes:
            class_name =int(box[0])
            (x, y, w, h) = box[1]
            x2 = (x+(w/2))/W
            h2 = h/H
            w2 = w/W
            y2 =(y+(h/2))/H
            txt_yolo.append((class_name,round(x2,4),round(y2,4),round(w2,4),round(h2,4)))
        return rgb,txt_yolo

    # -------- read image and label file -------------
    images = glob(input_dir + f'/*.{image_ext}')

    for image_path in tqdm(images):
        (hI, wI,image,boxes) = boxesFromYOLO(image_path,image_path.replace(image_ext, 'txt'))
        if aug_type == 'hflip':
            img,txt_yolo = flip_hor(image,boxes,hI,wI)
        elif aug_type == 'vflip':
            img,txt_yolo = flip_ver(image,boxes,hI,wI)
        elif aug_type == 'hvflip':
            img,txt_yolo = flip_hor_ver(image,boxes,hI,wI)
        elif aug_type == 'bright':
            img,txt_yolo = brightness_augment(image,boxes,hI,wI)
        else:
            log.error('Unknown augmentation type: {}'.format(aug_type))
            sys.exit(2)
        cv2.imwrite(output_dir + '/' + image_path.split('/')[-1], img)
        with open(output_dir + '/' + image_path.split('/')[-1].replace(image_ext, 'txt'), 'w') as f:
            if txt_yolo != []:
                for box in txt_yolo:
                    f.write(f'{box[0]} {box[1]} {box[2]} {box[3]} {box[4]}\n')
            else:
                f.write('')


if __name__ == '__main__':
    main(sys.argv[1:])