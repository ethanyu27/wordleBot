import random
import urllib.request
import itertools
import heapq

def run():
    print("Scoring: 0 = Black, 1 = Yellow, 2 = Green")
    print("Sample result format: \"00121\"")

    master_list = {}
    words = {}
    with open("words.txt") as w_file:
        for line in w_file:
            word = line.replace("\n","")
            words[word] = 0
            master_list[word] = 0
    letter_counts = letter_count(words)
    words = update_scores(words, letter_counts)
    
    green_list = []
    set_letters = []
    yellow_list = {}
    no_letter = []

    guess, _ = get_max(words)
    print("Guess:", guess)

    for i in range(5):
        result = input("Enter result: ")
        if result == "22222":
            print("success!")
            break
        result_list = str_to_list(result)
        guess_arr = str_to_list(guess)
        for ind in range(len(result_list)):
            l_score = result_list[ind]
            letter = guess_arr[ind]
            if l_score == '0':
                if letter not in set_letters:
                    no_letter.append(letter)
            elif l_score == '1':
                if letter not in yellow_list:
                    yellow_list[letter] = []
                if ind not in yellow_list[letter]:
                    yellow_list[letter].append(ind)
            elif l_score == '2':
                position = (letter, ind)
                if position not in green_list:
                    green_list.append(position)
                    set_letters.append(letter)

        to_pop = []
        for word in words:
            if not check_no_letter(no_letter, word):
                to_pop.append(word)
                continue
            if not check_yellow_list(yellow_list, word):
                to_pop.append(word)
                continue
            if not check_green_list(green_list, word):
                to_pop.append(word)
                continue
        for word in to_pop:
            words.pop(word)
        
        master_list = reset_scores(master_list)
        words = reset_scores(words)
        letter_counts = letter_count(words)
        master_list = update_scores(master_list, letter_counts)
        words = update_scores(words, letter_counts)
        guess, guess_score = get_max(words)
        best_master, bm_score = get_max(master_list)
        
        print("Guess:", guess)

def check_yellow_list(yellow_list, word):
    word_ls = str_to_list(word)
    for letter in yellow_list:
        if letter not in word_ls:
            return False
        for ind in yellow_list[letter]:
            if word_ls[ind] == letter:
                return False
    return True

def check_green_list(green_list, word):
    for letter, ind in green_list:
        if word[ind] != letter:
            return False
    return True

def check_no_letter(no_letter, word):
    for letter in word:
        if letter in no_letter:
            return False
    return True

def get_max(words):
    max_word = ("", 0)
    for word in words:
        if words[word] > max_word[1]:
            max_word = (word, words[word])
    return max_word[0], max_word[1]

def reset_scores(words):
    for word in words:
        words[word] = 0
    return words

def update_scores(words, letter_counts):
    for word in words:
        added = []
        for letter in word:
            if letter not in added and letter in letter_counts:
                words[word] += letter_counts[letter]
            added.append(letter)
    return words

def letter_count(word_list):
    alphabet = {}
    for word in word_list:
        for letter in word:
            if letter not in alphabet:
                alphabet[letter] = 0
            alphabet[letter] += 1
    return alphabet

def str_to_list(str):
    list = []
    for char in str:
        list.append(char)
    return list

def list_to_str(list):
    str = ""
    for char in list:
        str += char
    return str

def check_word(word):
    try:
        contents = urllib.request.urlopen("https://api.dictionaryapi.dev/api/v2/entries/en/" + word).read()
    except:
        return False
    return True



if __name__ == "__main__":
    run()