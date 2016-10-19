import json
import re

def read_twitter(path):
    file_path=path
    tweets_file=open(file_path,"r")

    tweets_data = []
    for line in tweets_file:
        try:
            tweet = json.loads(line)
            tweets_data.append(tweet)
        except:
            continue
    #tweet = json.loads(tweets_file)
    
def make_df(tweet):
    tweets_df = pd.DataFrame()
    tweets_df['text'] = [tweet['statuses'][i]['text'] for i in range(len(tweet['statuses']))]
    tweets_df['hashtag']=[tweet['statuses'][i]['entities']['hashtags'][0]['text'] 
                        if len(tweet['statuses'][i]['entities']['hashtags'])>0 else "Null" for i in range(len(tweet['statuses']))]
    tweets_df['language']=[tweet['statuses'][i]['metadata']['iso_language_code'] for i in range(len(tweet['statuses']))]

    #tweets_df['country']=[tweet['statuses'][i]['place']['country'] if tweet['place'] != None else None]
    #tweets['country'] = map(lambda tweet['statuses']: tweet['statuses']['place']['country'] if tweet['place'] != None 
    #                         else None, tweets_data)
    
    #change text type unicode-->str
    tweets_df['text']=[tweets_df['text'][i].encode('ascii','ignore') for i in range(len(tweets_df['text']))]
    tweets_df['language']=[tweets_df['language'][i].encode('ascii','ignore') for i in range(len(tweets_df['language']))]
    
    return tweets_df
    
    

def senti_dictionary(path)#'Y://data//python//AFINN-111.txt'

    senti_word=open(path)
    wordlst=[re.findall('([a-z]+)',line)[0] for line in senti_word]
    scorelst=[-int(re.findall('([0-9]+)',line)[0]) if '-' in line
              else int(re.findall('([0-9]+)',line)[0]) for line in senti_word]
    
    dic_senti=dict(zip(wordlst,scorelst))
    
    return dic_senti



def sentimental_analysis(dic_senti,tweets_df):
    f=lambda x: dic_senti[x] if x in dic_senti.keys() else 0
    score=[]
    dic_score={}
    for i in range(len(tweets_df)):
        try:
            if tweets_df['language'][i]!='en':
                continue
            else:
                #score=0
                #lst=tweets_df['text'][i].split(" ")
                sc=sum([f(x) for x in tweets_df['text'][i].split(" ")])
                score.append(sc)
                dic_score[i]=sc

        except:
            print '?'
            
if __name__=='__main__':
