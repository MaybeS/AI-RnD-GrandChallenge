cd detector;
python main.py inference --dataset /home/cvlab/datasets/AIGC/t1_video/$1 --dest /home/cvlab/datasets/AIGC/results/$1 --weights weights/mask_rcnn_coco.h5 --classes coco --no-cache --jump 10;
cd ../identifier;
python main.py --dataset /home/cvlab/datasets/AIGC/t1_video/$1 --support /home/cvlab/datasets/AIGC/results/$1/mask_rcnn_coco --support-only --type detection --dest /home/cvlab/datasets/AIGC/results --no-sequence --jump 10;
python evaluate.py --root /home/cvlab/datasets/AIGC  --sequence $1

