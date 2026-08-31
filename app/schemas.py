from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class TeamBase(BaseModel):
    name: str
    nationality: str
    base: Optional[str] = None


class TeamCreate(TeamBase):
    pass


class TeamOut(TeamBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class DriverBase(BaseModel):
    name: str
    number: int = Field(gt=0, lt=100)
    nationality: str
    team_id: int


class DriverCreate(DriverBase):
    pass


class DriverOut(DriverBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class RaceBase(BaseModel):
    name: str
    circuit: str
    country: str
    season: int = Field(gt=1950)


class RaceCreate(RaceBase):
    pass


class RaceOut(RaceBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class ResultBase(BaseModel):
    position: int = Field(gt=0)
    points: float = Field(ge=0)
    driver_id: int
    race_id: int


class ResultCreate(ResultBase):
    pass


class ResultOut(ResultBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
