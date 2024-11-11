from twikit import Client, TooManyRequests
import time
from datetime import datetime
import csv
from configparser import ConfigParser
from random import randint
import asyncio


MINIMUM_TWEETS = 10
# QUERY = '#maga'

MINIMUM_TWEETS = 10
QUERY = '(#VoteRed OR #NeverKalama OR #DrunkKamala OR #TrumpPence2024 OR #TRUMP2024ToSaveAmerica OR #TooBigToRig OR #Maga OR #VoteMaga OR #StopTheSteal) lang:en until:2024-11-10 since:2024-01-01'


#* login credentials
config = ConfigParser()
config.read('config.ini')
username = config['X']['username']
email = config['X']['email']
password = config['X']['password']

#* authenticate to X.com
#! 1) use the login credentials. 2) use cookies.
client = Client(language='en-US', user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:132.0) Gecko/20100101 Firefox/132.0')
# client.login(auth_info_1=username, auth_info_2=email, password=password)

# # Create the client instance
# client = Client(user_agent="YourUserAgentHere")

# Define async main function
async def login():
    await client.login(auth_info_1=username, auth_info_2=email, password=password)

client.load_cookies('cookies.json')


# client.save_cookies('cookies.json')

# # get tweets
async def get_tweets():
    tweets = await client.search_tweet(QUERY, product='Top')

    for tweet in tweets:
        print(vars(tweet))
        break

asyncio.run(get_tweets())
