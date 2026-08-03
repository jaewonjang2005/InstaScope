import os
import shutil
import tempfile
import zipfile
import json
from typing import Dict, Any
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, BackgroundTasks
from pydantic import BaseModel
from app.services.parser import InstaParser, InstaMemoryParser
from app.services.keyword_extractor import extract_taste_keywords
from app.services.search_service import get_recommendations_for_keywords
from app.services.db_service import save_analysis_result, fetch_analysis_result
from app.utils.cleanup import create_job, cleanup_expired_jobs

router = APIRouter()

# Temporary in-memory storage tracking chunked uploads
CHUNK_STORAGE: Dict[str, Dict[str, Any]] = {}

class JsonPayload(BaseModel):
    files: dict

def extract_and_parse_zip(zip_path: str, output_dir: str) -> str:
    """
    Extracts only the required JSON files from the ZIP archive to disk,
    bypassing the need to extract everything to disk (fixes Vercel 500MB tmp limit)
    and avoiding OOM memory limits by reading one file at a time.
    """
    required_files = [
        'your_instagram_activity/likes/liked_posts.json',
        'your_instagram_activity/saved/saved_posts.json',
        'your_instagram_activity/story_interactions/stories_viewed.json',
        'your_instagram_activity/story_interactions/story_likes.json',
        'your_instagram_activity/saved/saved_collections.json'
    ]
    
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            file_names = zip_ref.namelist()
            for req_file in required_files:
                matching_files = [f for f in file_names if f.lower().endswith(req_file.lower())]
                if matching_files:
                    target_path = os.path.join(output_dir, req_file)
                    os.makedirs(os.path.dirname(target_path), exist_ok=True)
                    with zip_ref.open(matching_files[0]) as source, open(target_path, 'wb') as target:
                        shutil.copyfileobj(source, target)
    except Exception as e:
        raise Exception(f"Failed to process zip file: {e}")
        
    return output_dir

