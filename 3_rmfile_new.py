import os, glob, shutil,argparse

def parse_args():
    """Parse input arguments."""
    parser = argparse.ArgumentParser(description='Video cropping')
    parser.add_argument('--source', dest='root', required=True, help='cropping videos into frames',)
    parser.add_argument('--target',dest='target', help='the stride by which frames are cropped', default='' )
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parse_args()
    if args.target == '':
        args.target = args.root
    pcams = glob.glob(os.path.join(args.root,'L*'))
    pcams.sort()
    for pcam in pcams:
        if not os.path.isdir(pcam):
            continue

        cam = pcam.split('/')[-1]

        pvideos = glob.glob(os.path.join(pcam, '2018*'))
        pvideos.sort()
        for pvideo in pvideos:
            if not (pvideo.endswith('mp4') or pvideo.endswith('ts')):
                continue
            video_name = pvideo.split('/')[-1]
            date = '{:02d}{:02d}'.format(int(video_name.split('_')[1]),int(video_name.split('_')[2]))



            if int(video_name.split('_')[3]) in [6, 7, 8]:
                date_r_t = '{}_{}_{}'.format(date, cam[1], 1)
            elif int(video_name.split('_')[3]) in [10, 11]:
                date_r_t = '{}_{}_{}'.format(date, cam[1], 2)
            elif int(video_name.split('_')[3]) in [12, 13]:
                date_r_t = '{}_{}_{}'.format(date, cam[1], 3)
            else:
                date_r_t = '{}_{}_{}'.format(date, cam[1], 4)

            targetfolder = os.path.join(args.target, date_r_t, '{} {}'.format(cam, date_r_t))
            os.makedirs(targetfolder)
            shutil.move(pvideo, os.path.join(targetfolder,video_name))
        if not os.listdir(pcam):
            os.rmdir(pcam)
