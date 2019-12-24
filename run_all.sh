ROOT=$1
JUMP=10

echo $ROOT
echo $JUMP

for f in $ROOT/t1_video/*; do
    SEQ=$(basename $f)
    echo $SEQ

    if [ -d "$f" ]; then
        cd detector;
        python main.py inference --dataset $ROOT/t1_video/$SEQ --config configs/config.aigc.json --dest $ROOT/results/$SEQ --classes coco --no-cache --jump $JUMP > /dev/null 2>&1;
        cd ../identifier;
        python main.py --dataset $ROOT/t1_video/$SEQ --support $ROOT/results/$SEQ/mask_rcnn_coco --support-only --type detection --dest $ROOT/results --no-sequence --jump $JUMP > /dev/null 2>&1;
        cd ..;
        python evaluate.py --root $ROOT/results --sequence $SEQ
    fi
done

python combine.py --root $ROOT/results --team_ID $2
