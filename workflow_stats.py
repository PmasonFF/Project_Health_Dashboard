# -*- coding: utf-8 -*-
"""
    Requires panoptes-client and (on Python 2) futures.
    pip install panoptes-client futures
"""
import argparse
import textwrap
import csv
import json
import os
import io
import operator
import sys
from datetime import datetime
import panoptes_client
from panoptes_client import Panoptes, Project
import gspread
from oauth2client.service_account import ServiceAccountCredentials
# from gspread_formatting import *


def output(location, build):
    with io.open(location, 'w', encoding='cp1252', newline='') as out_file:
        out_file.write(build)
    return


with open(r'C:\py_git_project_status\mapping_stack.csv', 'r') as map_file:
    mapping_dict = csv.DictReader(map_file)
    map_stack = {}
    for mapping in mapping_dict:
        map_stack[int(mapping['limit'])] = json.loads(mapping['mapping'])


def interpolate(ret_percent, retirement):
    lo = 0
    hi = len(map_stack[retirement])
    mid = (lo + hi) // 2
    while lo < hi:
        mid = (lo + hi) // 2
        if ret_percent < map_stack[retirement][mid][1]:
            hi = mid
        else:
            lo = mid + 1
    interpolation = int(map_stack[retirement][mid][0]
                        + (map_stack[retirement][mid - 1][0] - map_stack[retirement][mid][0])
                        / (map_stack[retirement][mid - 1][1] - map_stack[retirement][mid][1])
                        * (ret_percent - map_stack[retirement][mid][1]) + .5)

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


parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    fromfile_prefix_chars='@',
    description=textwrap.dedent("""
            This script produces a listing of the workflow details for projects 
            and workflows which are launched and currently live. 
            It requires the panoptes_client to be installed, and if run with 
            Python 2.7, it also requires the package futures as well.          
            It accepts an optional path and filename for a location to save the 
            output in a csv file format otherwises uses workflow_stats_output.csv
            in the current working directory. 
            It assumes the user's zooniverse users_name and password are set up
            in the operating system's environmental variables. Login is actually not
            required for public launched project stats. If credentials are not set-up,
            replace line 70 with Panoptes.connect(username= '', password='')            
            NOTE: You may use a file to hold the command-line arguments like:
            @/path/to/args.txt."""))

parser.add_argument('--save_to', '-s', required=False, default='workflow_stats_output.csv',
                    help="""An optional file name (including extension ".csv"
                    where the output will be saved in csv format. Give the full
                    path (from the directory where this script is run, or from the
                    root directory) and the file name. 
                    example -s some_path\workflow_stats_output.csv """)
args = parser.parse_args()

save_to = args.save_to
build_file = ''
build_part = "Detailed Workflow Stats for all live launched projects." + '\n' + '\n'

with open(r'C:\py_git_project_status\activity_stack.csv', 'r') as activity_file:
    activity = csv.DictReader(activity_file)
    stack = {}
    date_time = ''
    for act in activity:
        if act['key'] != 'datetime':
            stack[act['key']] = json.loads(act['value'])
        else:
            date_time = str(act['value'])

# get live launched project list
Panoptes.connect(username=os.environ['User_name'], password=os.environ['Password'])
all_projects = Project.where(launch_approved=True)
project_listing = []
for project in all_projects:
    if project.state == 'live':
        try:
            project_listing.append([int(project.id), project.subjects_count,
                                    project.retired_subjects_count, project.classifications_count,
                                    project.activity, int(project.completeness * 100 + .5),
                                    project.state, project.display_name])
        except panoptes_client.panoptes.PanoptesAPIException:
            print(str(sys.exc_info()[1]))

project_listing.sort(key=operator.itemgetter(0))

