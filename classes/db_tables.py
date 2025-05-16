from sqlalchemy import Column, String, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Asteroid(Base):
    __tablename__ = "asteroids"

    id = Column(String, primary_key=True)
    name = Column(String)
    abs_mag = Column(Float)
    min_d = Column(Float)
    max_d = Column(Float)
    hazard = Column(Boolean)
    eccentricity = Column(Float)
    semi_maj_ax = Column(Float)
    inclination = Column(Float)
    ascending_node_lon = Column(Float)
    perihelion_dist = Column(Float)
    aphelion_dist = Column(Float)