import os
import shutil
import tempfile
import zipfile
from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from app.services.parser import InstaParser
from app.services.taste_dna import analyze_taste_dna
from app.services.secret_collection import analyze_secret_collection
from app.services.ideal_type import analyze_ideal_type
from app.services.algorithm_expose import analyze_algorithm_expose
from app.services.db_service import save_analysis_result, fetch_analysis_result
from app.utils.cleanup import create_job, cleanup_expired_jobs

router = APIRouter()

def run_analysis(extract_dir: str) -> dict:
    # Check if there is a single top-level folder inside extract_dir
    subdirs = [os.path.join(extract_dir, d) for d in os.listdir(extract_dir) if os.path.isdir(os.path.join(extract_dir, d))]
    target_dir = extract_dir
    if len(subdirs) == 1 and ('ads_information' in os.listdir(subdirs[0]) or 'connections' in os.listdir(subdirs[0]) or 'your_instagram_activity' in os.listdir(subdirs[0])):
        target_dir = subdirs[0]

    parser = InstaParser(target_dir)
    taste_dna = analyze_taste_dna(parser)
    secret_collection = analyze_secret_collection(parser)
    ideal_type = analyze_ideal_type(parser)
    algorithm_expose = analyze_algorithm_expose(parser)

    return {
        "taste_dna": taste_dna,
        "secret_collection": secret_collection,
        "ideal_type": ideal_type,
        "algorithm_expose": algorithm_expose
    }

@router.post("/upload")
async def upload_zip(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    if not file.filename.endswith('.zip'):
        raise HTTPException(status_code=400, detail="ZIP 파일만 업로드할 수 있습니다.")

    temp_dir = tempfile.mkdtemp(prefix="instascope_")
    zip_path = os.path.join(temp_dir, "upload.zip")

    try:
        with open(zip_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        # Remove the zip file itself to free space
        os.remove(zip_path)

        job_id = create_job()
        analysis_result = run_analysis(temp_dir)
        
        # Save to DB (Supabase if env set, fallback to memory)
        save_analysis_result(job_id, analysis_result)

        background_tasks.add_task(cleanup_expired_jobs)

        return {"status": "success", "job_id": job_id}

    except Exception as e:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        raise HTTPException(status_code=500, detail=f"분석 중 오류 발생: {str(e)}")

@router.get("/results/{job_id}")
async def get_results(job_id: str):
    result = fetch_analysis_result(job_id)
    if not result:
        raise HTTPException(status_code=404, detail="분석 결과를 찾을 수 없거나 만료되었습니다.")
    return {"status": "success", "job_id": job_id, "data": result}
