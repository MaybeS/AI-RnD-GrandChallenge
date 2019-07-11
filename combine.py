import numpy as np
import math
import json
import argparse
from pathlib import Path

parser = argparse.ArgumentParser(description='Combine results to json file')
parser.add_argument('--root', required=False, default='/home/anears/Data/RNDGC', type=str)
parser.add_argument('--team_ID', default='team1', type=str)
parser.add_argument('--gt', type=str)
args = parser.parse_args()

root = Path(args.root)

with open(f't1_res_{args.team_ID}.json', 'w', encoding='utf-8') as f:
    results = {
        'track1_results': [json.loads(open(json_file).read()) for json_file in map(str, root.glob('*.json'))]
    }
    json.dump(results, f, ensure_ascii=False, indent='\t')

if args.gt:
    with open(args.gt) as f:
        ground_truths = json.load(f)
    
    preds = results['track1_results']
    gts = ground_truths['track1_GT']

    w = [5, 1, 1, 1, 1, 1]
    al = []

    for idx in range(len(gts)):
        gt = gts[idx]['objects']

        try:
            p = preds[idx]['objects']
        except:
            p = [0, 0, 0, 0, 0, 0]

        dist = [w[i]*((gt[i]-p[i])**2) for i in range(6)]
        print(gts[idx]['id'], math.sqrt(sum(dist)), math.sqrt(sum(dist)) > 30 or '')
        al.append(math.sqrt(sum(dist)))

    print('mean', np.array(al).mean())
