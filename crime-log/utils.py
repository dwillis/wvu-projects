import csv
from dateutil.parser import *
from collections import OrderedDict

incidents = []

with open('crime_log.csv', 'r') as existing_reports:
    reader = csv.DictReader(existing_reports)
    for row in reader:
        new_dt = parse(row['datetime'])
        row['datetime'] = new_dt
        incidents.append(row)

with open("crime_log.csv", 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=["id","title","year","datetime","building","address","outcome"])
    writer.writeheader()
    writer.writerows(incidents)
