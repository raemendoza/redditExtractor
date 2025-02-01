import praw
from nltk.probability import FreqDist
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import pandas as pd

# Run this on command line to get the stopwords: python -m nltk.downloader stopwords
stop_words = stopwords.words('english')
category = 'romance'

# Open txt file with subreddit list separated by lines
with open(f"D:\\User\\Documents\\{category}.txt") as f:
    sr_list = [line.rstrip('\n') for line in f]

# Function to tokenize data into meaningful words, removing stop words, and returning them in a list.
def process_text(headlines):
    tokens = []
    tokenizer = RegexpTokenizer(r'\w+')
    for line in headlines:
        toks = tokenizer.tokenize(line)
        toks = [t.lower() for t in toks if t.lower() not in stop_words]
        tokens.extend(toks)

    return tokens

# Pull data from reddit
def main():
    reddit = praw.Reddit(
        client_id="YOUR_REDDIT_CLIENT_ID",
        client_secret="YOUR_REDDIT_CLIENT_SECRET",
        user_agent="YOUR_REDDIT_USER_AGENT")

# Store data in tokenized data structure

    # Thread titles
    headlines = set()

    # Submission Captions
    submissions = set()

    # Comments
    comments = set()

    token_full_list = []
    # Iterates over the subreddits in sr_list, printing out each one as a progress bar.
    for sr in sr_list:
        print ('Reading through the r/' +  sr + ' subreddit.')

        # Iterates over the "new" posts in the subreddit with a limit provided (default 1000)
        for submission in reddit.subreddit(sr).new(limit=1000):
            headlines.add(submission.title)

            submissions.add(submission.selftext)
            submission.comments.replace_more(limit=None)
            for comment in submission.comments.list():
                comments.add(comment.body)

        # Process headlines and then add them to a full list through each iteration.
        tokenized_headers = process_text(headlines)
        tokenized_submissions = process_text(submissions)
        tokenized_comments = process_text(comments)

        token_full_list.extend(tokenized_headers)
        token_full_list.extend(tokenized_submissions)
        token_full_list.extend(tokenized_comments)

    # Create frequency list for the full token list with a parameter.
    frequency_list = FreqDist(token_full_list).most_common(5000)

    # Export data into a csv file and return success message.
    file_token = f'{category}_token_full.csv'
    file_name = f'{category}_freq_full.csv'
    pd.DataFrame(token_full_list).to_csv(file_token, index = False)
    pd.DataFrame(frequency_list, columns=['word','count']).to_csv(file_name, index = False)
    print('Excel sheet written successfully.')

# Run the program.
if __name__ == "__main__":
    main()