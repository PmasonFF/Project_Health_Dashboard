# -*- coding: utf-8 -*-
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
# Also options to open with key or open with url
# Need to share the folder where the file is with service account email address, don't need to specify path in code
# sheet = client.open("out_proj_stats_approved").sheet1

# # Extract and print all of the values
# list_of_hashes = sheet.get_all_records()
# print(list_of_hashes)

# # you can get a list of lists if you’d prefer:
# print(sheet.get_all_values())

# # Or you could just pull the data from a single row, column, or cell:
# print(sheet.row_values(1))
# print(sheet.col_values(1))
# print(sheet.cell(1, 1).value)

# # You can write to the spreadsheet by changing a specific cell:
# sheet.update_acell('A1', "projectid")
# print(sheet.acell('A1').value)
# sheet.update_cell(1, 1, "project_id")
# print(sheet.cell(1, 1).value)
#
# # Fetch a cell range
# cell_list = sheet.range('A1:B7')
# print(cell_list)
#
# # Update a range of cells
# cell_list = sheet.range('G1:H5')
# for cell in cell_list:
#     cell.value = ''
#
# # Update in batch
# sheet.update_cells(cell_list)
#
# # You can insert a row in the spreadsheet:
# row = ["I'm","inserting","a","row","into","a,","Spreadsheet","with","Python"]
# index = 1
# sheet.insert_row(row, index)

# # You can also delete a row from the spreadsheet:
# sheet.delete_row(187)
#
# # Insert a worksheet
# worksheet = sheet.add_worksheet(title="A worksheet", rows="200", cols="7")
#
# # And find out the total number of rows:
# print(sheet.row_count)

# # Export sheet as .csv format using pandas (Not tested yet)
# import pandas as pd
#
# your_data = sheet.get_all_values()
# your_data = pd.DataFrame(your_data)
# your_data.to_csv('filename.csv')
#

# # Create a blank spreadsheet  This places the spreadsheet in the root drive!
# sh = client.create('A new spreadsheet')
# sh.share('petermijo@bmts.com', perm_type='user', role='owner')
# sh.share('interface-with-google-sheets@zooniverse-project-health.iam.gserviceaccount.com',
#          perm_type='user', role='writer')
# sh = client.open("A new spreadsheet")
#
# # Read CSV file contents
# content = open('out_proj_stats_approved.csv', 'r', encoding='latin-1').read()
# client.import_csv(sh.id, content)
#
#  Create a blank spread sheet in a folder other than the root
# from googleapiclient.discovery import build
#
# drive_api = build('drive', 'v3', credentials=creds)
# folder_id = '1dJm4R1vDIfTL3ruIfK0KxqRhvoVT15tb'
# file_metadata = {
#     'name': 'Another_spreadsheet',
#     'mimeType': 'application/vnd.google-apps.spreadsheet',
#     'parents': [folder_id]  # this can actually be a list of parents
#     }
# file = drive_api.files().create(body=file_metadata,
#                                 fields='id').execute()
# req = drive_api.permissions().create(
#     fileId=file.get('id'),
#     body={'type': 'user',
#           'role': 'writer',
#           'emailAddress': 'interface-with-google-sheets@zooniverse-project-health.iam.gserviceaccount.com'
#           },
#     fields="id").execute()  # basic owner permissions created with the file using drive_api
#
# content = open('out_proj_stats_approved.csv', 'r', encoding='latin-1').read()
# client.import_csv(file.get('id'), content)
#

#
# # Using gspread_formatting to detect and set cell formats
# from gspread_formatting import *
#
# # Detect formats
# print(get_user_entered_format(sheet, 'A1'))
#
# # Set formats
# fmt = cellFormat(
#     backgroundColor=color(1, .9, .9),
#     textFormat=textFormat(bold=True, foregroundColor=color(1, 0, 0)),
#     horizontalAlignment='LEFT'
#     )
# format_cell_range(sheet, 'A1:J1', fmt)

# # Useful details:
#  colors = {'black': (0, 0, 0), 'white': (1, 1,1), 'red': (1, 0, 0), 'green': (0, 1, 0), 'blue': (0, 0, 1),
#  'yellow': (1, 1, 0), 'cyan': (0, 1, 1), 'magenta': (1, 0, 1), 'orange': (1, .6, 0), 'purple': .6, 0, 1)}
#  alignments = ['LEFT', 'CENTER', 'RIGHT']
#  https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets/cells#CellFormat