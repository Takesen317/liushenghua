# 留声画 - Photo Voice Narrator

AI-powered photo narration generator that analyzes images and generates voice narration with background music, then composes a shareable video.

## 快速启动 (Docker)

```bash
# 启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

访问 http://localhost:3000

## 开发模式

### 后端
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### 前端
```bash
cd frontend
npm install
npm run dev
```

## AI 服务说明

| 服务 | 模型 | 说明 |
|------|------|------|
| 图像分析 | BLIP-2 | 需要 GPU 运行 |
| 语音合成 | Edge-TTS | 免费中文语音 |
| 背景音乐 | MusicGen | 需要 GPU 运行 |
| 视频合成 | FFmpeg | 系统依赖 |

## 技术栈

- Frontend: Vue3 + Vite + Element Plus + Pinia
- Backend: Python FastAPI + SQLAlchemy + Celery
- Database: PostgreSQL
- Task Queue: Redis + Celery
