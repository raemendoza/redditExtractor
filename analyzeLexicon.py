import csv
from nltk import ngrams
import os
import pickle

# Function to create bigrams and generate probability list
def find_bigrams(token_path, num_bigrams, save_bigrams):
    # Create the directory if it doesn't exist
    os.makedirs(os.path.dirname(save_bigrams), exist_ok=True)

    with open(token_path, 'rb') as f:
        tokens = pickle.load(f)

    # Remove empty token
    tokens = [token for token in tokens if token.strip()]

    # Use the nltk ngrams() function to create bigrams
    bigrams = list(ngrams(tokens, 2))

    # Count the frequency of each bigram
    freq_dict = {}
    for bigram in bigrams:
        freq_dict[bigram] = freq_dict.get(bigram, 0) + 1

    # Sort the bigrams by frequency and get the top num_bigrams
    top_bigrams = sorted(freq_dict.items(), key=lambda x: x[1], reverse=True)[:num_bigrams]

    # Calculate the total number of bigrams
    total_bigrams = sum(freq_dict.values())

    # Calculate the probability of each bigram based on its frequency and the total number of bigrams
    bigrams_with_prob = []
    for bigram, freq in top_bigrams:
        prob = freq / total_bigrams
        bigrams_with_prob.append((bigram, prob))

    # Write the bigrams with probabilities to a file
    with open(save_bigrams, 'w') as f:
        for bigram, prob in bigrams_with_prob:
            f.write(f"{str(bigram)}, {prob}\n")

    # Print the number of bigrams found
    print(f"Found {len(top_bigrams)} bigrams.")


# Takes an appropriate word-frequency list and returns the parts of speech for each token
def save_tagged_words(freq_file: str, pos_tags: list):
    # Define file paths for saving the output
    file_dir, _ = os.path.split(freq_file)
    tagged_words_path = os.path.join(file_dir, f"{os.path.basename(freq_file)[:-4]}_tagged_words.txt")

    # PART OF SPEECH TAGS DEFINITION
    print('Loaded frequency file.')
    freq_list = []
    lemmatizer = WordNetLemmatizer()
    with open(freq_file, 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)  # skip the header row
        for row in csv_reader:
            word, freq = row
            lemma = lemmatizer.lemmatize(word)
            freq_list.append((word, int(freq)))

    # Tokenize and tag the words with part of speech
    tagged_words = []
    stop_words = set(stopwords.words('english'))

    for word, freq in freq_list:
        if word.lower() not in stop_words:
            tokens = word_tokenize(word)
            tagged = nltk.pos_tag(tokens)
            pos = tagged[0][1]
            if pos.startswith(tuple(pos_tags)):
                tagged_words.append((tagged[0][0], pos, freq))
    print('Written part-of-speech tags!')

    # Save the tagged words as a text file
    with open(tagged_words_path, 'w') as f:
        f.write('\n'.join([f"{word} ({pos}): {freq}" for word, pos, freq in tagged_words]))
        print('Words tagged and saved to:', tagged_words_path)

    return tagged_words

# Declare appropriate files
category = 'suicide' # family, romance, spiritual, suicide (depression, and death)
roundCount = 'Round Two' # 'Count' added to avoid command similarity
roundfile = str.strip(roundCount) # For file naming, can be modified below

# File Path Directory List
token_path = f'.\\Reddit\\{roundCount}\\Tokens\\Retokenized Pickle Files\\{category}_retokenized_full.pickle'
freq_file = f'.\\Reddit\\{roundCount}\\Frequency Analyses\\Retokenized Frequencies\\{category}_freq_{roundfile}.csv'
num_bigrams = 500
save_bigrams = f'.\\Reddit\\{roundCount}\\Bigrams\\{category}_bigrams_{roundfile}.txt'

# Call the bigram finder
# save_tagged_words(freq_file, ['JJ', 'NN'])
find_bigrams(token_path = token_path,
             num_bigrams = num_bigrams,
             save_bigrams = save_bigrams)


