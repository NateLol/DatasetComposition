import os, glob,shutil


def parse_args():
    """Parse input arguments."""
    parser = argparse.ArgumentParser(description='Renaming images cropped with different stride')
    parser.add_argument('--folder', dest='folder',required=True, help='image folder to be renamed')

    args = parser.parse_args()

    return args


if __name__ == "__main__":
    args = parse_args()
    files = glob.glob(os.path.join(args.folder,'*.jpg'))
    files.sort()
    for i in range(len(files)):
        os.rename(files[i], files[i][:-10]+'{:06d}.jpg'.format(i))
