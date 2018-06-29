import os, glob
from lxml import etree
import argparse,cv2, progressbar


def get_shapes(bndbox):
    xmin = int(bndbox.find('xmin').text)
    ymin = int(bndbox.find('ymin').text)
    xmax = int(bndbox.find('xmax').text)
    ymax = int(bndbox.find('ymax').text)
    points =[xmin, xmax, ymin, ymax]
    return points


def cutting(im, shapes, name):
    c=0
    for shape in shapes:
        im_tmp = im[shape[2]:shape[3], shape[0]:shape[1]]
        cv2.imwrite(name+str(c)+'.jpg', im_tmp)
        c=c+1


def cutout(xml_name, id, folderpath):
    im = cv2.imread(xml_name[0:-3]+'jpg')
    if im is None:
        return
    tree = etree.parse(xml_name)
    path = tree.find('path').text
    if '/' in path:
        sep = '/'
    else:
        sep = '\\'
    cam = path.split(sep)[-3]
    date = path.split(sep)[-2]
    image = path.split(sep)[-1]
    objects = tree.findall('object')
    for object in objects:
        name = object.find('name').text
        #print(name)
        if not name[0] == id:
            continue
        bndbox = object.find('bndbox')
        shape = get_shapes(bndbox)
        if None in shape:
            return
        im_tmp = im[shape[2]:shape[3], shape[0]:shape[1]]
        id_folder = os.path.join(folderpath, name)
        if not os.path.exists(id_folder):
            os.mkdir(id_folder)
        index = len(glob.glob(id_folder+'{}*jpg'.format(sep)))
        filename = os.path.join(id_folder, '{}_{}_{}_{:03d}.jpg'.format(cam, date, image.split('.')[0], index))
        cv2.imwrite(filename, im_tmp)
#    cutting(im, shapes, 'test')


def parse_args():
    """Parse input arguments."""
    parser = argparse.ArgumentParser(description='Read xml files and crop pedestrian images accordingly')
    parser.add_argument('--xmlfile', dest='xmlfile', help='xml file path',
                        default=' ')
    parser.add_argument('--image', dest='root', help='Path to root dir to run on', default='../data/demo')
    parser.add_argument('--id', dest='id', required=True)
    parser.add_argument('--target', dest='target', default='dataset')
    args = parser.parse_args()
    return args

def main(root, id, target):
    targetfolder = os.path.join(root, target)
    if not os.path.exists(targetfolder):
        os.makedirs(targetfolder)
    cams = glob.glob(os.path.join(root, '*'))
    cams.sort()
    for cam in cams:
        if not os.path.isdir(cam):
            continue
        if cam.split('/')[-1] == target:
            continue
        periods = glob.glob(os.path.join(cam, '*'))
        periods.sort()
        for period in periods:
            if not os.path.isdir(period):
                continue
            print('Now processing: {}'.format(period))
            xmls = glob.glob(os.path.join(period, '*.xml'))
            xmls.sort()
            for i in progressbar.progressbar(range(len(xmls))):
                cutout(xmls[i], id, targetfolder)


if __name__ =='__main__':
    args = parse_args()
    main(args.root, args.id, args.target)
