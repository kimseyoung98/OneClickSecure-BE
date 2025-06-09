from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import inventory
from app.database import Base, engine

app = FastAPI(
    title="Inventory Management API",
    description="API for managing hosts and running Ansible playbooks.",
    version="1.0.0"
)

# CORS 미들웨어
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB 테이블 자동 생성
Base.metadata.create_all(bind=engine)

# 라우터 등록
app.include_router(inventory.router)

@app.get("/")
def root():
    return {"message": "Inventory API is running."}
