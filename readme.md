## Prerequisition
```sh
pip install progressbar2,lxml,opencv-python
```

## Filing videos
Do note this step needs `Python3` for Chinese encoding.

1. `convert.py` is written for YuShi Cameras to create folder and structures same as the other system.
```sh
python3 convert.py --yushi /path/to/yushi/video/root 
```


2. `rename_raw.py` rename all folders in the form of `LXMXCXX` according to `listfile`:
```sh
python3 python rename_raw.py --root /path/to/video/root --listfile /path/to/list/file(default:Camlist.txt)
```


## Video to Images
`video2image_sep.py` will traverse all videos under `video` and crop images to exact same dir structure under `image`
```sh
python video2image_sep.py --video /path/to/video/root --image /path/to/image/root
```

## Image Checking
1. Check all images for each video clip to see if the cropping is performed right
2. if whole video is cropped incorrectly, use `fps.py`:
```sh
python fps.py --video /path/to/video.mp4(ts) --stride 1
```
3. if only part of the video is cropped incorrectly, say after `number` images, use `fps_part.py`
```sh
python fps_part.py --video /path/to/video.mp4(ts) --resume number
```
4. Results will be put in a folder sharing the same location and name with video, do check again! If you use `fps_part.py`, don't forget to use `renaming.py` to rename all images
```sh
python renaming.py -folder /path/to/video 
```
5. Manually move this folder to desired location under `/path/to/image/root/`

## Rearrange folders
`rmfile.py` will rearrange previous image folders structure for easier labeling distribution
```sh
python rmfile.py --source /path/to/image/root --target /path/to/target/image/root
```

## Faster-RCNN
`demo_batch_new.py` will traverse all images under `image` and create xml files storing all results accordingly.
```sh
cd $Faster-RCNN$/tools
python demo_batch_new.py --model ../model/VGGnet_fast_rcnn_iter_70000.ckpt --image /path/to/target/image/root 
```

## Labeling Distribution
Zip according to date and distribute for labeling.


## xml to pedestrains
`xml2pedestrain.py` will traverse all xml files collected labeling by `id`and extract pedestrains
```sh
python xml2pedestrain.py --image /path/to/target/image/root --id id --target target/folder/name(default:dataset)
```

