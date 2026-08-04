# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

"Insta Taste Recommender" — a web app where a user uploads their Instagram data export (ZIP), the backend parses their likes/saves/story-interaction JSONs to extract hashtags, scores them with a TF-IDF-like weighting scheme, classifies them into SFW / hidden / spicy taste categories, and returns Instagram explore-tag links as "recommendations". Everything is deployed as a single Vercel project (React SPA + Python serverless function).

## Commands

### Backend (FastAPI)
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --port 8000
```
Ad-hoc engine test against a real exported dataset (path is hardcoded in the file, edit before running):
```bash
python backend/test_run.py
```
There is no pytest suite and no lint config for the backend.

### Frontend (React + Vite)
```bash
cd frontend
npm install
npm run dev       # http://localhost:5173
npm run build
npm run preview
```
`frontend/.oxlintrc.json` configures oxlint (react-hooks rules), but no `lint` script is wired up in `package.json` — run it directly with `npx oxlint` if needed. There is no frontend test suite.

The frontend talks to the backend at `http://localhost:8000/api` in dev (`import.meta.env.DEV` check in `LoadingPage.jsx`) and at the relative path `/api` in production.

### Root / deploy
The root `package.json`'s only script (`build`) is what Vercel runs: it installs and builds the frontend. There is no root-level dev command — always `cd` into `frontend` or `backend`.

## Architecture

### Deployment topology
This is one Vercel project serving two things per `vercel.json`:
- `/api/*` rewrites to `api/index.py`, a thin shim that appends `backend/` to `sys.path` and imports the real FastAPI app from `backend/app/main.py`. There is no separate backend deployment — the FastAPI app runs as a single Vercel serverless function (`maxDuration: 60`).
- everything else rewrites to the built SPA (`frontend/dist`).

Because the whole backend is one serverless function with a short duration budget, the code is deliberately shaped around avoiding disk usage and long-running work (see "Constraints" below).

### Request pipeline (the core flow)
1. **Upload** — the frontend never uploads the whole ZIP in one request. `LoadingPage.jsx` slices the file into 2MB chunks and POSTs them sequentially to `/api/upload-chunk` with a shared `upload_id` (with retry/backoff per chunk). `routes.py` buffers chunks on disk under a per-upload temp dir; once every chunk index has arrived it concatenates them into `merged_upload.zip`.
2. **Selective extraction** — `extract_and_parse_zip()` in `routes.py` opens the ZIP and copies out only 5 known files (`liked_posts.json`, `saved_posts.json`, `stories_viewed.json`, `story_likes.json`, `saved_collections.json`) matched case-insensitively by suffix — it never extracts the full archive, which is what keeps this under Vercel's 500MB `/tmp` limit for large exports.
3. **Parsing** — `InstaParser` (disk-backed) / `InstaMemoryParser` (dict-backed, used by the alternate `/api/upload-payload` JSON-payload endpoint) in `parser.py` share the same `_extract_posts_list` logic: Instagram's export nests hashtags/captions/owner inside a generic `label_values` → `dict` → `dict` structure that has to be walked recursively rather than by fixed key path. All string values pass through `decode_insta_text` (`utils/encoding.py`), because Instagram exports mojibake text as UTF-8 bytes mis-decoded as Latin-1 — every parser must decode through this helper, not read fields raw.
4. **Keyword scoring** — `keyword_extractor.py::extract_taste_keywords` is the actual "algorithm" of the project. Per hashtag it computes: a time-decay weight (recent posts weighted higher, >1yr old posts heavily discounted), a public/private split (likes+story views = public, saves+collections = private, private weighted higher), a TF-IDF-style score (`idf = log10((total_posts+1)/doc_count)`) to punish hashtags that appear on nearly everything, and a "sibling penalty" that discounts hashtags from posts with >15 hashtags (spam/abuse signal). It also tracks tag co-occurrence per post to find hashtags related to a chosen "main category" instead of just returning a flat top-N list. Tags are then classified as `SFW` / `IMPLICIT_HIDDEN` / `EXPLICIT_HIDDEN` against two hardcoded Korean/English keyword dictionaries (`HIDDEN_MAPPING`, `IMPLICIT_HIDDEN_KEYWORDS`) with manually curated false-positive exclusions (e.g. `엉덩이탐정`, `섹스피어`, `자위대`, `비키니시티`). This produces three query buckets: `search_sfw_queries`, `search_hidden_queries`, `raw_hidden_tags` (spicy).
5. **"Recommendations"** — despite what `README.md` and `docs/` say about live DuckDuckGo (`ddgs`) scraping, `search_service.py` currently does **not** call any search engine. `get_recommendations_for_keywords()` just builds direct `instagram.com/explore/tags/<tag>/` links for each keyword. `is_valid_instagram_url()` (HTTP HEAD/GET liveness check) exists but is not called from the current route handlers. Don't assume the docs describe the shipped behavior — check `search_service.py` directly.
6. **Result storage & polling** — results are stored under a `job_id` (`utils/cleanup.py`'s in-memory `JOBS_STORE`, TTL 1hr) and, if `SUPABASE_URL`/`SUPABASE_KEY` env vars are set, also persisted to a Supabase `insta_analysis_results` table via `db_service.py` (reads prefer Supabase, fall back to memory). The frontend polls `GET /api/results/{job_id}` every 1.5s (`LoadingPage.jsx`) until it gets a non-404 response, then navigates to `/result` with the payload in router state.

There are three upload entry points in `routes.py` with the same downstream pipeline but different tradeoffs: `/upload-chunk` (chunked, used in prod, top-5 keywords searched per bucket), `/upload` (single-shot multipart, top-1 keyword per bucket — for the 10s function timeout), `/upload-payload` (pre-parsed JSON dict, no ZIP handling at all — used by `InstaMemoryParser`).

`services/one_pick.py` (`analyze_one_pick`, ranks *accounts* by weighted interaction count) is not wired into any route — treat it as unused/legacy unless you're explicitly resurrecting the "one pick account" feature.

### Frontend structure
Single-page flow driven by `react-router-dom`, state is passed between routes via router `state` (no global store): `/` (`UploadPage` — pick a file) → `/loading` (`LoadingPage` — owns the chunk-upload + polling loop above) → `/result` (`ResultPage` — renders categories/keywords via `Recommendations`, `TopPickCard`, `RunnerUpList`) → `/secret` (`SecretPickPage`). Styling is plain CSS (`App.css`/`index.css`) with a glassmorphism/neon look, no CSS framework.

### Constraints that shape the code (don't "clean up" without them in mind)
- No Vector DB / embeddings by design — the project intentionally avoided pgvector/FAISS to stay within Vercel serverless memory limits; keyword matching is dictionary + statistics based, not semantic.
- Never write the full uploaded ZIP or its full extracted contents to disk — only the 5 required JSON files are ever materialized.
- Backend serverless function timeout is tight (10s default / 60s configured) — this is why the search step slices keyword lists (`[:5]` or `[:1]`) before generating recommendations instead of processing everything found.
