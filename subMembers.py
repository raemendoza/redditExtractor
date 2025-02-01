import praw
from nltk.corpus import stopwords
import pandas as pd

# Run this on command line to get the stopwords: python -m nltk.downloader stopwords
stop_words = stopwords.words('english')
category = '' # family, romance, spiritual,suicide

# Open txt file with subreddit list separated by lines
with open(f".\\{category}.txt") as f:
    sr_list = [line.rstrip('\n') for line in f]

# Extracts the subscriber count of a given Subreddit list
def main():
    reddit = praw.Reddit(
        client_id="YOUR_REDDIT_CLIENT_ID",
        client_secret="YOUR_REDDIT_CLIENT_SECRET",
        user_agent="YOUR_REDDIT_USER_AGENT",)

# Store data in tokenized data structure

    # Thread titles
    members = {}

    # Iterates over the subreddits in sr_list, printing out each one as a progress bar.
    subreddits = [sr for sr in sr_list]
    for i, subreddit in enumerate(reddit.info(subreddits=subreddits)):
        print(f"Subreddit: {subreddit.display_name} has {subreddit.subscribers} members." )
        members[subreddit.display_name] = subreddit.subscribers

    # Export data into a csv file and return success message
    file_name = 'output_members.csv'
    df = pd.DataFrame([members])
    df.transpose().to_csv(file_name)
    print("File written.")

# Run the program.
if __name__ == "__main__":
    main()
