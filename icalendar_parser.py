#!/usr/bin/env python3
from icalendar import Calendar, Event
from urllib import request
import datetime

def ellipsis(s, maxlen=50):
    return (s[:maxlen] + "...") if len(s) > maxlen else s

import re
def escape_rn(s):
    s = re.sub(r"\r", r"\\r", s)
    s = re.sub(r"\n", r"\\n", s)
    return s

def dt_to_datetime(dt):
    if isinstance(dt, datetime.datetime):
        return dt
    elif isinstance(dt, datetime.date):
        dt = datetime.datetime.combine(dt, datetime.time.min)
        dt = dt.replace(tzinfo=datetime.timezone.utc)
        return dt
    else:
        raise TypeError(f"Unhandled input type: {type(dt)}")

makerspace_ical_url = "https://calendar.google.com/calendar/ical/makerspace.se_dsd75rv0l7rblcq1sd627fab38%40group.calendar.google.com/public/basic.ics"
req = request.urlopen(makerspace_ical_url)
ical_str = req.read()
cal = Calendar.from_ical(ical_str)

now = datetime.datetime.now(datetime.timezone.utc)
end_search_date = now + datetime.timedelta(days=30)
for event in cal.walk('vevent'):
    summary = str(event.get("summary"))
    description = ellipsis(escape_rn(str(event.get("description"))))
    dtstart = dt_to_datetime(event.get("dtstart").dt)
    if "dtend" not in event:
        dtend = dtstart
    else:
        dtend = dt_to_datetime(event.get("dtend").dt)
    if now <= dtend and dtstart < end_search_date:
        print(f"Event\n\tsummary: {summary}\n\tdescription: {description}\n\tdtstart: {dtstart}\n\tdtend: {dtend}")
