import pytest
from unittest.mock import Mock
from backend import profiler
import pandas

row1 = {
    "game_pk": 100000,
    "player_name": "Gausman, Kevin",
    "p_throws": "R",
    "arm_angle": 35.3,
    "pitch_type": "SL",
    "release_speed": 84.1,
    "ax": -3.0351056162759944,
    "ay": 19.303781208905853,
    "az": -27.79786019272075,
    "vx0": 7.014596532697568,
    "vy0": -122.460428051283,
    "vz0": -3.544837633065215,
    "release_pos_x": -2.54,
    "release_pos_y": 53.66,
    "release_pos_z": 5.72,
    "pfx_x": -0.19,
    "pfx_z": 0.39,
    "plate_x": 0.3227046842704261,
    "plate_z": 1.7461671330486317,
    "zone": 9,
    "pitches": 1,
    "total_pitches": 2142,
    "avg_arm_angle": 37.236227824463136,
    "avg_release_speed": 84.19411764705882,
    "avg_pfx_x": 0.0757918552036199,
    "avg_pfx_z": 0.30054298642533944,
    "total_pitch_type_pitches": 221,
    "total_pitch_type_pitches_in_zone": 12,
    "pitch_type_freq": 0.10317460317460317,
    "pitch_type_zone_freq": 0.05429864253393665,
    "ovr_pitch_freq": 0.0056022408963585435
}
row2 = {
    "game_pk": 100000,
    "player_name": "Gausman, Kevin",
    "p_throws": "R",
    "arm_angle": 37.3,
    "pitch_type": "FS",
    "release_speed": 82.6,
    "ax": -14.301884872420835,
    "ay": 22.366899857517012,
    "az": -31.38390134204662,
    "vx0": 8.818622304670026,
    "vy0": -120.04725288094517,
    "vz0": -2.6126033499025603,
    "release_pos_x": -2.63,
    "release_pos_y": 53.62,
    "release_pos_z": 5.68,
    "pfx_x": -1.31,
    "pfx_z": 0.05,
    "plate_x": 0.1064148348012554,
    "plate_z": 1.6237305662915484,
    "zone": 8,
    "pitches": 1,
    "total_pitches": 2142,
    "avg_arm_angle": 37.236227824463136,
    "avg_release_speed": 84.03394833948339,
    "avg_pfx_x": -1.1361377613776138,
    "avg_pfx_z": 0.370639606396064,
    "total_pitch_type_pitches": 813,
    "total_pitch_type_pitches_in_zone": 60,
    "pitch_type_freq": 0.3795518207282913,
    "pitch_type_zone_freq": 0.07380073800738007,
    "ovr_pitch_freq": 0.028011204481792718
}
row3 = {
    "game_pk": 100000,
    "player_name": "Gausman, Kevin",
    "p_throws": "R",
    "arm_angle": 37.5,
    "pitch_type": "FS",
    "release_speed": 81.0,
    "ax": -12.31005458317196,
    "ay": 20.299815514864314,
    "az": -23.69842453682761,
    "vx0": 6.978450223026714,
    "vy0": -117.80531525792608,
    "vz0": -4.926117746985368,
    "release_pos_x": -2.61,
    "release_pos_y": 53.72,
    "release_pos_z": 5.81,
    "pfx_x": -1.18,
    "pfx_z": 0.83,
    "plate_x": -0.5123671246511787,
    "plate_z": 1.2806232020360788,
    "zone": 13,
    "pitches": 1,
    "total_pitches": 2142,
    "avg_arm_angle": 37.236227824463136,
    "avg_release_speed": 84.03394833948339,
    "avg_pfx_x": -1.1361377613776138,
    "avg_pfx_z": 0.370639606396064,
    "total_pitch_type_pitches": 813,
    "total_pitch_type_pitches_in_zone": 336,
    "pitch_type_freq": 0.3795518207282913,
    "pitch_type_zone_freq": 0.4132841328413284,
    "ovr_pitch_freq": 0.1568627450980392
}
row4 = {
    "game_pk": 100000,
    "player_name": "Gausman, Kevin",
    "p_throws": "R",
    "arm_angle": 39.0,
    "pitch_type": "FF",
    "release_speed": 92.1,
    "ax": -13.004442499689972,
    "ay": 26.751179004711677,
    "az": -14.017029002282996,
    "vx0": 7.590970686310515,
    "vy0": -133.733019513295,
    "vz0": -8.044445464745346,
    "release_pos_x": -2.44,
    "release_pos_y": 53.6,
    "release_pos_z": 5.9,
    "pfx_x": -0.95,
    "pfx_z": 1.38,
    "plate_x": -0.2748840869454042,
    "plate_z": 1.577471236091014,
    "zone": 13,
    "pitches": 1,
    "total_pitches": 2142,
    "avg_arm_angle": 37.236227824463136,
    "avg_release_speed": 93.94493670886078,
    "avg_pfx_x": -0.9111301989150089,
    "avg_pfx_z": 1.409403254972875,
    "total_pitch_type_pitches": 1106,
    "total_pitch_type_pitches_in_zone": 96,
    "pitch_type_freq": 0.5163398692810458,
    "pitch_type_zone_freq": 0.0867992766726944,
    "ovr_pitch_freq": 0.04481792717086835
}
row5 = {
    "game_pk": 100000,
    "player_name": "Gausman, Kevin",
    "p_throws": "R",
    "arm_angle": 37.1,
    "pitch_type": "FF",
    "release_speed": 94.8,
    "ax": -19.478251557329827,
    "ay": 29.519278856819973,
    "az": -14.320158576469122,
    "vx0": 9.894849359436636,
    "vy0": -137.64246927404466,
    "vz0": -4.93412023678617,
    "release_pos_x": -2.46,
    "release_pos_y": 53.96,
    "release_pos_z": 5.69,
    "pfx_x": -1.36,
    "pfx_z": 1.33,
    "plate_x": 0.1648262942095362,
    "plate_z": 2.7200674336021033,
    "zone": 5,
    "pitches": 1,
    "total_pitches": 2142,
    "avg_arm_angle": 37.23622782446313,
    "avg_release_speed": 93.94493670886075,
    "avg_pfx_x": -0.9111301989150089,
    "avg_pfx_z": 1.4094032549728752,
    "total_pitch_type_pitches": 1106,
    "total_pitch_type_pitches_in_zone": 105,
    "pitch_type_freq": 0.5163398692810458,
    "pitch_type_zone_freq": 0.0949367088607595,
    "ovr_pitch_freq": 0.049019607843137254
}
row6 = {
    "game_pk": 100000,
    "player_name": "Gausman, Kevin",
    "p_throws": "R",
    "arm_angle": 31.1,
    "pitch_type": "FS",
    "release_speed": 83.3,
    "ax": -15.25089145727048,
    "ay": 26.899217970060516,
    "az": -32.29969535832753,
    "vx0": 6.544731551113431,
    "vy0": -121.09248926523848,
    "vz0": -2.1245986938463224,
    "release_pos_x": -2.45,
    "release_pos_y": 53.73,
    "release_pos_z": 5.59,
    "pfx_x": -1.42,
    "pfx_z": -0.04,
    "plate_x": -0.8349157918548555,
    "plate_z": 1.6799110517058495,
    "zone": 13,
    "pitches": 1,
    "total_pitches": 2142,
    "avg_arm_angle": 37.23622782446313,
    "avg_release_speed": 84.03394833948339,
    "avg_pfx_x": -1.1361377613776138,
    "avg_pfx_z": 0.3706396063960639,
    "total_pitch_type_pitches": 813,
    "total_pitch_type_pitches_in_zone": 336,
    "pitch_type_freq": 0.3795518207282913,
    "pitch_type_zone_freq": 0.4132841328413284,
    "ovr_pitch_freq": 0.1568627450980392
}
row7 = {
    "game_pk": 200000,
    "player_name": "Gausman, Kevin",
    "p_throws": "R",
    "arm_angle": 37.1,
    "pitch_type": "FF",
    "release_speed": 94.8,
    "ax": -19.478251557329827,
    "ay": 29.519278856819973,
    "az": -14.320158576469122,
    "vx0": 9.894849359436636,
    "vy0": -137.64246927404466,
    "vz0": -4.93412023678617,
    "release_pos_x": -2.46,
    "release_pos_y": 53.96,
    "release_pos_z": 5.69,
    "pfx_x": -1.36,
    "pfx_z": 1.33,
    "plate_x": 0.1648262942095362,
    "plate_z": 2.7200674336021033,
    "zone": 5,
    "pitches": 1,
    "total_pitches": 2142,
    "avg_arm_angle": 37.23622782446313,
    "avg_release_speed": 93.94493670886075,
    "avg_pfx_x": -0.9111301989150089,
    "avg_pfx_z": 1.4094032549728752,
    "total_pitch_type_pitches": 1106,
    "total_pitch_type_pitches_in_zone": 105,
    "pitch_type_freq": 0.5163398692810458,
    "pitch_type_zone_freq": 0.0949367088607595,
    "ovr_pitch_freq": 0.049019607843137254
}   # row5 w/ diff gameID
global INPUT_DF
INPUT_DF = pandas.DataFrame([row1, row2, row3, row4, row5, row6, row7])

