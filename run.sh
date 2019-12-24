SEQUENCE=$1
JUMP=10

# detector
cd detector
python main.py inference --dataset $SEQUENCE/img1 --config configs/config.aigc.json --dest $SEQUENCE/results --classes coco --no-cache --jump $JUMP > /dev/null 2>&1;

# identifier
cd ../identifier
python main.py --dataset $SEQUENCE/img1 --support $SEQUENCE/results/mask_rcnn_coco --support-only --type detection --dest $SEQUENCE/results --no-sequence --jump $JUMP > /dev/null 2>&1;

cd ..
python evaluate.py --root $SEQUENCE/results

