import requests
import feedparser
import pandas as pd

import settings as settings
from urllib.parse import urlencode


def get_data_url(product, suburb, brand, surrounding, day):
    params = {
        'Product': product,
        'Suburb': suburb,
        'Day': day,
        'Surrounding': surrounding
    }
    # If brand is not empty
    if brand != '0':
        params['Brand'] = brand

    print(settings.Config.URL + urlencode(params))
    fuel_watch_response = requests.get(settings.Config.URL + urlencode(params))
    fuel_data = feedparser.parse(fuel_watch_response.content)
    fuel_dataframe = pd.DataFrame.from_dict(fuel_data['entries'])
    fuel_dataframe = fuel_dataframe.add_suffix('_' + day)

    return fuel_dataframe


def get_data(product, suburb, brand, surrounding):
    df_today = get_data_url(product, suburb, brand, surrounding, 'today')
    df_tomorrow = get_data_url(product, suburb, brand, surrounding, 'tomorrow')

    if df_tomorrow.empty:
        print('Price is not listed yet.')
        merged_inner = df_today
    else:
        merged_inner = pd.merge(left=df_today, right=df_tomorrow, left_on=(['latitude_today', 'longitude_today']),
                                right_on=(['latitude_tomorrow', 'longitude_tomorrow']))
        merged_inner["price_today"] = merged_inner['price_today'].astype('float')
        merged_inner["price_tomorrow"] = merged_inner['price_tomorrow'].astype('float')

    return merged_inner

