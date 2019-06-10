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
# sheet.update_cell(1, 1, "project_id")
# print(sheet.cell(1, 1).value)

# # Or you can insert a row in the spreadsheet:
# row = ["I'm","inserting","a","row","into","a,","Spreadsheet","with","Python"]
# index = 1
# sheet.insert_row(row, index)

# # You can also delete a row from the spreadsheet:
# sheet.delete_row(187)
#
# # And find out the total number of rows:
# print(sheet.row_count)

# # Export sheet as .csv format using pandas (Not tested yet)
# import pandas as pd
#
# your_data = sheet.get_all_values()
# your_data = pd.DataFrame(your_data)
# your_data.to_csv('filename.csv')
