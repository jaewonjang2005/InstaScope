import os
import shutil
import uuid
import time
from typing import Dict, Any, Optional

# In-memory storage for analysis results mapped by job_id
# job_id -> {"timestamp": float, "result": dict, "temp_dir": str}
JOBS_STORE: Dict[str, Dict[str, Any]] = {}
TTL_SECONDS = 3600  # 1 hour TTL

def create_job() -> str:
    job_id = str(uuid.uuid4())
    return job_id

def store_job_result(job_id: str, result: Dict[str, Any], temp_dir: Optional[str] = None):
    JOBS_STORE[job_id] = {
        "timestamp": time.time(),
        "result": result,
        "temp_dir": temp_dir
    }

def get_job_result(job_id: str) -> Optional[Dict[str, Any]]:
    job = JOBS_STORE.get(job_id)
    if not job:
        return None
    return job.get("result")

def cleanup_expired_jobs():
    now = time.time()
    expired = [jid for jid, data in JOBS_STORE.items() if now - data["timestamp"] > TTL_SECONDS]
    for jid in expired:
        data = JOBS_STORE.pop(jid, None)
        if data and data.get("temp_dir") and os.path.exists(data["temp_dir"]):
            try:
                shutil.rmtree(data["temp_dir"])
            except Exception as e:
                print(f"Cleanup error for {jid}: {e}")
