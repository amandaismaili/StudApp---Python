# StudApp

A backend platform for university students to connect by university, degree, level, and year — ask questions, reply, and find classmates in the same program. Built with FastAPI and PostgreSQL.

## Features

- **Auth** — registration, login, and JWT-protected routes using Argon2 password hashing
- **Questions & replies** — post questions, reply to them, with ownership-enforced edit/delete
- **Filtering** — find questions or students by university, degree, level, or year (partial, case-insensitive match)
- **Account management** — view, update, and delete your own account
- **34 automated tests** covering every route's happy path, auth failures, and ownership checks

## Tech Stack

- **FastAPI** — async, with Pydantic schemas separating request and response shapes
- **PostgreSQL** + **async SQLAlchemy** (`asyncpg`) — ORM with relationships between users, questions, and replies
- **Alembic** — schema migrations, including enforced `UNIQUE` constraints on username/email
- **pwdlib (Argon2)** — password hashing
- **python-jose** — JWT issuing and verification
- **pydantic-settings** — config loaded from environment variables, not hardcoded
- **pytest + pytest-asyncio + httpx** — fully async test suite against an isolated in-memory SQLite database per test

## Architecture

Requests flow through routers (`users.py`, `section.py`) into Pydantic schemas that validate input and filter output, then through SQLAlchemy models to PostgreSQL. A few deliberate choices:

- **Separate input/output schemas.** A `UserCreate` schema accepts a password; the `UserPublic`/`UserOut` schemas returned to clients never include the password hash. This is enforced by `response_model`, not by convention.
- **Per-request DB sessions**, handed out via FastAPI's `Depends(get_db)`, so one request's work can't leak into another's.
- **Ownership checks on every mutation.** Updating or deleting a question/reply checks `current_user.id` against the resource's owner before acting — not just that *a* valid token was presented.
- **Migrations, not `create_all()`.** Every schema change (including the `username`/`email` unique constraints) is a tracked Alembic migration, so the schema's history is reproducible.

## Setup

```bash
git clone [your repo URL]
cd studapp
uv sync
```

Create a `.env` file in the project root:

DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/dbname
SECRET_KEY=[a long random string]
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30


Run migrations:
```bash
uv run alembic upgrade head
```

Start the server:
```bash
uv run fastapi dev main.py
```

API docs are available at `/docs`.

## Running Tests

```bash
uv run pytest -v
```

The test suite uses an isolated in-memory SQLite database per test (no PostgreSQL required to run tests), and has already caught two real bugs during development:
- A response model gap that leaked the password hash in the registration response
- A routing collision where two `PATCH` routes shared an identical URL pattern, silently making one of them unreachable

## API Overview

| Method | Path | Description | Auth |
|---|---|---|---|
| GET | `/` | API root / health check | — |
| POST | `/user/register` | Create an account | — |
| POST | `/user/login` | Get a JWT | — |
| GET | `/user/me` | Current user's profile | required |
| PUT | `/user/search/{user_id}` | Update account | required |
| DELETE | `/user/delete/` | Delete account | required |
| GET | `/user/filter/users` | Filter students by university/degree/level/year | — |
| GET | `/section` | List all questions | — |
| POST | `/section/questions` | Post a question | required |
| POST | `/section/{question_id}/reply` | Reply to a question | required |
| GET | `/section/search/{question_id}` | Get one question | — |
| GET | `/section/filter/questions` | Filter questions by asker's university/degree/level/year | — |
| PATCH | `/section/update/question/{id}` | Edit own question | required, owner only |
| PATCH | `/section/update/reply/{id}` | Edit own reply | required, owner only |
| DELETE | `/section/delete/question/{id}` | Delete own question | required, owner only |
| DELETE | `/section/delete/reply/{id}` | Delete own reply | required, owner only |

Full interactive docs at `/docs` once running.

## Status / Roadmap

- [x] Backend: auth, CRUD, filtering, ownership enforcement
- [x] 34 passing tests
- [ ] Frontend (planned once in progress on The Odin Project's API/fetch module)
- [ ] Deployment

## License

MIT — see [LICENSE](LICENSE)
