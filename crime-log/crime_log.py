import csv
from dateutil.parser import *
import requests
from bs4 import BeautifulSoup

with open('crime_log.csv', 'r') as existing_reports:
    reader = csv.DictReader(existing_reports)
    previous_ids = [x['id'] for x in reader]

r = requests.get("https://police.wvu.edu/clery-act/campus-safety/crime-log")
soup = BeautifulSoup(r.text, 'html.parser')
results = []
# crime log incidents are enclosed in individual <li> elements
incidents = soup.find_all('li', attrs={'class': 'incident'})

for incident in incidents:
    id, title = incident.find('h4').text.split(': ')
    for p in incident.find_all('p'):
        year = incident.find_all('p')[0].text
        keys = [x.find('strong').text.strip() for x in incident.find_all('p') if x.find('strong')]
        if "Building:" in keys:
            datetime = parse(incident.find_all('p')[1].text.split(": ")[1])
            building = incident.find_all('p')[2].text.split(": ")[1]
            address = incident.find_all('p')[3].text.split(": ")[1]
            outcome = incident.find_all('p')[4].text.split(": ")[1]
        else:
            datetime = parse(incident.find_all('p')[1].text.split(": ")[1])
            building = None
            address = incident.find_all('p')[2].text.split(": ")[1]
            outcome = incident.find_all('p')[3].text.split(": ")[1]
        result = [id, title, year, datetime, building, address, outcome]
        if result not in results:
            results.append(result)

new_incidents = [x for x in results if x[0] not in previous_ids]

if len(new_incidents) > 0:
    with open("crime_log.csv", 'a') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(new_incidents)
