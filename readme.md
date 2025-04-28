# Online Learning Platform
A full-stack web application for creating and managing online courses. Teachers can add courses, weeks, notes, videos, homework, and tests. Students can view course content and submit assignments.

## Features
- **User roles**: Teacher and Student
- **Course management**: Create, list, and view courses
- **Week organization**: Add sequential weeks to courses
- **Modules**: Notes (text + file), Videos, Homework (file + description), Tests
- **File uploads**: Handled via multipart/form-data
- **Authentication**: JWT access & refresh tokens
- **Storage**: MinIO (S3-compatible) for media files

## Tech Stack
- **Backend**: Django, Django REST Framework, drf-spectacular
- **Frontend**: Vue 3 (Composition API), Vuex, Vue Router, Axios, Bootstrap 5
- **Storage**: MinIO 
- **Database**: PostgreSQL 

## Prerequisites
- Python 3.10+ & pip
- Node.js 16+ & npm
- MinIO server (or AWS S3) running on `localhost:9000` for media files

## Environment Variables
Create a `.env` file in `backend/`:
```ini
SECRET_KEY=your-django-secret
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3  # or your Postgres URL
AWS_S3_ENDPOINT_URL=http://localhost:9000
AWS_ACCESS_KEY_ID=MINIO_ACCESS_KEY
AWS_SECRET_ACCESS_KEY=MINIO_SECRET_KEY
AWS_STORAGE_BUCKET_NAME=your-bucket
AWS_S3_USE_SSL=False
```

Create `.env.local` in `frontend/`:
```ini
VUE_APP_API_BASE_URL=http://localhost:8000/api
```

## Setup & Run
### Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate     # or .\.venv\Scripts\activate on Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
### Frontend
```bash
cd frontend/online-learning-frontend
npm install
npm run serve
```

Open your browser at:
- Backend API docs: `http://localhost:8000/api/schema/`
- Frontend: `http://localhost:8080`

## Contribution
1. Fork the repo
2. Create a feature branch (`git checkout -b feature-name`)
3. Commit your changes (`git commit -m "Add feature"`)
4. Push (`git push origin feature-name`)
5. Open a Pull Request

## License
MIT © Isaiah Pawenapakorn

