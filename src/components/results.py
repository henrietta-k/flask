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

    #Value of a topic is its rank + its cost
    for topic, score in all_ranks.items():
        value = int(all_costs[topic]) + score
        heapq.heappush(values, (value, topic))

    #TODO: store this result into the configured database
    #TODO: enumerate the html template
    result = ['{}) {}'.format(i, topic[1]) for i, topic in
              enumerate(heapq.nsmallest(max_topics, values), 1)]
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
        result[i] = ['{}) {}'.format(i, topic[1]) for i, topic in
                     enumerate(heapq.nsmallest(len(temp_rankings), temp_rankings), 1)]
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
