from .exceptions import NoDataFoundError, ServerError, ClientError
from requests.models import Response
import pandas as pd


def queryCDA(self, endpoint: str, payload: dict, headerList: dict):
    """Send a query.

    Wrapper for requests.get that handles errors and returns response.

    Parameters
    ----------
    endpoint: string
        URL to query
    payload: dict
        query parameters passed to ``requests.get``
    headerList: dict
        headers

    Returns
    -------
    string: query response
        The response from the API query ``requests.get`` function call.
    """

    response = self.get_session().get(endpoint, params=payload, headers=headerList)

    response = self.get_session().get(endpoint, params=payload,
                                      headers=headerList, verify=False)
    raise_for_status(response)
    return response


def raise_for_status(response: Response):
    if response.status_code == 404:
        raise NoDataFoundError(response)
    elif response.status_code >= 500:
        raise ServerError(response)
    elif response.status_code >= 400:
        raise ClientError(response)

    # if response.status_code > 200:

     #   raise Exception(
     #       f'Error Code: {response.status_code} \n Bad Request for URL: {response.url} \n response.text'
     #   )

    return response.json()


def return_df(dict: dict, dict_key: list):
    """Convert output to correct format requested by user
    Parameters
    ----------
    response : Request object
        response from get request
    dict_key : str
        key needed to grab correct values from json decoded dictionary.

    Returns
    -------
    pandas df
    """

    # converts dictionary to df based on the key provided for the endpoint
    temp_dict = dict
    for key in dict_key:
        temp_dict = temp_dict[key]
    df = pd.DataFrame(temp_dict)

    # if timeseries values are present then grab the values and put into dataframe
    if dict_key[-1] == 'values':
        df.columns = [sub['name'] for sub in dict['value-columns']]

        if 'date-time' in df.columns:
            df['date-time'] = pd.to_datetime(df['date-time'], unit='ms')

    return df
