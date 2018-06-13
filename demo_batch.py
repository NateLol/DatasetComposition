#!/usr/bin/env python
# coding:utf-8

import _init_paths
import tensorflow as tf
import progressbar
from fast_rcnn.config import cfg
from fast_rcnn.test import im_detect
from fast_rcnn.nms_wrapper import nms
from utils.timer import Timer
import matplotlib.pyplot as plt
import numpy as np
import os, sys, cv2
import glob
import argparse
from networks.factory import get_network

from lxml.etree import Element, SubElement, tostring
import pprint
from xml.dom.minidom import parseString

CLASSES = ('__background__',
           'aeroplane', 'bicycle', 'bird', 'boat',
           'bottle', 'bus', 'car', 'cat', 'chair',
           'cow', 'diningtable', 'dog', 'horse',
           'motorbike', 'person', 'pottedplant',
           'sheep', 'sofa', 'train', 'tvmonitor')


#CLASSES = ('__background__','person','bike','motorbike','car','bus')
#def vis_detections模块：画出测试图片的bounding boxes
# class_name 为类别名称，在前面定义的 CLASSES 中
#dets为非极大值抑制后的bbox和score的数组
# thresh是最后score的阈值,高于该阈值的候选框才会被画出来
def vis_detections(im, im_name, class_name, dets,ax, thresh=0.5):
    """Draw detected bounding boxes."""
    #选取候选框score大于阈值的dets
    inds = np.where(dets[:, -1] >= thresh)[0]
    seps = im_name.split('/')
    if len(inds) == 0:
        return
    with open('{}.xml'.format(im_name[0:-4]), 'w') as f:
        #IMAGE FOLDER NAME PATH


        node_root = Element('annotation')

        node_folder = SubElement(node_root, 'folder')
        node_folder.text = seps[-2]

        node_filename = SubElement(node_root, 'filename')
        node_filename.text = seps[-1]

        node_filepath = SubElement(node_root, 'path')
        node_filepath.text = im_name

        node_size = SubElement(node_root, 'size')
        node_width = SubElement(node_size, 'width')
        node_width.text = str(im.shape[1])

        node_height = SubElement(node_size, 'height')
        node_height.text = str(im.shape[0])

        node_depth = SubElement(node_size, 'depth')
        node_depth.text = str(im.shape[2])

        for i in inds:
            bbox = dets[i, :4]
            score = dets[i, -1]

            node_object = SubElement(node_root, 'object')
            node_name = SubElement(node_object, 'name')
            node_name.text = 'person'
            node_difficult = SubElement(node_object, 'difficult')
            node_difficult.text = '0'

            node_bndbox = SubElement(node_object, 'bndbox')
            node_xmin = SubElement(node_bndbox, 'xmin')
            node_xmin.text = str(int(bbox[0]+1))
            node_ymin = SubElement(node_bndbox, 'ymin')
            node_ymin.text = str(int(bbox[1]+1))
            node_xmax = SubElement(node_bndbox, 'xmax')
            node_xmax.text = str(int(bbox[2]+1))
            node_ymax = SubElement(node_bndbox, 'ymax')
            node_ymax.text = str(int(bbox[3]+1))



            #ax.add_patch(
            #plt.Rectangle((bbox[0], bbox[1]),
            #              bbox[2] - bbox[0],
             #             bbox[3] - bbox[1], fill=False,
            #              edgecolor='red', linewidth=3.5)
            #)
            #ax.text(bbox[0], bbox[1] - 2,
            #    '{:s} {:.3f}'.format(class_name, score),
            #    bbox=dict(facecolor='blue', alpha=0.5),
            #    fontsize=14, color='white')

            #ax.set_title(('{} detections with '
             #     'p({} | box) >= {:.1f}').format(class_name, class_name,
             #                                     thresh),
             #     fontsize=14)

        xml = tostring(node_root, pretty_print=True)  # 格式化显示，该换行的换行

        f.write(xml)
        #
    #plt.axis('off')
    #plt.tight_layout()
    #plt.draw()


