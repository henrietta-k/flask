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


class Tracker:
    """
    Keeps track of all the remaining topics. Has methods to check for remaining
    questions.

    Public attributes:

    """
    def __init__(self, ext=True):
        """
        """
        #Topic names with the Topics themselves
        self.e = {}
        self.s = {}
        self.g = {}

        #Heap of Topics that haven't been removed yet
        self.e_curr_heap = []
        self.s_curr_heap = []
        self.g_curr_heap = []

        #Tracker is for internal or external use
        self.ext = ext

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

        #Use these in For loops
        self.categories = [(self.e, self.e_heap),
                           (self.s, self.s_heap),
                           (self.g, self.g_heap)]


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
            self.e[topic.strip()] = Topic("E", topic.strip())
        for topic in s:
            self.s[topic.strip()] = Topic("S", topic.strip())
        for topic in g:
            self.g[topic.strip()] = Topic("G", topic.strip())

        return (list(self.e.keys()), list(self.s.keys()), list(self.g.keys()))


    def update(self, e, s, g, ext=True):
        """
        Performs all the necessary updates to the tracker after every question
        the user is asked.

        Inputs:
            e(list of str): all Environmental topics the user selected
            s(list of str): all Social topics the user selected
            g(list of str): all Governmental topics the user selected

        Returns(str or None): str of the next question or None if there are
        no more questions to ask
        """

        self.update_topics(e, s, g, ext)
        self.remove_topics(ext)
        if self.next_question():
            self.curr_id += 1
            return self.next_question()
        return None


    def update_topics(self, e, s, g, ext=True):
        """
        Updates the attributes for each Topic based on the user input. Adds 1
        to the Topic's score if a user has selected it for either external
        or internal (company) impact. Removes Topics if they exceed the question
        bound.

        Inputs:
            e(list of str):
            s(list of str):
            g(list of str):

        Returns: (does not return a value)
        """
        #TODO: Use for loops to shorten the code here

        #When answering questions about the external impact
        #TODO: update the current heap as well OR do this in the remove_topics function
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


    def remove_topics(self, ext):
        """
        Removes topics based on a bound as user answers questions about them.

        Inputs:
            ext(bool): checking for external/ internal score

        Returns():
        """
        #NOTE: remove topics if the difference between one topic and the one previosu to it is larger than the number of questions left
        #8 questions to ask total for external
        #Either use mergesort for this or use something in the heap module

        bound = self.bounds[self.curr_id]

        if ext:
            for category, heap in self.categories:
                for name, topic in category.items():
                    if topic.external <= bound:
                        #Topic score is too low
                        heap.heappush(topic.external, topic)
                        del category[name]
        else:
            for category, heap in self.categories:
                for name, topic in category.items():
                    if topic.internal <= bound:
                        heap.heappush(topic.internal, topic)
                        del category[name]


    def no_questions_remaining(self):
        """
        Pushes all material topics into the heap when there are no more
        questions left to ask.

        Input:
            ext(bool): whether this Tracker is for

        Returns: (does not return a value)
        """

        for category, heap in self.categories:
            if category:
                for topic in category.values():
                    if self.ext:
                        heap.heappush(topic.external, topic)
                    else:
                        heap.heappush(topic.internal, topic)


    def next_question(self) -> tuple:
        """
        Checks to see if any more questions need to be asked and returns a question
        if there are any remaining. Returns False otherwise.

        NOTE: figure out HOW to terminate the program --> maybe difference in scores of the topics
        are all smaller than the number of questions remaining
        Reasons for termination
        (1) No more topics
        (2)
        (3)

        Inputs:

        Returns(tuple of str or False): tuple of the question title and the
            question itself if there are questions remaining. False otherwise.
        """
        if questions_ext and not self.terminate():
            question = self.questions[self.curr_id]
            return question
        return False


    def get_topic(self):
        """
        Returns a list of remaining topics as a list of str.

        Returns(tuple of lst of str): the topics that still need to be asked
        about
        """

        e = list(self.e.keys())
        s = list(self.s.keys())
        g = list(self.g.keys())

        return (e, s, g)


    def terminate(self):
        """
        Uses a greedy algorithm to rank the topics currently if the user decides
        to end the program early.

        Inputs:
        """
        #TODO
        return False

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

