import cv2,time,os, argparse, threading

def save_img(path, frame):
    cv2.imwrite(path, frame)


def parse_args():
    """Parse input arguments."""
    parser = argparse.ArgumentParser(description='Crop a single video with a provided stride')
    parser.add_argument('--video', dest='name', help='video path',
                        required=True)
    parser.add_argument('--folder', dest='folder', help='image folder path',
                        default="")
    parser.add_argument('--stride', dest='stride', help='desired stride',
                        default=1, type=int)

    args = parser.parse_args()

    return args


def main(name, folder, stride):
    (major_ver, minor_ver, subminor_ver) = cv2.__version__.split('.')
    fps=0
    frames=0
    video = cv2.VideoCapture(name)
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
    if folder == "":
        folder = name.split('.')[-2]
    print(folder)
    if not os.path.exists(folder):
        os.makedirs(folder)
    while rval:
        rval, frame = video.read()
        if c % stride == 0:
            path = os.path.join(folder, '{:06d}'.format(int(c / stride)) + '.jpg')
            save_img(path, frame)
            #thread=threading.Thread(target=save_img, args=(path, frame))
            #thread.start()
        c = c + 1
    timestop = time.time()
    print(timestop-timestart)
    video.release()


if __name__ == '__main__':
    args = parse_args()
    main(args.name, args.folder, args.stride)

    
