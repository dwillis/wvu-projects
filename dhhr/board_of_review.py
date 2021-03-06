import requests
import csv
import tabula
import re
import time

URLS = [{'year': 2020, 'url': "FY 2020 Report by Category and Decision.pdf"}, {'year': 2019, 'url': 'FY 2019 Report by Category and Decision.pdf'},
{'year': 2018, 'url': "FY 2018  Report by Category and Decision.pdf"}, { 'year': 2017, 'url': "FY 2017 Report by Category and Decision.pdf"},
{'year': 2016, 'url': "FY 2016 Report by Category and Decision.pdf"}, {'year': 2015, 'url': "Report by Category and Decision FISCAL YEAR 2015.pdf"},
{'year': 2014, 'url': "FY 2014 Report by Category and Decision.pdf"}]

HEADERS = ['year', 'categories', 'total_received', 'total_adjudicated', 'upheld', 'reversed', 'total_written', 'abandoned', 'withdrawn', 'dismissed', 'remanded', 'invalid']

HEADERS_PRE_2016 = ['year', 'categories', 'total_received', 'total_adjudicated', 'upheld', 'reversed', 'total_written', 'abandoned', 'withdrawn_claimant_favor', 'withdrawn_no_change', 'dismissed', 'remanded', 'invalid']

for report in URLS:
    year = report['year']

    json = tabula.read_pdf(report['url'], pages="all", output_format='json')

    # strip out empty rows and remove the bad header
    try:
        rows = [r for r in json[1]['data'][2:-1] if r[0]['text'] != '']
    except:
        rows = [r for r in json[0]['data'][2:-1] if r[0]['text'] != '']

    with open(f'board_of_review_{year}.csv', 'w') as f:
        writer = csv.writer(f)
        if year > 2015:
            writer.writerow(HEADERS)
        else:
            writer.writerow(HEADERS_PRE_2016)
        for row in rows:
            category = row[0]['text']
            writer.writerow([year] + [category] + [re.sub("[^[0-9]", "", str(r['text'])) for r in row[1:]])
