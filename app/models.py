from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    nationality = Column(String, nullable=False)
    base = Column(String, nullable=True)

    drivers = relationship("Driver", back_populates="team")


class Driver(Base):
    __tablename__ = "drivers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    number = Column(Integer, nullable=False)
    nationality = Column(String, nullable=False)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)

    team = relationship("Team", back_populates="drivers")
    results = relationship("Result", back_populates="driver")


class Race(Base):
    __tablename__ = "races"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    circuit = Column(String, nullable=False)
    country = Column(String, nullable=False)
    season = Column(Integer, nullable=False)

    results = relationship("Result", back_populates="race")


class Result(Base):
    __tablename__ = "results"

    id = Column(Integer, primary_key=True, index=True)
    position = Column(Integer, nullable=False)
    points = Column(Float, nullable=False, default=0.0)
    driver_id = Column(Integer, ForeignKey("drivers.id"), nullable=False)
    race_id = Column(Integer, ForeignKey("races.id"), nullable=False)

    driver = relationship("Driver", back_populates="results")
    race = relationship("Race", back_populates="results")
