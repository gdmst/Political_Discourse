import asyncio
from twikit import Client
from configparser import ConfigParser

USERNAME = 'example_user'
EMAIL = 'email@example.com'
PASSWORD = 'password0000'


#* login credentials
config = ConfigParser()
config.read('config.ini')
USERNAME = config['X']['username']
EMAIL = config['X']['email']
PASSWORD = config['X']['password']

# Initialize client
client = Client('en-US')

async def main():
    await client.login(
        auth_info_1=USERNAME,
        auth_info_2=EMAIL,
        password=PASSWORD
    )

asyncio.run(main())

client.save_cookies('cookies.json')