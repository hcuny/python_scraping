__author__      = "C.Y. Huang"

from bs4 import BeautifulSoup
import json
from urllib.request import urlopen
import re
import pandas as pd
import pyprind

def fetzer_search():
    
    court_id={'FetzerGymA':'9098585f-7c43-49c3-bf5d-b3b6e7ac914a',
             'FetzerGymB':'2011c53e-b4c5-437d-b51e-c316653d72d0'}

    homepage='https://campusrec.oasis.unc.edu/FacilityScheduling/FacilitySchedule.aspx'

    for ele in sorted(court_id.keys()):
        start=[]
        end=[]
        subject=[]
        
        website='{}?FacilityId={}'.format(homepage,court_id[ele])
        readpage=urlopen(website).read().decode('utf-8')
        soup = BeautifulSoup(readpage,'html.parser')
        activity_info = soup.findAll('span', {'class': 'dxeBase_Metropolis'})
        time_info = [obj.get_text() for obj in activity_info]
        
        
        try:
            for elem in time_info:
                if ('AM' in elem or 'PM' in elem) and ('-' in elem):
                    start.append(elem)
                elif ('AM' in elem or 'PM' in elem) and ('-' not in elem):
                    end.append(elem)
                elif 'Subject:' in elem:
                    subject.append(elem.split(':')[1])


            df = pd.DataFrame(
                {'start': start,
                 'end': end,
                 'subject':subject
                 })
            df=df[['start','end','subject']]
        
        except:
            print("parsing error!")
            continue
        
        print(ele)
        
        print('\n')
        
        if df.shape[0]==0:
            print("Congratulations! No activity in {} today!".format(ele))
        else:
            print(df)
        print("--------------------------------------------------------------------------------")


        
def wollen_search():
    
    court_id={'WollenCourt1':'c879fb7c-0882-49f5-b48a-1c9255b8d02d',
             'WollenCourt2':'bc30a713-c95a-4b93-953d-85c903cdbc14',
             'WollenCourt3':'a626ab66-c531-431b-847a-c06e9b642284',
             'WollenCourt4':'a3c399e2-138f-4318-b49f-3ffb283e8310',
             'WollenCourt5':'0b3bec50-94cc-4b68-a4c1-8e0521dea8a1',
             'WollenCourt6':'ff34b2ea-ca41-4b20-9ffd-244f7591e6b9',
             'WollenCourt7':'bf168d03-c089-48ba-bc7d-1e6fa4e2541a',
             'WollenCourt8':'f822f2b3-bb54-41b4-8185-8d079b185691'
            }

    homepage='https://campusrec.oasis.unc.edu/FacilityScheduling/FacilitySchedule.aspx'
    
    avail_lst=[]
    
    pbar = pyprind.ProgBar(len(court_id.keys()),monitor=True)
    print('\n')

    for ele in sorted(court_id.keys()):
        start=[]
        end=[]
        subject=[]
        
        website='{}?FacilityId={}'.format(homepage,court_id[ele])
        readpage=urlopen(website).read().decode('utf-8')
        soup = BeautifulSoup(readpage,'html.parser')
        activity_info = soup.findAll('span', {'class': 'dxeBase_Metropolis'})
        time_info = [obj.get_text() for obj in activity_info]
               
        try:
            for elem in time_info:
                if ('AM' in elem or 'PM' in elem) and ('-' in elem):
                    start.append(elem)
                elif ('AM' in elem or 'PM' in elem) and ('-' not in elem):
                    end.append(elem)
                elif 'Subject:' in elem:
                    subject.append(elem.split(':')[1])
                    
            df = pd.DataFrame(
                {'start': start,
                 'end': end,
                 'subject':subject
                 })
            df=df[['start','end','subject']]
        
        except:
            print("parsing error!")
            continue
        
        if df.shape[0]==0:
            avail_lst.append(ele)
        else:
            
            print(ele)
            print('\n')
            print(df)
            print("--------------------------------------------------------------------------------")
            
        pbar.update()
        print('\n')
            
    avail_lst=sorted(avail_lst)
    
    if len(avail_lst)>0:
        print('\n')
        print("Congratulations! No activity in {} today!".format(', '.join(avail_lst)))
        

def timetable():
    court_id={'FetzerGym':'9098585f-7c43-49c3-bf5d-b3b6e7ac914a','Wollen':'c879fb7c-0882-49f5-b48a-1c9255b8d02d'}
    
    homepage='https://campusrec.oasis.unc.edu/FacilityScheduling/FacilityDetails.aspx'
    
    for ele in court_id.keys():
        
        start=[]
        end=[]
        day=[]
        
        website='{}?FacilityId={}'.format(homepage, court_id[ele])
        readpage=urlopen(website).read().decode('utf-8')
        soup = BeautifulSoup(readpage,'html.parser')
        activity_info = soup.findAll('table', {'id': 'ctl00_contentMain_tableHours'})
        time_info = activity_info[0].findAll('tr')[1:]
        for t in time_info:
            lst_time=t.findAll('td')
            day.append(lst_time[0].get_text())
            start.append(lst_time[1].get_text())
            end.append(lst_time[3].get_text())
        df = pd.DataFrame(
                {'start': start,
                 'end': end,
                 'day': day
                 })
        df=df[['start','end','day']]
        print(ele)
        print("--------------------------------------------------------------------------------")
        print(df)
        print('\n')
        
if __name__ == '__main__':
    print('\n')
    print("Loading Today's Activities...........")
    print("================================================================================")
    fetzer_search()
    print("################################################################################")
    print("Facility Opening Time")
    print("################################################################################")
    print('\n')
    timetable()
    
    print("Do you want to check details of Wollen?(y/n)")
    check = input()
    try:
        if check.lower()=='y' or check.lower()=='yes':
            print("Processing...... This may take about 1 minute")
            wollen_search()
        elif check.lower()=='n' or check.lower()=='no':
            print("Search finished, enjoy!")
    except:
        print('Sorry, something went wrong!')
