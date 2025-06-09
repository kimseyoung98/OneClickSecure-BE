from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import crud, schemas, models
from app.ansible_utils import get_os_info_with_ansible
from app.check_runner import run_os_check_script  

router = APIRouter(prefix="/inventory", tags=["Inventory"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=schemas.HostRead)
def register_host(host: schemas.HostCreate, db: Session = Depends(get_db)):
    os_info = get_os_info_with_ansible(host.ip, host.username, host.password)
    return crud.create_host(db, host, os_info)

@router.get("/list", response_model=list[schemas.HostRead])
def list_hosts(db: Session = Depends(get_db)):
    return crud.get_hosts(db)

@router.delete("/delete/{host_id}")
def delete_host(host_id: int, db: Session = Depends(get_db)):
    host = db.query(models.Host).filter(models.Host.id == host_id).first()
    if not host:
        raise HTTPException(status_code=404, detail="Host not found")
    db.delete(host)
    db.commit()
    return {"msg": "삭제 완료"}

@router.post("/check")
def check_host(info: schemas.HostCheck, db: Session = Depends(get_db)):
    host = db.query(models.Host).filter(models.Host.ip == info.ip).first()
    if not host:
        raise HTTPException(status_code=404, detail="Host not found")
    os_info = host.os
    return run_os_check_script(info.ip, info.username, info.password, os_info, host.id)  # host.id 추가
