"""
Contains all the backend functions for the program

Functions include:
- Function that checks if there are any more questions to be asked
- Prioritize different topics
- Greedy algorithm that gives the current best answer
"""

from utils import *

class Topic:
    """
    Class for a singular Topic

    Public attributes:

    """

    def __init__(self, esg: str, name: str):
        """
        Initializes one material topic
        """
        self.esg = esg
        self.name = name
        self.external = 0
        self.company = 0


#Not sure if I need to create an object for this
class Tracker:
    """
    Keeps track of all the remaining topics. Has methods to check for remaining
    questions.

    Public attributes:

    """
    def __init__(self):
        """
        """
        self.e = []
        self.s = []
        self.g = []


    def initialize(self, e, s, g):
        """
        Takes in a list of E, S, G topics that the user inputs and sets the
        attributes for this class.

        Inputs:
            e(list of str): all Environmental topics
            s(list of str): all Social topics
            g(list of str): all Governmental topics

        Returns: (does not return a value)
        """
        for topic in e:
            self.e.append(Topic("E", topic))
        for topic in s:
            self.e.append(Topic("S", topic))
        for topic in g:
            self.e.append(Topic("G", topic))


    def update_topics(self, e, s, g):
        """
        Updates the attributes for self based on user input.

        Inputs:
            e(list of str):
            s(list of str):
            g(list of str):

        Returns: (does not return a value)
        """

    def get_topic(self, category):
        """
        Returns a list of remaining topics depending on the input category
        (E, S, G).

        Input:
            category(str): what category to return a list for

        Returns(list of str):
        """

def questions_left() -> tuple:
    """
    Checks to see if any more questions need to be asked and returns a question
    if there are any remaining. Returns False otherwise.

    Inputs:

    Returns(tuple of str): tuple of the question title and the question itself
    """
    if questions_ext and not end_program():
        question = questions_ext.pop(0)
        return question
    return False


def next_question() -> bool:
    """
    Checks to see if there is another question after the current question.
    """
    pass

def end_program() -> bool:
    """
    Ends the program if there are:
    (1) Only 3 topics left per E, S, G
    (2) Only ___ of topics left
    """



    #Ends the program if there are only 3 topics left for every


def end_early():
    pass