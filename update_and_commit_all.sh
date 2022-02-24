#!/bin/bash

# scrape_and_commit_reports () {
#     cd wv-legislature
#     python agency_reports.py
#     git add *.csv
#     git commit -m "updated reports" && \
#         git push -q https://${GITHUB_PERSONAL_TOKEN}@github.com/dwillis/wvu-projects.git master \
#         || true
# }
#
# scrape_and_commit_crimelog () {
#     cd ..
#     cd crime-log
#     python crime_log.py
#     git add .
#     git commit -m "updated crimelog" && \
#         git push -q https://${GITHUB_PERSONAL_TOKEN}@github.com/dwillis/wvu-projects.git master \
#         || true
# }
#
# scrape_and_commit_meetings () {
#     cd ..
#     cd meeting-notices
#     python scraper.py
#     git add *.csv
#     git commit -m "updated meeting notices" && \
#         git push -q https://${GITHUB_PERSONAL_TOKEN}@github.com/dwillis/wvu-projects.git master \
#         || true
# }
#
# scrape_and_commit_lobbying () {
#     cd ..
#     cd lobbying
#     python lobbying_filings.py
#     git add .
#     git commit -m "updated lobbying filings" && \
#         git push -q https://${GITHUB_PERSONAL_TOKEN}@github.com/dwillis/wvu-projects.git master \
#         || true
# }
#
# scrape_and_commit_wvu_testing () {
#     cd ..
#     cd wvu-covid-tests
#     python wvu_tests.py
#     git add .
#     git commit -m "updated wvu tests" && \
#         git push -q https://${GITHUB_PERSONAL_TOKEN}@github.com/dwillis/wvu-projects.git master \
#         || true
# }
#
# git config --global user.email "wvu_projects@example.com"
# git config --global user.name "WVU Projects"
#
# scrape_and_commit_reports
# scrape_and_commit_crimelog
# scrape_and_commit_meetings
# scrape_and_commit_lobbying
# scrape_and_commit_wvu_testing
