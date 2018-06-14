import cv2,time,os, argparse, threading

def save_img(path, frame):
    cv2.imwrite(path, frame)


def parse_args():
    """Parse input arguments."""
    parser = argparse.ArgumentParser(description='Crop a single video with a provided stride')
    parser.add_argument('--video', dest='name', help='target video path',
                        required=True)
    parser.add_argument('--stride', dest='stride', help='desired stride',
                        default=1, type=int)
    args = parser.parse_args()

    return args


if __name__ == '__main__':
    args = parse_args()

    (major_ver, minor_ver, subminor_ver) = cv2.__version__.split('.')
    fps=0
    frames=0
    video = cv2.VideoCapture(args.name)
    if int(major_ver) < 3:
        fps = video.get(cv2.cv.CV_CAP_PROP_FPS)
        frames = video.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)
        print("Frames per second using video.get(cv2.cv.CV_CAP_PROP_FPS): {0},{1}".format(fps,frames))
    else:
        fps = int(video.get(cv2.CAP_PROP_FPS))
        frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        print("Frames per second using video.get(cv2.CAP_PROP_FPS) : {0},{1}".format(fps,frames))
    #wanted = range(0,frames,int(fps))
    timestart=time.time()
    rval = True
    c=0
    folder = args.name.split('.')[-2]
    print(folder)
    if not os.path.exists(folder):
        os.mkdir(folder)
    while rval:
        rval, frame = video.read()
        if c % args.stride == 0:
            path = os.path.join(folder, '{:06d}'.format(int(c / args.stride)) + '.jpg')
            thread=threading.Thread(target=save_img, args=(path, frame))
            thread.start()
        c = c + 1
    timestop = time.time()
    print(timestop-timestart)
    video.release()
