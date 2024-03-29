import pandas as pd
import subprocess
from datetime import datetime, timedelta
from twilio.rest import Client
import pyodbc
import keys
import schedule
import time

"""Gets the URL of the specified path.

The function runs a JavaScript file to navigate and get the URL of the 
route.

Keyword arguments:
route_num -- the route number of the bus

Returns the URL as a string.
"""
def get_url(route_num, station) -> str:
    try:
        # Running the JavaScript file in a separate process.
        process = subprocess.Popen(["node", "vta-nav.js", route_num, station], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        # Checking if the file returned an error.
        if stderr:
            print("Error:", stderr.decode().strip())
        # Decoding and returning the URL.
        return stdout.decode().strip()
    except Exception as e:
        print("Exception:", str(e))
       
"""Gets the schedule from a certain time frame.

Uses pandas to return a list of times within a certain time frame.

Keyword Arguments:
departure_times -- a list returned by pandas for the day's schedule
start -- the start time for the search
end -- the end time for the search

Returns a list of ideal times for departure.
""" 
def get_schedule(departure_times, start, end):
    ideal_times = []
    # Converting a list item to time object and making a list of ideal times.
    for i in range(len(departure_times)):
        # Check for discrepancies on the website
        try:
            today_date = datetime.now().date() 
            depart_time = datetime.strptime(departure_times[i], "%I:%M %p").time()
            depart_at = datetime.combine(today_date, depart_time)
        except:
            continue
        time = datetime.strftime(depart_at, "%H:%M")
        # Adding specific times to the list
        if start <= time <= end:
            ideal_times.append(time)
        elif end < time:
            break
    return ideal_times

def push_notification(departure_time, send_to):
    client = Client(keys.account_sid, keys.auth_token)
    today_date = datetime.now().date() 
    depart_time = datetime.strptime(departure_time, "%H:%M").time()
    departs_at = datetime.combine(today_date, depart_time)
    send_when = departs_at + timedelta(hours=2, minutes=50)
    time = datetime.strftime(departs_at, "%H:%M")
    message = client.messages.create(
        from_=keys.msg_service_sid,
        to=send_to,
        body="Your transit is leaving at " + time + ".",
        schedule_type="fixed",
        send_at=send_when.isoformat() + 'Z',
    )
    
def main():
    # Connect to the MS SQL database using pyodbc
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};\
                      SERVER='+keys.server+';\
                      DATABASE='+keys.database+';\
                      UID='+keys.username+';\
                      PWD='+ keys.password)

    # Select the row from the table
    cursor = cnxn.cursor()
    cursor.execute("SELECT * FROM user_info;")
    row = cursor.fetchone() 
    
    URL = ""
    departure_times = []
    while row:
        # Get the url for the specified route using JS
        URL = get_url(row[2], row[3])

        # Parse the data using pandas to get all the departure times at a station
        dfs = pd.read_html(URL)
        for i, item in enumerate(dfs):
            if row[3] in item:
                departure_times = item.loc[:, row[3]]
                break

        # Filter the list of desired times to get a list of ideal times
        today_date = datetime.now().date()
        start_time = datetime.strptime(row[1], "%I:%M %p").time()
        start = datetime.combine(today_date, start_time)
        end = start + timedelta(minutes=30) # Only need the buses within 30 minutes of set time
        start = datetime.strftime(start, "%H:%M") # Convert to military format 
        end = datetime.strftime(end, "%H:%M")
        ideal_times = get_schedule(departure_times, start, end) # List of ideal times

        # Push notifications to the users phone
        for t in ideal_times:
            push_notification(t, row[4])

        row = cursor.fetchone()
    
schedule.every().day.at("00:15").do(main)

while 1:
    schedule.run_pending()
    time.sleep(1) 