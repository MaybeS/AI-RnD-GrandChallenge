ROOT=$1
JUMP=10

echo $ROOT
echo $JUMP

for f in $ROOT/videos/*; do
    echo $f
    if [ -d "$f" ]; then
        cd detector;
        python main.py inference --dataset $ROOT/videos/$f --dest $ROOT/results/$f --classes coco --no-cache --jump $JUMP > /dev/null 2>&1;
        cd ../identifier;
        python main.py --dataset $ROOT/videos/$f --support $ROOT/results/$f/mask_rcnn_coco --support-only --type detection --dest $ROOT/results --no-sequence --jump $JUMP > /dev/null 2>&1;
        cd ..;
        python evaluate.py --root /home/cvlab/datasets/AIGC  --sequence $f
    fi
done
