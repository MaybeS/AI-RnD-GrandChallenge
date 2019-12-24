import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd


def compute_iou(boxA, boxB):
	xA = max(boxA[0], boxB[0])
	yA = max(boxA[1], boxB[1])
	xB = min(boxA[0] + boxA[2] - 1, boxB[0] + boxB[2] - 1)
	yB = min(boxA[1] + boxA[3] - 1, boxB[1] + boxB[3] - 1)

	interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)

	boxAArea = boxA[2] * boxA[3]
	boxBArea = boxB[2] * boxB[3]

	iou = interArea / float(boxAArea + boxBArea - interArea)

	return iou


def main(args):
    target = Path(args.root)

    # tracking = target.joinpath(f'{args.sequence}.txt')
    # detections = list(sorted(target.joinpath(f'{args.sequence}/mask_rcnn_coco').glob('*.txt')))
    tracking = target.joinpath('img1.txt')
    detections = list(sorted(target.joinpath(f'mask_rcnn_coco').glob('*.txt')))

    dets = np.empty((0, 7))
    for p, detection in enumerate(detections, 1):
        det = pd.read_csv(str(detection), header=None).values
        det[:, -2:] -= det[:, -4:-2]
        dets = np.concatenate((dets, np.hstack((np.full((np.size(det, 0), 1), p), det))))

    tracker = pd.read_csv(str(tracking), header=None).values[:, :-5]
    init_frame = np.zeros(int(np.unique(tracker[:, 1]).max()) + 1)

    klass_map = {
        1: 'person',
        2: 'bicycle',
        3: 'car',
        4: 'motorcycle',
        6: 'car',
        8: 'cark',
        11: 'firehydrant',
    }
    klass_counts = {k: 0 for k in set(klass_map.values())}

    for frame, iid, *box in tracker:
        if not init_frame[int(iid)]:
            init_frame[int(iid)] = int(frame)

            max_iou, keep = 0, 0
            for f, klass, conf, *bbox in dets[dets[:, 0] == int(frame)]:
                iou = compute_iou(box, bbox)
                
                if iou > max_iou:
                    max_iou = iou
                    keep = klass
            
            try:
                klass_counts[klass_map[int(keep)]] += 1
            except:
                pass

    # json.dump({
    #     'id': int(args.sequence[9:]),
    #     'objects': [klass_counts.get(k, 0) for k in ['person', 'fire', 'firehydrant', 'car', 'bicycle', 'motorcycle']]
    # }, open(target.joinpath(f'{args.sequence}.json'), 'w'))
    json.dump({
        'id': 0,
        'objects': [klass_counts.get(k, 0) for k in ['person', 'fire', 'firehydrant', 'car', 'bicycle', 'motorcycle']]
    }, open(target.joinpath('result.json'), 'w'))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Train Mask R-CNN to detect webtoon characters.')
    parser.add_argument('--root', required=False, default='/home/jiun/datasets/AIGC', type=str)
    parser.add_argument('--sequence', required=False, type=str)
    arguments = parser.parse_args()
    main(arguments)