def test_load_pitch_data():
    """Test data loader with no input.
    
    Where 824815 is the gameID of the first row of pitch data in the parsed dataset.
    """
    
    # Call and verify
    res = profiler.load_pitch_data()
    assert res['game_pk'].iloc[0] == 824815
    
def test_load_pitch_data_valid():
    """Test data loader with valid input."""
    
    # Call and verify
    res = profiler.load_pitch_data("Gausman, Kevin")
    assert res['player_name'].iloc[0] == "Gausman, Kevin"
    
def test_get_durability_valid():
    
    """Test durability extractor with valid input."""
    
    # Call and verify
    res = profiler.get_durability(INPUT_DF)
    assert res == 2142
    
def test_get_handedness_valid():
    """Test handedness extractor with valid input."""
    
    # Call and verify
    res = profiler.get_handedness(INPUT_DF)
    assert res == "R"
    
def test_get_arm_angle_valid():
    """Test arm angle extractor with valid input."""
    
    # Call and verify
    res = profiler.get_arm_angle(INPUT_DF)
    assert res == 37.236227824463136
    
def test_get_arsenal_valid():
    """Test arsenal extractor with valid input."""
    
    # Call and verify
    res = profiler.get_arsenal(INPUT_DF)
    assert res == pytest.approx({'SL': 0.103, 'FS': 0.380, 'FF': 0.516}, abs=0.001)
    
