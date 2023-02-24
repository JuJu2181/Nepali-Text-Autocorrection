import pandas as pd 
import numpy as np 
import textdistance
from collections import Counter
import time


def get_vocabulary():
    words = []
    with open('./nepali_dict_words.txt','r',encoding='utf-8') as f:
        data = f.read()
        words = data.split()
    vocabulary = set(words)
    return words, vocabulary

def get_frequency_of_words(words):
    word_count_dict = {}
    for word in words:
        if word in word_count_dict:
            word_count_dict[word] += 1
        else:
            word_count_dict[word] = 1 
    return word_count_dict

def get_probs(word_count_dict):
    probs = {}
    total = sum(word_count_dict.values())
    for key in word_count_dict.keys():
        probs[key] = word_count_dict[key]/total 
    return probs 

def get_suggestions(input_word, vocabulary, word_freq, probs, no_of_suggestions = 5, distance="jac"):
    """
    **Description**
    This function will return top n similar words that could be correction for given word
    - Similarity can either be based on Jaccard similarity or based on Levenshtein distance

    **Arguments** 
    input_word: word to be corrected
    vocabulary: vocabulary of unique Nepali words
    word_freq: dictionary with frequency of words
    probs: dictionary with probabilities of words
    no_of_suggestions: no of corrections suggested for input_word
    distance: similarity to be used. Use "jac" for Jaccard Similarity and "lev" for Levenshtein distance

    **Returns**
    A dataframe showing the top n suggestions along with their probability and similarity
    """
    if distance == "jac":
        sim = [1-(textdistance.Jaccard(qval=2).distance(v,input_word)) for v in word_freq.keys()]
    elif distance == "lev":
        sim = [1-(textdistance.levenshtein(v,input_word)) for v in word_freq.keys()]
    df = pd.DataFrame.from_dict(probs,orient='index').reset_index() 
    df = df.rename(columns={'index':'Word',0:'Prob'})
    df['Similarity'] = sim 
    output = df.sort_values(['Similarity','Prob'],ascending=False).head(no_of_suggestions)
    return list(output['Word'])

def main():
    input_word = input("Enter the word to get suggestions: ")
    words, vocabulary = get_vocabulary() 
    word_freq = get_frequency_of_words(words)
    probs = get_probs(word_freq)
    # if input_word in vocabulary:
    #     print("Word is correct, so no correction needed")
    #     return list(input_word)
    # else: 
    start = time.time()
    print("Getting possible suggestions for given word:")
    suggestions_jac = get_suggestions(input_word, vocabulary, word_freq, probs, 5, "jac")
    suggestions_lev = get_suggestions(input_word, vocabulary, word_freq, probs, 5, "lev")
    print(f"Suggestions using Jaccard Similarity: \n{suggestions_jac}")
    print(f"Suggestions using Levenshthein distance: \n{suggestions_lev}")
    end = time.time() 
    print(f"Time taken for suggesting words: {end-start}")
    return suggestions_jac

def check_spell(input_word):
    words, vocabulary = get_vocabulary() 
    word_freq = get_frequency_of_words(words)
    probs = get_probs(word_freq)
    suggestions_jac = get_suggestions(input_word, vocabulary, word_freq, probs, 10, "jac")
    return suggestions_jac

if __name__ == "__main__":
    main()