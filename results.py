"""
Generating results for the program
"""

from backend import *

all_ranks = {}

def merge_costs(ext_tracker):
    """
    Shows the top Material topics to prioritize taking its account its rank and
    its cost. Number of topics shown is specified by what the user input at
    the beginning.

    Inputs:
        ext_tracker(Tracker): external tracker with costs of Topics and the max
            number of topics the user wants to see

    Returns (lst of str): the
    """

    #Max number of topics the user wants to rank
    max_topics = ext_tracker.max

    #Storing the value of every topic in all_values
    values = []
    all_costs = ext_tracker.costs
    print("All costs: ", all_costs)

    #Value of a topic is its rank + its cost
    for topic, score in all_ranks.items():
        value = all_costs[topic] + score
        heapq.heappush(values, (value, topic))

    print("Values of all topics: ", values)
    #TODO: this part is not producing anything yet
    #TODO: enumerate the html template
    result = [topic[1] for topic in heapq.nsmallest(max_topics, values)]
    return result


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
    int_rankings = __get_ranking(int_tracker)
    ext_rankings = __get_ranking(ext_tracker)

    for i, category_dict in enumerate(ext_rankings):
        temp_rankings = []
        for topic, ranking in category_dict.items():
            ranking_sum = ranking + int_rankings[i][topic]
            all_ranks[topic] = ranking_sum
            heapq.heappush(temp_rankings, (ranking_sum, topic))
        result[i] = [topic for _, topic in heapq.nsmallest(len(temp_rankings), temp_rankings)]
    return result


def __get_ranking(tracker):
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
