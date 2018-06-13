import cv2,os
import argparse

def parse_args():
    """Parse input arguments."""
    parser = argparse.ArgumentParser(description='Video cropping')
    parser.add_argument('--video_path', dest='video_path', help='cropping videos into frames',
                        default='')
    parser.add_argument('--frame_stride',dest='frame_stride', help='the stride by which frames are cropped', default=25, type=int)
    parser.add_argument('--folder', dest='folder', help='Path to folder that needs to run on', default='../data/demo')

    args = parser.parse_args()

    return args

if __name__ == '__main__':
    args = parse_args()



    video_path  = os.path.abspath(args.video_path)
    folder = video_path[0:-len(video_path.split('/')[-1])]
    video_name = video_path.split('/')[-1]
    image_folder_name = os.path.join(folder, video_name.split('.')[0])
    if not os.path.exists(image_folder_name):
        os.mkdir(image_folder_name)
    vc = cv2.VideoCapture(video_path)
    if vc.isOpened():
        rval, frame = vc.read()
    else:
        rval = False
        print('File can not be opened correctly!')

    c=0
    while rval:
        rval, frame = vc.read()
        if c % args.frame_stride == 0:
            cv2.imwrite(os.path.join(image_folder_name,'{:06d}'.format(int(c/args.frame_stride)) + '.jpg'), frame)
        c = c + 1


    vc.release()
