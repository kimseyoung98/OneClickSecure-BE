from sqlalchemy.orm import Session
from . import models, schemas

def create_host(db: Session, host: schemas.HostCreate, os_info: str):
    db_host = models.Host(
        name=host.name,
        username=host.username,
        password=host.password,
        ip=host.ip,
        os=os_info   # ← OS 정보 저장
    )
    db.add(db_host)
    db.commit()
    db.refresh(db_host)
    return db_host

def get_hosts(db: Session):
    return db.query(models.Host).all()
