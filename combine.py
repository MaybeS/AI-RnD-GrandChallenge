import numpy as np
import math
import json
import argparse
from pathlib import Path

parser = argparse.ArgumentParser(description='Combine results to json file')
parser.add_argument('--root', required=False, default='/home/anears/Data/RNDGC', type=str)
parser.add_argument('--team_ID', default='team1', type=str)
parser.add_argument('--gt', type=str)
parser.add_argument('--size', type=int, default=500, required=False)
args = parser.parse_args()

root = Path(args.root)

with open(f't1_res_{args.team_ID}.json', 'w', encoding='utf-8') as f:
    results = {f'{i:05}': {
        'id': i,
        'objects': [5, 0, 0, 3, 0, 0]
    } for i in range(args.size)}

    for josn_file in map(str, root.glob('*.json')):
        index = int(json_file[:9])
        results[f'{index:05}']['objects'] = json.loads(open(json_file).read())['objects']

    json.dump(results, f, ensure_ascii=False, indent='\t')

if args.gt:
    with open(args.gt) as f:
        ground_truths = json.load(f)
    
    preds = {x['id']: x['objects'] for x in results['track1_results']}
    gts = {x['id']: x['objects'] for x  in ground_truths['track1_GT']}

    w = [5, 1, 1, 1, 1, 1]
    al = []

    for k, gt in gts.items():
        p = preds.get(k, [0, 0, 0, 0, 0, 0])
        
        dist = [w[i]*((gt[i]-p[i])**2) for i in range(6)]
        print(k, math.sqrt(sum(dist)), math.sqrt(sum(dist)) > 30 or '')
        al.append(math.sqrt(sum(dist)))

    print('mean', np.array(al).mean())
