import os
import time
from typing import Dict, Any, Optional
from app.utils.cleanup import JOBS_STORE

# Try importing supabase client if installed
try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False
    Client = None

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")

supabase_client: Optional[Any] = None

if SUPABASE_AVAILABLE and SUPABASE_URL and SUPABASE_KEY:
    try:
        supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("Connected to Supabase DB successfully.")
    except Exception as e:
        print(f"Supabase connection warning: {e}")

def save_analysis_result(job_id: str, result_data: Dict[str, Any]) -> str:
    """
    Saves analysis result to Supabase if configured, otherwise falls back to local memory store.
    """
    taste_dna = result_data.get("taste_dna", {})
    secret_collection = result_data.get("secret_collection", {})
    ideal_type = result_data.get("ideal_type", {})
    algorithm_expose = result_data.get("algorithm_expose", {})

    if supabase_client:
        try:
            record = {
                "id": job_id,
                "taste_dna": taste_dna,
                "secret_collection": secret_collection,
                "ideal_type": ideal_type,
                "algorithm_expose": algorithm_expose
            }
            supabase_client.table("analysis_jobs").insert(record).execute()
            print(f"Saved job {job_id} to Supabase DB.")
        except Exception as e:
            print(f"Failed to insert into Supabase DB, using memory fallback: {e}")

    # Memory fallback
    JOBS_STORE[job_id] = {
        "timestamp": time.time(),
        "result": result_data
    }
    return job_id

def fetch_analysis_result(job_id: str) -> Optional[Dict[str, Any]]:
    """
    Fetches analysis result from Supabase if available, otherwise from local memory store.
    """
    if supabase_client:
        try:
            response = supabase_client.table("analysis_jobs").select("*").eq("id", job_id).execute()
            if response.data and len(response.data) > 0:
                data = response.data[0]
                return {
                    "taste_dna": data.get("taste_dna"),
                    "secret_collection": data.get("secret_collection"),
                    "ideal_type": data.get("ideal_type"),
                    "algorithm_expose": data.get("algorithm_expose")
                }
        except Exception as e:
            print(f"Supabase fetch warning: {e}")

    # Fallback to local memory store
    job = JOBS_STORE.get(job_id)
    if job:
        return job.get("result")
    return None
