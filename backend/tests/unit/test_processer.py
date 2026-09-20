import pytest
from unittest.mock import Mock
from scribbles import processer_demo
INPUT_PROFILES = {
    "Player A": {
        "tunnels": {
            "FF": {"FF": 0.0, "SL": 0.015, "CH": 0.010},
            "SL": {"FF": 0.015, "SL": 0.0, "CH": 0.005},
            "CH": {"FF": 0.010, "SL": 0.005, "CH": 0.0}
        }
    },
    "Player B": {
        "tunnels": {
            "FF": {"FF": 0.0, "SL": 0.0, "CH": 0.020},
            "SL": {"FF": 0.0, "SL": 0.0, "CH": 0.0},
            "CH": {"FF": 0.020, "SL": 0.0, "CH": 0.0}
        }
    },
    "Player C": {
        "tunnels": {
            "FF": {"FF": 0.0, "SL": 0.025, "CH": 0.0},
            "SL": {"FF": 0.025, "SL": 0.0, "CH": 0.0},
            "CH": {"FF": 0.0, "SL": 0.0, "CH": 0.0}
        }
    }
}

def test_init_two_dim_dict_w_lst_valid():
    """Test 2D-dictionary-containing-list initializer with valid input."""
    
    # Build input
    input_keys = ['a', 'b', 'c']
    
    # Call and verify
    res = processer_demo.init_two_dim_dict_w_lst(input_keys, input_keys)
    assert res == {'a': {'a': [], 'b': [], 'c': []}, 'b': {'a': [], 'b': [], 'c': []}, 'c': {'a': [], 'b': [], 'c': []}}
    
def test_extract_tunnel_pairs_valid():
    """Test tunnel pair extractor with valid input."""
    
    # Call and verify
    res = processer_demo.extract_tunnel_pairs(INPUT_PROFILES)
    
    # Non-exhaustive assertions to avoid hefty-text of null pairs of the 19x19 pitch-types
    assert [("Player A", 0.015), ("Player B", 0.0), ("Player C", 0.025)] == res["FF"]["SL"]
    assert [("Player A", 0.010), ("Player B", 0.020), ("Player C", 0.0)] == res["FF"]["CH"]
    assert [("Player A", 0.005), ("Player B", 0.0), ("Player C", 0.0)] == res["SL"]["CH"]
    
def test_get_percentalized_tunnel_profiles_valid():
    """Test tunnel percentalizor with valid input."""
    
    # Call and verify
    res = processer_demo.get_percentalized_tunnel_profiles(INPUT_PROFILES)
    
    # Non-exhaustive assertions to avoid hefty-text of null pairs of the 19x19 pitch-types
    assert [("Player B", 0.0), ("Player C", 1.0), ("Player A", 0.5)] == res["FF"]["SL"]
    assert [("Player C", 0.0), ("Player B", 1.0), ("Player A", 0.5)] == res["FF"]["CH"]
    assert [("Player B", 0.0), ("Player C", 0.0), ("Player A", 1.0)] == res["SL"]["CH"]
    
def test_main_valid():
    """Test main with valid input."""
    # TODO