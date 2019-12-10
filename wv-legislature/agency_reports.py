import requests
from bs4 import BeautifulSoup
import csv

r = requests.get("http://www.wvlegislature.gov/Reports/Agency_Reports/agencylist_all.cfm")
soup = BeautifulSoup(r.text, 'html.parser')
results = []
reports = soup.find_all('tr')[1:-1]

for report in reports:
    agency, title, year, filler = [x.text for x in report.find_all('td')]
    if report.find('a'):
        results.append([agency, title, year, "http://www.wvlegislature.gov"+report.find('a')['href']])
    else:
        results.append([agency, title, year, "No Report"])

with open("agency_reports.csv", 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['agency', 'title', 'year', 'url'])
    writer.writerows(results)
