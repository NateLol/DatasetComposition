import cv2,glob,argparse,os

def parse_args():
    parser = argparse.ArgumentParser(description='resize pedestrains to a uniform size.')
    parser.add_argument('--root', dest='root',required=True, help='path to root')
    parser.add_argument('--id', dest='id', required=True, help='which id to extract')
    parser.add_argument('--width', dest='width', type=int, help='desired width of output image',default=64)
    parser.add_argument('--height', dest='height', type=int, help='desired height of output image',default=128)
    args = parser.parse_args()
    return args

if __name__ =='__main__':
    args = parse_args()
    folders = glob.glob(os.path.join(args.root,'{}*'.format(args.id)))
    for folder in folders:
        if not os.path.isdir(folder):
            continue
        ims = glob.glob(folder+'\\*.jpg')
        for im in ims:
            img = cv2.imread(im)
            img = cv2.resize(img, (args.width, args.height))
            #im = im.replace(im.split('\\')[-1],'r_'+im.split('\\')[-1])
            cv2.imwrite(im, img)
