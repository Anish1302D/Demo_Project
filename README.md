# Teamboard Demo Project

Teamboard is a small demo project that shows a simple collaboration dashboard:

- a static frontend for viewing tasks and sending a message,
- a Python backend that serves JSON API endpoints,
- an AI helper module that generates a short response for the demo.

## Layout

- `frontend/index.html` - browser UI
- `backend/server.py` - HTTP API and static file server
- `ai/assistant.py` - mock AI helper used by the backend

## Run It

1. Open a terminal in `teamboard`.
2. Run `python backend/server.py`.
3. Open `http://localhost:8000/` in a browser.

## What It Does

- Shows a dashboard summary with a task list.
- Lets you post a quick team update.
- Returns a demo AI suggestion based on your message.
