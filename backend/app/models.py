from sqlalchemy import Column, Integer, String
from .database import Base

class Host(Base):
    __tablename__ = "hosts"
    id = Column(Integer, primary_key=True, index=True)      # DB PK
    name = Column(String, index=True)                       # 호스트명
    username = Column(String)                               # 서버 계정명 (ex: root)
    password = Column(String)                               # 서버 비밀번호
    ip = Column(String, unique=True, index=True)            # 서버 IP
    os = Column(String, index=True)                         # OS 정보
