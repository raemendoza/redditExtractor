import pandas as pd
from scipy.stats import kendalltau
from scipy.stats.mstats import winsorize
from scipy.stats import shapiro
import numpy as np


# Compares two given word frequency analyses (of the same size), confirms non-Normality, and computes similarity stats
# Jaccard similarity is used to check for consistency across extractions
def compare_lists(category_names, file1, file2):
    # Load the CSV files into dataframes
    df1 = pd.read_csv(file1, header=0, names=['word', 'count'], skiprows=1)
    df2 = pd.read_csv(file2, header=0, names=['word', 'count'], skiprows=1)

    # Check DF rows are the same.
    if df1.shape[0] != df2.shape[0]:
        raise ValueError("DataFrames have different numbers of rows")


    # Apply Winsorization to counts
    df1['count'] = winsorize(df1['count'], limits=[0.05, 0.05])
    df2['count'] = winsorize(df2['count'], limits=[0.05, 0.05])

    # Shapiro Wilk Test for Normality
    count_data_1 = df1['count']
    stat1, p1 = shapiro(count_data_1)
    count_data_2 = df2['count']
    stat2, p2 = shapiro(count_data_2)

    # Print test statistics of SW
    print(f"Results for {category_names} lists:")
    print(f"Shapiro-Wilk test statistic for first list in {category_names}: {round(stat1, 3)}, p = {round(p1, 3)}")
    print(f"Shapiro-Wilk test statistics for second list {category_names}: {round(stat2, 3)}, p = {round(p2, 3)}")

    # Interpret
    if p1 and p2 > 0.05:
        print("Both count data is likely drawn from a normal distribution")
    else:
        print("Both count data is not likely drawn from a normal distribution")

    # Compute the Jaccard similarity - Accounts for presence and absence of words
    set1 = set(df1['word'])
    set2 = set(df2['word'])

    jaccard_similarity = len(list(set1.intersection(set2))) / len(list(set1.union(set2)))

    print("Jaccard similarity=", round(jaccard_similarity, 4))

    # Compute the Kendall rank correlation coefficient and p-value - takes account the correlation between the ranks
    tau, p_value = kendalltau(df1['word'], df2['word'])

    # Compute the effect size of kendall.
    n_size = len(df1['word'])
    effect_size = (2 * np.sin(np.pi * tau / 6)) * np.sqrt((n_size * (n_size - 1)) / 2)

    print(f"Kendall's tau = {round(tau, 3)}, p = {round(p_value, 3)}, η2 = {round(effect_size, 3)}\n")

# Sorts words before running intersection function
def find_top_words(file):
    words = read_csv_file(file)
    sorted_words = sorted(words.items(), key=lambda x: x[1], reverse=True)
    return [word for word, _ in sorted_words]

# Takes the shared words across three files and generates a new list of the top shared words up to 2500 (return statement)
def find_top_shared_words(file1, file2, file3, words1, words2, words3):
    top_words1 = set(find_top_words(file1))
    top_words2 = set(find_top_words(file2))
    top_words3 = set(find_top_words(file3))

    shared_words = top_words1.intersection(top_words2, top_words3)

    # Compute the sum of frequencies for each shared word
    shared_words_with_sum = []
    for word in shared_words:
        sum_of_frequencies = words1[word] + words2[word] + words3[word]
        shared_words_with_sum.append((word, sum_of_frequencies))

    shared_words_with_sum = sorted(shared_words_with_sum, key=lambda x: x[1], reverse=True)
    return shared_words_with_sum[:2500]

def read_csv_file(filename):
    df = pd.read_csv(filename, encoding = 'utf-8')
    words = df.set_index('word')['count'].to_dict()
    return words

def write_shared_words_to_file(shared_words, output_file):
    df = pd.DataFrame(shared_words, columns=['Word', 'Frequency'])
    df.to_csv(output_file, index=False)


category = 'suicide'
file_one = f'.\\Reddit\\Round Two\\Frequency Analyses\\{category}_freq_full_new.csv'
file_two = f'.\\Reddit\\Round Three\\Frequency Analyses\\{category}_freq_full_new.csv'
file_three = f'.\\Reddit\\Round Three\\Frequency Analyses\\{category}_freq_full_new.csv'
output_file_path = f'{category}_shared_words.csv'

words_one = read_csv_file(file_one)
words_two = read_csv_file(file_two)
words_three = read_csv_file(file_three)

# # Run the Shared Words function for three files then write them into a new file
# shared_words_total = find_top_shared_words(file1 = file_one,
#                                            file2 = file_two,
#                                            file3 = file_three,
#                                            words1 = words_one,
#                                            words2 = words_two,
#                                            words3 = words_three)
# write_shared_words_to_file(shared_words = shared_words_total,
#                            output_file = output_file_path)


# # Run the list comparing function
# compare_lists(category,
#                  file1 = f'.\\Reddit\\Round Two\\Frequency Analyses\\{category}_freq_full_new.csv',
#                  file2 = f'.\\Reddit\\Round Three\\Frequency Analyses\\{category}_freq_full_new.csv')


