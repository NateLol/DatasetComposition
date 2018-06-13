import argparse
import glob, os


def read_list(filename):
    with open('Camlist.txt', 'r') as f:
        dicts={}
        lines = f.readlines()
        for line in lines:
            dicts[line.split(' ')[0]] = line.split(' ')[1].replace('\n','')
        return dicts



def parse_args():
    """Parse input arguments."""
    parser = argparse.ArgumentParser(description='folder renaming')
    parser.add_argument('--root', dest='root', required=True, help='renaming the folders to defined names',
                        default='')
    parser.add_argument('--listfile', dest='listfile', help='the pre-defined names for all cameras', default='Camlist.txt')

    args = parser.parse_args()

    return args

if __name__ == '__main__':
    args = parse_args()
    dictionary = read_list(args.listfile)


    folders = glob.glob(os.path.abspath(args.root+'/*'))
    folders.sort()
    for folder in folders:
        if not os.path.isdir(folder):
            continue

        print('Now processing folder {:s}'.format(folder.split("/")[-1]))
        foldername = folder.split('/')[-1]
        if '-' in foldername:
            keyname = foldername.split('-')[0]
        elif ' ' in foldername:
            keyname = foldername.split(' ')[0]
        elif '_' in foldername:
            keyname = foldername.split('_')[0]
        else:
            keyname = foldername.split('1')[0]
            #strtmp = repr(foldername)[1:-1].rstrip()
        newname = dictionary.get(keyname, None)
        if newname == None:
            continue
        os.rename(folder, folder.replace(foldername, newname))


