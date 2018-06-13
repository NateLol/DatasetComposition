#!/usr/bin/env python
# coding:utf-8

import _init_paths
import tensorflow as tf
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

def vis_detections(im, im_name, class_name, dets,ax, thresh=0.5):
    """Draw detected bounding boxes."""
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

    # Load the demo image
    #im_file = os.path.join(cfg.DATA_DIR, 'demo', image_name)
    #im_file = os.path.join('/home/corgi/Lab/label/pos_frame/ACCV/training/000001/',image_name)
    im = cv2.imread(image_name)


    # Detect all object classes and regress object bounds
    timer = Timer()
    timer.tic()
    scores, boxes = im_detect(sess, net, im)
    timer.toc()
    print('Detection took {:.3f}s for '
           '{:d} object proposals').format(timer.total_time, boxes.shape[0])


    # Visualize detections for each class
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
                        default=' ')
    parser.add_argument('--folder', dest='folder', help='Path to folder that needs to run on', default='../data/demo')

    args = parser.parse_args()

    return args
if __name__ == '__main__':
    cfg.TEST.HAS_RPN = True  # Use RPN for proposals

    args = parse_args()

    if args.model == ' ':
        raise IOError(('Error: Model not found.\n'))

    print('Runing faster rcnn on image from folder {:s}'.format(args.folder))
    # init session
    sess = tf.Session(config=tf.ConfigProto(allow_soft_placement=True))
    # load network
    net = get_network(args.demo_net)
    # load model
    saver = tf.train.Saver(write_version=tf.train.SaverDef.V1)
    saver.restore(sess, args.model)
   
    #sess.run(tf.initialize_all_variables())

    print('\n\nLoaded network {:s}'.format(args.model))

    im_names = glob.glob(args.folder+'/*jpg')


    for im_name in im_names:
        im_name = os.path.abspath(im_name)
        #print('predicting for {:s}'.format(im_name))
        demo(sess, net, im_name)

    #plt.show()

