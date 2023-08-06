## GeePal: Make your calendar work for you

   This project is intended to provide a minimal bootstrap for using the Google Calendar API to parse your calendar data. The primary motivation is to use the API to generate invoces for freelancers.

   The project consists of a simple modification of the Google Calendar quickstart in Python, *get_events*, to produce a dictionary for each calendar specified, containing all calendar events within a relative time period described by keywords: 'week', 'lastWeek', 'month', 'lastMonth', etc.

   A second module, *dfsort*, creates a data frame for each set of events per calendar,  in the period, adding a 'Durations' column for calculating elapsed time.

   In addition, *dfsort* contains functions for sorting by event name, *get_unique_events()*, searching for summary statements and producing an data-frame for itemized invoicing with summary, event start and elapsed time, *get_projects()*, and a simple formatting function, *hrs_min_sec()* for elapsed datetime objects.

## Get Started
1. Fork this repository
2. Clone your fork to your development machine
2. Navigate to the repository folder in your terminal
3. Create a new Python file and import modules as below
4. Set up your [Google Calendar credentials](https://developers.google.com/google-apps/calendar/quickstart/go) add them to a file in your repository folder

## Code Example

```python

import get_events as ge
import dfsort as df

SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'

credentials = ge.get_credentials()
service = ge.create_svs_obj(credentials)
evStart_evEnd = ge.event_range('week')
evStartEvEnd_eventsDct = ge.get_events(service, evStart_evEnd, pvt.calendars)
evStartEvEnd_calEvDfsDct = dfs.add_durations(evStartEvEnd_eventsDct)
(evStart_evEnd, calEvDfsDct) = evStartEvEnd_calEvDfsDct

calendar = 'Production'
workTypesDct = dfs.get_unique_events(evStartEvEnd_calEvDfsDct, calendar)

workType = 'Contract Work'
projectNm = 'Project Name'
workTypesDf = workTypesDct[workType]
projectDf = dfs.get_projects(workTypesDf, projectNm)
projectDf.to_csv(projectNm+'.csv')

with open('projectNameHrs.tex', 'w') as f:
    f.write(tabulate(projectDf, tablefmt="latex"))
```

## Motivation

   This project was motivated by my experience as an independent contractor and as the president of a small startup where all the workers are contractors and client invoices require detailed accounting of tasks performed and time spent, as well as, occasionally, percent of contract for fixed-price projects.

   I found the simplest way to avoid the burdensome overhead of invoicing every month was to simply track my time on the same calendar that I use to plan it; namely, Google Calendar. The API is relatively easy to work with and provides plenty of flexibility, as well as a great example of a well structured and maintained system.

   The main requirement is to maintain the discipline of updating the calendar as work is done and to establish conventions for documenting it. I use different calendars for diferent categories of work (production, business, etc.) and the event name as a descriptor of the work type (contract, project, product, etc.). Inside the *Description* field I use the markdown bullet & 'checkbox' to indicate tasks; some are done with and 'x' while other are not done with an empty checkbox (`- [x]`, `- [ ]`). The intent is to allow planned events that were not done to pass through with being captured in the invoice without requiring the user to manage planned vs accomplished subtasks.

   The current regex in *get_events()* function will capture any symbol in the 'box' but it only captures the first item. It should capture the full nested structure of subtasks to provide maximum flexibility.

## Tests

Testing currently only covers the **get_events** module. Testing uses [PyTest](https://docs.pytest.org/en/latest/) and Google's HttMock library to allow automated testing even when completely offline.

## Contributors

   At this point, just give a shout if you're intersted or want to share code. I'd really like to get test more coverage before moving on to more functionality.
   
   Also, I'm a self-taught programmer, so feel free to make recommendations on style or structure.

## License

Licensed under the GNU Affero General Pulbic License
