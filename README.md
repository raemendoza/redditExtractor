# Reddit Extractor
By @raemendoza

## Purpose
This project is a preliminary step of creating an affiliation dictionary for Google Trends timeline extraction. The purpose of this code includes extracting token data from Reddit using PRAW,
processing and filtering the tokens, and running various analyses on the token list such as word-frequency analyses, bigram distributions, and comparisons across separate extractions for consistency checks.

## Requiremenets
This project was prepared through PyCharm and uses the packages in the requirements.txt file.
In order to use PRAW, you need a Reddit API token.

## Code Index (In procedural order)
- extract(category).py files are the main token extraction scripts that pull tokens from a text file containing the list of subreddits to utilize.
- analyzeFreq.py contains the token processor, a csv to pickle converter for the list, and word frequency analysis.
- compareLists.py contains a comparer for two extractions and a function to find top shared words across three extractions.
- analyzeLexicon.py contains a bigram generator and a part-of-speech tagger for word-frequency analyses made through analyzeFreq
- subMembers.py contains a function to obtain the member counts for a given list of subreddits in a text file.
