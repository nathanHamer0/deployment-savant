WITH pitches_table AS (
    SELECT
        game_pk,
        player_name,
        p_throws,
        arm_angle,
        pitch_type,
        release_speed,
        ax,
        ay,
        az,
        vx0,
        vy0,
        vz0,
        release_pos_x,
        release_pos_y,
        release_pos_z,
        pfx_x,
        pfx_z,
        plate_x,
        plate_z,
        zone,
        COUNT(*) AS pitches
    FROM 'backend/parser/raw_data.csv'
    -- Selects all desired data points
    GROUP BY game_pk, player_name, p_throws, arm_angle, pitch_type, release_speed, ax, ay, az, vx0, vy0, vz0, release_pos_x, release_pos_y, release_pos_z, pfx_x, pfx_z, plate_x, plate_z, zone
),

total_pitches_table AS (
    SELECT
        player_name,
        COUNT(*) AS total_pitches,
        SUM(arm_angle) / COUNT(*) AS avg_arm_angle
    FROM 'backend/parser/raw_data.csv'
    -- Selects a player
    GROUP BY player_name
),

pitch_type_pitches_table AS (
    SELECT
        player_name,
        pitch_type,
        SUM(release_speed) / COUNT(*) AS avg_release_speed,
        SUM(pfx_x) / COUNT(*) AS avg_pfx_x,
        SUM(pfx_z) / COUNT(*) AS avg_pfx_z,
        COUNT(*) AS total_pitch_type_pitches
    FROM 'backend/parser/raw_data.csv'
    -- Selects a player and pitch
    GROUP BY player_name, pitch_type
),

pitch_type_pitches_in_zone_table AS (
    SELECT
        player_name,
        pitch_type,
        zone,
        COUNT(*) AS total_pitch_type_pitches_in_zone,
    FROM 'backend/parser/raw_data.csv'
    -- Selects a player, pitch, and zone
    GROUP BY player_name, pitch_type, zone
)

SELECT
    *,
    total_pitch_type_pitches / total_pitches AS pitch_type_freq,
    total_pitch_type_pitches_in_zone / total_pitch_type_pitches AS pitch_type_zone_freq,
    total_pitch_type_pitches_in_zone / total_pitches AS ovr_pitch_freq
FROM pitches_table 
    JOIN total_pitches_table ON pitches_table.player_name = total_pitches_table.player_name
    JOIN pitch_type_pitches_table ON 
        pitches_table.player_name = pitch_type_pitches_table.player_name 
        AND pitches_table.pitch_type = pitch_type_pitches_table.pitch_type
    JOIN pitch_type_pitches_in_zone_table ON 
        pitches_table.player_name = pitch_type_pitches_in_zone_table.player_name 
        AND pitches_table.pitch_type = pitch_type_pitches_in_zone_table.pitch_type
        AND pitches_table.zone = pitch_type_pitches_in_zone_table.zone