"""
Generating results for the program
"""

from backend import *

all_ranks = {}

def merge_costs(int_tracker, ext_tracker):
    """
    Uses dynamic programing to figure out which Material topics to prioritize.

    Inputs:
        int_tracker(Tracker): internal tracker
        ext_tracker(Tracker): external tracker

    Returns (tuple of lst of str): tuple of two separate results
    (1) Most valuable material topics under a certain cost to the company
        (Dynamic Programming)
    (2) Max number of material topics as specific by the user (Greedy)
    """

    #Max number of topics the user wants to rank
    max_topics = ext_tracker.max
    max_cost = 50 #TODO: get user input for this

    values = []
    costs = []
    #ext_tracker.costs TODO:check to see if the costs have been correctly assigned

    #Total number of topics
    total_q = len(ext_tracker.e) + len(ext_tracker.s) + len(ext_tracker.g)
    worst_score = 2 * total_q

    for topic, score in all_ranks.items():
        #Value of a Topic is determined by its rank and its cost
        values.append(topic, abs(worst_score - score))
        costs.append(topic, ext_tracker.costs[topic])

    array = []

    #Initializing an empty array to store values
    #TODO: change this to list comprehension
    for i in range(len(values) + 1):
        temp_row = []
        for j in range(max_cost + 1):
            temp_row.append(None)
        array.append(temp_row)
        temp_row = []

    #Looping through the array and assigning values
    for row, line in enumerate(array):
        for col, _ in enumerate(line):
            if row == 0 or col == 0:
                array[row][col] = 0
            elif costs[row-1] <= row:
                array[row][col] = max(values[row-1] +
                                      array[row-1][col-costs[row-1]],
                                      array[row-1][col])
            else:
                array[row][col] = array[row-1][col]
    print(array[-1][-1])


def merge_ranking(int_tracker, ext_tracker):
    """
    Merges topics after answering internal and external questions solely based
    on their ranking.

    Inputs:
        int_tracker(Tracker): internal Tracker
        ext_tracker(Tracker): external Tracker

    Returns (lst of lst of str): all the topics in E, S, G ranked based on
        their ranking from highest to lowest priority
    """

    #TODO: test this function
    #TODO: fix code quality of this function
    assert type(int_tracker) == Tracker
    assert type(ext_tracker) == Tracker

    result = [[], [], []]

    #TODO: make functions private later
    int_rankings = get_ranking(int_tracker)
    ext_rankings = get_ranking(ext_tracker)

    for i, category_dict in enumerate(ext_rankings):
        temp_rankings = []
        for topic, ranking in category_dict.items():
            ranking_sum = ranking + int_rankings[i][topic]
            all_ranks[topic] = ranking_sum
            heapq.heappush(temp_rankings, (ranking_sum, topic))
        result[i] = [topic for _, topic in heapq.nsmallest(len(temp_rankings), temp_rankings)]
    return result


def get_ranking(tracker):
    """
    Helper function that assigns a ranking to a topic based on their position
    in a heap. Need to do this because scores are not comparable across the two
    Tracker objects.

    Inputs:
        tracker(Tracker): Tracker object to assign rankings for

    Returns(lst of dicts): dict of Topic objects mapped to their ranking for
        E, S, G
    """

    heaps = [tracker.e_heap, tracker.s_heap, tracker.g_heap]
    result = [{}, {}, {}]

    for i, heap in enumerate(heaps):
        heap = heap[::-1]
        for rank, topic in enumerate(heap, 1):
            _, name = topic
            result[i][name] = rank
    return result
