import dateparser
import requests
from bs4 import BeautifulSoup
import csv

r = requests.get("https://www.wvu.edu/return-to-campus/daily-test-results/morgantown/all#daily-campus-testing")
html = "".join(line.strip() for line in r.text.split('\n'))
soup = BeautifulSoup(html, 'html.parser')
results = []

rows = soup.find_all('table')[0].find_all('tr')[2:]

for row in rows:
    date = dateparser.parse(row.find('time').text)
    total_results, total_positive, total_positive_pct = [x.text for x in row.find_all('td')]
    results.append([date, total_results, total_positive, total_positive_pct])

with open('wvu_morgantown_covid_testing_2021.csv', 'w') as tests:
    writer = csv.writer(tests)
    writer.writerow(['date', 'total_results', 'total_positive', 'total_positive_pct'])
    writer.writerows(results)
