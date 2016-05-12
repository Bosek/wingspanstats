# db_create.py
# Author: Valtyr Farshield
# Author: Tomas Bosek

import os
import urllib2
import gzip
import json
import sys
import re
from StringIO import StringIO
from rules.statsconfig import StatsConfig
from datetime import datetime


def zkill_fetch(year, month, page_nr):
    headers = {
        "User-Agent": "WINGSPAN Statistics, Mail: bosektom@gmail.com",
        "Accept-encoding": "gzip"
    }

    # WiNGSPAN Delivery Network
    corporation_ids = ",".join([str(corp) for corp in StatsConfig.CORP_IDS])
    url = "https://zkillboard.com/api/kills/corporationID/" \
        "{}/year/{}/month/{}/page/{}/".format(
            corporation_ids,
            year,
            month,
            page_nr,
        )

    try:
        request = urllib2.Request(url, None, headers)
        response = urllib2.urlopen(request)
    except urllib2.URLError as e:
        print "[Error]", e.reason
        return None

    if response.info().get("Content-Encoding") == "gzip":
        buf = StringIO(response.read())
        f = gzip.GzipFile(fileobj=buf)
        data = f.read()
    else:
        data = response.read()

    return data


def extract_data(year, month):
    print "Trying to extract killmails from {}-{}".format(year, month)

    db_dir = os.path.join(
        StatsConfig.DATABASE_PATH,
        "{}-{:02d}".format(year, month)
    )
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)

    page_nr = 1
    requests = 0
    while True:
        data = zkill_fetch(year, month, page_nr)
        requests += 1

        # try to parse JSON received from server
        try:
            parsed_json = json.loads(data)
        except ValueError as e:
            print "[Error]", e
            return

        if len(parsed_json) > 0:
            file_name = os.path.join(
                db_dir,
                "{}-{:02d}_{:02d}.json".format(year, month, page_nr)
            )
            with open(file_name, 'w') as f_out:
                f_out.write(data)

        if len(parsed_json) < 200:
            break
        else:
            page_nr += 1
    return requests


def get_daterange(start_range, end_range):
    regstr = "^([0-9]{4})-(0?[1-9]|1[012])$"

    start = re.search(regstr, start_range) if start_range else None
    end = re.search(regstr, end_range) if end_range else None

    if start and not end:
        return [{'year': int(start.group(1)), 'month': int(start.group(2))}]
    elif start and end:
        years_delta = int(end.group(1)) - int(start.group(1))
        daterange = list()
        for year in range(int(start.group(1)), int(end.group(1))+1):
            for month in range(1, 13):
                if year == int(start.group(1)) and month < int(start.group(2)):
                    continue
                if year == int(end.group(1)) and month > int(end.group(2)):
                    break
                daterange.append({'year': year, 'month': month})
        return daterange
    else:
        return None


def main():
    args = sys.argv

    daterange = get_daterange(args[1] if len(args) >= 2 else None, args[2] if len(args) >= 3 else None)
    if not daterange:
        print "You have to specify the start date and optionally the end date in format YYYY-MM"
        return

    start_time = datetime.now()
    requests = 0
    for date in daterange:
        requests += extract_data(date['year'], date['month'])

    end_time = datetime.now()
    print "Extraction done in {} seconds".format((end_time-start_time).seconds)
    print "Sent {} requests".format(requests)

if __name__ == "__main__":
    main()
