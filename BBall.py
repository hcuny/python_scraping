from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import pandas as pd

# Fetzer
def fetzer_search():
    dict_id={'FetzerGymA':'9098585f-7c43-49c3-bf5d-b3b6e7ac914a','FetzerGymB':'2011c53e-b4c5-437d-b51e-c316653d72d0'}

    homepage='https://campusrec.oasis.unc.edu/FacilityScheduling/FacilitySchedule.aspx'

    for ele in dict_id.keys():
        start=[]
        end=[]
        subject=[]
        
        website='{}?FacilityId={}'.format(homepage,dict_id[ele])
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

            #print(start)
            #print(end)
            #print(subject)
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





def timetable():
    dict_id={'FetzerGym':'9098585f-7c43-49c3-bf5d-b3b6e7ac914a','Wollen':'c879fb7c-0882-49f5-b48a-1c9255b8d02d'}
    
    homepage='https://campusrec.oasis.unc.edu/FacilityScheduling/FacilityDetails.aspx'
    
    for ele in dict_id.keys():
        
        start=[]
        end=[]
        day=[]
        
        website='{}?FacilityId={}'.format(homepage,dict_id[ele])
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