import argparse,os,glob,shutil


def parse_args():
    """Parse input arguments."""
    parser = argparse.ArgumentParser(description='Renaming and arranging YUSHI videos to be compatibale for subsequent processing')
    parser.add_argument('--yushi', dest='yushi', help='path to yushi video root',
                        required=True)
    args = parser.parse_args()

    return args


if __name__ == '__main__':
    args = parse_args()
    videos = glob.glob(os.path.join(args.yushi,'*.ts'))
    videos.sort()
    for video in videos:
        name = video.split('/')[-1]
        foldername = name.split('-')[0]
        targetfolder= os.path.join(os.path.split(args.yushi)[0], foldername)
        period = name[name.index('2018'):]
        rename = '{}_{}_{}_{}_{}_{}--{}_{}_{}_{}_{}_{}'.format(period[0:4], int(period[4:6]), int(period[6:8]), period[8:10], period[10:12], period[12:14],
                                                                              period[15:19],int(period[19:21]), int(period[21:23]), period[23:25], period[25:27], period[27:29])
        if not os.path.exists(targetfolder):
            os.mkdir(targetfolder)
        shutil.move(video, os.path.join(targetfolder, rename + '.ts'))
    if not os.listdir(args.yushi):
        os.rmdir(args.yushi)
        #nate=1
