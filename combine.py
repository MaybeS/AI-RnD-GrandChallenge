import glob
import argparse
import json

parser = argparse.ArgumentParser(description='Combine results to json file')
parser.add_argument('--root', required=False, default='/home/anears/Data/RNDGC', type=str)
parser.add_argument('--team_ID', default='team1', type=str)
arguments = parser.parse_args()

results = {"track1_results":[]}
for jsonPath in sorted(glob.glob('*.json')):
	res = json.loads(open(jsonPath).read())
	results["track1_results"].append(res)

with open('t1_res_'+arguments.team_ID+'.json','w', encoding='utf-8') as fp:
	json.dump(results, fp, ensure_ascii=False, indent='\t')