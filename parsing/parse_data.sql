WITH pitches_table AS (
    SELECT
        player_name,
        pitch_type,
        pfx_x,
        pfx_z,
        zone,
        COUNT(*) AS pitches
    FROM 'raw_data.csv'
    -- Selects a player, pitch, its movement, and its zone location
    GROUP BY player_name, pitch_type, pfx_x, pfx_z, zone
),

total_pitch_type_pitches_table AS (
    SELECT
        player_name,
        pitch_type,
        COUNT(*) AS total_pitch_type_pitches
    FROM 'raw_data.csv'
    -- Selects a player and pitch
    GROUP BY player_name, pitch_type
),

total_pitches_table AS (
    SELECT
        player_name,
        COUNT(*) AS total_pitches
    FROM 'raw_data.csv'
    -- Selects a player
    GROUP BY player_name
)

SELECT
    *,
    total_pitch_type_pitches / total_pitches AS pitch_type_freq,
    pitches / total_pitch_type_pitches AS pitch_type_zone_freq,
    pitches / total_pitches AS pitch_freq
FROM pitches_table 
    JOIN total_pitch_type_pitches_table ON 
        pitches_table.player_name = total_pitch_type_pitches_table.player_name 
        AND pitches_table.pitch_type = total_pitch_type_pitches_table.pitch_type
    JOIN total_pitches_table ON pitches_table.player_name = total_pitches_table.player_name;