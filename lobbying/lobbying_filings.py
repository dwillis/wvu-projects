import requests
from bs4 import BeautifulSoup
import csv

with open('lobbying_filings.csv', 'r') as existing_reports:
    reader = csv.DictReader(existing_reports)
    previous_ids = [x['url'] for x in reader]

r = requests.get("https://ethics.wv.gov/lobbyist/Pages/2019-2020.aspx")
soup = BeautifulSoup(r.text, 'html.parser')
results = []

# filings are inside multiple <p> tags

containers = soup.find_all('p')

for container in containers:
    links = container.find_all('a')
    for link in links:
        url = "https://ethics.wv.gov" + link['href']
        name = link.previous.previous.previous.strip()
        results.append([name, link.text, url])

new_filings = [x for x in results if x[2] not in previous_ids]

if len(new_filings) > 0:
    with open("lobbying_filings.csv", 'a') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(new_filings)