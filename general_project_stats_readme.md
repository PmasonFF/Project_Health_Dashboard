## general_project_stats.py

This script is written in Python 3.7 and requires panoptes_client to be installed with all normal dependencies.

The script uses environmental variables to pass zooniverse credentials to panoptes.  Without logging in all public launched approved projects will be listed. If you are logged in, approved projects you have status on will show regardless of status, including projects which have been taken private and/or under Development.

The script produces a sorted listing of all launch_approved projects. It shows the following fields for each project:
'project.id', 'subjects_count', 'retired_subjects_count', 'launch_approved', 'state', 'display_name' 

The list is sorted by status and then by project.id

Projects with 0 subjects are likely broken, though some link to more recent versions of the project which are live and functioning.

In the future tracking of changes to the retirement counts will be used to estimate the health of the project and flag projects which may have issues.
