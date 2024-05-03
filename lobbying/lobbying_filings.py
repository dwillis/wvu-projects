import os
import sys
import requests
from bs4 import BeautifulSoup
import csv

def download_pdf(url, directory):
    filename = os.path.join(directory, url.split('/')[-1])
    if not os.path.exists(filename):
        response = requests.get(url)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded: {filename}")
        else:
            print(f"Failed to download: {url}")
    else:
        print(f"Skipped: {filename} (already exists)")

def main(registration_cycle):
    # Create directory if it doesn't exist
    directory = 'pdfs'
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Read existing reports
    existing_files = os.listdir(directory)

    # Scrape new filings
    if registration_cycle == '2019-2020':
        url = f"https://ethics.wv.gov/lobbyist/Pages/{registration_cycle}.aspx"
    else:
        url = f"https://ethics.wv.gov/lobbyist/Pages/{registration_cycle}-Registration-Cycle.aspx"
    
    r = requests.get(url)
    html = "".join(line.strip() for line in r.text.split('\n'))
    soup = BeautifulSoup(html, 'html.parser')
    links = [x['href'] for x in soup.find_all('a') if 'href' in x.attrs and 'SiteCollectionDocuments' in x['href']]
    results = []

    for link in links:    
        url = "https://ethics.wv.gov" + link
        parts = link.split('/')
        period = parts[4]
        name = parts[5].split('.')[0].replace(period,'').replace('%20',' ').strip().upper()
        results.append([name, period, url])

    # Write all filings to CSV
    with open("lobbying_filings.csv", 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(results)

    # Download PDFs
    for filing in results:
        download_pdf(filing[2], directory)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script_name.py registration_cycle")
        sys.exit(1)
    
    registration_cycle = sys.argv[1]
    main(registration_cycle)
