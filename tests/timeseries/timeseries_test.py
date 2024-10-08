#  Copyright (c) 2024
#  United States Army Corps of Engineers - Hydrologic Engineering Center (USACE/HEC)
#  All Rights Reserved.  USACE PROPRIETARY/CONFIDENTIAL.
#  Source may not be released without written approval from HEC

from datetime import datetime

import pandas as pd
import pytest
import pytz

import cwms.api
import cwms.timeseries.timeseries as timeseries
from tests._test_utils import read_resource_file

_MOCK_ROOT = "https://mockwebserver.cwms.gov"
_VERS_TS_JSON = read_resource_file("versioned_num_ts.json")
_UNVERS_TS_JSON = read_resource_file("unversioned_num_ts.json")
_TS_GROUP = read_resource_file("time_series_group.json")


@pytest.fixture(autouse=True)
def init_session():
    cwms.api.init_session(api_root=_MOCK_ROOT)


def test_get_timeseries_unversioned_default(requests_mock):
    requests_mock.get(
        f"{_MOCK_ROOT}"
        "/timeseries?office=SWT&"
        "name=TEST.Text.Inst.1Hour.0.MockTest&"
        "unit=EN&"
        "begin=2008-05-01T15%3A00%3A00%2B00%3A00&"
        "end=2008-05-01T17%3A00%3A00%2B00%3A00&"
        "page-size=500000",
        json=_UNVERS_TS_JSON,
    )

    timeseries_id = "TEST.Text.Inst.1Hour.0.MockTest"
    office_id = "SWT"

    # explicitly format begin and end dates with default timezone as an example
    timezone = pytz.timezone("UTC")
    begin = timezone.localize(datetime(2008, 5, 1, 15, 0, 0))
    end = timezone.localize(datetime(2008, 5, 1, 17, 0, 0))

    data = timeseries.get_timeseries(
        ts_id=timeseries_id, office_id=office_id, begin=begin, end=end
    )
    assert data.json == _UNVERS_TS_JSON
    assert type(data.df) is pd.DataFrame
    assert "date-time" in data.df.columns
    assert data.df.shape == (4, 3)


def test_get_timeseries_group_default(requests_mock):
    requests_mock.get(
        f"{_MOCK_ROOT}"
        "/timeseries/group/USGS%20TS%20Data%20Acquisition?office=CWMS&"
        "category-id=Data%20Acquisition",
        json=_TS_GROUP,
    )

    group_id = "USGS TS Data Acquisition"
    category_id = "Data Acquisition"
    office_id = "CWMS"

    data = timeseries.get_timeseries_group(
        group_id=group_id, category_id=category_id, office_id=office_id
    )

    assert data.json == _TS_GROUP
    assert type(data.df) is pd.DataFrame
    assert "timeseries-id" in data.df.columns
    assert data.df.shape == (11, 5)
    values = data.df.to_numpy().tolist()
    assert values[0] == [
        "LRL",
        "Buckhorn-Lake.Stage.Inst.5Minutes.0.USGS-raw",
        6245109,
        "59905",
        0,
    ]


def test_create_timeseries_unversioned_default(requests_mock):
    requests_mock.post(
        f"{_MOCK_ROOT}/timeseries?"
        f"create-as-lrts=False&"
        f"override-protection=False"
    )

    data = _UNVERS_TS_JSON
    timeseries.store_timeseries(data=data)

    assert requests_mock.called
    assert requests_mock.call_count == 1


def test_get_timeseries_versioned_default(requests_mock):
    requests_mock.get(
        f"{_MOCK_ROOT}"
        "/timeseries?office=SWT&"
        "name=TEST.Text.Inst.1Hour.0.MockTest&"
        "unit=EN&"
        "begin=2008-05-01T15%3A00%3A00%2B00%3A00&"
        "end=2008-05-01T17%3A00%3A00%2B00%3A00&"
        "page-size=500000&"
        "version-date=2021-06-20T08%3A00%3A00%2B00%3A00",
        json=_VERS_TS_JSON,
    )

    timeseries_id = "TEST.Text.Inst.1Hour.0.MockTest"
    office_id = "SWT"

    # explicitly format begin and end dates with default timezone as an example
    timezone = pytz.timezone("UTC")
    begin = timezone.localize(datetime(2008, 5, 1, 15, 0, 0))
    end = timezone.localize(datetime(2008, 5, 1, 17, 0, 0))
    version_date = timezone.localize(datetime(2021, 6, 20, 8, 0, 0))

    data = timeseries.get_timeseries(
        ts_id=timeseries_id,
        office_id=office_id,
        begin=begin,
        end=end,
        version_date=version_date,
    )
    assert data.json == _VERS_TS_JSON
    assert type(data.df) is pd.DataFrame
    assert "date-time" in data.df.columns
    assert data.df.shape == (4, 3)


def test_create_timeseries_versioned_default(requests_mock):
    requests_mock.post(
        f"{_MOCK_ROOT}/timeseries?"
        f"create-as-lrts=False&"
        f"override-protection=False"
    )

    data = _VERS_TS_JSON
    timeseries.store_timeseries(data=data)

    assert requests_mock.called
    assert requests_mock.call_count == 1