def test_get_stuff_valid(mocker):
    """Test stuff extractor with valid input."""
    
    # Stub dependencies
    mocker.patch(
        "backend.profiler.profiler.get_arsenal",
        return_value={'SL': 0.103, 'FS': 0.380, 'FF': 0.516}
    )
    
    # Call and verify
    res = profiler.get_stuff(INPUT_DF)
    assert res == {
        'movement': {
            "SL": (0.0757918552036199, 0.30054298642533944), 
            "FS": (-1.1361377613776138, 0.370639606396064), 
            "FF": (-0.9111301989150089, 1.409403254972875)
        }, 
        'velocity': {
            "SL": 84.19411764705882, 
            "FS": 84.03394833948339, 
            "FF": 93.94493670886078
        }
    }
    
def test_get_locations_valid(mocker):
    """Test locations extractor with valid input."""
    # Stub dependencies
    mocker.patch(
        "backend.profiler.profiler.get_arsenal",
        return_value={'SL': 0.103, 'FS': 0.380, 'FF': 0.516}
    )
    
    # Call and verify
    res = profiler.get_locations(INPUT_DF)
    assert res == {
        "SL": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.05429864253393665, 0.0, 0.0, 0.0, 0.0, 0.0], 
        "FS": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.07380073800738007, 0.0, 0.0, 0.0, 0.0, 0.4132841328413284, 0.0], 
        "FF": [0.0, 0.0, 0.0, 0.0, 0.0949367088607595, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0867992766726944, 0.0]
    }
   
