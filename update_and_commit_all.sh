#!/bin/bash

scrape_and_commit () {
    cd wv-legislature
    python agency_reports.py
    git add *.csv
    git commit -m "updated reports" && \
        git push -q https://${GITHUB_PERSONAL_TOKEN}@github.com:dwillis/wvu-projects.git master \
        || true
}

git config --global user.email "wvu_projects@example.com"
git config --global user.name "WVU Projects"

scrape_and_commit
