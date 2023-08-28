import csv
from dateutil.parser import *
import requests
from bs4 import BeautifulSoup

with open('crime_log.csv', 'r') as existing_reports:
    reader = csv.DictReader(existing_reports)
    previous_ids = [x['id'] for x in reader]

r = requests.get("https://police.wvu.edu/clery-act/crime-and-fire-log")
soup = BeautifulSoup(r.text, 'lxml')
results = []

incidents = soup.find('data').find_all('data')

for incident in incidents:
    title = incident.find('incident_code').contents[0]
    id = incident.find('case_number').contents[0]
    datetime = parse(incident.find('incident_start_date_time').contents[0])
    year = datetime.year
    if len(incident.find('building_name').contents) > 0:
        building = incident.find('building_name').contents[0]
    else:
        building = None
    if len(incident.find('address').contents) > 0:
        address = incident.find('address').contents[0]
    else:
        address = None
    outcome = incident.find('disposition').contents[0]
    result = [id, title, year, datetime, building, address, outcome]
    if result not in results:
        results.append(result)

new_incidents = [x for x in results if x[0] not in previous_ids]

if len(new_incidents) > 0:
    with open("crime_log.csv", 'a') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(new_incidents)
