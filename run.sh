cd detector;
python main.py inference --dataset /home/cvlab/datasets/AIGC/t1_video/t1_video_00001 --dest /home/cvlab/datasets/AIGC/results/t1_video_00001 --weights weights/mask_rcnn_coco.h5 --classes coco --no-cache --jump 10;
cd ../identifier;
python main.py --dataset /home/cvlab/datasets/AIGC/t1_video/t1_video_00001 --support /home/cvlab/datasets/AIGC/results/t1_video_00001/mask_rcnn_coco --support-only --type detection --dest /home/cvlab/datasets/AIGC/results --no-sequence --jump 10;

