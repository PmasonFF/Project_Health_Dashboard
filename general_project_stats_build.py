# -*- coding: utf-8 -*-

import os
import io
import csv
import json
import operator
import sys
from datetime import datetime
import panoptes_client
from panoptes_client import Panoptes, Project
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread_formatting import *

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

Panoptes.connect(username=os.environ['User_name'], password=os.environ['Password'])

with open('activity_stack.csv', 'r') as activity_file:
    activity = csv.DictReader(activity_file)
    stack = {}
    date_time = ''
    for act in activity:
        if act['key'] != 'datetime':
            stack[act['key']] = json.loads(act['value'])
        else:
            date_time = str(act['value'])

flag = False
if str(datetime.utcnow())[8:10] != date_time[8:10]:
    flag = True

project_listing = []
for project in Project.where(launch_approved=True):
    try:
        project_listing.append([int(project.id), project.subjects_count,
                                project.retired_subjects_count, project.activity, int(project.completeness * 100 + .5),
                                project.state, project.display_name])
    except panoptes_client.panoptes.PanoptesAPIException:
        print(str(sys.exc_info()[1]))
project_listing.sort(key=operator.itemgetter(0))
sorted_on_state = sorted(project_listing, key=operator.itemgetter(5))

with io.open('out_proj_stats_approved.csv', 'w', encoding='cp1252', newline='') as out_file:
    out_file.write('project_id' + ',' + 'subjects_count' + ','
                   + 'retired_subjects_count' + ',' + 'activity' + ','
                   + 'completeness' + ',' + 'state' + ',' + 'display_name' + '\n')
    for line in sorted_on_state:
        out_file.write(str(line[0]) + ',' + str(line[1]) + ',' + str(line[2]) + ',' + str(line[3]) + ',' + str(
            line[4]) + ',' + line[5] + ',' + line[6] + '\n')
        if line[5] == 'live'and flag:
            try:
                new = stack[str(line[0])][1:]
                new.append(int(line[3]))
                stack[str(line[0])] = new
            except KeyError:
                new = stack['new'][:]
                new[13] = line[3]
                stack[str(line[0])] = new
    if flag:
        date_time = str(datetime.utcnow())[:16]

with io.open('activity_stack.csv', 'w', newline='') as out_act_file:
    fieldnames = ['key', 'value']
    writer = csv.DictWriter(out_act_file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerow({'key': 'datetime', 'value': date_time})
    for item in list(stack.keys()):
        writer.writerow({'key': item, 'value': json.dumps(stack[item])})

content = open('out_proj_stats_approved.csv', 'r', encoding='latin-1').read()
client.import_csv('1Wg2ZNDeDZpxEwmY97b5ppb3VtO2Qd9jYKgC7EF0A3yo', content)
sheet = client.open("out_proj_stats_approved").sheet1
sheet.insert_row([''], 1)
sheet.insert_row([''], 2)
sheet.insert_row([''], 3)
sheet.update_cell(1, 1, "Listing as of  " + str(datetime.utcnow())[0:10] + '  at '
                  + str(datetime.utcnow())[10:16] + '  UTC')
# ____________________________________________________________________________________________________________________
# This next section applies some tests to various field for a project and flags it with colours based on the findings
sheet.update_acell('B2', "live, broken")
sheet.update_acell('E2', "live, no activity")
sheet.update_acell('G2', "paused, no subjects")
sheet.update_acell('B3', "slow completion")
sheet.update_acell('E3', "very slow completion")
format_cell_range(sheet, 'A2:A2', CellFormat(backgroundColor=Color(1, 0, 0)))
format_cell_range(sheet, 'D2:D2', CellFormat(backgroundColor=Color(1, 1, 0)))
format_cell_range(sheet, 'F2:F2', CellFormat(backgroundColor=Color(1, .9, .9)))
format_cell_range(sheet, 'A3:A3', CellFormat(backgroundColor=Color(.98, .8, .6)))
format_cell_range(sheet, 'D3:D3', CellFormat(backgroundColor=Color(1, .7, 0)))

with open('out_proj_stats_approved.csv', 'r', encoding='cp1252') as file:
    project_details = csv.DictReader(file)
    rc = 4
    for row in project_details:
        rc += 1
        if row['activity'] == '0' and row['state'] == 'live':
            fmt = CellFormat(backgroundColor=Color(1, 1, 0))
            row_range = 'A' + str(rc) + ':F' + str(rc)
            format_cell_range(sheet, row_range, fmt)
        elif row['state'] == 'live':
            if (int(row['subjects_count']) - int(row['retired_subjects_count'])) / int(row['activity']) >= 1095:
                fmt = CellFormat(backgroundColor=Color(1, .7, 0))
                row_range = 'A' + str(rc) + ':F' + str(rc)
                format_cell_range(sheet, row_range, fmt)
            elif (int(row['subjects_count']) - int(row['retired_subjects_count'])) / int(row['activity']) >= 547:
                fmt = CellFormat(backgroundColor=Color(.98, .8, .6))
                row_range = 'A' + str(rc) + ':F' + str(rc)
                format_cell_range(sheet, row_range, fmt)
        if row['subjects_count'] == '0' and row['state'] == 'live':
            fmt = CellFormat(backgroundColor=Color(1, 0, 0))
            row_range = 'A' + str(rc) + ':F' + str(rc)
            format_cell_range(sheet, row_range, fmt)
        if row['subjects_count'] == '0' and row['state'] == 'paused':
            fmt = CellFormat(backgroundColor=Color(1, .9, .9))
            row_range = 'A' + str(rc) + ':F' + str(rc)
            format_cell_range(sheet, row_range, fmt)

#  ____________________________________________________________________________________________________________________