def demo(sess, net, image_name):
    """Detect object classes in an image using pre-computed object proposals."""
    #def demo模块:对测试图片提取预选框,并进行非极大值抑制,然后调用def vis_detections 画矩形框
    #参数：net 测试时使用的网络结构
    #image_name:图片名称
    # Load the demo image
    #im_file = os.path.join(cfg.DATA_DIR, 'demo', image_name)
    #im_file = os.path.join('/home/corgi/Lab/label/pos_frame/ACCV/training/000001/',image_name)
    # 参数im为测试图片
    im = cv2.imread(image_name)
    if im is None:
        print('image is none and removing it from the folder')
        os.remove(image_name)
        return
    # Detect all object classes and regress object bounds
    #timer = Timer()
    #timer.tic()
    scores, boxes = im_detect(sess, net, im)
    #timer.toc()
    #print ('Detection took {:.3f}s for 's
    #       '{:d} object proposals').format(timer.total_time, boxes.shape[0])


    # Visualize detections for each class
    # python-opencv 中读取图片默认保存为[w,h,channel](w,h顺序不确定)
    # 其中 channel：BGR 存储，而画图时，需要按RGB格式，因此此处作转换。
    im = im[:, :, (2, 1, 0)]
    #fig, ax = plt.subplots(figsize=(12, 12))
    #ax.imshow(im, aspect='equal')
    ax=None
    CONF_THRESH = 0.8
    NMS_THRESH = 0.3
    for cls_ind, cls in enumerate(CLASSES[1:]):
        # see if cls is 'person' continue,
        if cls != 'person':
            continue

        cls_ind += 1 # because we skipped background
        cls_boxes = boxes[:, 4*cls_ind:4*(cls_ind + 1)]
        cls_scores = scores[:, cls_ind]
        dets = np.hstack((cls_boxes,
                          cls_scores[:, np.newaxis])).astype(np.float32)
        keep = nms(dets, NMS_THRESH)
        dets = dets[keep, :]
        vis_detections(im, image_name, cls, dets, ax, thresh=CONF_THRESH)

def parse_args():
    """Parse input arguments."""
    parser = argparse.ArgumentParser(description='Faster R-CNN demo')
    parser.add_argument('--gpu', dest='gpu_id', help='GPU device id to use [0]',
                        default=0, type=int)
    parser.add_argument('--cpu', dest='cpu_mode',
                        help='Use CPU mode (overrides --gpu)',
                        action='store_true')
    parser.add_argument('--net', dest='demo_net', help='Network to use [vgg16]',
                        default='VGGnet_test')
    parser.add_argument('--model', dest='model', help='Model path',
                        default='../model/VGGnet_fast_rcnn_iter_70000.ckpt')
    parser.add_argument('--root', dest='root', help='Path to root dir to run on', default='../data/demo')
    parser.add_argument('--from', dest='start_from', help='continue from which folder index', default=0, type=int)
    parser.add_argument('--history', dest='history', help='a file to help remember processing history', default='history.txt')

    args = parser.parse_args()

    return args


if __name__ == '__main__':
    cfg.TEST.HAS_RPN = True  # Use RPN for proposals

    args = parse_args()

    if args.model == ' ':
        raise IOError(('Error: Model not found.\n'))

    # init session
    sess = tf.Session(config=tf.ConfigProto(allow_soft_placement=True))
    # load network
    net = get_network(args.demo_net)
    # load model
    saver = tf.train.Saver(write_version=tf.train.SaverDef.V1)
    saver.restore(sess, args.model)
    print('\n\nLoaded network {:s}'.format(args.model))

    print('Running faster rcnn on image from folder {:s}'.format(args.root))
    count = 1
    if not os.path.exists(os.path.join(args.root, args.history)):
        with open(os.path.join(args.root, args.history),'w') as f:
            pass
    try:
        with open(os.path.join(args.root, args.history), 'r') as f:
            lines = f.readlines()
            args.start_from = int(lines[-1])
    except Exception as e:
        print(e)
    finally:
        print('continue from {:d}'.format(args.start_from))

    folders = glob.glob(os.path.abspath(os.path.join(args.root, './*')))
    folders.sort()
    idx=0
    for folder in folders:
        if not os.path.isdir(folder):
            continue
        subfolders = glob.glob(folder+'/*')
        subfolders.sort()

        for subfolder in subfolders:
            print(subfolder)
            if not os.path.isdir(subfolder):
                continue

            subsubfolders = glob.glob(subfolder+'/*')
            subsubfolders.sort()
            for subsubfolder in subsubfolders:
                if not os.path.isdir(subsubfolder):
                    continue
                if count < args.start_from:
                    count = count + 1
                    continue
                print('----------------------------------------------------------')
                print('Processing {:s}'.format(subsubfolder))
                im_names = glob.glob(subsubfolder+'/*jpg')
                im_names.sort()
                try:
                    for i in progressbar.progressbar(range(len(im_names))):
                        im_name = im_names[i]
                        im_name = os.path.abspath(im_name)
                        idx = i+1
                        demo(sess, net, im_name)
                except KeyboardInterrupt:
                    print('Interrupted, saved checkpoint to {:s}'.format(args.history))
                    exit()
                finally:
                    with open(os.path.join(args.root, args.history), 'a') as f:
                        f.write(subsubfolder+'\n')
                        f.write('{:d}/{:d}\n'.format(idx, len(im_names)))
                        f.write('{:d}\n'.format(count))
                    count = count + 1
