import random
import urllib.request
import itertools
import heapq
import random
import argparse
import json
import heapq
from operator import itemgetter


def run():

    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--size", help="Search size for candidate selection")
    parser.add_argument("-f", "--first", help="First guess word")
    args = parser.parse_args()

    search_size = 10
    if args.size and args.size.isdigit():
        search_size = int(args.size)

    first = "f"
    if args.first:
        first = args.first

    print("Scoring: 0 = Black, 1 = Yellow, 2 = Green")
    print("Sample result format: \"00121\"")

    master_list = {}
    words = {}
    with open("words_official.txt") as w_file:
        for line in w_file:
            word = line.replace("\n","")
            words[word] = 0
            master_list[word] = 0
    with open("words_valid.txt") as v_file:
        for line in v_file:
            word = line.replace("\n", "")
            master_list[word] = 0
    letter_counts = letter_count(master_list)
    words = update_scores(words, letter_counts, [])
    master_list = update_scores(master_list, letter_counts, [])
    
    green_list = []
    set_letters = []
    used = []
    yellow_list = {}
    no_letter = []

    for i in range(6):
        if i != 0:
            result = input("Enter result: ")
            if result == "22222":
                print("success!")
                break
            result_list = str_to_list(result)
            guess_arr = str_to_list(guess)
            for letter in guess_arr:
                if letter not in used:
                    used.append(letter)

            green_list, yellow_list, no_letter, set_letters = adjust_lists(guess_arr, result_list, set_letters, green_list, yellow_list, no_letter)
            words, _ = prune_list(words, green_list, yellow_list, no_letter)

            master_list = reset_scores(master_list)
            words = reset_scores(words)
            letter_counts = letter_count(words)
            master_list = update_scores(master_list, letter_counts, used)
            words = update_scores(words, letter_counts, [])

        if i == 0 and len(first) == 5:
            guess = first
        else:
            adj_size = search_size * (len(green_list) + 1)
            top_master = getTopsHQ(adj_size, master_list)
            top_words = getTopsHQ(adj_size, words)

            for word in top_master:
                if word not in top_words:
                    top_words.append(word)
            if "" in top_words:
                top_words.remove("")
            
            best_score = len(words) ** 2
            candidates = []
            for guess_sim in top_words:
                    total_score = 0
                    for sol_sim in words:

                        words_cpy = words.copy()
                        green_cpy = green_list.copy()
                        yellow_cpy = copy_r(yellow_list)
                        noL_cpy = no_letter.copy()
                        set_cpy = set_letters.copy()
                        guess_res = check_guess(guess_sim, sol_sim)
                        guess_arr = str_to_list(guess_sim)
                        
                        green_cpy, yellow_cpy, noL_cpy, _ = adjust_lists(guess_arr, guess_res, set_cpy, green_cpy, yellow_cpy, noL_cpy)
                        _, score = prune_list(words_cpy, green_cpy, yellow_cpy, noL_cpy)
                        
                        total_score += score
                        if total_score > best_score:
                            break

                    if total_score == best_score:
                        candidates.append(guess_sim)
                    elif total_score < best_score:
                        candidates = [guess_sim]
                        best_score = total_score

            guess = get_max(candidates, master_list)
            wc_match = []
            for word in words:
                if word in candidates:
                    wc_match.append(word)
            if len(wc_match) > 0:
                guess = get_min_freq(wc_match)

        print("Guess:", guess)

    print("Game End")


def get_min_freq(words):
    if len(words) == 1:
        return words[0]
    min_word = words[0]
    min_score = get_frequency_score(min_word)
    for word in words:
        score = get_frequency_score(word)
        if min_score == -1 or score < min_score and score != -1:
            min_score = score
            min_word = word
    return min_word

def getTops(num, words):
    if len(words) <= num:
        return list(words.keys())
    top = []
    for i in range(num):
        selection = ""
        score = 0
        for word in words:
            if word not in top and words[word] > score:
                score = words[word]
                selection = word
        top.append(selection)
    return top

def getTopsHQ(num, words):
    if len(words) <= num:
        return list(words.keys())
    top = heapq.nlargest(num, words.items(), key=itemgetter(1))
    top_list = list(dict(top).keys())
    return top_list

def copy_r(orig):
    new_list = orig.copy()
    for item in orig:
        new_list[item] = orig[item].copy()
    return new_list

def check_guess(guess, solution):
    result = ['1', '1', '1', '1', '1']
    guess_arr = str_to_list(guess) 
    sol_arr = str_to_list(solution) 
    for i in range(len(guess_arr)):
        if guess_arr[i] == sol_arr[i]:
            result[i] = '2'
            guess_arr[i] = '0'
            sol_arr[i] = '0'
    for i in range(len(guess_arr)):
        if guess_arr[i] == 0:
            continue
        wrong_letter = True
        saved_ind = 0

        for j in range(len(sol_arr)):
            if guess_arr[i] == sol_arr[j]:
                wrong_letter = False
                saved_ind = j
        if wrong_letter:
            result[i] = '0'
        else:
            sol_arr[saved_ind] = '0'
    
    return result

def adjust_lists (guess_arr, result_list, set_letters, green_list, yellow_list, no_letter):
    for ind in range(len(result_list)):
        l_score = result_list[ind]
        letter = guess_arr[ind]
        if l_score == '0':
            if letter not in set_letters and letter not in no_letter:
                no_letter.append(letter)
        elif l_score == '1':
            if letter not in yellow_list:
                yellow_list[letter] = []
                set_letters.append(letter)
                if letter in no_letter:
                    no_letter.remove(letter)
            if ind not in yellow_list[letter]:
                yellow_list[letter].append(ind)
        elif l_score == '2':
            position = (letter, ind)
            if position not in green_list:
                green_list.append(position)
                set_letters.append(letter)
                if letter in no_letter:
                    no_letter.remove(letter)
    return green_list, yellow_list, no_letter, set_letters

def prune_list (words, green_list, yellow_list, no_letter):
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
    return words, len(words)

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

def get_max(words, master):
    max_score = 0
    max_word = ""
    for word in words:
        score = master[word]
        if score > max_score:
            max_score = score
            max_word = word
    return max_word

def reset_scores(words):
    for word in words:
        words[word] = 0
    return words

def update_scores(words, letter_counts, used):
    for word in words:
        added = []
        for letter in word:
            if letter not in added and letter in letter_counts and letter not in used:
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

def get_frequency_score(word):
    score = -1
    try:
        contents = urllib.request.urlopen("https://api.datamuse.com/words?sp=" + word + "&md=f&max=1").read()
        dec_con = json.loads(contents)
        score = dec_con[0]["score"]
    except:
        return -1
    return score



if __name__ == "__main__":
    run()
