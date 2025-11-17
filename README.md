# CinemaToday

CinemaToday is a daily film guessing game that spotlights the current UK box-office Top 10.  
Each day the FastAPI backend serves a mystery film, the React/Next.js frontend reveals
progressively easier clues, and optional offline pipelines keep the catalogue fresh by
syncing with TMDB and generating AI-written hints.

## Features
- **Modern UI** – Next.js 16 + Tailwind CSS blur/unblur the poster art, track clue progress,
  and drive the entire game through a single page (`frontend/src/app/page.tsx`).
- **Typed FastAPI service** – `/today-game` selects a random active movie, `/guess`
  validates answers with forgiving normalisation, and `/health` supports monitoring.
- **Postgres + SQLAlchemy models** – `Movie`, `Clue`, and `DailySelection` tables keep the
  playable catalogue and truths consistent.
- **Offline automation** – Scripts in `backend/offline/` ingest TMDB's “now playing”
  feed, log MLflow experiments, and (optionally) call OpenAI to create ranked clues.

## Repository layout

```
backend/          FastAPI app, SQLAlchemy models, DB + ingestion scripts
frontend/         Next.js UI (app router) and Tailwind styles
mlruns/           Local MLflow tracking store for offline experiments
generated_*.txt   Artifacts logged by ingestion/clue pipelines
requirements.txt  Backend + offline Python dependencies mirror of backend/requirements.txt
```

## Prerequisites
- Python 3.11+ (dev uses 3.12)
- Node.js 18.18+ (Next.js 16 requirement) and npm
- Postgres database (Supabase works; SSL parameters already baked in)
- An OpenAI API key (only required if you run the GPT-based clue generator)
- A TMDB API key (needed for `ingest_now_playing`)

## Backend setup
1. **Create a virtualenv and install dependencies**

   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

2. **Configure `backend/.env`** – this file is read automatically by `backend/db.py`.

   ```dotenv
   # Postgres
   user=postgres
   password=postgres
   host=127.0.0.1
   port=5432
   dbname=cinematoday

   # Optional integrations used by offline scripts
   TMDB_API_KEY=your_tmdb_key
   TMDB_BASE_URL=https://api.themoviedb.org/3            # default
   TMDB_IMAGE_BASE_URL=https://image.tmdb.org/t/p/w500   # default
   OPENAI_API_KEY=sk-...
   MLFLOW_TRACKING_URI=mlruns
   ```

3. **Initialise the database**

   ```bash
   # still inside the virtualenv, from the repo root
   python -m backend.init_db
   ```

4. **(Optional) Load the placeholder catalogue**

   ```bash
   python -m backend.seed_db
   ```

5. **Run the API locally**

   ```bash
   uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
   # Swagger docs: http://127.0.0.1:8000/docs
   ```

### API surface

| Method | Route        | Description                                                         |
|--------|--------------|---------------------------------------------------------------------|
| GET    | `/health`    | Lightweight readiness probe                                         |
| GET    | `/today-game`| Returns `{movie_slug, total_clues, current_clue_text, poster_url}`  |
| POST   | `/guess`     | Body: `{movie_slug, guess, current_clue_index}`; advances the game  |

`submit_guess` lowercases and strips punctuation (`normalise_title`) so “Jaws!!!” matches
“jaws”. When the final clue is exhausted the API reveals the movie title and poster.

## Frontend setup
1. Install dependencies once:

   ```bash
   cd frontend
   npm install
   ```

2. Point the UI at the API (create `frontend/.env.local`):

   ```dotenv
   NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000
   ```

3. Start the dev server:

   ```bash
   npm run dev
   # http://localhost:3000
   ```

The page automatically calls `/today-game`, shows the current clue, keeps a history of the
previous hints, and blurs/unblurs the poster based on how many clues you have used. Use the
“New movie” button to fetch a different random active title without refreshing the page.

## Offline pipelines

1. **Sync the catalogue with TMDB**

   ```bash
   # Requires TMDB_API_KEY and MLflow configured
   python -m backend.offline.ingest_now_playing
   ```

   - Pulls “Now Playing” (region GB, language en-GB) with pagination.
   - Keeps only the 10 most popular titles and toggles `Movie.is_active`.
   - Writes titles to `ingested_movies.txt` and logs params/metrics/artifacts to MLflow.

2. **Inspect existing clues (no LLM required)**

   ```bash
   python -m backend.offline.generate_clues_dummy
   ```

   Logs aggregate clue lengths and dumps samples to `sample_clues.txt`.

3. **Generate new clues with OpenAI (optional)**

   ```bash
   python -m backend.offline.generate_clues_openai
   ```

   Adjust `PROMPT_VERSION`, `MODEL_NAME`, or `num_movies` inside the module as needed.

4. **Persist GPT clues back into Postgres**

   ```bash
   python -m backend.offline.apply_clues_to_db              # fills missing clues only

   # Example: regenerate clues for 5 movies even if they already have data
   python - <<'PY'
   from backend.offline.apply_clues_to_db import apply_generated_clues_to_db
   apply_generated_clues_to_db(num_movies=5, overwrite_existing=True)
   PY
   ```

All offline scripts reuse the same SQLAlchemy session factory, so they benefit from the
`backend/.env` config. Each run lands metrics/artifacts inside `mlruns/`; view them with:

```bash
mlflow ui --backend-store-uri mlruns
```

## Development notes
- The backend requirements pin FastAPI 0.110+, SQLAlchemy 2.x, and MLflow to simplify
  deployment on hosted platforms (Supabase + Render works out-of-the-box).
- The project intentionally keeps state in Postgres only—no Redis cache is required.
- Frontend styling sticks to Tailwind v4 class syntax; if you prefer CSS modules you can
  add them without touching the backend.

## Troubleshooting
- **DB connection errors** – verify `backend/.env` is reachable; `db.py` raises early if
  any of `user/password/host/dbname` are missing.
- **CORS issues** – the API currently allows `http://localhost:3000` and
  `http://127.0.0.1:3000`. Extend `allow_origins` in `backend/main.py` when deploying.
- **No clues returned** – run either `seed_db.py` or the TMDB + OpenAI pipeline above so
  that every active movie has four ordered clues.

Happy guessing!
