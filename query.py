from twikit import Client, TooManyRequests
import time
from datetime import datetime
import csv
from configparser import ConfigParser
from random import randint
import asyncio
import argparse
import calendar
import json
import pandas as pd

# Create the argument parser
parser = argparse.ArgumentParser(description="Process date value")
parser.add_argument('--start_day', type=int, help='Start date for query')
parser.add_argument('--start_month', type=int, help='Start month for query')

# read 

# Parse the arguments
args = parser.parse_args()

# Access the retstart argument
print(f"Running script with start_day={args.start_day} , start_month = {args.start_month}")
start_day=int(args.start_day)
start_month=int(args.start_month)

last_day = [31, 28, 31, 30, 31, 30]

end_day = ( start_day) % last_day[start_month-1] +1
end_month = start_month

if end_day == 1:
    end_month += 1

date_arg_end = str(end_day).zfill(2)
date_arg_start = str(start_day).zfill(2)

month_arg_str = str(start_month).zfill(2)
month_arg_end = str(end_month).zfill(2)

start_date = '2025-'+month_arg_str+'-'+str(date_arg_start)
end_date = '2025-'+month_arg_end+'-'+str(date_arg_end)

print('start - end ', start_date, end_date)
# start_date = '2025-01-01'
# end_date = '2025-05-31'

#FlagstaffFire (bounding_box:[-105.301758 39.964069 -105.178505 40.09455] OR place:Boulder)

MINIMUM_TWEETS = 100000

#* authenticate to X.com
#! 1) use the login credentials. 2) use cookies.
client = Client(language='en-US', user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:132.0) Gecko/20100101 Firefox/132.0')
# client.login(auth_info_1=username, auth_info_2=email, password=password)
# client.save_cookies('cookies.json')

client.load_cookies('cookies.json')

# meales lang:en until:2025-06-04 since:2025-01-01
# QUERY = 'measles lang:en until:'+end_date+' since:'+start_date

# for user in 
# todo: read file and read source users, to retrieve replies by users only in January 2025

df = pd.read_csv(dir+'Replied_tweets.csv', dtype={'tweet_id': str})

# QUERY = 'to:@'+username+' filter:replies lang:en until:'+end_date+' since:'+start_date
# to: @satyakumar_y filter:replies since:2025-01-01 until:2025-02-01 lang:en

# QUERY = 'measles lang:en retweets_of_status_id:1936268716074807379'

# QUERY = '#FlagstaffFire (bounding_box:[-105.301758 39.964069 -105.178505 40.09455] OR place:Boulder) AND (since:2022-01-01 until:2025-06-09)'
# QUERY = '(from:beatrice_ujan)'


#  texas boudling box (bounding_box:[-106.64719063660635 25.840437651866516 -93.5175532104321 36.50050935248352])
async def get_tweets(tweets, QUERY):
    if tweets is None:
        #* get tweets
        print(f'{datetime.now()} - Getting tweets...')
        tweets = await client.search_tweet(QUERY, product='Latest')
    else:
        wait_time = randint(5, 10)
        print(f'{datetime.now()} - Getting next tweets after {wait_time} seconds ...')
        time.sleep(wait_time)
        tweets = await tweets.next()

    return tweets



# #* login credentials
# config = ConfigParser()
# config.read('config.ini')
# username = config['X']['username']
# email = config['X']['email']
# password = config['X']['password']

#* create a csv file

async def retrieve_all_replies(username):

    dataset_filename = "results/measles/replies/replies_"+username+".csv"
    with open(dataset_filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Source_user', 'Tweet_count', 'Username', 'Tweet_id','In_reply_to', 'Created At', 'Retweets', 'Likes'])



    QUERY = 'to:@'+username+' filter:replies lang:en until:'+end_date+' since:'+start_date

    tweet_count = 0
    tweets = None
    while tweet_count < MINIMUM_TWEETS:

        try:
            # tweets = asyncio.run(get_tweets(tweets))
            if tweets is None:
            #* get tweets
                print(f'{datetime.now()} - Getting tweets...')
                tweets = await client.search_tweet(QUERY, product='Latest')
            else:
                wait_time = randint(5, 10)
                print(f'{datetime.now()} - Getting next tweets after {wait_time} seconds ...')
                time.sleep(wait_time)
                tweets = await tweets.next()
        except TooManyRequests as e:
            rate_limit_reset = datetime.fromtimestamp(e.rate_limit_reset)
            print(f'{datetime.now()} - Rate limit reached. Waiting until {rate_limit_reset}')
            wait_time = rate_limit_reset - datetime.now()
            time.sleep(wait_time.total_seconds())
            continue

        if not tweets:
            print(f'{datetime.now()} - No more tweets found')
            break

        for tweet in tweets:
            # print(type(tweet))
            # break
            tweet_count += 1
            tweet_data = [username, tweet_count, tweet.user.name, tweet.id, tweet.in_reply_to, tweet.created_at, tweet.retweet_count, tweet.favorite_count]
               # Open a file in write mode ('w') and create it if it doesn't exist
                
            article_filename = "results/measles/replies/replies_"+username+"_"+tweet_count+".json"
            with open(article_filename, "w") as file:
                file.write(str(vars(tweet)))

                # json.dump(vars(tweet), file)

            dataset_filename = "results/measles/dataset/replies_"+username+".csv"
            with open(dataset_filename, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(tweet_data)

        print(f'{datetime.now()} - Got {tweet_count} tweets')


    print(f'{datetime.now()} - Done! Got {tweet_count} tweets found')


for i in range(0,702):
    username = df.loc[i, 'username']

    asyncio.run(retrieve_all_replies(username))
    