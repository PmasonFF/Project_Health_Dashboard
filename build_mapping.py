import csv
import json
from random import *


def get_mapping(retirement):
    sub_count = 500000
    step = int(sub_count * retirement / 100)
    subject_list = [0 for _ in range(0, sub_count)]
    classifications = 0
    retired = 0
    mapping = []
    while True:
        classifications += 1
        x = randint(1, len(subject_list))
        subject_list[x - 1] += 1
        if subject_list[x - 1] == retirement:
            del subject_list[x - 1]
            if len(subject_list) == 0:
                break
            retired += 1
        if classifications % step == 0:
            if retired / sub_count >= .1:
                mapping.append((round(classifications / (sub_count * retirement) * 100, 2),
                                round(retired / sub_count * 100, 2)))
    mapping.append((100, 100))
    return mapping


ret_limit_options = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 16, 15, 17, 20, 21, 25, 30, 31, 40, 41, 50, 60]

with open(r'C:\py_git_project_status\mapping_stack_16.csv', 'w', newline='') as out_map_file:
    fieldnames = ['limit', 'mapping']
    writer = csv.DictWriter(out_map_file, fieldnames=fieldnames)
    writer.writeheader()
    for limit in ret_limit_options:
        print(limit)
        writer.writerow({'limit': limit, 'mapping': json.dumps(get_mapping(limit))})
