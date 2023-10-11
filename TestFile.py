import pandas as pd
import numpy as np

Parts = pd.read_excel('RegistryParts.xlsx')
partName = Parts['part_name'].values
#partName = ['A', 'B', 'C', 'D']
shortDesc = Parts['short_desc'].values
description = Parts['description'].values
source = Parts['source'].values
author = Parts['author'].values
database_sequences = Parts['sequence'].values
#database_sequences = ["ACTGAGC", "TGCAAGC", "AACTAGC", "ACGTAGC"]
nickname = Parts['nickname'].values

database_sequences = [i for i in database_sequences if i is not np.nan]
partName = [i for i in partName if i is not np.nan]

def longest_common_subsequence(X, Y):
    m = len(X)
    n = len(Y)
    L = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0 or j == 0:
                L[i][j] = 0
            elif X[i - 1] == Y[j - 1]:
                L[i][j] = L[i - 1][j - 1] + 1
            else:
                L[i][j] = max(L[i - 1][j], L[i][j - 1])

    index = L[m][n]
    lcs_sequence = [''] * (index + 1)
    lcs_sequence[index] = ''

    i = m
    j = n
    while i > 0 and j > 0:
        if X[i - 1] == Y[j - 1]:
            lcs_sequence[index - 1] = X[i - 1]
            i -= 1
            j -= 1
            index -= 1
        elif L[i - 1][j] > L[i][j - 1]:
            i -= 1
        else:
            j -= 1

    return ''.join(lcs_sequence)

def calculate_similarity(input_sequence):
    # Initialize a list to store similarity scores for each subsequence
    similarity_scores = []
    count = 0
    
    # Iterate over each database sequence
    for db_sequence in database_sequences:
        # Determine the window size based on the length of the current database sequence
        window_size = len(db_sequence)
        first = 1;
        # Slide a window over the input sequence
        for i in range(len(input_sequence) - window_size + 1):
            window = input_sequence[i:i+window_size]
            
            # Calculate LCS for the current window with the database sequence
            lcs_sequence = longest_common_subsequence(window, db_sequence)
            similarity_score = len(lcs_sequence) / window_size * 100

            if similarity_score > 85:
                last = first + window_size - 1
                similarity_scores.append(( count, first, last, window, similarity_score, db_sequence))

            first = first + 1

        count = count + 1
    
    return similarity_scores

def Final(input_sequence):
    similarity_scores = calculate_similarity(input_sequence)
    msg = "<table style='width:100%'><tr><th>1st Base Pair Position</th><th>Last Base Pair Position</th>"
    msg = msg + "<th>Part Name</th><th>Similarity Score</th></tr>"

    # Print the subsequence and their corresponding similarity scores
    for count, first, last, window, similarity_score, db_sequence in similarity_scores:
        msg = msg + "<tr><td>" + str(first) + "</td>" + "<td>" + str(last) + "</td>"
        msg = msg + "<td>" + partName[count] + "</td>" + "<td>" + str(similarity_score)
        msg = msg + "</td></tr>"
##        print("Subsequence:", window)
##        print("Similarity Score:", similarity_score)
##        print("Database sequence:", db_sequence)
##        print("---")
    msg = msg + "</table>"
    print(msg)


# Sample input sequence and database sequences
input_sequence = "ACGTAGCTGCAAGC"

# Calculate similarity for each subsequence using LCS
Final(input_sequence)
