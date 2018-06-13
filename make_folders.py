import os, glob, argparse

root ='/media/jane/0a36d079-2c65-49f6-b9cd-2fed6b9d6f25/2018/0*'
target='/media/jane/0a36d079-2c65-49f6-b9cd-2fed6b9d6f25/data5-11'


def parse_args():
    """Parse input arguments."""
    parser = argparse.ArgumentParser(description='Video cropping')
    parser.add_argument('--root', dest='root', required=True, help='cropping videos into frames')
    parser.add_argument('--target', dest='target', required=True, help='the stride by which frames are cropped')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    pdates = glob.glob(os.path.join(args.root,'0*'))
    pdates.sort()
    for pdate in pdates:
        if not os.path.isdir(pdate):
            continue
        date = pdate.split('/')[-1] #0405
        if int(date)>404:
            continue
        for i in [1, 3]:
            for j in range(1,5):
                targetfolder = os.path.join(args.target, '{}_{}_{}'.format(date, i, j)) # 0405_1_1
                if not os.path.exists(targetfolder):
                    os.mkdir(targetfolder)
                    print(targetfolder)

        pcams = glob.glob(os.path.join(pdate, 'L*'))
        pcams.sort()
        for pcam in pcams:
            cam_name = pcam.split('/')[-1].split(' ')[0] #L1M1C01
            targetfolders = glob.glob(os.path.join(target, '{}_*'.format(date)))
            for targetfolder in targetfolders:
                targetcam = os.path.join(targetfolder, '{} {}'.format(cam_name, targetfolder.split('/')[-1]))
                if not os.path.exists(targetcam):
                    os.mkdir(targetcam)