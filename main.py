from fastapi import FastAPI, Depends, status, HTTPException
from typing import List
import schemas,  models
from sqlalchemy.orm import Session
from database import engine
from database import get_db

app = FastAPI()

models.Base.metadata.create_all(engine)

@app.get('/', tags = ['Personal'])
def welcome_page():
    info = 'These are Josh\'s APIs'
    return info


@app.get('/data', response_model=List[schemas.ShowData], tags = ['Datas'])
def all_data(db: Session = Depends(get_db)):
    data = db.query(models.Data).all()
    return data

@app.post('/data', status_code=status.HTTP_201_CREATED, tags = ['Datas'])
def create_data(request: schemas.Data, db: Session = Depends(get_db)):
    new_data = models.Data(name=request.name, phone=request.phone, message=request.message)
    db.add(new_data)
    db.commit()
    db.refresh(new_data)
    return new_data

@app.get('/data/{id}', status_code=200, response_model=schemas.ShowData, tags = ['Datas'])
def show_data(id: int, db: Session = Depends(get_db)):
    data = db.query(models.Data).filter(models.Data.id == id).first()
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Data with the id {id} is not found')
    return data

@app.delete('/data/{id}', status_code=status.HTTP_204_NO_CONTENT, tags = ['Datas'])
def delete_data(id: int, db: Session = Depends(get_db)):
    data = db.query(models.Data).filter(models.Data.id == id)

    if not data.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Data with the id {id} is not found in the database')
    data.delete(synchronize_session=False)
    db.commit()
    return f'Data {id} has been deleted from the database'