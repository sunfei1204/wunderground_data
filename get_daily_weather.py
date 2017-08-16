
# coding: utf-8

# This script downloads daily historical weather data from wunderground,
# for citibike analysis project.

# Imports
import sqlite3
import pandas as pd
import boto3

# connect to sqlite database
con = sqlite3.connect('wunderground_daily.db')

def get_wea_data_yearly(year,station):
    """
    Get historical (daily) weather data from wunderground for specified year and station
    """
    url = 'http://www.wunderground.com/history/airport/' + station + '/' + str(year) + '/1/1/CustomHistory.html?dayend=31&monthend=12&yearend=' + str(year) + '&req_city=NA&req_state=NA&req_statename=NA&format=1'
    dat = pd.read_csv(url,parse_dates=True)
    # Name of date column is tz, which varies so we can't hardwire name
    dat.iloc[:,0] =  pd.to_datetime(dat.iloc[:,0])
    dat['date'] = dat.iloc[:,0]
    dat.set_index(dat.date, inplace=True)
    dat['yday']  = dat.date.dt.dayofyear
    dat['month'] = dat.date.dt.month
    dat['year']  = dat.date.dt.year
    dat.rename(columns=lambda x: x.replace(' ', '_'), inplace=True)
    dat['st_code'] = station
    vars_to_keep = ['date','st_code','Max_TemperatureF','Min_TemperatureF','Mean_TemperatureF','year','yday','month','PrecipitationIn','_CloudCover','_Max_Gust_SpeedMPH','_Events']
    dat = dat[vars_to_keep]
    dat.rename(columns={'Max_TemperatureF':'max_temp','Min_TemperatureF':'min_temp','Mean_TemperatureF':'mean_temp','PrecipitationIn':'precip_In','_CloudCover':
        'cloud_cover','_Max_Gust_SpeedMPH':'max_gust_mph','_Events':'events'},inplace=True)

    return dat

# Load list of stations
sta_list = pd.read_csv('USAirportWeatherStations.csv')

years = range(1950,2017)
for sta in stcodes:
    print('getting data for ' + sta )
    for year in years:
        try:
            dat = get_wea_data_yearly(year,sta)
            if (dat.shape[0]!=0):

                # Write to sql database
                dat.to_sql("wea",con,if_exists='append',index=False)

                # write to AWS S3 bucket
                s3 = boto3.resource('s3')
                key_name = sta + '_' + str(year) + '.csv'
                data = dat.to_csv(None,index=False)
                s3.Bucket('wundergrounddaily').put_object(Key=key_name, Body=data)

        except:
            pass

            del dat
