## Prerequisition
```sh
pip install progressbar2,lxml,opencv-python
```

## Filing videos
Do note this step needs `Python3` for Chinese encoding.

1. `1_convert.py` is written for YuShi Cameras to create folder and structures same as the other system.
```sh
python3 1_convert.py --yushi /path/to/yushi/video/root 
```


2. `2_rename_raw.py` rename all folders in the form of `LXMXCXX` according to `listfile`:
```sh
python3 python 2_rename_raw.py --root /path/to/video/root --listfile /path/to/list/file(default:Camlist.txt)
```

## Rearrange folders
`3_rmfile_new.py` will rearrange previous image folders of structure `cam-date-time` for easier labeling distribution to the structure of `date-lane-time-cam`
```sh
python 3_rmfile_new.py --source /path/to/image/root --target /path/to/target/image/root
```

## Video to Images
`4_video2image_sep.py` will traverse all videos under `video` and crop images to exact same dir structure under `image`
```sh
python 4_video2image_sep.py --video /path/to/video/root --image /path/to/image/root
```

## Image Checking
1. `5_fpscount.py` will help check all images for each video clip to see if the cropping is performed right(this might not be supported by `python3`)
```sh
python 5_fpscount.py --image /path/to/image/root --file /file/name(default:imagecounts.txt)
```

within generated `file` default under `path/to/image/root`, one can estimate whether image numder is right according to its corresponding time period

2. if whole video is cropped incorrectly, use `6_fps.py`:
```sh
python 6_fps.py --video /path/to/video.mp4(ts) --stride 1
```
3. if only part of the video is cropped incorrectly, say after `number` images, use `7_fps_part.py`
```sh
python 7_fps_part.py --video /path/to/video.mp4(ts) --resume number
```
4. Results will be put in a folder sharing the same location and name with video, do check again! If you use `7_fps_part.py`, don't forget to use `8_rename_part.py` to rename all images
```sh
python 8_rename_part.py -folder /path/to/video 
```
5. Manually move this folder to desired location under `/path/to/image/root/`



## Faster-RCNN
`9_demo_batch_new.py` will traverse all images under `image` and create xml files storing all results accordingly.
```sh
cd $Faster-RCNN$/tools
source activate fasterrcnn
python 9_demo_batch_new.py --model ../model/VGGnet_fast_rcnn_iter_70000.ckpt --image /path/to/target/image/root 
```

## Labeling Distribution
Zip according to date and distribute for labeling.


## xml to pedestrains
`10_xml2pedestrain.py` will traverse all xml files collected labeling by `id`and extract pedestrains
```sh
python 10_xml2pedestrain.py --image /path/to/target/image/root --id id --target target/folder/name(default:dataset)
```


## labeling summary
`11_labelsum.py` will summarize the labeling output.
```sh
python 11_labelsum.py --root /path/to/image/root --id id
```
It will output two files under `/path/to/image/root`, namely `counts.txt` and `results.txt`. `counts.txt` tells ids captures by different numbers of cameras, and `results.txt` tells the detailed information for each id.

## Resizing
!IT WILL REPLACE ORIGINAL IMAGE, PLEASE BACK UP FIRST!
`12_resize.py` will resize all images under `path/to/image/root` to a fixed size, default to 64*128
```sh
python 12_resize.py --root /path/to/image/root --id id 
```
This may see to an update for imporved experinece, avoid using for now!
