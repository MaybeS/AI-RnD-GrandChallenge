ROOT=$1
JUMP=10

echo $ROOT
echo $JUMP

for f in $ROOT/videos/*; do
    SEQ=$(dirname $f)

    if [ -d "$f" ]; then
        cd detector;
        python main.py inference --dataset $ROOT/videos/$SEQ --dest $ROOT/results/$SEQ --classes coco --no-cache --jump $JUMP > /dev/null 2>&1;
        cd ../identifier;
        python main.py --dataset $ROOT/videos/$SEQ --support $ROOT/results/$SEQ/mask_rcnn_coco --support-only --type detection --dest $ROOT/results --no-sequence --jump $JUMP > /dev/null 2>&1;
        cd ..;
        python evaluate.py --root /home/cvlab/datasets/AIGC  --sequence $SEQ
    fi
done
