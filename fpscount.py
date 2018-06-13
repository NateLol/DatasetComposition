import argparse,os,shutil


def parse_args():
    """Parse input arguments."""
    parser = argparse.ArgumentParser(description='Video cropping to images with exact same dirs')
    parser.add_argument('--image', dest='image', required=True, help='image root path',
                        default='')
    parser.add_argument('--file',dest='file', help='the stride by which frames are cropped', default='imagecounts.txt')

    args = parser.parse_args()
    return args


def find_file(args, dirname, files):
    if len(files) != 0 and '.' in files[0]:
        with open(filepath,'a') as f:
            f.write('{} has {} images\n'.format(dirname, len(files)))




if __name__ == '__main__':
    args = parse_args()
    filepath = os.path.join(args.image, args.file)
    if os.path.exists(filepath):
        os.remove(filepath)
    os.path.walk(args.image, find_file, filepath)
