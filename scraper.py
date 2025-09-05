import asyncio
from twikit import Client
import csv
import time
import os

# Configuration
USERNAME = ''  # Your Twitter username
EMAIL = ''  # Your Twitter email
PASSWORD = ''  # Your Twitter password
QUERY = 'bitcoin lang:en'  # Search for Bitcoin-related tweets in English
TARGET_TWEET_COUNT = 5000  # Number of tweets to scrape
OUTPUT_FILE = 'tweets.csv'  # Output CSV file
COOKIES_FILE = 'cookies.json'  # File to store cookies for reusing login session


async def main():
    # Initialize the client
    client = Client('en-US')

    # Load cookies if they exist to avoid re-login
    if os.path.exists(COOKIES_FILE):
        client.load_cookies(COOKIES_FILE)
        print("Loaded cookies from file.")
    else:
        # Login if no cookies
        await client.login(
            auth_info_1=USERNAME,
            auth_info_2=EMAIL,
            password=PASSWORD
        )
        # Save cookies for future use
        client.save_cookies(COOKIES_FILE)
        print("Logged in and saved cookies.")

    # List to store tweets
    all_tweets = []
    cursor = None
    fetched_count = 0

    print(f"Starting to scrape tweets for query: '{QUERY}'")

    while fetched_count < TARGET_TWEET_COUNT:
        try:
            # Search tweets (use 'Latest' for real-time recent tweets)
            tweets = await client.search_tweet(
                query=QUERY,
                product='Latest',
                count=20,  # Max per request; adjust if needed, but 20 is safe to avoid rate limits
                cursor=cursor
            )

            if not tweets:
                print("No more tweets found.")
                break

            # Process tweets
            for tweet in tweets:
                all_tweets.append({
                    'id': tweet.id,
                    'text': tweet.text,
                    'created_at': tweet.created_at,
                    'user': tweet.user.screen_name,
                    'favorite_count': tweet.favorite_count,
                    'retweet_count': tweet.retweet_count
                })
                fetched_count += 1
                if fetched_count >= TARGET_TWEET_COUNT:
                    break

            # Update cursor for next page
            cursor = tweets.next_cursor

            print(f"Fetched {fetched_count} tweets so far...")

            # Sleep to avoid rate limits (Twitter limits requests; adjust as needed)
            await asyncio.sleep(5)  # 5 seconds delay between requests

        except Exception as e:
            print(f"Error occurred: {e}")
            # Wait longer if rate limited
            if 'rate limit' in str(e).lower():
                print("Rate limit hit. Sleeping for 15 minutes.")
                await asyncio.sleep(900)  # 15 minutes
            else:
                await asyncio.sleep(10)  # General error sleep

    # Save to CSV
    if all_tweets:
        keys = all_tweets[0].keys()
        with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, keys)
            writer.writeheader()
            writer.writerows(all_tweets)
        print(f"Saved {len(all_tweets)} tweets to {OUTPUT_FILE}")
    else:
        print("No tweets fetched.")

# Run the async main function
asyncio.run(main())
