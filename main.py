"""
Author: Zesheng Xu
Date: Feb 6 2022
Functions:

"""

from letter import letter
from english_words import english_words_lower_alpha_set
import numpy as np

def main():
    """
    Author: Zesheng Xu
    Date: Feb 6 2022
    Description: the driver function that calls other functions to accomplish the task of guessing word

    :return: none
    """
    word = "skill"
    word_list = load_list()

    excluded = []  # excluded letter
    certain = []  # a bool array to sure if a letter's location is certain or not
    for i in range(0,5):
        guess = np.random.choice(word_list)



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


def update_list(list, excluded, certain):
    """
    Author: Zesheng Xu
    Date: Feb 6 2022
    Description: remove disqualified words based on known information
    :param list: Existing word list that has not been updated
    :param excluded: An array of letters that do not exist in target word
    :param certain: letters that we know exist in the target word
    :return updated_list: List after removing disqualified words
    """

    updated_list = list
    for word in updated_list:  # go through each word in the word list
        removed = false  # bool variable to prevent double removal of the same word
        for letter in excluded:
            if word.contains(letter) and not removed:  # if the word have excluded letters, we remove it from the list
                updated_list.remove(word)
                removed = True
                break
        if not removed:
            index = 0
            for letter_2 in certain:
                count = count_occurance(letter_2.get_letter(), certain)
                if word.count(letter_2.get_letter()) != count:  # if the word does not have required number of
                    # letters needed i.e build while we need 2 L
                    updated_list.remove(word)
                    removed = True
                    break
                if letter_2.get_state() == "exist":  # if the word do not have the needed letters
                    if not word.contains(letter_2.get_letter()):
                        updated_list.remove(word)
                        removed = True
                        break
                if letter_2.get_state() == "confirmed":  # if the word do not have the needed letter at the needed
                    # location
                    if not word[index] != letter_2.get_letter():
                        updated_list.remove(word)
                        removed = True
                        break
                index += 1

    return updated_list


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
        if temp.get_letter() == letter:
            count += 1
    return count


if __name__ == "__main__":
    main()
