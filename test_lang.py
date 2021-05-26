import panoptes_client
from panoptes_client import Panoptes, Project
import os

Panoptes.connect(username=os.environ['User_name'], password=os.environ['Password'])
all_projects = Project.where(launch_approved=True)

for item in all_projects:
    print(item.id, ';', item.display_name, ';', item.available_languages)