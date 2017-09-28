# wunderground_data

## Daily weather data from <https://www.wunderground.com/>, in easy-to-use format.

- I often find myself using historical weather data from <https://www.wunderground.com/> various projects (for example <https://github.com/andypicke/WeatherComparer>); it is very simple and easy to download yearly csv files of daily weather at any US airport station. Instead of always downloading the files, I decided to download them all once and put them in a SQL database that can be queried from any project. I'm making the database publicly available for others to use also.

## Data gathering
- Raw data was downloaded and put in a sqlite database w/ *get_daily_weather.py*. The raw files for each station and year were also saved to an AWS S3 bucket.


## Cleaning

- Data was then cleaned with the script *clean_wea_data.py*. Cleaned data were saved to a separate table in the sqlite database. Combined files for each station were also saved to a S3 bucket.

Data meeting the following criteria were considered bad and NAN'd:
- temp < -100 (applied to *mean_temp*, *max_temp*, and *min_temp*)
- temp > 150 (applied to *mean_temp*, *max_temp*, and *min_temp*)
- *max_temp* < *min temp*
- temp = -99999 (used as bad flag in raw data??)
- *max_gust_mph* > 300
- *precip_In* > 50

## Access to data
- Raw and cleaned data were uploaded to a public AWS S3 bucket: 'wundergrounddaily'
- Cleaned data are in the */cleaned* folder and named as *<station>_cleaned.csv*
- Example: https://s3-us-west-2.amazonaws.com/wundergrounddaily/cleaned/K11R_cleaned.csv

## Updates
- My plan was to write a script to update with new data and set up a chron job to run ~weekly. However, downloading the data from wunderground in this way seems to have been broken. So this is on hold for now until I figure out a new method. It may be that wunderground now requires an API key to download.
- I plan to put the sqlite database containing all the data on S3 also.
