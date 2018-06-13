import cv2,  os
import argparse


def cropping(video, image_folder):
    vc = cv2.VideoCapture(video)
    if vc.isOpened():
        rval, frame = vc.read()
    else:
        rval = False
        print('File can not be opened correctly!')

    c=0
    while rval:
        rval, frame = vc.read()
        if c % args.frame_stride == 0:
            cv2.imwrite(os.path.join(image_folder,'{:06d}.jpg'.format(c/args.frame_stride)), frame)
        c = c + 1
    vc.release()

def parse_args():
    """Parse input arguments."""
    parser = argparse.ArgumentParser(description='Video cropping to images into separate but exact same dirs')
    parser.add_argument('--video', dest='video', required=True, help='video root path',
                        default='')
    parser.add_argument('--image', dest='image', required=True, help='image root path',
                        default='')
    parser.add_argument('--frame_stride',dest='frame_stride', help='the stride by which frames are cropped', default=25, type=int)

    args = parser.parse_args()
    return args


def find_file(args, dirname, files):
    files.sort()
    for file in files:
        file_path=os.path.join(dirname, file)
        if os.path.isfile(file_path):
            target_path = os.path.join(args.image, file_path[len(args.video)+1:].split('.')[0])
            if not os.path.exists(target_path):
                os.makedirs(target_path)
            cropping(file_path, target_path)


if __name__ == '__main__':
    args = parse_args()
    os.path.walk(args.video, find_file, args)



