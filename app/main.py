from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import Base, engine, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Circuito API",
    description="API para gerenciar equipes, pilotos, corridas e resultados de F1.",
    version="1.0.0",
)


@app.get("/health", tags=["Health"])
def health_check():
    # so confirma que a api ta no ar
    return {"status": "ok"}

# Bloco de times


@app.post("/teams", response_model=schemas.TeamOut, status_code=201, tags=["Teams"])
def create_team(team: schemas.TeamCreate, db: Session = Depends(get_db)):
    # confere se ja existe uma equipe com esse nome antes de criar
    existing = db.query(models.Team).filter(models.Team.name == team.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Ja existe uma equipe com esse nome")
    db_team = models.Team(**team.model_dump())
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team


@app.get("/teams", response_model=List[schemas.TeamOut], tags=["Teams"])
def list_teams(db: Session = Depends(get_db)):
    return db.query(models.Team).all()


@app.get("/teams/{team_id}", response_model=schemas.TeamOut, tags=["Teams"])
def get_team(team_id: int, db: Session = Depends(get_db)):
    team = db.query(models.Team).filter(models.Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Equipe nao encontrada")
    return team

# Bloco de pilotos


@app.post("/drivers", response_model=schemas.DriverOut, status_code=201, tags=["Drivers"])
def create_driver(driver: schemas.DriverCreate, db: Session = Depends(get_db)):
    # confere se a equipe existe antes de criar o piloto vinculado a ela
    team = db.query(models.Team).filter(models.Team.id == driver.team_id).first()
    if not team:
        raise HTTPException(status_code=400, detail="team_id invalido: equipe nao existe")
    db_driver = models.Driver(**driver.model_dump())
    db.add(db_driver)
    db.commit()
    db.refresh(db_driver)
    return db_driver


@app.get("/drivers", response_model=List[schemas.DriverOut], tags=["Drivers"])
def list_drivers(db: Session = Depends(get_db)):
    return db.query(models.Driver).all()


@app.get("/drivers/{driver_id}", response_model=schemas.DriverOut, tags=["Drivers"])
def get_driver(driver_id: int, db: Session = Depends(get_db)):
    driver = db.query(models.Driver).filter(models.Driver.id == driver_id).first()
    if not driver:
        raise HTTPException(status_code=404, detail="Piloto nao encontrado")
    return driver

# Bloco de corridas


@app.post("/races", response_model=schemas.RaceOut, status_code=201, tags=["Races"])
def create_race(race: schemas.RaceCreate, db: Session = Depends(get_db)):
    db_race = models.Race(**race.model_dump())
    db.add(db_race)
    db.commit()
    db.refresh(db_race)
    return db_race


@app.get("/races", response_model=List[schemas.RaceOut], tags=["Races"])
def list_races(db: Session = Depends(get_db)):
    return db.query(models.Race).all()


@app.get("/races/{race_id}", response_model=schemas.RaceOut, tags=["Races"])
def get_race(race_id: int, db: Session = Depends(get_db)):
    race = db.query(models.Race).filter(models.Race.id == race_id).first()
    if not race:
        raise HTTPException(status_code=404, detail="Corrida nao encontrada")
    return race

# Bloco de resultados


@app.post("/results", response_model=schemas.ResultOut, status_code=201, tags=["Results"])
def create_result(result: schemas.ResultCreate, db: Session = Depends(get_db)):
    # confere se o piloto existe
    driver = db.query(models.Driver).filter(models.Driver.id == result.driver_id).first()
    if not driver:
        raise HTTPException(status_code=400, detail="driver_id invalido: piloto nao existe")
    # confere se a corrida existe
    race = db.query(models.Race).filter(models.Race.id == result.race_id).first()
    if not race:
        raise HTTPException(status_code=400, detail="race_id invalido: corrida nao existe")
    db_result = models.Result(**result.model_dump())
    db.add(db_result)
    db.commit()
    db.refresh(db_result)
    return db_result


@app.get("/results", response_model=List[schemas.ResultOut], tags=["Results"])
def list_results(db: Session = Depends(get_db)):
    return db.query(models.Result).all()


@app.get(
    "/results/race/{race_id}",
    response_model=List[schemas.ResultOut],
    tags=["Results"],
)
def get_results_by_race(race_id: int, db: Session = Depends(get_db)):
    # confere se a corrida existe antes de listar os resultados dela
    race = db.query(models.Race).filter(models.Race.id == race_id).first()
    if not race:
        raise HTTPException(status_code=404, detail="Corrida nao encontrada")
    return db.query(models.Result).filter(models.Result.race_id == race_id).all()