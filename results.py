"""
Generating results for the program
"""

from backend import *

def merge_costs(int_tracker, ext_tracker, max):
    """
    Uses dynamic programing

    NOTE: figure out which Tracker object the costs are aligned with

    Inputs:
        int_tracker(Tracker): internal tracker
        ext_tracker(Tracker): external tracker

    Returns (tuple of lst of str): all the topics in E, S, G ranked based on
        their ranking and costs
    """
    #TODO: get the ranking of each topic now
    #TODO: merge them using DP

    max = ext_tracker.max

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
