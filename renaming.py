import os,argparse
import glob
from lxml import etree
from os.path import exists

folder='/home/jane/Desktop/dataset/images/'

def parse_args():
    """Parse input arguments."""
    parser = argparse.ArgumentParser(description='Faster R-CNN demo')
    parser.add_argument('--folder', dest='folder',required=True, help='GPU device id to use [0]')

    args = parser.parse_args()

    return args


if __name__ == '__main__':
	args = parse_args()
	filepath = glob.glob(args.folder + '*.jpg')
	for file in filepath:
		name = file.split('/')[-1]
		number = name.split('.')[-2]
		count = int(number)
		os.rename(folder + number + '.jpg', os.path.join(folder, '{:06d}.jpg'.format(count)))
		if not exists(folder + number + '.xml'):
			continue;
		os.rename(folder + number + '.xml', os.path.join(folder, '{:06d}.xml'.format(count)))
		#handle the file name in xml
		tree = etree.parse(os.path.join(folder, '{:06d}.xml'.format(count)))
		if not tree.find('filepath') ==None:
			tree.find('filepath').tag='path'
		path= tree.xpath('//path')
		path[0].text=os.path.join(folder,'{:06d}.jpeg'.format(count));
		filename=tree.xpath('//filename')
		filename[0].text='{:06d}.jpg'.format(count)
		with open(os.path.join(folder, '{:06d}.xml'.format(count)),'w') as f:
			f.write(etree.tostring(tree))

