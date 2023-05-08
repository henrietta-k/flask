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
    assert type(int_tracker) == Tracker
    assert type(ext_tracker) == Tracker

    result = [[], [], []]

    int_rankings = __get_ranking(int_tracker)
    ext_rankings = __get_ranking(ext_tracker)

    for i, category in enumerate(ext_rankings):
        temp_rankings = []
        for topic, ranking in category.items():
            ranking_sum = ranking + int_rankings[i][topic]
            heapq.heappush(temp_rankings, (ranking_sum, topic))
        for _, _ in enumerate(temp_rankings):
            _, item = heapq.heappop(temp_rankings)
            result[i].append(item)
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

    #TODO: test this function
    heaps = [tracker.e_heap, tracker.s_heap, tracker.g_heap]
    result = [{}, {}, {}]

    for i, heap in enumerate(heaps):
        heap = heap[::-1]
        for rank, topic in enumerate(heap):
            _, name = topic
            result[i][name] = rank
    return result


def __get_costs(tracker, e, s, g):
    """
    #TODO: THIS FUNCTION CAN BE DELETED
    Gets the user input for the costs of the different topics. Helper function
    for merge_costs.

    Inputs:
        tracker(Tracker): a Tracker object containing all the topics
        e(lst of ints): cost of all e topics
        s(lst of ints): cost of all s topics
        g(lst of ints): cost of all g topics

    Returns(tuple of dicts): dictionaries of all the topics mapped to
        their costs
    """

    #TODO: check the order of all the topics being displayed and make sure the cost is correctly assigned to each topic
    #TODO: test this function

    e_cost = {}
    s_cost = {}
    g_cost = {}

    heaps = [(e_cost, tracker.e_heap, e),
             (s_cost, tracker.s_heap, s),
             (g_cost, tracker.g_heap, g)]

    for i, heap_tuple in enumerate(heaps):
        cost_dict, heap, input = heap_tuple
        for _, topic in heap:
            cost_dict[topic] = input[i]

    return (e_cost, s_cost, g_cost)

