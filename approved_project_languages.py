import json
from panoptes_client import Panoptes, Project
import os

Panoptes.connect()
all_projects = Project.where(launch_approved=True)

with open('Approved_projects_languages.csv', 'w', encoding='utf-8', newline='') as out_file:
    out_file.write('project_id' + ',' 'state' + ',' + 'display_name' + ',' 'project.available_languages' + '\n')

    for item in all_projects:
        print(item.id, ';', item.state, ';', item.display_name, ';', item.available_languages)
        out_file.write(item.id + ',' + item.state + ','
                       + item.display_name + ',' + json.dumps(str(item.available_languages)) + '\n')