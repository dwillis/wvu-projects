#!/bin/bash

scrape_and_commit_reports () {
    cd wv-legislature
    python agency_reports.py
    git add *.csv
    git commit -m "updated reports" && \
        git push -q https://github.com:dwillis/wvu-projects.git master \
        || true
}

scrape_and_commit_crimelog () {
    cd ..
    cd crime-log
    current_time=$(date "+%Y.%m.%d-%H.%M.%S")
    mv crime_log.csv crime_log.csv.$current_time
    python crime_log.py
    git add *.csv
    git commit -m "updated crimelog" && \
        git push -q https://github.com:dwillis/wvu-projects.git master \
        || true
}

git config --global user.email "wvu_projects@example.com"
git config --global user.name "WVU Projects"

scrape_and_commit_reports
scrape_and_commit_crimelog
