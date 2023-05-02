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

def test_initialize_1():
    assert result == (['Energy efficiency of products', 'GHG reduction solutions'],
                      ['Technology for good', 'Forced labor in the supply chain', 'Raw material sourcing', 'Employee talent acquisition'],
                      ['Ethical conduct', 'Product security', 'Product quality', 'Innovation & IP', 'Supply chain security'])

def test_update_1():
    #TODO: continue writing this function
    #User input appears 
    pass
