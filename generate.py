import csv
import argparse
import re
from datetime import datetime, timedelta

def parse_time_interval(time_interval):
    s, e = time_interval.split("~")
    ss = datetime.strptime(s, "%H:%M%p")
    ee = datetime.strptime(e, "%H:%M%p")
    if (ee - ss).total_seconds() < 0:
        ee += timedelta(days=0.5)
    return (ee-ss).total_seconds() / 3600.0

def add_project(timesheet, project_name, contents):
    regex = re.compile(r"\b\d{1,2}:\d{2}(?:[APap][Mm])~\d{1,2}:\d{2}(?:[APap][Mm])\b")
    times = regex.findall(contents)
    total_time = 0.0
    for x in times:
        total_time += parse_time_interval(x)
    if project_name in timesheet:
        timesheet[project_name] += total_time
    else:
        timesheet[project_name] = total_time
    return total_time
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str, required=True, help="input file")
    args = parser.parse_args()

    timesheet = dict()

    with open(args.input, "r") as f:
        reader = csv.reader(f)
        for row in reader:
           project_name = row[2].strip()
           contents = row[3].strip()
           if project_name == '':
               continue
           tt = add_project(timesheet, project_name, contents)

    sum_ = 0.0
    for x in timesheet:
        print(f"{x}: {timesheet[x]}")
        sum_ += timesheet[x]
    
    print(f"total: {sum_}")