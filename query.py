from twikit import Client, TooManyRequests
import time
from datetime import datetime
import csv
from configparser import ConfigParser
from random import randint
import asyncio


MINIMUM_TWEETS = 1000
# QUERY = '( #VoteBlue OR #VoteTheBlutToStopTheStupid OR #NeverTrump OR #TrumpIsNotFitForOffice OR #TrumpIsALaughingStock OR #TrumpisaNationalDisgrace OR #TrumpIsNotWell OR #savedemocracy OR #BidenHarris2024) lang:en '
# QUERY = '(#VoteRed OR #NeverKalama OR #DrunkKamala OR #TrumpPence2024 OR #TRUMP2024ToSaveAmerica OR #TooBigToRig OR #Maga OR #VoteMaga OR #StopTheSteal) lang:en '
# QUERY = ' ( #FDT) lang:en '
QUERY = ' ( #FDT) lang:en until:2024-11-01 since:2024-10-01' #UnhingedKamala

#Democrat --> #VoteBlue, #FDT, #NeverTrump

#cheating #TrumpCheated #TrumpIsAGlobalLaughingStock #TrumpIsAnExistentialThreat #TrumpIsACoward #trumpisinsane #TrumpIsALiarandACriminal #impeachhim #UnfitForOffice #NeverTrump #recountthevotes #RecountEveryVote #RecountNow #WeDemandARecount"


async def get_tweets(tweets):
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
with open('tweets_democrat_FDT_20241101_20241001.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Tweet_count', 'Username', 'Text', 'Created At', 'Retweets', 'Likes'])



#* authenticate to X.com
#! 1) use the login credentials. 2) use cookies.
client = Client(language='en-US', user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:132.0) Gecko/20100101 Firefox/132.0')
# client.login(auth_info_1=username, auth_info_2=email, password=password)
# client.save_cookies('cookies.json')

client.load_cookies('cookies.json')

async def main_function():

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
            tweet_count += 1
            tweet_data = [tweet_count, tweet.user.name, tweet.text, tweet.created_at, tweet.retweet_count, tweet.favorite_count]

            with open('tweets_democrat_FDT_20241101_20241001.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(tweet_data)

        print(f'{datetime.now()} - Got {tweet_count} tweets')


    print(f'{datetime.now()} - Done! Got {tweet_count} tweets found')

asyncio.run(main_function())