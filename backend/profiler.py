import pandas

BALL_DIAM = 2.9
TUNNEL_END_Y = 23.8     # Decision point (point at which tunnel ends)
TUNNEL_MARGIN = BALL_DIAM / 12    # Convert inches to feet
PINGS = 4      # Number of tunnel-forming pings along pitch's pre-decision-point trajectory

AVG_PITCH_COUNT_PER_IP = 16     # sourced by GoogleAI overview
IP_THRESHOLD = 50   # modifiable parameter

FASTBALL = ["FF", "SI", "FC"]
BREAKING = ["CU", "KC", "CS", "SL", "ST", "SV", "SC"]
OFFSPEED = ["CH", "FS", "FO"]
MISC = ["KN", "EP", "FA", "IN", "PO", "UN"]

def load_pitch_data(player_name=""):
    """Loads pitch data as a DataFrame from the parsed Statcast data CSV.

    Args:
        player_name (str, optional): name of player for whom data is specifically seeked. Defaults to "".

    Returns:
        DataFrame: specified pitch data.
    """
    pitches = pandas.read_csv('backend/data/parsed_data.csv')
    if player_name:
        pitches = pitches[pitches['player_name'] == player_name]
    return pitches

def get_durability(pitches):
    """Returns durability of player given their pitch data.

    Args:
        pitches (DataFrame): player's pitch data.

    Returns:
        int: total pitches thrown by player.
    """
    return pitches['total_pitches'].iloc[0]

def get_handedness(pitches):
    """Returns handedness of player given their pitch data.

    Args:
        pitches (DataFrame): player's pitch data.

    Returns:
        str: player handedness.
    """
    return pitches['p_throws'].iloc[0]
    
def get_arm_angle(pitches):
    """Returns arm angle of player given their pitch data.

    Args:
        pitches (DataFrame): player's pitch data.

    Returns:
        float: player arm angle.
    """
    return pitches['avg_arm_angle'].iloc[0]
    
def get_arsenal(pitches):
    """Returns arsenal of player given their pitch data.

    Args:
        pitches (DataFrame): player's pitch data.

    Returns:
        dict[str]: player's pitch type frequencies.
    """
    arsenal = {}
    for pt in pitches['pitch_type']:
        if pt not in arsenal:
            arsenal[pt] = pitches[pitches['pitch_type'] == pt].iloc[0]['pitch_type_freq']
    return arsenal
    
def get_stuff(pitches):
    """Returns a stuff profile (in terms of movement and velocity) of player given their pitch data.

    Args:
        pitches (DataFrame): player's pitch data.

    Returns:
        dict[dict]: player's movement and velocity profile by pitch type.
    """
    arsenal = get_arsenal(pitches)
    mov = {}
    velo = {}
    for pt in arsenal:
        pt_pitches = pitches[pitches['pitch_type'] == pt]
        mov[pt] = (pt_pitches['avg_pfx_x'].iloc[0], pt_pitches['avg_pfx_z'].iloc[0])
        velo[pt] = pt_pitches['avg_release_speed'].iloc[0]
    return {'movement': mov, 'velocity': velo}

def get_locations(pitches):
    """Returns a location profile (in terms of attack zone frequencies) of player given their pitch data.

    Args:
        pitches (DataFrame): player's pitch data.

    Returns:
        dict[dict]: player's location profile by pitch type.
    """
    arsenal = get_arsenal(pitches)
    locs = {}
    for pt in arsenal:
        locs[pt] = []
        pt_pitches = pitches[pitches['pitch_type'] == pt]
        for zone in range(1, 15):   # idx(zone) = zone - 1
            pt_pitches_in_zone = pt_pitches[pt_pitches['zone'] == zone]
            if pt_pitches_in_zone.empty:
                locs[pt].append(0.0)
            else:
                locs[pt].append(pt_pitches_in_zone['pitch_type_zone_freq'].iloc[0])
    return locs

