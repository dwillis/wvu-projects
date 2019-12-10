# WVU Projects

Scripts and data from West Virginia University investigative journalism class in Fall 2019.

### Crime Log

Basic scraper for the WVU campus police [crime log](https://police.wvu.edu/clery-act/campus-safety/crime-log) that outputs a CSV file. The log itself contains the previous 90 days' worth of incidents, so this would be useful for storing information before it disappears from the site.

Use the following commands to run the script:

`cd crime-log`

`pip3 install -r requirements.txt`

`python3 crime_log.py`


### State Agency Reports

Basic scraper for [state agency reports to the legislature](http://www.wvlegislature.gov/Reports/Agency_Reports/agencylist_all.cfm) that outputs two CSV files: one, `all_reports.csv`, is the complete list of reports from the site. The second, `new_reports.csv`, is those that have appeared since the last time the script was run.

Use the following commands to run the script:

`cd wv-legislature`

`pip3 install -r requirements.txt`

`python3 agency_reports.py`