@router.post("/upload-chunk")
async def upload_chunk(
    background_tasks: BackgroundTasks,
    upload_id: str = Form(...),
    chunk_index: int = Form(...),
    total_chunks: int = Form(...),
    file: UploadFile = File(...)
):
    if upload_id not in CHUNK_STORAGE:
        CHUNK_STORAGE[upload_id] = {
            "temp_dir": tempfile.mkdtemp(prefix=f"chunk_{upload_id}_"),
            "total_chunks": total_chunks,
            "received_chunks": set()
        }

    chunk_info = CHUNK_STORAGE[upload_id]
    chunk_path = os.path.join(chunk_info["temp_dir"], f"chunk_{chunk_index}")

    try:
        with open(chunk_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        chunk_info["received_chunks"].add(chunk_index)

        # If all chunks are received
        if len(chunk_info["received_chunks"]) == total_chunks:
            temp_dir = chunk_info["temp_dir"]
            merged_zip_path = os.path.join(temp_dir, "merged_upload.zip")

            # Reassemble binary chunks
            with open(merged_zip_path, "wb") as merged_file:
                for i in range(total_chunks):
                    part_path = os.path.join(temp_dir, f"chunk_{i}")
                    if os.path.exists(part_path):
                        with open(part_path, "rb") as part_file:
                            shutil.copyfileobj(part_file, merged_file)
                        os.remove(part_path)

            # Stream required JSONs directly from ZIP to disk
            extract_and_parse_zip(merged_zip_path, temp_dir)
            os.remove(merged_zip_path)

            # Parse and analyze (Low Memory)
            parser = InstaParser(temp_dir)
            keywords_result = extract_taste_keywords(parser)
            
            job_id = create_job()
            
            tag_to_urls = keywords_result.get("tag_to_urls", {})
            used_urls = set()
            
            # Search top 5 keywords for SFW and Hidden to fit within Vercel 10s limit
            sfw_recs = get_recommendations_for_keywords(keywords_result["search_sfw_queries"][:5], tag_to_urls, used_urls=used_urls)
            hidden_recs = get_recommendations_for_keywords(keywords_result["search_hidden_queries"][:5], tag_to_urls, used_urls=used_urls)
            spicy_recs = get_recommendations_for_keywords(keywords_result["raw_hidden_tags"][:5], tag_to_urls, used_urls=used_urls)
            buldak_recs = get_recommendations_for_keywords(keywords_result["buldak_tags"][:5], tag_to_urls, used_urls=used_urls)
            
            analysis_result = {
                "keywords": keywords_result,
                "sfw_recommendations": sfw_recs,
                "hidden_recommendations": hidden_recs,
                "spicy_recommendations": spicy_recs,
                "buldak_recommendations": buldak_recs
            }
            save_analysis_result(job_id, analysis_result)
            
            background_tasks.add_task(cleanup_expired_jobs)

            # Cleanup
            del CHUNK_STORAGE[upload_id]
            shutil.rmtree(temp_dir)

            return {"status": "success", "job_id": job_id, "completed": True}

    except Exception as e:
        if upload_id in CHUNK_STORAGE:
            del CHUNK_STORAGE[upload_id]
        if os.path.exists(chunk_info["temp_dir"]):
            shutil.rmtree(chunk_info["temp_dir"])
        raise HTTPException(status_code=500, detail=f"데이터 병합 및 파싱 중 오류 발생: {str(e)}")

    return {"status": "chunk_received", "chunk_index": chunk_index, "completed": False}

@router.post("/upload-payload")
async def upload_payload(payload: JsonPayload, background_tasks: BackgroundTasks):
    try:
        parser = InstaMemoryParser(payload.files)
        keywords_result = extract_taste_keywords(parser)
        job_id = create_job()
        
        tag_to_urls = keywords_result.get("tag_to_urls", {})
        used_urls = set()
        
        sfw_recs = get_recommendations_for_keywords(keywords_result["search_sfw_queries"][:5], tag_to_urls, used_urls=used_urls)
        hidden_recs = get_recommendations_for_keywords(keywords_result["search_hidden_queries"][:5], tag_to_urls, used_urls=used_urls)
        spicy_recs = get_recommendations_for_keywords(keywords_result["raw_hidden_tags"][:5], tag_to_urls, used_urls=used_urls)
        buldak_recs = get_recommendations_for_keywords(keywords_result["buldak_tags"][:5], tag_to_urls, used_urls=used_urls)
        
        analysis_result = {
            "keywords": keywords_result,
            "sfw_recommendations": sfw_recs,
            "hidden_recommendations": hidden_recs,
            "spicy_recommendations": spicy_recs,
            "buldak_recommendations": buldak_recs
        }
        save_analysis_result(job_id, analysis_result)
        background_tasks.add_task(cleanup_expired_jobs)

        return {"status": "success", "job_id": job_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"분석 중 오류 발생: {str(e)}")

@router.post("/upload")
async def upload_zip(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    if not file.filename.endswith('.zip'):
        raise HTTPException(status_code=400, detail="ZIP 파일만 업로드할 수 있습니다.")

    temp_dir = tempfile.mkdtemp(prefix="instascope_")
    zip_path = os.path.join(temp_dir, "upload.zip")

    try:
        with open(zip_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        extract_and_parse_zip(zip_path, temp_dir)
        os.remove(zip_path)

        parser = InstaParser(temp_dir)
        keywords_result = extract_taste_keywords(parser)
        job_id = create_job()
        
        tag_to_urls = keywords_result.get("tag_to_urls", {})
        used_urls = set()
        
        # Search top 1 keyword for SFW and Hidden to fit within Vercel 10s limit
        sfw_recs = get_recommendations_for_keywords(keywords_result["search_sfw_queries"][:1], tag_to_urls, max_per_keyword=4, used_urls=used_urls)
        hidden_recs = get_recommendations_for_keywords(keywords_result["search_hidden_queries"][:1], tag_to_urls, max_per_keyword=4, used_urls=used_urls)
        spicy_recs = get_recommendations_for_keywords(keywords_result["raw_hidden_tags"][:1], tag_to_urls, max_per_keyword=4, used_urls=used_urls)
        buldak_recs = get_recommendations_for_keywords(keywords_result["buldak_tags"][:1], tag_to_urls, max_per_keyword=4, used_urls=used_urls)
        
        analysis_result = {
            "keywords": keywords_result,
            "sfw_recommendations": sfw_recs,
            "hidden_recommendations": hidden_recs,
            "spicy_recommendations": spicy_recs,
            "buldak_recommendations": buldak_recs
        }
        save_analysis_result(job_id, analysis_result)
        background_tasks.add_task(cleanup_expired_jobs)

        # Cleanup
        shutil.rmtree(temp_dir)

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
