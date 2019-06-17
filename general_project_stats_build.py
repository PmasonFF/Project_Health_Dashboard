# -*- coding: utf-8 -*-

import os
import io
import operator
import sys
from datetime import datetime
import panoptes_client
from panoptes_client import Panoptes, Project
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

Panoptes.connect(username=os.environ['User_name'], password=os.environ['Password'])

project_listing = []
for project in Project.where(launch_approved=True):
    try:
        project_listing.append([int(project.id), project.subjects_count,
                                project.retired_subjects_count, project.launch_approved,
                                project.state, project.display_name])
    except panoptes_client.panoptes.PanoptesAPIException:
        print(str(sys.exc_info()[1]))
project_listing.sort(key=operator.itemgetter(0))
sorted_on_state = sorted(project_listing, key=operator.itemgetter(4))

with io.open('out_proj_stats_approved.csv', 'w', encoding='cp1252', newline='') as out_file:
    out_file.write("Listing as of  " + str(datetime.utcnow())[0:10] + '  at '
                   + str(datetime.utcnow())[10:16] + '  UTC' + '\n' + '\n')
    out_file.write('project_id' + ',' + 'subjects_count' + ','
                   + 'retired_subjects_count' + ',' + 'launch_approved' + ',' + 'state' + ',' + 'display_name' + '\n')
    for line in sorted_on_state:
        print(line)
        out_file.write(str(line[0]) + ',' + str(line[1]) + ',' + str(line[2]) + ',' + str(line[3]) + ',' + str(
            line[4]) + ',' + str(line[5]) + '\n')

content = open('out_proj_stats_approved.csv', 'r', encoding='latin-1').read()
client.import_csv('1Wg2ZNDeDZpxEwmY97b5ppb3VtO2Qd9jYKgC7EF0A3yo', content)
#  ____________________________________________________________________________________________________________________
