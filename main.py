"""
Author: Zesheng Xu
Date: Feb 6 2022
Functions:
main() - the driver function
load_list() - from the english dictionary, load all 5 letter word into an array
update_list() - remove unfitting words from the words list according to known knowledge
count_occurance() - count how many times a letter appeared in a letter_object list
letter_object_set_Value() - updating value of the letter_object array smartly

"""
import time

from selenium.webdriver.common.by import By

from letter import letter_object
from english_words import english_words_lower_alpha_set
from random import choice
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup


def main():
    """
    Author: Zesheng Xu
    Date: Feb 6 2022
    Description: the driver function that calls other functions to accomplish the task of guessing word

    :return: none
    """

    #launch wordle website
    driver = webdriver.Chrome("chromedriver.exe")
    driver.get("https://www.powerlanguage.co.uk/wordle/")

    # close  the introduction page
    time.sleep(1)

    Elem = driver.find_element_by_tag_name('html') # get the entire webpage 

    Elem.click() # skip introduction

    word_list = load_list() # get all 5 letter words 

    excluded = []  # excluded letter
    total_excluded = [] # an overall storage for excluded letter for display purpose 
    guessed = [] # storing all words we guessed 
    for i in range(0, 6):
        certain = [None, None, None, None, None]  # a letter obj array to store the letters that we know either exist or confirmed

        if(len(word_list) > 0):

            # Handle guesses that aren't in wordle's dictionary
            accepted = False
            while not accepted and len(word_list) > 0: # we keeps entering until our answer was accepted by the wordle 
                guess = choice(word_list) # randomly choose a new word from word list to enter 
                guessed.append(guess) 

                # send guess to wordle.com
                Elem.send_keys(guess) # send the key to wordle and enter
                Elem.send_keys(Keys.ENTER)

                time.sleep(2) # wait for wordle to play the annimation 

                excluded, certain, accepted = get_row_result(driver, i, certain) # update excluded, certain. accepted stores wether wordle accepts our input or not
                if not accepted: # if the answer was rejected, we remove that word from the word list and delete our entries 
                    word_list.remove(guess)
                    Elem.send_keys([Keys.BACKSPACE] * 6) 

            total_excluded += excluded

            """
            Following were for local testing of the word guessing algorithm
            """
            # if(guess == word):
            #     print("Success on %s try, and the word is: %s"% ( i, guess))
            #     print(guessed)
            #     return 0;
            # else:
            #
            #     for j in range(0,len(word)):
            #         if(guess[j] == word[j]):
            #             print('%s at location %s confirmed'% (guess[j],j))
            #             temp_letter = letter_object(guess[j], "confirmed")
            #             certain = letter_object_set_Value(certain, temp_letter, j)
            #
            #
            #         elif (guess[j] in word):
            #             print('%s at location %s exists'% (guess[j], j))
            #             temp_letter = letter_object(guess[j], "exist")
            #             certain = letter_object_set_Value(certain, temp_letter, j)
            #
            #
            #         else:
            #             if(guess[j] not in excluded):
            #                 excluded.append(guess[j])
            if(check_success(certain)):
                print("On turn %s we successfully guessed word: %s" % (i+1, guess))
                break
            word_list = update_list(word_list, excluded, certain)
        else:
            print("This word is not within our dictionary")
            break
    print("Excluded letters: ", total_excluded)
    print("Guesses words: ", guessed)
    for i in certain:
        if i is not None:
            print(i.get_letter(), i.get_state())
    driver.close()
    return


def load_list():
    """
    Author: Zesheng Xu
    Date: Feb 6 2022
    Description: Get all 5 letter words from the database
    :return list: An array of 5 letter string
    """
    list = []

    for word in english_words_lower_alpha_set:
        if len(word) == 5:
            list.append(word)

    return list


