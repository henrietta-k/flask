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
        self.cost = None


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
        else:
            self.questions = questions_int

        #When topics are no longer being asked about
        self.e_heap = []
        self.s_heap = []
        self.g_heap = []

        #Current question being asked
        self.curr_id = 1

        #Checks if the user still wants the program to run
        self.terminate = False

        #Use these in For loops
        #TODO: add curr_heap to these and use them in more functions for better code quality
        self.categories = [(self.e, self.e_heap),
                           (self.s, self.s_heap),
                           (self.g, self.g_heap)]

        #Checks to see if there is a next question
        self.next = True


    def initialize(self, e, s, g):
        """
        Takes in a list of E, S, G topics that the user inputs and sets the
        attributes for this class.

        Inputs:
            e(list of str or str): all Environmental topics
            s(list of str or str): all Social topics
            g(list of str or str): all Governmental topics

        Returns: (does not return a value)
        """
        if type(e) == str:
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

        return (list(self.e.keys()), list(self.s.keys()), list(self.g.keys()))


    def assign_costs(self, e, s, g):
        """
        Assigns a cost to every Topic object based on user input.

        Inputs:
            e(lst of ints): costs of all individual environmental topics
            s(lst of ints): costs of all individual social topics
            g(lst of ints): costs of all individual governance topics
        """
        #print("Inputs E: ", e, "S: ", s, "G: ", g)
        categories = [(list(self.e.values()), e),
                      (list(self.s.values()), s),
                      (list(self.g.values()), g)]

        #print("Self values: ", self.e.values(), self.s.values(), self.g.values())
        #print("Inputs: ", e, s, g)

        for costs, input in categories:
            for i, topic in enumerate(costs):
                topic.cost = input[i]


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
        for esg_dict, heap, char in heaps:
            new_heap = []
            for _, topic in heap:
                if self.ext:
                    priority = esg_dict[topic].external
                else:
                    priority = esg_dict[topic].internal
                heapq.heappush(new_heap, (priority, topic))
            if char == "E":
                self.e_curr_heap = new_heap
            elif char == "S":
                self.s_curr_heap = new_heap
            else:
                self.g_curr_heap = new_heap
            new_heap = []


    def update(self, e, s, g):
        """
        Performs all the necessary updates to the tracker after every question
        the user is asked.

        Inputs:
            e(list of str): all Environmental topics the user selected
            s(list of str): all Social topics the user selected
            g(list of str): all Governmental topics the user selected

        #TODO: Edited this
        Returns(str or None): str of the next question or None if there are
        no more questions to ask
        """
        #print("updating now")

        self.update_topics(e, s, g)
        self.remove_topics()
        self.curr_id += 1
        #return self.next_question()


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
            e(list of str): list of E topics the user chose
            s(list of str): list of S topics the user chose
            g(list of str): list of G topics the user chose

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
            self.update_heap()

        #When answering questions about the internal impact
        else:
            for esg_dict, category in inputs:
                for topic in category:
                    esg_dict[topic].internal += 1
            self.update_heap()


    def remove_topics(self):
        """
        Removes topics based on a bound as user answers questions about them.
        Topics are removed if the difference between one topic's score and the
        next topic's score is larger than the number of questions remaining.
        """
        #TODO: if there is only one topic remaining for each category, delete it
        #TODO: update this in the no_questions_remaining function as well
        questions_remaining = len(self.questions) - self.curr_id

        heaps = [(self.e_curr_heap, self.e_heap, self.e),
                 (self.s_curr_heap, self.s_heap, self.s),
                 (self.g_curr_heap, self.g_heap, self.g)]

        to_delete = []
        for curr_heap, heap, _ in heaps:
            for i, topic_tuple in enumerate(curr_heap):
                if i < len(curr_heap) - 1:
                    cost_prev = topic_tuple[0]
                    cost_next = curr_heap[i+1][0]
                    if cost_next - cost_prev > questions_remaining:
                        to_delete.append(topic_tuple)
            self.delete_topics(curr_heap, heap, to_delete)
            to_delete = []


    def delete_topics(self, old_heap, new_heap, topics):
        """
        Helper function for remove_topics(). Deletes all the specified topics
        in a heap and pushes it into the heap when the topics aren't being
        asked about anymore.

        Inputs:
            heap(lst of tuples):
            topics(lst of str):

        Returns: (does not return a value)
        """
        for topic in topics:
            old_heap.remove(topic)
            heapq.heappush(new_heap, topic)


    def next_question(self) -> tuple:
        """
        Checks to see if any more questions need to be asked and returns a question
        if there are any remaining. Returns None otherwise.

        Reasons for termination
        (1) There are no more questions to ask
        (2) The highest scoring topics across E, S, G all have a difference
            greater than the number of questions remaining
        (3) Only one topic left for E, S, G

        Returns(tuple of str or None): tuple of the question title and the
            question itself if there are questions remaining. False otherwise.
        """
        #TODO: write a pytest for this function
        questions_remaining = len(self.questions) - self.curr_id
        #print("Questions remaining: ", questions_remaining, "all questions: ", len(self.questions), "Self curr_id", self.curr_id, )

        max_e = self.e_curr_heap[-1][0]
        max_s = self.s_curr_heap[-1][0]
        max_g = self.g_curr_heap[-1][0]

        min_diff = min(abs(max_e - max_s),
                       abs(max_e - max_g), abs(max_s - max_g))

        if min_diff > questions_remaining:
            self.no_questions_remaining()
            self.next = False
            return None

        #Only one topic left in E, S, G
        if (len(self.e_curr_heap) <= 1 and len(self.s_curr_heap) <= 1
                and len(self.g_curr_heap) <= 1):
            self.no_questions_remaining()
            self.next = False
            return None

        if questions_remaining > 0:
            question = self.questions[self.curr_id]
            return question


    def no_questions_remaining(self):
        """
        Pushes all material topics into the heap when there are no more
        questions left to ask.

        Returns: (does not return a value)
        """

        for category, heap in self.categories:
            if category:
                for topic in category.values():
                    if self.ext:
                        heapq.heappush(heap, (topic.external, topic.name))
                    else:
                        heapq.heappush(heap, (topic.internal, topic.name))

