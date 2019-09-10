"""
05-Oct-2017: Scratch script for blog post about Google Calendar API
This script is a sample and NOT indicative of Qxf2's programming habits.

This script will:
a) Connect to Google Calendar
b) Get calendar ids for all Qxf2 employees
c) Execute a search in a given hardcoded timeframe for all employees
d) List any event with the word PTO in the summary

To setup, I followed this reference:
https://developers.google.com/google-apps/calendar/quickstart/python

References:
1. https://developers.google.com/google-apps/calendar/quickstart/python
2. https://developers.google.com/google-apps/calendar/v3/reference/events/list
3. https://developers.google.com/google-apps/calendar/v3/reference/calendarList/list
"""


from __future__ import print_function
import httplib2
import os

# from apiclient import discovery
# Commented above import statement and replaced it below because of
# reader Vishnukumar's comment
# Src: https://stackoverflow.com/a/30811628

import googleapiclient.discovery as discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime

try:
	import argparse
	flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
	flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Quickstart'
MAKERSPACE_CALENDAR_ID = "makerspace.se_dsd75rv0l7rblcq1sd627fab38@group.calendar.google.com"


def get_credentials():
	"""Gets valid user credentials from storage.

	If nothing has been stored, or if the stored credentials are invalid,
	the OAuth2 flow is completed to obtain the new credentials.

	Returns:
		Credentials, the obtained credential.
	"""
	credential_dir = os.path.join(".", '.credentials')
	if not os.path.exists(credential_dir):
		os.makedirs(credential_dir)
	credential_path = os.path.join(credential_dir,
								   'calendar-python-quickstart.json')

	store = Storage(credential_path)
	credentials = store.get()
	if not credentials or credentials.invalid:
		flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
		flow.user_agent = APPLICATION_NAME
		if flags:
			credentials = tools.run_flow(flow, store, flags)
		else:  # Needed only for compatibility with Python 2.6
			credentials = tools.run(flow, store)
		print('Storing credentials to ' + credential_path)
	return credentials

def get_makerspace_calendar_entry(service):
	calendar_list = service.calendarList().list().execute()
	for calendar_list_entry in calendar_list['items']:
		if MAKERSPACE_CALENDAR_ID == calendar_list_entry['id']:
			return calendar_list_entry
	else:
		raise KeyError(f"Could not find the Makerspace calendar '{MAKERSPACE_CALENDAR_ID}' among the shared calendars")

def main():
	"""Shows basic usage of the Google Calendar API.

	Creates a Google Calendar API service object and outputs a list of the next
	10 events on the user's calendar.
	"""
	credentials = get_credentials()
	http = credentials.authorize(httplib2.Http())
	service = discovery.build('calendar', 'v3', http=http)

	# This code is to fetch the calendar ids shared with me
	# Src: https://developers.google.com/google-apps/calendar/v3/reference/calendarList/list
	makerspace_calendar_entry = get_makerspace_calendar_entry(service)

	# This code is to look for all-day events in each calendar for the month of September
	# Src: https://developers.google.com/google-apps/calendar/v3/reference/events/list
	# You need to get this from command line
	# Bother about it later!
	start_date = datetime.datetime.now().isoformat() + 'Z'
	end_date = (datetime.datetime.now() + datetime.timedelta(days=30)).isoformat() + 'Z'

	count = 0
	print('\n----%s:\n' % MAKERSPACE_CALENDAR_ID)
	eventsResult = service.events().list(
		calendarId=MAKERSPACE_CALENDAR_ID,
		timeMin=start_date,
		timeMax=end_date,
		singleEvents=True,
		orderBy='startTime').execute()
	events = eventsResult.get('items', [])
	key_events = [event for event in events if "summary" in event and "Nyckel" in event["summary"]]

	print("")
	if len(key_events) == 0:
		print('No upcoming events found.')
	else:
		print(f"There are {len(key_events)} key handouts in the next 30 days in calendar '{MAKERSPACE_CALENDAR_ID}':")
		for event in key_events:
			print(f"event: {event}")



if __name__ == '__main__':
	main()