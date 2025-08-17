import asyncio
from twikit import Client



async def get_user_followers(username):
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

    try:
        user = await client.get_user_by_screen_name(username)
        print(f"Followers of @{username}:")
        async for follower in user.followers:
            print(f"- {follower.screen_name} (ID: {follower.id})")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    target_username = "satyakumar_y" # Replace with the username you want to check
    asyncio.run(get_user_followers(target_username))