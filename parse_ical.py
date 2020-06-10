# parse Geology seminar calendar and display in HTML

from datetime import datetime, timedelta, timezone
import icalendar
from dateutil.rrule import *
import requests
import re
import os

from flask import Flask, render_template, flash, request

# return list of dicts for each seminar
def get_calendar_data(url):

    resp = requests.get(url)
    gcal = icalendar.Calendar.from_ical(resp.text)

    event_list = []

    for component in gcal.walk():
        if component.name == "VEVENT":
            summary = component.get('summary')
            description = component.get('description')
            location = component.get('location')
            startdt = component.get('dtstart').dt
            enddt = component.get('dtend').dt
            exdate = component.get('exdate')
            #print(startdt, summary, description)
            event_list.append([str(startdt)[:10], str(summary), str(description)])
    event_list.sort()
    outstr = ""
    seminar_list = []

    for e in event_list:
        date = datetime.strptime(e[0], "%Y-%m-%d")
        summary = e[1]
        descr = e[2]

        outdict = {}

        # parse description
        #print("\n------------------", descr)

        #Speaker:<name>/n
        r = re.search("Speaker:(.*?)\n", descr)
        if r:
            print(date.strftime("%a. %B %d, %Y"))
            outdict["date"] = date.strftime("%a. %B %d, %Y")
            print(r.group(1))
            outdict["speaker"] = r.group(1)

            outstr += date.strftime("%a. %B %d, %Y") + "\n" + r.group(1) + "\n"


        r = re.search("Affiliation:(.*?)\n", descr)
        if r:
            print(r.group(1))
            outdict["affiliation"] = r.group(1)
            outstr += r.group(1) + "\n"

        r = re.search("Title:(.*?)\n", descr)
        if r:
            print(r.group(1))
            outdict["title"] = r.group(1)
            outstr += r.group(1) + "\n"

        r = re.search("Abstract:(.*?)", descr)
        if r:
            print(r.group(1))
            outdict["abstract"] = r.group(1)
            outstr += r.group(1) + "\n"

        if outdict.get("date") != None:
            seminar_list.append(outdict)

    return seminar_list

# my seminar google calendar
url = "https://calendar.google.com/calendar/ical/egdnrrp6oh8325lf720rv01dno%40group.calendar.google.com/public/basic.ics"
app = Flask(__name__)

@app.route("/", methods=['GET'])
def main():

    data = get_calendar_data(url)
    rt = render_template('seminar_calendar.html', title="GeAt Seminar", data=data)
    return rt

if __name__ == "__main__":
    app.run(debug=True)
