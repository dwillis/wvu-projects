import os
import requests
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
            print(response.status_code)
    else:
        print(f"Skipped: {filename} (already exists)")

def main():
    # Create directory if it doesn't exist
    directory = 'pdfs'
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Read CSV file and download PDFs
    with open('lobbying_filings.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            download_pdf(row['url'], directory)

if __name__ == "__main__":
    main()