if str(datetime.utcnow())[8:10] != date_time[8:10]:
    for line in project_listing:
        new = []
        try:
            if len(stack[str(line[0])]) >= 14:
                new = stack[str(line[0])][-13:]
            else:
                new = stack[str(line[0])][:]
        except KeyError:
            pass
        new.append(int(line[4]))
        stack[str(line[0])] = new[:]
    date_time = str(datetime.utcnow())[:16]

    with io.open(r'C:\py_git_project_status\activity_stack.csv', 'w', newline='') as out_act_file:
        fieldnames = ['key', 'value']
        writer = csv.DictWriter(out_act_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({'key': 'datetime', 'value': date_time})
        for item in list(stack.keys()):
            writer.writerow({'key': item, 'value': json.dumps(stack[item])})
# ___________________________________________________________________________________________________________________

build_part += "All live launched projects and active workflows" + '\n' + '\n'
build_file += build_part

i = 0
for line in project_listing:
    build_part = ''
    try:
        avg_act = int((sum(stack[str(line[0])]) / len(stack[str(line[0])])) + .5)
    except KeyError:
        avg_act = line[4]
    try:
        build_part += "{:<12},{:<13},{:<16},{:<25},{:<22},{:<19},{:<21},{:<19},{:<21},{:<22},{}".format(
            'Project_id',
            'Workflow_id',
            'Subjects_count',
            'Retired_subjects_count',
            'Classifications_count',
            'Project activity',
            '14 day avg. activity',
            'Retirement_limit',
            'Class_Completeness',
            'Retired_Completeness',
            'Linearized completeness',
            'Display_name') + '\n'
        build_overall = "{:<12},{:<13},{:<16},{:<25},{:<22},{:<19},{:<21},{:<19},{:<21},{:<22},{:<24},{}".format(
            str(line[0]),
            'Over_all',
            str(line[1]),
            str(line[2]),
            str(line[3]),
            str(line[4]),
            str(avg_act),
            '',
            '',
            str(line[5]),
            '',
            json.dumps(str(line[7]), ensure_ascii=False)) + '\n'

        project = Project.find(str(line[0]))
        for wrkflw in project.links.workflows:
            if wrkflw.active == 1:
                try:
                    ret_limit = wrkflw.retirement['options']['count']
                    if wrkflw.classifications_count < (wrkflw.subjects_count * ret_limit):
                        class_comp = int(wrkflw.classifications_count / (wrkflw.subjects_count * wrkflw.retirement[
                            'options']['count']) * 100 + .5)
                    else:
                        class_comp = 100
                except KeyError:
                    ret_limit = wrkflw.retirement[
                        'options']
                    class_comp = ''
                if wrkflw.subjects_count > 0:
                    ret_comp = int(wrkflw.retired_set_member_subjects_count / wrkflw.subjects_count * 100 + .5)
                    linearized = model_stats(ret_comp, ret_limit, class_comp)
                else:
                    ret_comp = ''
                    linearized = ''
                if wrkflw.subjects_count == line[1]:
                    build_part += "{:<12},{:<13},{:<16},{:<25},{:<22},{:<19},{:<21}," \
                                  "{:<19},{:<21},{:<22},{:<24},{}".format(str(line[0]),
                                                                          wrkflw.id,
                                                                          wrkflw.subjects_count,
                                                                          wrkflw.retired_set_member_subjects_count,
                                                                          wrkflw.classifications_count,
                                                                          str(line[4]),
                                                                          str(avg_act),
                                                                          str(ret_limit),
                                                                          str(class_comp),
                                                                          str(ret_comp),
                                                                          str(linearized),
                                                                          json.dumps((str(
                                                                              line[7])) + ' - ' + wrkflw.display_name),
                                                                          ensure_ascii=False) + '\n'
                else:
                    build_part += build_overall
                    build_overall = ''
                    build_part += "{:<12},{:<13},{:<16},{:<25},{:<22},{:<19},{:<21}," \
                                  "{:<19},{:<21},{:<22},{:<24},{}".format(str(line[0]),
                                                                          wrkflw.id,
                                                                          wrkflw.subjects_count,
                                                                          wrkflw.retired_set_member_subjects_count,
                                                                          wrkflw.classifications_count,
                                                                          '',
                                                                          '',
                                                                          str(ret_limit),
                                                                          str(class_comp),
                                                                          str(ret_comp),
                                                                          str(linearized),
                                                                          json.dumps(wrkflw.display_name,
                                                                                     ensure_ascii=False)) + '\n'

    except panoptes_client.panoptes.PanoptesAPIException:
        build_part += str(sys.exc_info()[1]) + '\n'
    build_part += '\n'
    print(build_part)
    build_file += build_part
output(save_to, build_file)
# ____________________________________________________________________________________________________________________
# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

content = open(save_to, 'r', encoding='latin-1').read()
client.import_csv('1JOzKlzfCMBVzvbxoyvcY8P3GyfPzZF5dkKR8STWHx4E', content)
sheet = client.open("workflow_stats_output").sheet1
sheet.insert_row([''], 1)
sheet.insert_row([''], 2)
sheet.update_cell(1, 1, "Listing as of  " + str(datetime.utcnow())[0:10] + '  at '
                  + str(datetime.utcnow())[10:16] + '  UTC')
#  ___________________________________________________________________________________________________________________
