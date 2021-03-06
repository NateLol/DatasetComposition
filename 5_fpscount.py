import argparse,os,shutil,glob


def parse_args():
    """Parse input arguments."""
    parser = argparse.ArgumentParser(description='Counting images for each video clip')
    parser.add_argument('--image', dest='image', required=True, help='image root path',
                        default='')
    parser.add_argument('--file',dest='file', help='the file storing the results', default='imagecounts.txt')

    args = parser.parse_args()
    return args


def find_file(args, dirname, files):
    files.sort()
    if len(files) != 0 and 'jpg' in files[0]:
        with open(args,'a') as f:
            f.write('{} has {} images\n'.format(dirname, len(glob.glob(os.path.join(dirname,'*.jpg')))))


def main(image, file):
    filepath = os.path.join(image, file)
    if os.path.exists(filepath):
        os.remove(filepath)
    os.path.walk(image, find_file, filepath)

if __name__ == '__main__':
    args = parse_args()
    main(args.image, args.file)

