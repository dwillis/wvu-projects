import requests
from bs4 import BeautifulSoup
import csv

with open('meeting_notices.csv', 'r') as existing_notices:
    reader = csv.DictReader(existing_notices)
    previous_ids = [x['id'] for x in reader]

r = requests.get("http://apps.sos.wv.gov/adlaw/meetingnotices/")
soup = BeautifulSoup(r.text, 'html.parser')
results = []
table = soup.find("table", { "id" : "tableResults" })
links = table.find_all('a')

for link in links:
    url = "http://apps.sos.wv.gov/adlaw/meetingnotices/" + link['href']
    id = url.split('=')[1]
    date, time = link.text.split(' -- ')
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    if soup.find('th').find('h2'):
        agency = soup.find('th').find('h2').find('br').previous
        if len(soup.find('th').find('h2').find_all('em')) > 0:
            subagency = " ".join([x.text for x in soup.find('th').find('h2').find_all('em')])
        else:
            subagency = None
    else:
        agency = soup.find('th').text
        subagency = None
    details = soup.find_all('td')
    location = details[1].find('pre').text.replace('\r\n',' ').replace('  ',' ')
    purpose = details[2].text.split('Purpose: ')[1]
    notes = details[3].text.split('Notes: ')[1]
    results.append([id, date, time, agency, subagency, location, purpose, notes])

new_notices = [x for x in results if x[0] not in previous_ids]

if len(new_notices) > 0:
    with open("meeting_notices.csv", 'a') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(new_notices)
