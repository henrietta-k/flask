"""
Contains all the backend functions for the program

Functions include:
- Function that checks if there are any more questions to be asked
- Prioritize different topics
- Greedy algorithm that gives the current best answer
"""

from utils import *
import heapq

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
        self.internal = 0


#Not sure if I need to create an object for this
class Tracker:
    """
    Keeps track of all the remaining topics. Has methods to check for remaining
    questions.

    Public attributes:

    NOTE: FIGURE OUT IF IT IS BETTER TO MAKE TWO TRACKERS, OR ONLY ONE TRACKER
    SEEMS LIKE IT'S BETTER TO ONLY USE ONE TRACKER FOR NOW

    """
    def __init__(self, ext=True):
        """
        """
        self.e = {}
        self.s = {}
        self.g = {}

        if ext:
            self.questions = questions_ext
            self.bounds = bounds_ext
        else:
            self.questions = questions_int
            self.bounds = bounds_int

        #When topics are no longer being asked about
        self.e_heap = []
        self.s_heap = []
        self.g_heap = []

        #Current question being asked
        self.curr_id = 0


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
        e = e.split(",")
        s = s.split(",")
        g = g.split(",")

        for topic in e:
            self.e[topic] = Topic("E", topic.strip())
        for topic in s:
            self.s[topic] = Topic("S", topic.strip())
        for topic in g:
            self.g[topic] = Topic("G", topic.strip())

        return (self.e.keys(), self.s.keys(), self.g.keys())


    def update(self, e, s, g, ext=True):
        """
        Performs all the necessary updates to the tracker after every question
        the user is asked.

        """

        self.update_topics(e, s, g, ext)
        self.remove_topics(ext)

    def update_topics(self, e, s, g, ext=True):
        """
        Updates the attributes for each Topic based on the user input. Adds 1
        to the Topic's score if a user has selected it for either external
        or internal (company) impact.

        Inputs:
            e(list of str):
            s(list of str):
            g(list of str):

        Returns: (does not return a value)
        """
        #When answering questions about the external impact
        if ext:
            for topic in e:
                self.e[topic].external += 1
            for topic in s:
                self.s[topic].external += 1
            for topic in g:
                self.g[topic].external += 1

        #When answering questions about the internal impact
        else:
            for topic in e:
                self.e[topic].internal += 1
            for topic in s:
                self.s[topic].internal += 1
            for topic in g:
                self.g[topic].internal += 1


    def remove_topics(self, bound, ext):
        """
        Removes topics based on a bound as user answers questions about them.

        Inputs:
            bound(int): bound that a Topic must reach to not be removed from
                the program
            ext(bool): checking for external/ internal score

        Returns():
        """

        if ext:
            for topic in self.e:
                if topic.external <= bound:
                    self.e_heap.heappush(topic.external, topic)
                    self.e.remove(topic) #figure this out
            for topic in self.s:
                pass
            for topic in self.g:
                pass

    def questions_left(self) -> tuple:
        """
        Checks to see if any more questions need to be asked and returns a question
        if there are any remaining. Returns False otherwise.

        Inputs:

        Returns(tuple of str): tuple of the question title and the question itself
        """
        if questions_ext and not self.terminate():
            question = questions_ext.pop(0)
            return question
        return False

    def get_topic(self, category):
        """
        Returns a list of remaining topics depending on the input category
        (E, S, G).

        Input:
            category(str): what category to return a list for

        Returns(list of str):
        """
        pass

    def terminate(self):
        """
        Uses a greedy algorithm to rank the topics currently if the user decides
        to end the program early.

        Inputs:
        """
        pass

    def final(self):
        """
        Uses dynamic programming to optimize the solution for both internal
        and external topics.
        """
        pass

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
    pass



    #Ends the program if there are only 3 topics left for every

