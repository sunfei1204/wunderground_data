# wunderground_data

- I often find myself using wunderground data in various projects; it is very simple and easy to download yearly csv files of daily weather at any airport station.

- I decided that instead of always downloading the files, I would download them all once and put them in a sql database that can be queried from any project.

- This is in progress; I plan to make the database publicly available for others to use when it is done.

### Data gathering
- Raw data was downloaded and put in a sqlite database w/ *wea_to_sql.py*. The raw files for each station and year were also saved to an AWS S3 bucket.


### Cleaning

- Data was then cleaned with the script *clean_wea_data.py*. Cleaned data was saved to a separate table in the sqlite database. Combined files for each station were also saved to a S3 bucket.

Data meeting the following criteria were considered bad and NAN'd:
- temp < -100 (applied to *mean_temp*, *max_temp*, and *min_temp*)
- temp > 150 (applied to *mean_temp*, *max_temp*, and *min_temp*)
- *max_temp* < *min temp*
- temp = -99999 (used as bad flag in raw data??)
- *max_gust_mph* > 300
- *precip_In* > 50

### Access to data
Raw and cleaned data were uploaded to a public AWS S3 bucket: 'wundergrounddaily'