def update_list(lst, excluded, certain):
    """
    Author: Zesheng Xu
    Date: Feb 6 2022
    Description: remove disqualified words based on known information
    :param lst: Existing word list that has not been updated
    :param excluded: An array of letters that do not exist in target word
    :param certain: letters that we know exist in the target word
    :return updated_list: List after removing disqualified words
    """

    updated_list = lst
    index = 0
    while index < len(updated_list):  # go through each word in the word list
        word = updated_list[index]
        removed = False  # bool variable to prevent double removal of the same word
        for letter in excluded:
            if letter in word:  # if the word have excluded letters, we remove it from the list
                print("removal 0 ", word, "Had ", letter)
                updated_list.pop(index)
                index -= 1
                removed = True
                break

        if not removed:
            for letter_2 in certain:
                if letter_2 is not None:
                    letter_count = certain.count(letter_2.get_letter())
                    if letter_count > 1 and word.count(letter_2.get_letter()) != letter_count:  # if the word does not have required number of
                        # letters needed i.e build while we need 2 L
                        print("removal 1 ", word, "looking for ", letter_count, letter_2.get_letter(), "it had ", word.count(letter_2.get_letter()))
                        updated_list.pop(index)
                        index -= 1
                        break
                    elif letter_2.get_state() == "exist":  # if the word do not have the needed letters or having that letter on where the letter currently at 
                        if not letter_2.get_letter() in word or certain.index(letter_2) == word.index(letter_2.get_letter()):
                            print("removal 2 ", word, "Looking for", letter_2.get_letter())
                            updated_list.pop(index)
                            index -= 1
                            break
                    elif letter_2.get_state() == "confirmed":  # if the word do not have the needed letter at the needed
                        # location
                        if word[certain.index(letter_2)] != letter_2.get_letter():
                            print("removal 3 ", word, "Had ", word[certain.index(letter_2)], " at where should be ", letter_2.get_letter())
                            updated_list.pop(index)
                            index -= 1
                            break

        index += 1
        #print (count, len(updated_list))
        if(index < 0):
            print("Count is negative")
            break
    return updated_list


# DEPRECIATED
def count_occurance(letter, letter_list):
    """
    Author: Zesheng Xu
    Date: Feb 6 2022
    Description: remove disqualified words based on known information
    :param letter_list: An array of Letter object to check against
    :param letter: a letter object to check for
    :return count: int
    """

    count = 0
    for temp in letter_list:  # goes through enough letter to get their char value and compare
        if temp is not None and temp.get_letter() == letter:
            count += 1
    return count


# DEPRECATED
def letter_object_set_Value(certain_list, new_letter, index):
    """
    Author: Zesheng Xu
    Date: Feb 7 2022
    Description: systematically setting letter into certain_list, changing letter from exist to confirmed without
        duplicating it
    :param certain_list: list of letters that are in the target word
    :param new_letter: the letter that is being added
    :param index: where the letter to be added
    :return: the list after process
    """

    for i in range(0, len(certain_list)):
        if certain_list[i] is not None:
            if certain_list[i].get_letter() == new_letter.get_letter() and certain_list[i].get_state() == "exist" \
                    and new_letter.get_state() == "confirmed":
                # if the new object is confirmed and we found a letter object that is only "exist", we know that this
                # letter needs to be updated
                certain_list[i] == None

    certain_list[index] = new_letter
    return certain_list


def get_row_result(webdriver, index, cert):
    """
    Author: Zesheng Xu
    Date: Feb 8 2022
    Description: Check latest row and retrieve the letter information such as wether a letter is correct, absent or,
        present
    :param webdriver: The wordle website
    :param webdriver: The Row number to get
    :param cert: The list of known certain letters
    :return: list - a letter_object list containing the result of our previous entrance - including the state of the letter
    :return: to_exclude - letters to exclude from the gusses
    :return: accepted - A boolean indicating if the submitted word was accepted by wordle
    """
    to_exclude = []
    temp_cert = []
    # locating the game-row through the series of shadow roots - I hate this
    host = webdriver.find_element(By.TAG_NAME, "game-app")
    game = webdriver.execute_script("return arguments[0].shadowRoot.getElementById('game')", host)
    board = game.find_element(By.ID, "board")
    rows = webdriver.execute_script("return arguments[0].getElementsByTagName('game-row')", board)
    row = webdriver.execute_script("return arguments[0].shadowRoot.querySelector(""'.row').innerHTML", rows[index])

    bs_text = BeautifulSoup(row, 'html.parser')

    for letter_index, tile in enumerate(bs_text.findAll('game-tile')):  # goes through each tile in the row
        if tile.get('evaluation') is None:
            return [], cert, False

        if cert[letter_index] is not None and cert[letter_index].get_state() == 'confirmed':  # Skip already confirmed letters
            continue

        letter = tile.get('letter')
        status = tile.get('evaluation')

        if(status == "present"):
            temp = letter_object(letter, "exist")
            cert[letter_index] = temp
            temp_cert.append(letter)

        elif (status == "correct"):
            temp = letter_object(letter, "confirmed")
            cert[letter_index] = temp
            temp_cert.append(letter)

        elif (status == "absent") and letter not in temp_cert:  # remove words that are absent from answer, while prevent removal of needed letters
            to_exclude.append(letter)

    return to_exclude, cert, True


def check_success(certain_list):
    """
    Author: Zesheng Xu
    Date: Feb 8 2022
    Description: Check if we have 5 confirmed letter - that means we guesses the word
    :param certain_list: A letter_object list where letters we know at least exists are stored
    :return: True if all 5 are confirmed, else return False
    """
    for letter in certain_list:
        if letter is None or letter.get_state() != "confirmed":
            return False
    return True


if __name__ == "__main__":
    main()
