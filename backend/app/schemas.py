from pydantic import BaseModel, ConfigDict
from typing import Optional

# 호스트 등록용 (POST /register)
class HostCreate(BaseModel):
    name: str           # 호스트명 (ex: web-01)
    username: str       # 서버 접속 계정명 (ex: root)
    password: str       # 서버 접속 비밀번호
    ip: str             # 서버 IP

# 호스트 조회용 (GET /list, etc)
class HostRead(BaseModel):
    id: int             # DB PK (고유번호)
    name: str           # 호스트명
    username: str       # 서버 접속 계정명
    ip: str             # 서버 IP
    os: Optional[str] = None  # OS 정보 (등록 시 자동 수집)

    model_config = ConfigDict(from_attributes=True)  # ✅ 올바른 들여쓰기

# 점검용 (POST /check)
class HostCheck(BaseModel):
    username: str       # 서버 접속 계정명 (ex: root)
    password: str       # 서버 접속 비밀번호
    ip: str             # 서버 IP
