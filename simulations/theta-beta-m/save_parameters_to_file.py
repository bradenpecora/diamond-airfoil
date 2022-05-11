import json
import sys

output = {
    'm':sys.argv[2],
    't':sys.argv[3],
    'c':sys.argv[4],
    'alpha':sys.argv[5],
    'stop_time':sys.argv[6],
    'dxa':sys.argv[7]
}

dir_loc = sys.argv[1]

with open("{}/parameters.json".format(dir_loc),'w') as f:
    json.dump(output,f)