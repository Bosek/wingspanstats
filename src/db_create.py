# db_create.py
# Author: Valtyr Farshield
# Author: Tomas Bosek

import os
import urllib2
import gzip
import json
from StringIO import StringIO
from rules.statsconfig import StatsConfig
from datetime import datetime


def zkill_fetch(year, month, page_nr):
    headers = {
        "User-Agent": "Wingspan Stats Fork, Mail: bosektom@gmail.com",
        "Accept-encoding": "gzip"
    }

    # The Wingspan LOGO Alliance
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


def main():
    start = datetime.now()
    requests = 0
    requests += extract_data(2014, 7)
    requests += extract_data(2014, 8)
    requests += extract_data(2014, 9)
    requests += extract_data(2014, 10)
    requests += extract_data(2014, 11)
    requests += extract_data(2014, 12)

    requests += extract_data(2015, 1)
    requests += extract_data(2015, 2)
    requests += extract_data(2015, 3)
    requests += extract_data(2015, 4)
    requests += extract_data(2015, 5)
    requests += extract_data(2015, 6)
    requests += extract_data(2015, 7)
    requests += extract_data(2015, 8)
    requests += extract_data(2015, 9)
    requests += extract_data(2015, 10)
    requests += extract_data(2015, 11)
    requests += extract_data(2015, 12)

    requests += extract_data(2016, 1)
    requests += extract_data(2016, 2)
    requests += extract_data(2016, 3)
    requests += extract_data(2016, 4)
    end = datetime.now()
    print "Extraction done in {} seconds".format((end-start).seconds)
    print "Sent {} requests".format(requests)

if __name__ == "__main__":
    main()
