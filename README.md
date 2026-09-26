# demo-devops-project

A minimal Flask application that will grow incrementally into a DevOps portfolio project.

## Project structure

```text
.
├── app/
│   ├── __init__.py
│   └── routes.py
├── tests/
│   └── test_routes.py
├── .dockerignore
├── .gitignore
├── Dockerfile
├── README.md
├── requirements-dev.txt
└── requirements.txt
```

## Endpoints

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/` | Returns a welcome message. |
| `GET` | `/health` | Confirms that the application can respond. |
| `GET` | `/api/info` | Returns the application name and version. |

## Local setup

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the development dependencies. This installs both Flask and pytest because
`requirements-dev.txt` references `requirements.txt`:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
```

Run the application:

```bash
python -m flask --app app run
```

Open <http://127.0.0.1:5000> in a browser. Stop the development server with
`Ctrl+C`.

Run the tests from the project root:

```bash
python -m pytest
```

## Phase 2: Docker

Prerequisite: Docker must be installed and running. Run all commands below from
the repository root; the final `.` in the build command is the build context.

The image uses `python:3.12-slim-bookworm` and installs only runtime dependencies.
Gunicorn runs `app:create_app()` with one worker as the non-root user `appuser`
(UID/GID 10001). It listens on `0.0.0.0:5000` inside the container, using the same
unprivileged port as local development. Access and error logs go to container
output. The unused Gunicorn control interface is disabled with `--no-control-socket`.
`EXPOSE 5000` documents the port; the run command publishes it.

### Build and run

```bash
docker build --pull -t demo-devops-project:phase2 .
docker run --detach --name demo-devops \
  -p 127.0.0.1:5000:5000 demo-devops-project:phase2
```

Open <http://127.0.0.1:5000>. The published port is accessible only from your local
machine. Stop any local Flask server using port 5000 before starting the container.

### Test

Run the existing tests in your activated local Python 3.12 virtual environment:

```bash
python -m pip install -r requirements-dev.txt
python -m pytest
```

All three tests should pass. Tests and pytest are excluded from the runtime image.
Check the running container separately:

```bash
curl --fail-with-body -i http://127.0.0.1:5000/
curl --fail-with-body -i http://127.0.0.1:5000/health
curl --fail-with-body -i http://127.0.0.1:5000/api/info
docker exec demo-devops id
docker logs demo-devops
```

Each endpoint should return HTTP 200 with the following JSON (key order may vary):

| Path | Expected JSON |
| --- | --- |
| `/` | `{"message":"Welcome to demo-devops-project"}` |
| `/health` | `{"status":"ok"}` |
| `/api/info` | `{"name":"demo-devops-project","version":"0.1.0"}` |

The `id` output should show UID/GID 10001, and the logs should show Gunicorn startup
and the requests above without errors.

To check layer caching, repeat the build:

```bash
docker build --progress=plain -t demo-devops-project:phase2 .
```

Unchanged layers should be marked `CACHED`. Dependencies are copied and installed
before the application code, so changing only `app/` preserves the dependency
installation cache.

### Stop and remove

```bash
docker stop demo-devops
docker logs demo-devops
docker inspect --format '{{.State.ExitCode}}' demo-devops
docker rm demo-devops
```

The logs should show a graceful Gunicorn shutdown and the exit code should be `0`.
Removing the stopped container leaves the image available for the next run.
