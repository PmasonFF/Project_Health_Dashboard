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
# Need to share the folder where the file is with service account email address, don't need to specify path in code
sheet = client.open("out_proj_stats_approved").sheet1

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
# # Or you can insert a row in the spreadsheet:
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
# # Fetch a cell range
# cell_list = sheet.range('A1:B7')
# print(cell_list)
#
# # Create a blank speadsheet
# sh = client.create('A new spreadsheet')
# sh.share('petermijo@bmts.com', perm_type='user', role='owner')
# sh.share('interface-with-google-sheets@zooniverse-project-health.iam.gserviceaccount.com',
#          perm_type='user', role='writer')
#
# # Update a range of cells
# cell_list = sheet.range('G1:H5')
# for cell in cell_list:
#     cell.value = ''
#
# # Update in batch
# sheet.update_cells(cell_list)
#
# Read CSV file contents  This is not yet working!
# sh = client.open("A new spreadsheet").sheet1
# sh.update_acell('A1', "projectid")  # these two lines worked
# print(sh.id)  # this did not, returned '0', but works for 'sheet' when opened in line 14 above'
# content = open('out_proj_stats_approved.csv', 'r', encoding='latin-1').read()
# print(content)  # This is working
# client.import_csv(sheet.id, content)  # file not found error
client.list_permissions(sheet.id)  # file not found error