def calc_tunnel(pitch):
    """Tracks pitch trajectory and returns the xz-coordinates of a given pitch at its tunneling 
    points. See scribbles/tunnel_heuristics.txt for underlying algebra formulizations.

    Args:
        pitch (DataFrame): data for a singular pitch.

    Returns:
        tuple[float]: xz-coordinates of pitch at tunnel pings.
    """
    # Extract metrics
    ax = pitch['ax']
    ay = pitch['ay']
    az = pitch['az']
    vx0 = pitch['vx0']
    vy0 = pitch['vy0']
    vz0 = pitch['vz0']
    release_pos_x = pitch['release_pos_x']
    release_pos_y = pitch['release_pos_y']
    release_pos_z = pitch['release_pos_z']
    
    # Calculate displacements of tunnel pings
    dy = TUNNEL_END_Y - release_pos_y
    delta_dp = dy / (PINGS - 1)
    d_pings = []
    for i in range(PINGS):
        d_pings.append(i * delta_dp)
        
    tunnel = []
    for dp in d_pings:
        
        # Apply quadratic formula (get time to reach tunnel pings)
        t1 = (-vy0 + (vy0**2 - 4*(0.5*ay)*-1*dp)**0.5) / (2*(0.5*ay))
        t2 = (-vy0 - (vy0**2 - 4*(0.5*ay)*-1*dp)**0.5) / (2*(0.5*ay))
        if t1 > 0 and t1 <= t2:     # Parse roots for sensical root
            t = t1
        else:
            t = t2
    
        # Calculate tunnel (get xz-coordinates at tunnel pings)
        tunnel.append((release_pos_x + vx0*t + 0.5*ax*t**2, release_pos_z + vz0*t + 0.5*az*t**2))
            
    return tunnel

# LOOK
def pair_tunnels(tunnel_a, tunnel_b):
    """Given a pair of pitches and the xz-pings along their tunnel, returns whether the pitches tunnel or not.

    Args:
        tunnel_a (list[tuple]): xz-pings of pitch a's tunnel.
        tunnel_b (list[tuple]): xz-pings of pitch b's tunnel.

    Returns:
        bool: trueness of the tunneling pair.
    """
    for i in range(PINGS):
        ping_a = tunnel_a[i]
        ping_b = tunnel_b[i]
        # LOOK: design choice; margin is a square (rectangular) rather than a circle (euclidean), maybe fix [AI-GEN: see ClaudeSonnet5 chat for help]
        if abs(ping_a[0] - ping_b[0]) > TUNNEL_MARGIN or abs(ping_a[1] - ping_b[1]) > TUNNEL_MARGIN:
            return False
    return True

def symmetrize_tunnel_pair(tps, pt_a, pt_b):
    """Reflects tunnel pair frequencies across commutative 2D dictionary entries (i.e., reflecting corresponding floats onto those commutative 
    2D keys which were not acknowledged in the original tunneling pair count in the parent function find_tunnels).

    Args:
        tps (dict[dict]): asymmetrical tunnel pair frequencies.
        pt_a (str): a pitch type of a tunnel pair.
        pt_b (str): a pitch type of a tunnel pair.
    """
    if tps[pt_a][pt_b] > 0:
        tps[pt_b][pt_a] = tps[pt_a][pt_b]

# OPTIMIZE: O(n^2)
def find_tunnels(pitches):
    """Returns a tunneling profile of player given their pitch data. A tunnel being respected as 
    two pitches of different pitch-types which exist within a TUNNEL_MARGIN of eachother along the pings of 
    their pre-decision-point trajectory (~23.8 feet from homeplate [https://www.baseballprospectus.com/news/article/31030/prospectus-feature-introducing-pitch-tunnels/]).
    A pitch's tunnel occurs over its pre-decision-point trajectory, as a tunnel is effective so long 
    as it remains intact up until the batter's decision point, and so, the tunnel exists up until this same point. 
    
    To respect the contextuality of tunneling pairs, two pitches only tunnel if they are thrown in the same game.

    Args:
        pitches (DataFrame): player's pitch data.

    Returns:
        dict[dict]: player's tunneling profile by pitch type.
    """
    
    # Initialize tunneling pair data structure
    arsenal = get_arsenal(pitches)
    tunnel_pairs = {}
    for pt_a in arsenal:
        tunnel_pairs[pt_a] = {}
        for pt_b in arsenal:
            tunnel_pairs[pt_a][pt_b] = 0 
            
    # Calculate tunnels (and cache other info relevant to tunnel-pairing)
    tunnel_packs = []
    for i, p in pitches.iterrows():
        tunnel_packs.append({'game_pk': p['game_pk'], 'pitch_type': p['pitch_type'], 'tunnel': calc_tunnel(p)})
    
    # Count tunneling pairs [OPTIMIZE: ~O(n^2)]
    n = len(tunnel_packs)
    for i in range(n):
        tunnel_pack_a = tunnel_packs[i]
        for j in range(i + 1, n):   # start=i+1; as to not check pairs backwards, as such pairs have already been evaluated in forwards
            tunnel_pack_b = tunnel_packs[j]
            if tunnel_pack_a['game_pk'] == tunnel_pack_b['game_pk']:    # OPTIMIZE: should group pitches by game_pk beforehand to avoid checking overhead
                pt_a = tunnel_pack_a['pitch_type']
                pt_b = tunnel_pack_b['pitch_type']
                if pt_a == pt_b:
                    continue
                if pair_tunnels(tunnel_pack_a['tunnel'], tunnel_pack_b['tunnel']):
                    tunnel_pairs[pt_a][pt_b] += 1
                    
    # Symmetrize tunnel pair frequencies across 2D-dicitonary
    for pt_a in arsenal:
        for pt_b in arsenal:
            symmetrize_tunnel_pair(tunnel_pairs, pt_a, pt_b)
               
    # Find frequencies (tunnel-rate) of counted tunneling pairs (where tunnel-rate is tunnel pairings per total pitches)
    p_tot = pitches['total_pitches'].iloc[0]
    for pt_a in arsenal:
        for pt_b in arsenal:
            tunnel_pairs[pt_a][pt_b] = tunnel_pairs[pt_a][pt_b] / p_tot
    return tunnel_pairs

