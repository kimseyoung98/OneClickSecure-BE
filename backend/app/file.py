from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import glob
import os

router = APIRouter(prefix="/inventory", tags=["Inventory"])

@router.get("/download/{host_id}")
def download_check_result(host_id: int):
    file_path = f"./collected_results/Results_{host_id}_*.txt"
    files = glob.glob(file_path)
    if not files:
        raise HTTPException(status_code=404, detail="결과 파일이 없습니다")
    latest_file = max(files, key=os.path.getctime)
    filename = f"check_result_{host_id}.txt"
    return FileResponse(latest_file, filename=filename)
