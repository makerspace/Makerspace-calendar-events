#!/usr/bin/env python3
from icalendar import Calendar, Event
from urllib import request

def ellipsis(s, maxlen=50):
    return (s[:maxlen] + "...") if len(s) > maxlen else s

import re
def escape_rn(s):
    s = re.sub(r"\r", r"\\r", s)
    s = re.sub(r"\n", r"\\n", s)
    return s

makerspace_ical_url = "https://calendar.google.com/calendar/ical/makerspace.se_dsd75rv0l7rblcq1sd627fab38%40group.calendar.google.com/public/basic.ics"
req = request.urlopen(makerspace_ical_url)
ical_str = req.read()
cal = Calendar.from_ical(ical_str)
for event in cal.walk('vevent'):
    summary = str(event.get("summary"))
    description = ellipsis(escape_rn(str(event.get("description"))))
    print(f"Event\n\tsummary: {summary}\n\tdescription: {description}")
