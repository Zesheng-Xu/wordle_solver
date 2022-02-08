"""
Author: Zesheng Xu
Date: Feb 6 2022
Functions:

"""

from letter import letter_object
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
    guessed = []
    for i in range(0,6):
        certain = [None, None, None, None, None]  # a bool array to sure if a letter's location is certain or not

        if(len(word_list) > 0):
            guess = np.random.choice(word_list)
            guessed.append(guess)
            if(guess == word):
                print("Success on %s try, and the word is: %s"% ( i, guess))
                return 0;
            else:

                for j in range(0,len(word)):
                    if(guess[j] == word[j]):
                        print('%s at location %s confirmed'% (guess[j],j))
                        temp_letter = letter_object(guess[j], "confirmed")
                        certain = letter_object_set(certain, temp_letter, j)


                    elif (guess[j] in word):
                        print('%s at location %s exists'% (guess[j], j))
                        temp_letter = letter_object(guess[j], "exist")
                        certain = letter_object_set(certain, temp_letter, j)


                    else:
                        if(guess[j] not in excluded):
                            excluded.append(guess[j])
            word_list = update_list(word_list, excluded, certain)
        else:
            print("This word is not within our dictionary")
    print("Target",word)
    print("Excluded",excluded)
    print(guessed)
    for i in certain:
        if i != None:
            print(i.get_letter(), i.get_state())

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
    count = 0
    while count < len(updated_list):  # go through each word in the word list
        word = updated_list[count]
        removed = False  # bool variable to prevent double removal of the same word
        for letter in excluded:
            if letter in word and not removed:  # if the word have excluded letters, we remove it from the list
                print("removed 0 ", word , "Had " ,letter)
                updated_list.pop(count)
                count -= 1
                removed = True
                break
        if not removed:

            for letter_2 in certain:
                if letter_2 is not None:
                    letter_count = count_occurance(letter_2.get_letter(), certain)
                    if letter_count > 1 and  word.count(letter_2.get_letter()) != letter_count:  # if the word does not have required number of
                        # letters needed i.e build while we need 2 L
                        print("removed 1 ", word, "looking for " ,letter_count , letter_2.get_letter() , "it had ",word.count(letter_2.get_letter())  )
                        updated_list.pop(count)
                        count -= 1
                        break
                    elif letter_2.get_state() == "exist":  # if the word do not have the needed letters
                        if not letter_2.get_letter() in word or certain.index(letter_2) == word.index(letter_2.get_letter()):
                            print("removed 2 ", word,"Looking for" ,letter_2.get_letter())
                            updated_list.pop(count)
                            count -= 1
                            break
                    elif letter_2.get_state() == "confirmed":  # if the word do not have the needed letter at the needed
                        # location
                        if word[certain.index(letter_2)] != letter_2.get_letter():
                            print("removed 3 ", word , word[certain.index(letter_2)], letter_2.get_letter())
                            updated_list.pop(count)
                            count -= 1
                            break

        count += 1
        print (count, len(updated_list))
        if(count < 0):
            print("Count is negative")
            break
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
        if temp != None and temp.get_letter() == letter:
            count += 1
    return count

def letter_object_set(certain_list, new_letter, index):
    """
    Author: Zesheng Xu
    Date: Feb 7 2022
    Description: systematically setting letter into certain_list, changing letter from exist to confirmed without
        duplicating it
    :param certain_list: list of letters that are in the target word
    :param letter_obj: the letter that is being added
    :param index: where the letter to be added
    :return: the list after process
    """



    for i in range(0,len(certain_list)):
        if certain_list[i] != None:
            if certain_list[i].get_letter() == new_letter.get_letter() and certain_list[i].get_state() == "exist" \
                    and new_letter.get_state() == "confirmed":
                # if the new object is confirmed and we found a letter object that is only "exist", we know that this
                # letter needs to be updated
                certain_list[i] == None


    certain_list[index] = new_letter
    return certain_list;



if __name__ == "__main__":
    main()
