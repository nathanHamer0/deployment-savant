import pandas

BALL_DIAM = 2.9
TUNNEL_END_Y = 23.8     # Decision point (point at which tunnel ends)
TUNNEL_MARGIN = BALL_DIAM / 12    # Convert inches to feet
PINGS = 4      # Number of tunnel-forming pings along pitch's pre-decision-point trajectory

def load_pitch_data(player_name=""):
    """Loads pitch data as a DataFrame from the parsed Statcast data CSV.

    Args:
        player_name (str, optional): name of player for whom data is specifically seeked. Defaults to "".

    Returns:
        DataFrame: specified pitch data.
    """
    pitches = pandas.read_csv('backend/parser/parsed_data.csv')
    if player_name:
        pitches = pitches[pitches['player_name'] == player_name]
    return pitches

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
        
    # Apply quadratic formula (get time to reach tunnel pings)
    t_pings = []
    for dp in d_pings:
        t1 = (-vy0 + (vy0**2 - 4*(0.5*ay)*-1*dp)**0.5) / (2*(0.5*ay))
        t2 = (-vy0 - (vy0**2 - 4*(0.5*ay)*-1*dp)**0.5) / (2*(0.5*ay))
        
        # Parse roots for sensical root
        if t1 > 0 and t1 <= t2:
            t = t1
        else:
            t = t2
        t_pings.append(t)
    
    # Calculate tunnel (get xz-coordinates at tunnel pings)
    tunnel = []
    for tp in t_pings:
        tunnel.append((release_pos_x + vx0*tp + 0.5*ax*tp**2, release_pos_z + vz0*tp + 0.5*az*tp**2))
    return tunnel

# FIXME
def tunnel_pair(tunnel_a, tunnel_b):
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
        # FIXME: design choice; margin is a square (rectangular) rather than a circle (euclidean), maybe fix [AI-GEN: see ClaudeSonnet5 chat for help]
        if abs(ping_a[0] - ping_b[0]) > TUNNEL_MARGIN or abs(ping_a[1] - ping_b[1]) > TUNNEL_MARGIN:
            return False
    return True

def find_tunnels(pitches):
    """Returns a tunneling profile of player given their pitch data. A tunnel being respected as 
    two pitches of different pitch-types which exist within a TUNNEL_MARGIN of eachother along the pings of 
    their pre-decision-point trajectory (~23.8 feet from homeplate [https://www.baseballprospectus.com/news/article/31030/prospectus-feature-introducing-pitch-tunnels/]).
    A pitch's tunnel occurs over its pre-decision-point trajectory, as a tunnel is effective so long 
    as it remains intact up until the batter's decision point, and so, the tunnel exists up until this same point. 

    Args:
        pitches (DataFrame): player's pitch data.

    Returns:
        dict[dict]: player's tunneling profile by pitch type.
    """
    # Initialize tunneling pair data structure
    arsenal = get_arsenal(pitches)
    tunnels = {}
    for pt_a in arsenal:
        tunnels[pt_a] = {}
        for pt_b in arsenal:
            tunnels[pt_a][pt_b] = 0
            
    # Count tunneling pairs
    for i, p_a in pitches.iterrows():
        tunnel_a = calc_tunnel(p_a)
        for j, p_b in pitches.iterrows():
            tunnel_b = calc_tunnel(p_b)   
            if tunnel_pair(tunnel_a, tunnel_b) and i != j:
                tunnels[p_a['pitch_type']][p_b['pitch_type']] += 1
               
    # Find frequencies (tunnel-rate) of counted tunneling pairs (where tunnel-rate is tunnel pairings per total pitches)
    p_tot = pitches['total_pitches'].iloc[0]
    for p_a in arsenal:
        for p_b in arsenal:
            tunnels[p_a][p_b] = tunnels[p_a][p_b] / p_tot
    return tunnels
    
def profile_player(player_name):
    """Given a player's name, builds a profile for that player and returns it.

    Args:
        player_name (str): name of player for whom a profile is seeked.

    Returns:
        dict[dict]: dictionary of pitcher attributes that make up a player's pitcher-profile.
    """
    pitches = load_pitch_data(player_name)
    profile = {}
    profile['handedness'] = get_handedness(pitches)
    profile['arm_angle'] = get_arm_angle(pitches)
    profile['arsenal'] = get_arsenal(pitches)
    profile['stuff'] = get_stuff(pitches)
    profile['locations'] = get_locations(pitches)
    profile['tunnels'] = find_tunnels(pitches)
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
        profiles[n] = profile_player(n)
    return profiles

if __name__ == "__main__":
    main()