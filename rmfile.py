import os, glob, shutil,argparse



def parse_args():
    """Parse input arguments."""
    parser = argparse.ArgumentParser(description='Video cropping')
    parser.add_argument('--source', dest='root', required=True, help='cropping videos into frames',)
    parser.add_argument('--target',dest='target', required=True, help='the stride by which frames are cropped', )
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parse_args()
    pdates = glob.glob(os.path.join(args.root,'0*'))
    pdates.sort()
    for pdate in pdates:
        if not os.path.isdir(pdate):
            continue

        date = pdate.split('/')[-1]
        if int(date) > 404:
            continue
        pcams = glob.glob(os.path.join(pdate, 'L*'))
        pcams.sort()
        for pcam in pcams:
            if not os.path.isdir(pcam):
                continue
            tmp = pcam.split('/')[-1]
            cam = tmp.split(' ')[0]
            pperiods = glob.glob(os.path.join(pcam, '2018*'))
            pperiods.sort()
            for pperiod in pperiods:
                if not os.path.isdir(pperiod):
                    continue
                period = pperiod.split('/')[-1]
                parts = period.split('_')
                if len(parts) < 7:
                    newperiod = '{}_{}_{}_{}_{}_{}--{}_{}_{}_{}_{}_{}'.format(period[0:4], int(period[4:6]), int(period[6:8]), period[8:10], period[10:12], period[12:14],
                                                                              period[15:19],int(period[19:21]), int(period[21:23]), period[23:25], period[25:27], period[27:29])
                else:
                    newperiod = period

                if int(newperiod.split('_')[3]) in [6, 7, 8]:
                    date_r_t = '{}_{}_{}'.format(date, cam[1], 1)
                elif int(newperiod.split('_')[3]) in [10, 11]:
                    date_r_t = '{}_{}_{}'.format(date, cam[1], 2)
                elif int(newperiod.split('_')[3]) in [12, 13]:
                    date_r_t = '{}_{}_{}'.format(date, cam[1], 3)
                else:
                    date_r_t = '{}_{}_{}'.format(date, cam[1], 4)

                targetfolder = os.path.join(args.target, date_r_t,'{} {}'.format(cam, date_r_t), newperiod)
                shutil.move(pperiod, targetfolder)
                #nate=1
