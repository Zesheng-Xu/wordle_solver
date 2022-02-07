
"""
Author: Zesheng Xu
Date: Feb 6 2022
Description: A letter object class to store the letter and if it is certain to our word guess

Functions:
    letter(string c, string state)
    set_state(string state)
    get_state()
        return the state of the  letter
    get_letter()
        return the stored letter
"""

class letter():
    letter = ''
    state = ""

    def letter(self, char, s):
        """
        Author: Zesheng Xu
        Date: Feb 6 2022
        Description: A constructor class to set parameters
        :param char: A single letter to be stored
        :param s: A string object with following 3 possibilities: non_exist, exist, confirmed
                    non_exist: letter char do not exist in the word
                    exist: letter char exist but location unsure
                    confirmed: the letter char exist and its location is certain
        :return: none
        """
        self.letter = char
        self.state = s
    def set_state(self, s):
        """
        Author: Zesheng Xu
        Date: Feb 6 2022
        Description: A setter class to set parameter value
        :param s: A string object with following 3 possibilities:  exist, confirmed
                    exist: letter char exist but location unsure
                    confirmed: the letter char exist and its location is certain
        :return: none
        """
        self.state = s
    def get_state(self):
        """
        Author: Zesheng Xu
        Date: Feb 6 2022
        Description: A getter class to return state of the letter
        :return: state
        """
        return self.state

    def get_letter(self):
        """
        Author: Zesheng Xu
        Date: Feb 6 2022
        Description: A getter class to return letter
        :return: letter
        """
        return  self.letter