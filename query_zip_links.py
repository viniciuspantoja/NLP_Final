"""This class will be responsible for dealing with gdelt database, retrieving
 the raw data (links and information). It loops over all the zips and extract the csvs
 from the desired date. This will be used as an input for the query_key_words class
 that will filter the news links with the desired keywords.

 You can query a specific day, or a month. For the second choice, leave the day
 input empty"""

import requests
import pandas as pd
import os
import re
from zipfile import ZipFile
from urllib.request import urlopen


class queryZip():
    def __init__(self, month = 12, year = 2015, day = None):

        self.day = day
        self.month = month
        self.year = year

        return None

    def get_date(self,x):

        if self.day == None:
                return re.findall('gdeltv2/{}{}'.format(self.year,self.month),x)

        else:
            return re.findall('gdeltv2/{}{}{}'.format(self.year,self.month,self.day),x)


    def get_zip_links(self):
        zip_links = requests.get('http://data.gdeltproject.org/gdeltv2/masterfilelist.txt').content
        zip_links = zip_links.decode("utf-8")

        final_zip_list = []

        for item in zip_links.split():
            if len(re.findall('export.CSV.zip', item))>0:
                final_zip_list.append(item)

        # Here we filter out the zip links that are within our time range.
        final_zip_list = [x for x in final_zip_list if self.get_date(x)]

        return final_zip_list


    def get_links_from_zip(self,zip):
        cols = ['GLOBALEVENTID','MonthYear','Year','SOURCEURL']
        try:

            cols_raw =['GLOBALEVENTID','SQLDATE','MonthYear','Year','FractionDate','Actor1Code','Actor1Name','Actor1CountryCode','Actor1KnownGroupCode','Actor1EthnicCode','Actor1Religion1Code','Actor1Religion2Code','Actor1Type1Code','Actor1Type2Code','Actor1Type3Code','Actor2Code','Actor2Name','Actor2CountryCode','Actor2KnownGroupCode','Actor2EthnicCode','Actor2Religion1Code','Actor2Religion2Code','Actor2Type1Code','Actor2Type2Code','Actor2Type3Code','IsRootEvent','EventCode','EventBaseCode','EventRootCode','QuadClass','GoldsteinScale','NumMentions','NumSources','NumArticles','AvgTone','Actor1Geo_Type','Actor1Geo_FullName','Actor1Geo_CountryCode','Actor1Geo_ADM1Code','Actor1Geo_ADM2Code','Actor1Geo_Lat','Actor1Geo_Long','Actor1Geo_FeatureID','Actor2Geo_Type','Actor2Geo_FullName','Actor2Geo_CountryCode','Actor2Geo_ADM1Code','Actor2Geo_ADM2Code','Actor2Geo_Lat','Actor2Geo_Long','Actor2Geo_FeatureID','ActionGeo_Type','ActionGeo_FullName','ActionGeo_CountryCode','ActionGeo_ADM1Code','ActionGeo_ADM2Code','ActionGeo_Lat','ActionGeo_Long','ActionGeo_FeatureID','DATEADDED','SOURCEURL']

            df = pd.read_csv(zip, compression='zip', sep='\t', header = None, names = cols_raw, index_col=False)

            if self.day == None:
                df = df[(df['Actor1Geo_CountryCode'] == 'US')&(df['MonthYear'] == int(self.year+self.month))][cols]

            else:
                df = df[(df['Actor1Geo_CountryCode'] == 'US')&(df['SQLDATE'] == int(self.year+self.month+self.day))][cols]

            return df

        except:
            return pd.DataFrame(columns = cols)

    def build_all_links(self,zip_list):
        cols = ['GLOBALEVENTID','MonthYear','Year','SOURCEURL']
        count = 0
        link_list = pd.DataFrame(columns = cols)

        for item in zip_list:

            df = self.get_links_from_zip(item)


            link_list = pd.concat([link_list,df])


        return link_list


    def final(self):
        zip_links = self.get_zip_links()

        return self.build_all_links(zip_links)
