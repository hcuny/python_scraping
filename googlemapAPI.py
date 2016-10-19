import googlemaps
from datetime import datetime
import pandas as pd
import re
import numpy as np
import urllib.request
from urllib.parse import urlparse                                                
import json  

#gmaps = googlemaps.Client(key='AIzaSyCdbsnlk9x0fOyoPm1CMWeEqfSC_U3HX5g')

def zipcd(full_ad):
    gmaps = googlemaps.Client(key='AIzaSyCdbsnlk9x0fOyoPm1CMWeEqfSC_U3HX5g')
    n=len(full_ad)
    zipc=[]
    for i in range(n):
        try:
            geocode_result = gmaps.geocode(full_ad[i])
            formate_ad=geocode_result[0]['formatted_address']
            print(formate_ad)
            zp=formate_ad.split(',')[-2].split(' ')[2]
            zipc.append(zp)
        except:
            zipc.append(formate_ad)
            print(i, 'cannot be read')
            continue
    return(zipc) #c:code
	


def dis_mat(ad):    
    gmaps_m = googlemaps.Client(key='AIzaSyCdbsnlk9x0fOyoPm1CMWeEqfSC_U3HX5g')
    now = datetime.now()
    dist=[]
    time=[]
    for i in range(len(ad)):
        try:
            distance_result = gmaps_m.distance_matrix(ad[i],"101 Manning Drive, NC", departure_time=now)
            if (distance_result==[]):
                print(i,'th is problemmatic')
                dist.append(ad[i])
                time.append(ad[i])
                
            else:
                dist.append((distance_result['rows'][0]['elements'][0]['distance']['text']))
                time.append(distance_result['rows'][0]['elements'][0]['duration']['text'])
                print(i, 'is good')
        except:
            print(i,'th ad cannot be read')
            dist.append(ad[i])
            time.append(ad[i])
            continue
    
    return(dist, time)
	
	
def fileprocess(path):
    xls = pd.ExcelFile(path)
    df = xls.parse('Sheet1')

    org_zip=df['ZIP'].tolist()
    det_null=pd.isnull(df['ADDRESS_LINE2'])
	
    ads=[]
    adfull=[]
    for i in range(len(org_zip)):
        if (det_null[i]==True):
            ads.append(df['ADDRESS_LINE1'][i])
        else:
            ads.append(df['ADDRESS_LINE1'][i]+df['ADDRESS_LINE2'][i])
    
    for i in range(len(org_zip)):
        adfull.append(str(ads[i])+', '+str(df['CITY'][i])+', '+str(df['STATE'][i]))
		
    return adfull
		

if __name__ == "__main__" :
    address=fileprocess('Y://Code//address.xls')
    zipcode=zipcd(address)
    for ele in zipcode:
        print(ele)




