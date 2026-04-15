# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**留声画 (Photo Voice Narrator)** — AI-powered photo narration generator that analyzes images and generates voice narration with background music, then composes a shareable video.

## Tech Stack

| Component | Technology |
|-----------|------------|
| Frontend | Vue3 + Vite + Element Plus + Pinia |
| Backend | Python FastAPI + SQLAlchemy + Pydantic v2 |
| Task Queue | Celery + Redis |
| Image Analysis | BLIP-2 (Salesforce) |
| Voice Synthesis | Edge-TTS (Microsoft) — free Chinese voice |
| Background Music | MusicGen (Meta) |
| Video Composition | FFmpeg |
| Database | PostgreSQL (dev: SQLite) |

## Architecture

```
Photo Upload → BLIP-2 Scene Analysis → Text Description
                               ↓
              Edge-TTS Voice Synthesis + MusicGen BGM
                               ↓
                      FFmpeg Video Composition
```

## Development Commands

### Frontend
```bash
cd frontend
npm install
npm run dev      # Dev server with proxy to backend
npm run build    # Production build
```

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000   # API dev server
celery -A app.tasks worker --loglevel=info  # AI task worker (requires Redis)
```

### Testing
```bash
# Backend tests
pytest tests/ -v
pytest tests/test_api.py::test_endpoint -v    # Single test

# Frontend unit tests
npm run test
```

### Docker Deployment (Production)
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## Project Structure

```
留声画/
├── frontend/               # Vue3 SPA
│   └── src/
│       ├── api/           # Axios API client
│       ├── components/     # UploadPanel, TaskProgress, VideoPlayer, TaskList, FlowingCloudBg
│       ├── views/          # Home, Login, Register, Dashboard
│       ├── stores/         # Pinia state (user store)
│       └── router/         # Vue Router config
│
├── backend/                # FastAPI application
│   └── app/
│       ├── api/v1/        # REST endpoints (auth, files, tasks, share)
│       ├── core/           # Config, security, database
│       ├── models/         # SQLAlchemy models (User, File, Task, Share)
│       ├── schemas/        # Pydantic v2 schemas
│       ├── services/       # AI services: blip2, tts, music, video
│       └── tasks.py        # Celery async task definitions
│
├── docs/                   # Project documentation
│   ├── 01_项目调研报告.md
│   ├── 02_可行性研究报告.md
│   ├── 03_概要设计说明书.md
│   ├── 04_项目开发报告.md
│   └── 05_前端设计规范.md
│
└── docker-compose.yml       # Full stack: postgres, redis, backend, frontend, celery
```

## Key Implementation Notes

### AI Pipeline (Celery Tasks)
Tasks are defined in `backend/app/tasks.py` and processed asynchronously:
1. `process_narration_task(task_id)` - Main orchestration task
2. BLIP-2 analyzes image → generates description
3. Edge-TTS synthesizes Chinese voice narration → MP3
4. MusicGen generates scene-matched background music → WAV
5. FFmpeg composes final MP4 video

**Note:** When Celery/Redis is unavailable, tasks are processed synchronously in the request thread (see `tasks.py` `queue_task()` fallback logic).

### API Endpoints
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/auth/register` | POST | User registration (email, password, nickname) |
| `/api/v1/auth/login` | POST | OAuth2 password flow login |
| `/api/v1/files/upload` | POST | Upload photo (multipart/form-data) |
| `/api/v1/tasks` | POST | Create narration task |
| `/api/v1/tasks/{id}` | GET | Get full task details including result_data |
| `/api/v1/tasks/{id}/status` | GET | Get task progress/status |
| `/api/v1/share` | POST | Create share link |
| `/results/{task_id}/{filename}` | GET | Serve generated video files |

### Database
- Dev: SQLite (`backend/liushenghua.db`)
- Production: PostgreSQL (via docker-compose)

### Key Files
- `backend/app/services/__init__.py` — `process_narration()` function
- `backend/app/tasks.py` — Celery task definitions with sync fallback
- `backend/app/api/v1/tasks.py` — Task creation/tracking endpoints
- `backend/app/main.py` — FastAPI app with video serving endpoint
- `backend/test_ai_services.py` — Standalone AI services test script
- `frontend/src/views/DashboardView.vue` — Main user interface
- `frontend/src/components/FlowingCloudBg.vue` — Animated background with flowing clouds and waves
- `frontend/src/components/TaskList.vue` — Task list with play/download/share modals

### Edge-TTS Chinese Voices
Use: `xiaoxiao`, `yunyang`, `yunxia` (free, no API key needed)
