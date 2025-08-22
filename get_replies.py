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


df = pd.read_csv('Source_users_engaged.csv', dtype={'user': str})


parser = argparse.ArgumentParser(description="Process date value")
parser.add_argument('--position', type=int, help='Start position for query')

args = parser.parse_args()
position=int(args.position)


async def get_user_following(username, user_id,position):
    client = Client(language='en-US', user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:132.0) Gecko/20100101 Firefox/132.0')
    # client.login(auth_info_1=username, auth_info_2=email, password=password)
    # client.save_cookies('cookies.json')

    client.load_cookies('cookies.json')

    # Authenticate (replace with your actual credentials or session)
    # client.load_cookies('cookies.json') # Load from saved cookies
    # OR
    # await client.login(
    #     auth_info_1='your_email_or_username',
    #     auth_info_2='your_password'
    # )
    user_followings = None
    following_count = 0
    # total_followings = user.followings_count
    # print(user.id+" count"+str(total_followings))
    while True:
        try:
            if user_followings is None:
                user_followings = await client.get_friends_ids(user_id = user_id, screen_name = username, count=5000)
                print(f'found it')
            else:
                wait_time = randint(5, 10)
                print(f'{datetime.now()} - Getting next followings after {wait_time} seconds ...')
                time.sleep(wait_time)
                user_followings = await user_followings.next()
                # break
            
        except TooManyRequests as e:
            rate_limit_reset = datetime.fromtimestamp(e.rate_limit_reset)
            print(f'{datetime.now()} - Rate limit reached. Waiting until {rate_limit_reset}')
            wait_time = rate_limit_reset - datetime.now()
            time.sleep(wait_time.total_seconds())
            continue

        if not user_followings:
            print(f'{datetime.now()} - No more followings found')
            break
        
        for following in user_followings:
            following_count += 1
            following_data = [following]
            # print(f"- {following.screen_name} (ID: {following.id})")

            dataset_filename = "results/measles/following/following_"+str(position)+"_"+username+".csv"
            with open(dataset_filename, 'a', newline='', encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(following_data)

        print(f'{datetime.now()} - Got {following_count} following')


    print(f'{datetime.now()} - Done! Got {following_count} following found')

if __name__ == "__main__":
    username = df.loc[position, 'username']
    user_id = df.loc[position, 'user']
    print("user_id "+user_id)
    asyncio.run(get_user_following(username, user_id,position))
