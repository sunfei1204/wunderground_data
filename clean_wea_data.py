
# coding: utf-8


import boto3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# make plots look nice
plt.rcParams['font.size'] = 14
plt.rcParams['axes.labelsize'] = 'large'
plt.rcParams['xtick.labelsize'] = 'large'
plt.rcParams['ytick.labelsize'] = 'large'
plt.rcParams['lines.linewidth'] = 3

import sqlite3
con = sqlite3.connect('/Users/Andy/Projects/wunderground_data/wunderground_daily.db')


def clean_data(dat):

    dat.date = pd.to_datetime(dat.date)

    Tmin = -100
    Tmax =  150

    dat.where(dat.mean_temp>Tmin, inplace=True)
    dat.where(dat.mean_temp<Tmax, inplace=True)

    dat.where(dat.min_temp>Tmin, inplace=True)
    dat.where(dat.min_temp<Tmax, inplace=True)

    dat.where(dat.max_temp>Tmin, inplace=True)
    dat.where(dat.max_temp<Tmax, inplace=True)

    dat.where(dat.max_temp > dat.min_temp, inplace=True)

    dat.drop_duplicates(inplace=True)

    # convert 'Trace' precip to 0.01
    # I want to preserve the fact that there was rain, but very small amount
    # Also, sometimes precip_In is read in as float, not object? (maybe if it contains no 'T'?)
    if dat.precip_In.dtype=='object':
        dat['precip_In'].loc[dat['precip_In']=='T'] = '0.01'
        dat.precip_In = pd.to_numeric(dat.precip_In)

    # some precip values are way too large
    # According to weather.com :The most extreme 24-hour rainfall total on record
    # in the U.S. is 42.0 inches near Alvin, Texas, between 7 a.m. July 25 and 7 a.m.
    # July 26, 1979.
    # I will keep values < 50
    dat.where(dat.precip_In<50, inplace=True)

    # screen unreasonably high winds
    dat.where(dat.max_gust_mph<300, inplace=True)

    return dat


# If processing stops/interupts and need to restart
#sta_df = pd.read_csv('USAirportWeatherStations.csv')
#sta_df.head()
#st_list = sta_df['airportCode'].values
#st_list
#sta_df[sta_df.airportCode=='KUCY']



for sta in st_list:
    print('cleaning ' + sta)
    try:
        dat = pd.read_sql_query("SELECT * FROM wea WHERE st_code=? ",con,params=[sta])
        #dat.head()
        dat = clean_data(dat)
        #dat.to_csv('cleaned/' + sta + '_cleaned.csv',index=False)

        # write to S3
        s3 = boto3.resource('s3')
        #fname = csv_name
        key_name = 'cleaned/' + sta + '_cleaned.csv'
        #data = open(fname, 'rb')
        data = dat.to_csv(None,index=False)
        s3.Bucket('wundergrounddaily').put_object(Key=key_name, Body=data)

        # write to 'clean' database table
        dat.to_sql("wea_clean",con,if_exists='append',index=False)
        del dat
    except:
        pass
