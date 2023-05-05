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
        #Used to get the Topic object using its str name
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

        categories = [(e, self.e, self.e_curr_heap, "E"),
                      (s, self.s, self.s_curr_heap, "S"),
                      (g, self.g, self.g_curr_heap, "G")]

        for category, esg_dict, esg_heap, esg_str in categories:
            for topic in category:
                topic = topic.strip()
                esg_dict[topic] = Topic(esg_str, topic)
                #Topic needs to be a str for this function to work
                heapq.heappush(esg_heap, (0, topic))

        #Heap looks like this:
        #Curr heap:  [(0, 'a'), (0, 'b'), (0, 'c')]
        return (list(self.e.keys()), list(self.s.keys()), list(self.g.keys()))


    def update_heap(self):
        """
        Remakes the heap for self.e_curr_heap, self.s_curr_heap,
        self.g_curr_heap using updated values.
        """

        new_heap = []
        heaps = [(self.e, self.e_curr_heap, "E"),
                (self.s, self.s_curr_heap, "S"),
                (self.g, self.g_curr_heap, "G")]

        #TODO: tidy the function here --> fix code quality
        #Remaking the heap with the new values
        if self.ext:
            for esg_dict, heap, char in heaps:
                new_heap = []
                for _, topic in heap:
                    priority = esg_dict[topic].external
                    heapq.heappush(new_heap, (priority, topic))
                if char == "E":
                    self.e_curr_heap = new_heap
                elif char == "S":
                    self.s_curr_heap = new_heap
                else:
                    self.g_curr_heap = new_heap
                new_heap = []

        #TODO: paste the code from above and tweak it
        else:
            for esg_dict, heap in heaps:
                new_heap = []
                for _, topic in heap:
                    priority = esg_dict[topic].internal
                    heapq.heappush(new_heap, (priority, topic))
                heap = new_heap
                new_heap = []


    def update(self, e, s, g):
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

        self.update_topics(e, s, g)
        self.remove_topics()
        if self.next_question():
            self.curr_id += 1
            return self.next_question()
        return None


    def get_topics(self):
        """
        Returns the questions that are still being asked about in the program.

        Returns(tuple of lst of str): returns (E, S, G) topics that still need
            to be asked about.
        """

        e = []
        s = []
        g = []

        categories = [(e, self.e_curr_heap),
                      (s, self.s_curr_heap),
                      (g, self.g_curr_heap)]

        for result, category in categories:
            for _, topic in category:
                result.append(topic)
        return (e, s, g)


    def update_topics(self, e, s, g):
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

        inputs = [(self.e, e),
                (self.s, s),
                (self.g, g)]

        #When answering questions about the external impact
        if self.ext:
            for esg_dict, category in inputs:
                for topic in category:
                    esg_dict[topic].external += 1
                    #print("Topic name: ", topic, "Score: ", esg_dict[topic].external)
            self.update_heap()
            #print("E heap: ", self.e_curr_heap, "S: ", self.s_curr_heap, "G: ", self.g_curr_heap)

        #When answering questions about the internal impact
        else:
            for esg_dict, category in inputs:
                for topic in category:
                    esg_dict[topic].internal += 1
            self.update_heap()


    def remove_topics(self):
        """
        Removes topics based on a bound as user answers questions about them.
        """

        #TODO: see if there is an algorithm that can make this work (right now
        # it's not really working)


        #Total external questions: 8
        questions_remaining = len(self.questions) - self.curr_id

        #Topics removed if the difference between one topic's score and the
        #score of the one before it is larger than the number of questions
        #remaining
        heaps = [(self.e_curr_heap, self.e_heap, self.e),
                 (self.s_curr_heap, self.s_heap, self.s),
                 (self.g_curr_heap, self.g_heap, self.g)]

        result = []

        for curr_heap, heap, category in heaps:
            for i, topic_tuple in enumerate(curr_heap):
                #print("i: ", i, "i + 1: ", i + 1, "Length of heap: ", len(curr_heap), curr_heap)
                to_delete= []
                if i < len(curr_heap) - 1: #figur ethis out
                    cost_prev, prev = topic_tuple
                    cost_next, next = curr_heap[i+1]
                    print("Diff: ", cost_next - cost_prev, "Remainign: ", questions_remaining, "PRev: ", prev, "Next: ", next)
                    if cost_next - cost_prev > questions_remaining:
                        print("I'm here now")
                        to_delete.append(prev)
                        print("To delete:", to_delete)
                        if self.ext:
                            heapq.heappush(heap, (category[prev].external, prev))
                        else:
                            heapq.heappush(heap, (category[prev].internal, prev))
                #print("Tod delete: ", to_delete)
                self.delete_topic(curr_heap, to_delete)
                to_delete = []


    def delete_topic(self, heap, topics):
        """
        Helper function for remove_topics(). Deletes all the specified topics
        in a heap.

        Inputs:
            heap(lst of tuples):
            topics(lst of str):

        Returns: (does not return a value)
        """
        #TODO: change this to a quickselect algorithm
        #TODO: test this function
        for topic in topics:
            for i, topic_tuple in enumerate(heap):
                _, name = topic_tuple
                if topic == name:
                    heap.pop(i)


    def no_questions_remaining(self):
        """
        #TODO: is this method actually used or not
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
        NOTE: heaps look like this
        E heap:  [(2, 'b'), (3, 'a'), (3, 'c')] S:  [(2, 'e'), (3, 'd'), (3, 'f')] G:  [(2, 'h'), (3, 'g'), (2, 'i')]

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
        #TODO: write a pytest for this function
        questions_remaining = len(self.questions) - self.curr_id

        #Terminate the program if the highest scores in every current heap
        #are greater than the number of questions remaining
        max_e = self.e_curr_heap[-1][0]
        max_s = self.s_curr_heap[-1][0]
        max_g = self.g_curr_heap[-1][0]

        min_diff = min(abs(max_e - max_s),
                       abs(max_e - max_g), abs(max_s - max_g))

        if min_diff > questions_remaining:
            return False

        #Only one topic left in E, S, G
        if (self.e_curr_heap <= 1 and self.s_curr_heap <= 1
                and self.g_curr_heap <= 1):
            return False

        if questions_remaining > 0  and not self.terminate():
            question = self.questions[self.curr_id]
            return question


    def terminate(self):
        """
        Uses a greedy algorithm to rank the topics currently if the user decides
        to end the program early.

        Inputs:
        """
        #TODO
        return False


def merge_solutions(self, int_tracker, ext_tracker):
    """
    Uses dynamic programming to optimize the solution for both internal
    and external topics.

    Make several rankings:
    (1) Greedy solution for terminating early / some sort of backtracking algorithm
    (2) Ranking by priority (code some sort of search algorithm for this)
    (3) Use DP to calculate the costs of a topic given user input
    """
    #NOTE: ask the user to assign a cost of fixing each topic --> use this in an
    #algorithm to solve it (backtracking/ DP/ greedy) --> use DP for this by
    #initializing an array



    #STEP 1: rank all of the topics for E, S, G for both internal and external
    #OR use the priority that they have already been assigned
    #Figure out which one is more accurate here
    #Probably ranking
    pass



