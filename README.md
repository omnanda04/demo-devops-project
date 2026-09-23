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
├── .gitignore
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
