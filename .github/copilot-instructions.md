# Copilot instructions for this repository

Purpose: Short, actionable guidance to help AI coding agents work productively in this codebase.

- **Big picture**: This is a small single-process Flask web app that provides a tiny auth UI and stores users in Postgres. The stack is defined in [docker-compose.yml](docker-compose.yml): services `postgres`, `flask` (the app) and a `sonarqube` service for CI scanning.

- **Key files**:
  - App server: [app.py](app.py) — routes, DB helpers, and startup (`wait_for_db()` + `init_db()`).
  - Frontend: [templates/auth.html](templates/auth.html) and [static/auth.js](static/auth.js) — client interacts with `/login` and `/register`.
  - Container config: [Dockerfile](Dockerfile) and [docker-compose.yml](docker-compose.yml).

- **Data flow / service boundaries**:
  - Browser → `auth.js` posts JSON to `/login` and `/register` on port 5000.
  - `app.py` uses `psycopg2` to query Postgres; DB credentials come from env vars set in Compose (`DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`).
  - `init_db()` in `app.py` ensures the `users` table exists on startup.

- **Project-specific conventions & patterns**:
  - Single-file Flask app (no blueprints). Make minimal edits in `app.py` for new endpoints.
  - DB access is raw `psycopg2` queries via `get_db_connection()`; follow the existing cursor/connection open→commit→close pattern.
  - Passwords: `generate_password_hash(..., method="scrypt")` and `check_password_hash(...)` (see `app.py`).
  - Client-side username rule: a symbol is required (see regex in [static/auth.js](static/auth.js)). Server only enforces uniqueness via DB.

- **Common tasks / commands**:
  - Start full stack (recommended):
    ```bash
    docker compose up --build
    ```
    Compose waits for Postgres healthcheck before starting Flask (`depends_on` with `service_healthy`).
  - Start only Flask locally (development): set env vars and run:
    ```bash
    export DB_NAME=... DB_USER=... DB_PASSWORD=... DB_HOST=localhost
    python3 app.py
    ```
  - Inspect logs for debugging:
    ```bash
    docker compose logs -f flask
    docker compose logs -f postgres
    ```

- **Integration points & side effects**:
  - Postgres volume `pgdata` persists DB state (see `docker-compose.yml`).
  - SonarQube exposes port 9000 and is included for static analysis in `docker-compose.yml`.

- **What to look out for when editing**:
  - Keep connection/cursor lifecycle consistent to avoid leaks (open → execute → commit → close).
  - `wait_for_db()` is called before `init_db()` in `if __name__ == "__main__"` — when running outside Compose, ensure DB is reachable or the app will block.
  - The frontend `apiUrl` in [static/auth.js](static/auth.js) is `http://localhost:5000`. If running in containers, prefer using the Compose mapping (host:5000) or change to relative paths.

- **No test harness found**: There are no unit tests in the repo. If you add tests, place them under `tests/` and run with `pytest` after adding it to `requirements.txt`.

If anything above is unclear or you want the instructions expanded (examples for adding endpoints, SQL migration guidance, or CI steps), tell me which area to expand. I'll iterate. 
