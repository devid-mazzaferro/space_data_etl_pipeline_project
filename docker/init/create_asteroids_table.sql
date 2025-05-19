CREATE TABLE IF NOT EXISTS asteroids (
    id TEXT PRIMARY KEY,
    name TEXT,
    abs_mag FLOAT,
    min_d FLOAT,
    max_d FLOAT,
    hazard BOOLEAN,
    eccentricity FLOAT,
    semi_maj_ax FLOAT,
    inclination FLOAT,
    ascending_node_lon FLOAT,
    perihelion_dist FLOAT,
    aphelion_dist FLOAT,
    perihelion_argument FLOAT,
    mean_anomaly FLOAT,
    mean_motion FLOAT,
    epoch_osculation FLOAT
);