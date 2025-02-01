from nltk import FreqDist
import pandas as pd
import csv
import pickle
from nltk.stem import WordNetLemmatizer
import re
from tqdm import tqdm

# Initiative lemmatizer and regex for numbers and computer term recognition
lemmatizer = WordNetLemmatizer()
numerical_pattern = r"^\d+$"
computer_terms_pattern = r"^(https?|www|com|r)$"

# Quick function reads csv containing tokens and returns all words in a list
def read_csv_to_list(filename):
    with open(filename, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        all_words = []
        counter = 0
        for word in reader:
            all_words += word
            counter += 1
            if counter % 1000000 == 0:
                count = int(str(counter)[:-6])
                print(f'{count} million tokens encoded! ε=ε=ε=ε=┌(;￣▽￣)┘')
        print(f'All tokens encoded: {len(all_words):,}! Conversion to list complete.')

    return all_words

# Quick function to remove digits and computer-related language, then lemmatize the word and return it
def preprocess_word(word):
    lemmatized_word = ''
    if not re.match(numerical_pattern, word):
        if not re.match(computer_terms_pattern, word):
            lemmatized_word = lemmatizer.lemmatize(word.lower())

    return lemmatized_word

def preprocess_words(all_words, filename, batch_size):
    '''
    Runs the preprocessor for all tokens, removes blanks, and dumps into a pickle file

    :param all_words: List of tokenize words in csv format
    :param filename: File name to write pickle file
    :param batch_size: Size of batches to process the data
    :return:
    '''
    processed_words = []
    num_batches = len(all_words) // batch_size + 1

    with tqdm(total=len(all_words), ncols=80, desc="Processing") as pbar:
        for i in range(num_batches):
            batch = all_words[i * batch_size: (i + 1) * batch_size]
            processed_batch = [preprocess_word(word) for word in batch if
                               preprocess_word(word) is not None]
            processed_words.extend(processed_batch)
            pbar.update(len(batch))

    with open(f'{filename.split(".")[0]}_retoken.pickle', 'wb') as f:
        pickle.dump(processed_words, f)
        print(f'Token list saved to {filename.split(".")[0]}_retoken.pickle')

    return None

# Loads pickle file and conducts word frequency analysis for a given size n.
def word_frequency_analysis(filename, n, save_file):
    with open(filename, 'rb') as f:
        all_words = pickle.load(f)
        all_words = [w for w in all_words if w is not None and w != '']
        print(f'Loaded {len(all_words):,} tokens from {filename}. Running frequency analysis...')

    common = FreqDist(all_words).most_common(n)

    df = pd.DataFrame(common[0:], columns=['word', 'count'])
    df['word'] = df['word'].replace('', 'EMPTY')
    df.to_csv(save_file, index=False)
    print(f'Top {n} words saved to {save_file}')

    return common

# Variable calls for functions. Rounds refer to the iteration of reddit token extraction to check for consistency over time; categories refers to the dictionary's category
rounds = ['Round Four']
categories = ['romance', 'spiritual', 'family']
batches = 100000

# # Loop to iterate through all rounds, then all categories, and run the preprocess_words function for each word list, then save them into separate files based on their unique parameters
# for r in rounds:
#     for category in categories:
#         word_list = read_csv_to_list(filename = f'.\\Reddit\\{r}\\Tokens\\Raw Tokens\\{category}_token_full.csv')
#         preprocess_words(all_words = word_list, filename = f'.\\Reddit\\{r}\\Tokens\\Retokenized Pickle Files\\{category}', batch_size = batches)

# # Convert files to pickle files
# for r in rounds:
#     for category in categories:
#         read_csv_to_list(filename = f'.\\Reddit\\{r}\\Tokens\\Raw Tokens\\{category}_token_full.csv')

# # Run Frequency Analysis
# n_size = 5000
# for round_name in rounds:
#      for category in categories:
#          word_frequency_analysis(filename = f'.\\Reddit\\{round_name}\\Tokens\\Retokenized Pickle Files\\{category}_retoken.pickle', n = n_size,
#                                  save_file = f'.\\Reddit\\{round_name}\\Frequency Analyses\\{category}_freq_full_new.csv')