def test_calc_tunnel_valid():
    """Test tunnel calculator with valid input.
    
    LOOK: Calculations verified by both ClaudeSonnet5 and ChatGPT.
    """
    
    # Call and verify
    res = profiler.calc_tunnel(INPUT_DF.iloc[5])
    assert res == [
        pytest.approx((-2.450, 5.590), abs=0.001),
        pytest.approx((-1.959, 5.302), abs=0.001),
        pytest.approx((-1.566, 4.778), abs=0.001),
        pytest.approx((-1.279, 4.005), abs=0.001)
    ]

def test_pair_tunnels_valid_pos():
    """Test tunnel pairer with valid positive input.
    
    LOOK: Tunnel pairs verified by ClaudeSonnet5, ChatGPT, and by my observation of overlay videos.
    """
      
    # Call and verify
    # LOOK: calc_tunnel is used as a helper function within the context of this module, so it need not be stubbed/mocked
    assert profiler.pair_tunnels(profiler.calc_tunnel(INPUT_DF.iloc[1]), profiler.calc_tunnel(INPUT_DF.iloc[4])) == True   # tunnel_25
    
def test_pair_tunnels_valid_neg():
    """Test tunnel pairer with valid negative input."""
      
    # Call and verify
    assert profiler.pair_tunnels(profiler.calc_tunnel(INPUT_DF.iloc[0]), profiler.calc_tunnel(INPUT_DF.iloc[5])) == False   # tunnel_16

def test_symmetrize_tunnel_pair():
    """Test symmetrizer with valid input."""

    # Build input
    input = {'FF': {'FF': 0.0, 'FS': 0.5}, 'FS': {'FF': 0.0, 'FS': 0.0}}

    # Call and verify
    profiler.symmetrize_tunnel_pair(input, "FF", "FS")
    res = input
    assert res == {'FF': {'FF': 0.0, 'FS': 0.5}, 'FS': {'FF': 0.5, 'FS': 0.0}}   
    
def test_find_tunnels_valid(mocker):
    """Test tunnel profiler with valid input."""
    
    # Stub dependencies
    mocker.patch(
        "backend.profiler.profiler.get_arsenal",
        return_value={'SL': 0.103, 'FS': 0.380, 'FF': 0.516}
    )
    # TODO: stub calc_tunnel and pair_tunnels as well
    
    # Call and verify
    res = profiler.find_tunnels(INPUT_DF)
    assert res == {
    "FF": {
        "FF": 0.0,
        "FS": 2 / 2142,     # tunnel_34, tunnel_25, not tunnel_27 due to differing gameID
        "SL": 0.0
    },
    "FS": {
        "FF": 2 / 2142,
        "FS": 0.0,
        "SL": 1 / 2142     # tunnel_12
    },
    "SL": {
        "FF": 0.0,
        "FS": 1 / 2142,
        "SL": 0.0
    }
}
    
def test_aggregate_tunnels():
    """Test tunnel aggregator with valid input."""

    # Build input
    input = {
        'FF': {'FF': 0.0, 'FS': 0.5, 'SL': 0.25}, 
        'FS': {'FF': 0.5, 'FS': 0.0, 'SL': 0.0}, 
        'SL': {'FF': 0.25, 'FS': 0.0, 'SL': 0.0}
    }

    # Call and verify
    res = profiler.aggregate_tunnels(input)
    assert res == {'A': 0.75, 'F-F': 0.0, 'F-B': 0.25, 'F-O': 0.5, 'B-O': 0.0}
    
def test_profile_player_valid():
    """"""
    # TODO
    pass

def test_get_all_player_names(mocker):
    """Test pitcher name extractor."""
    
    # Stub dependencies
    mocker.patch(
        "backend.profiler.profiler.load_pitch_data",
        return_value=INPUT_DF
    )
    
    # Call and verify
    res = profiler.get_all_player_names()
    assert res == ["Gausman, Kevin"]

def test_main():
    """"""
    # TODO
    pass
