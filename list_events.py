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
	page_token = None
	calendar_ids = []
	while True:
		calendar_list = service.calendarList().list(pageToken=page_token).execute()
		for calendar_list_entry in calendar_list['items']:
			print(f"Calendar list entry: {calendar_list_entry['summary']}")
			calendar_ids.append(calendar_list_entry['id'])
		page_token = calendar_list.get('nextPageToken')
		if not page_token:
			break

	# This code is to look for all-day events in each calendar for the month of September
	# Src: https://developers.google.com/google-apps/calendar/v3/reference/events/list
	# You need to get this from command line
	# Bother about it later!
	start_date = datetime.datetime(2017, 10, 1, 0, 0, 0, 0).isoformat() + 'Z'
	end_date = datetime.datetime(2017, 12, 30, 23, 59, 59, 0).isoformat() + 'Z'

	for calendar_id in calendar_ids:
		count = 0
		print('\n----%s:\n' % calendar_id)
		eventsResult = service.events().list(
			calendarId=calendar_id,
			timeMin=start_date,
			timeMax=end_date,
			singleEvents=True,
			orderBy='startTime').execute()
		events = eventsResult.get('items', [])
		if not events:
			print('No upcoming events found.')
		for event in events:
			if event.has_key('summary'):
				if 'PTO' in event['summary']:
					count += 1
					start = event['start'].get(
						'dateTime', event['start'].get('date'))
					print(start, event['summary'])
		print('Total days off for %s is %d' % (calendar_id, count))


if __name__ == '__main__':
	main()