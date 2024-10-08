#  Copyright (c) 2024
#  United States Army Corps of Engineers - Hydrologic Engineering Center (USACE/HEC)
#  All Rights Reserved.  USACE PROPRIETARY/CONFIDENTIAL.
#  Source may not be released without written approval from HEC
import json
from datetime import datetime

import pytz

import cwms

cwms.api.init_session(
    api_root="http://localhost:7001/swt-data/", api_key="apikey testkey"
)


def run_text_ts_examples():
    print("------Running through text ts examples-------")

    location = """
        {
          "name": "TEST",
          "latitude": 0,
          "longitude": 0,
          "active": true,
          "public-name": "CWMS TESTING",
          "long-name": "CWMS TESTING",
          "description": "CWMS TESTING",
          "timezone-name": "America/Los_Angeles",
          "location-kind": "PROJECT",
          "nation": "US",
          "state-initial": "CA",
          "county-name": "Yolo",
          "nearest-city": "Davis, CA",
          "horizontal-datum": "NAD83",
          "vertical-datum": "NGVD29",
          "elevation": 320.04,
          "bounding-office-id": "SPK",
          "office-id": "SPK"
        }
        """

    print("Storing location TEST")
    cwms.store_location(data=location)

    text_ts = json.loads(
        """
        {
          "office-id": "SPK",
          "name": "TEST.Text.Inst.1Hour.0.MockTest",
          "version-date": "2024-02-12T00:00:00Z",
          "regular-text-values": [
            {
              "date-time": "2024-02-12T00:00:00Z",
              "data-entry-date": "2024-02-12T00:00:00Z",
              "text-value": "Hello, Davis"
              "media-type": "text/plain",
              "filename": "test.txt",
              "quality": 0,
            },
            {
              "date-time": "2024-02-12T01:00:00Z",
              "data-entry-date": "2024-02-12T00:00:00Z",
              "text-value": "Hello, USA"
              "media-type": "text/plain",
              "filename": "test.txt",
              "quality": 0,
            }
          ]
        }
        """
    )
    print(f"Storing text ts {text_ts['name']}")
    cwms.store_text_timeseries(text_ts, False)

    timezone = pytz.timezone("UTC")
    begin = timezone.localize(datetime(2024, 2, 12, 0, 0, 0))
    end = timezone.localize(datetime(2024, 2, 12, 2, 0, 0))
    text_ts_dict = cwms.get_text_timeseries(text_ts["name"], "SPK", begin, end)
    print(text_ts_dict.json)

    print(f"Deleting text ts {text_ts['name']}")
    cwms.delete_text_timeseries(text_ts["name"], "SPK", begin, end)
    text_ts_dict = cwms.get_text_timeseries(text_ts["name"], "SPK", begin, end)
    print(f"Confirming delete of text ts {text_ts['name']}")
    print(text_ts_dict.json)


def run_std_text_examples():
    text_ts = json.loads(
        """
        {
          "id": {
            "office-id": "SPK",
            "id": "HW"
          },
          "standard-text": "Hello, World"
        }
        """
    )
    office_id = text_ts.get("id").get("office-id")
    text_id = text_ts.get("id").get("id")
    print(f"Storing standard text id: {text_id}")
    cwms.store_standard_text(text_ts)
    print(f"Retrieving standard text id: {text_id}")
    print(cwms.get_standard_text(text_id, office_id).json)
    print(f"Deleting standard text id: {text_id}")
    cwms.delete_standard_text(text_id, cwms.DeleteMethod.DELETE_ALL, office_id)
    try:
        cwms.get_standard_text(text_id, office_id)
    except ValueError:
        print(f"Confirmed standard text was deleted: {text_id}")


if __name__ == "__main__":
    run_text_ts_examples()
    run_std_text_examples()
