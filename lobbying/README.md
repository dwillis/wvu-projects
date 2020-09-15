### WV Lobbyist Activity Report Forms

These are forms filed with the West Virginia Ethics Commission by registered lobbyists. They are PDF images, but would be great to have as data. Using [this report](https://ethics.wv.gov/SiteCollectionDocuments/Lobby/ACTIVITY%20REPORTS/2019-3/ADKINS%20J%20MARK%202019-3.pdf) as an example, we might extract the following information:

* Name
* Business Address
* Phone
* Business Email
* City
* State
* Zip
* Reporting Period `2019-3`
* Period Start Date `9/1/2019`
* Period End Date `12/31/2019`
* Due Date `1/15/2020`
* Employers
* Lobbying Activity Summary
* Expenditures (with breakdowns by category)

Since a lobbyist can list more than one employer, it seems like the proper format for this data would be JSON:

```
{
	"url": "https://ethics.wv.gov/SiteCollectionDocuments/Lobby/ACTIVITY%20REPORTS/2019-3/ADKINS%20J%20MARK%202019-3.pdf",
	"name": "J. Mark Adkins",
	"business_address": "600 Quarrier Street",
	"phone": "304-347-1768",
	"business_email": "madkins@bowlesrice.com",
	"city": "Charleston",
	"state": "WV",
	"zip": "25301",
	"reporting_period": "2019-3",
	"period_start_date": "2019-09-01",
	"period_end_date": "2019-12-31",
	"due_date": "2020-01-15",
	"employers": [{
			"number": 1,
			"name": "RAI Services Company"
		},
		{
			"number": 2,
			"name": "Multistate Associates / EPIC Pharmacies Inc."
		},
		{
			"number": 3,
			"name": "Community Bankers of West Virginia"
		}
	],
	"activity_summary": "All of the matters and issues listed on the employer representation authorization form filed in respect to each of these.",
	"expenditures": [
  {
    "employer_number": "1",
    "meals_and_beverages": "0",
    "lodging": "0",
    "advertising": "0",
    "travel": "0",
    "gifts": "0",
    "other_expenses": "0",
    "group_expenditures": "0"
  },
  {
    "employer_number": "2",
    "meals_and_beverages": "0",
    "lodging": "0",
    "advertising": "0",
    "travel": "0",
    "gifts": "0",
    "other_expenses": "0",
  },
  {
    "employer_number": "3",
    "meals_and_beverages": "0",
    "lodging": "0",
    "advertising": "0",
    "travel": "0",
    "gifts": "0",
    "other_expenses": "0",
  }
  {
		"campaign_contributions": "1050"
	}
  ]
}
```