def aggregate_tunnels(tunnel_pairs):
    """Given tunnel-pair frequencies specified by pitch-type, aggregate those frequencies into broader pitch-class specified tunnel-pairs.

    Args:
        tunnel_pairs (dict[dict]): a player's tunneling frequencies by pitch-type pairs (pairs conveyed structurally by 2D-dictionary).

    Returns:
        dict: a player's tunneling frequencies by pitch-class pairs (pairs conveyed literally by 1D-dictionary).
    """
    aggregate_tunnels = {
        'A': 0.0,   # Any
        'F-F': 0.0,     # Fastball-Fastball
        'F-B': 0.0,     # Fastball-Breaking
        'F-O': 0.0,     # Fastball-Offspeed
        'B-O': 0.0      # Breaking-Offspeed
    }
    n = len(tunnel_pairs)
    for i in range(n):
        pt_a = list(tunnel_pairs.keys())[i]
        for j in range(i + 1, n):   
            pt_b = list(tunnel_pairs.keys())[j]
            freq = tunnel_pairs[pt_a][pt_b]
            aggregate_tunnels['A'] += freq
            if pt_a in FASTBALL and pt_b in FASTBALL:
                aggregate_tunnels['F-F'] += freq
            elif (pt_a in FASTBALL and pt_b in BREAKING) or (pt_a in BREAKING and pt_b in FASTBALL):
                aggregate_tunnels['F-B'] += freq
            elif (pt_a in FASTBALL and pt_b in OFFSPEED) or (pt_a in OFFSPEED and pt_b in FASTBALL):
                aggregate_tunnels['F-O'] += freq
            elif (pt_a in BREAKING and pt_b in OFFSPEED) or (pt_a in OFFSPEED and pt_b in BREAKING):
                aggregate_tunnels['B-O'] += freq
    return aggregate_tunnels

def profile_player(player_name):
    """Given a player's name, builds a profile for that player and returns it.

    Args:
       player_name (str): name of player.

    Returns:
        dict[dict]: dictionary of pitcher attributes that make up a player's pitcher-profile.
    """
    pitches = load_pitch_data(player_name)
    profile = {}
    profile['durability'] = get_durability(pitches)   
    profile['handedness'] = get_handedness(pitches)
    profile['arm_angle'] = get_arm_angle(pitches)
    profile['arsenal'] = get_arsenal(pitches)
    profile['stuff'] = get_stuff(pitches)
    profile['locations'] = get_locations(pitches)
    profile['tunnel_pairs'] = find_tunnels(pitches)
    profile['aggregate_tunnel_pairs'] = aggregate_tunnels(profile['tunnel_pairs'])
    return profile

def get_all_player_names():
    """Returns a list of player names from loaded pitch data.

    Returns:
        list[str]: list of player names.
    """
    pitches = load_pitch_data()
    player_names = []
    for name in pitches['player_name']:
        if name not in player_names:
            player_names.append(name)
    return player_names
    
def main():
    """Returns a dictionary of player pitcher-profiles.

    Returns:
        dict[dict]: dictionary of player pitcher-profiles.
    """
    profiles = {}
    names = get_all_player_names()
    for n in names:
        # Check sample qualification
        pitches = load_pitch_data(n)
        pitch_count = get_durability(pitches)   
        if pitch_count >= AVG_PITCH_COUNT_PER_IP * IP_THRESHOLD:
            profiles[n] = profile_player(n)
    return profiles

if __name__ == "__main__":
    main()