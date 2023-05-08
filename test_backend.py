"""
Pytests for backend.py
"""

from backend import *

#Source: https://www.amd.com/en/corporate-responsibility/material-esg-issues
input = ["Energy efficiency of products, GHG reduction solutions",
            "Technology for good, Forced labor in the supply chain, Raw material sourcing, Employee talent acquisition",
            "Ethical conduct, Product security, Product quality, Innovation & IP, Supply chain security"]
tracker = Tracker()
result = tracker.initialize(input[0], input[1], input[2])

def test_initialize_topics():
    assert result == (['Energy efficiency of products', 'GHG reduction solutions'],
                      ['Technology for good', 'Forced labor in the supply chain', 'Raw material sourcing', 'Employee talent acquisition'],
                      ['Ethical conduct', 'Product security', 'Product quality', 'Innovation & IP', 'Supply chain security'])


#Making an external Tracker object
curr_ext = Tracker()
curr_ext.e = {"a": Topic("E", "a"), "b": Topic("E", "b"), "c": Topic("E", "c")}
curr_ext.s = {"d": Topic("S", "d"), "e": Topic("S", "e"), "f": Topic("S", "f")}
curr_ext.g = {"g": Topic("G", "g"), "h": Topic("G", "h"), "i": Topic("G", "i")}

curr_ext.curr_id = 6 #There are only two more questions to ask after this

e_scores = [1, 5, 8]
s_scores = [2, 4, 5]
g_scores = [1, 4, 8]

e_names = list(curr_ext.e.keys())
s_names = list(curr_ext.s.keys())
g_names = list(curr_ext.g.keys())

for i, topic in enumerate(curr_ext.e.values()):
    topic.external = e_scores[i]
    heapq.heappush(curr_ext.e_curr_heap, (topic.external, e_names[i]))
for i, topic in enumerate(curr_ext.s.values()):
    topic.external = s_scores[i]
    heapq.heappush(curr_ext.s_curr_heap, (topic.external, s_names[i]))
for i, topic in enumerate(curr_ext.g.values()):
    topic.external = g_scores[i]
    heapq.heappush(curr_ext.g_curr_heap, (topic.external, g_names[i]))

def test_remove_topics():

    curr_ext.remove_topics()

    assert curr_ext.e_curr_heap == [(8, 'c')]
    assert curr_ext.s_curr_heap == [(2, 'd'), (4, 'e'), (5, 'f')]
    assert curr_ext.g_curr_heap == [(8, 'i')]

