# Makerspace calendar events
Listing events in the Makerspace calendar, such as key handouts.

## Install
First install the python dependencies
```bash
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

Then create a new Google project by following the instructions on [this page](https://developers.google.com/calendar/quickstart/python). There you will be presented with a link that creates a new Cloud Platform project and automatically enable the Google Calendar API (this can most likely be done manually by going to the [Google API console](https://console.developers.google.com/apis) and setting the correct permissions etc.).

Make sure to save the client secret and name it `client_secret.json`. One can retrieve the credentials later from the Google API console as well.

Run the script as `./list_events.py --noauth_local_webserver`. <br>
The first time you run it, you will be presented with a link that you should enter into your browser. This will take you to a page where you have to consent to the Google API accessing some information (your calendar as read-only). At the end of the set up, you will be presented with a *verification code* that you need to copy and into the terminal. The API should then be activated for the project.

The credentials will then be saved into a folder called `.credentials` which will be used for subsequent requests. A refresh token that is created on the first request will be used for creating the new credentials when your token expires.
