import csv
import json

with open(r'C:\py_git_project_status\mapping_stack.csv', 'r') as map_file:
    mapping_dict = csv.DictReader(map_file)
    map_stack = {}
    for mapping in mapping_dict:
        map_stack[int(mapping['limit'])] = json.loads(mapping['mapping'])


def interpolate(ret_percent, retirement):
    lo = 0
    hi = len(map_stack[retirement])
    print(hi)
    mid = (lo + hi) // 2
    while lo < hi:
        mid = (lo + hi) // 2
        print(mid, ret_percent, map_stack[retirement][mid][1])
        if ret_percent < map_stack[retirement][mid][1]:
            hi = mid
        else:
            lo = mid + 1
    interpolation = map_stack[retirement][mid][0] \
                    + (map_stack[retirement][mid - 1][0] - map_stack[retirement][mid][0]) \
                    / (map_stack[retirement][mid - 1][1] - map_stack[retirement][mid][1]) \
                    * (ret_percent - map_stack[retirement][mid][1])
    return interpolation


def model_stats(ret_percent, retirement, class_percent):
    if retirement == 1:
        return ret_percent
    if retirement > 60:
        return ''
    if ret_percent == 100:
        return 100
    elif ret_percent >= 10.0:
        return interpolate(ret_percent, retirement)
    else:
        return class_percent


print(model_stats(10, 11, 50))
