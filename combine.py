import json
import argparse
from pathlib import Path

parser = argparse.ArgumentParser(description='Combine results to json file')
parser.add_argument('--root', required=False, default='/home/anears/Data/RNDGC', type=str)
parser.add_argument('--team_ID', default='team1', type=str)
args = parser.parse_args()

root = Path(args.root)

with open(f't1_res_{args.team_ID}.json', 'w', encoding='utf-8') as f:
    json.dump({
        'track1_results': [json.loads(open(json_file).read()) for json_file in map(str, root.glob('*.json'))]
    }, f, ensure_ascii=False, indent='\t')

