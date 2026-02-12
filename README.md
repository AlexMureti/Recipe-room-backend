# Recipe Room 🍳

A collaborative platform for sharing and discovering recipes with friends and groups.

## 📋 Overview

Recipe Room is a full-stack web application that allows users to:
- 🔐 Register and authenticate securely
- 📝 Create, edit, and manage recipes
- 👥 Create groups and collaborate with others
- 🖼️ Upload recipe and profile images
- 💳 Process payments (optional)
- 🔍 Search and discover recipes

## 🛠️ Tech Stack

### Backend
- **Framework**: Flask 3.0
- **Database**: PostgreSQL / SQLite
- **Authentication**: JWT (Flask-JWT-Extended)
- **Image Storage**: Cloudinary
- **ORM**: SQLAlchemy
- **Payments**: PayD (optional)

### Frontend
- **Framework**: React 18+ with Vite
- **State Management**: Redux Toolkit
- **HTTP Client**: Axios
- **Styling**: [Your CSS framework]

## 🚀 Quick Start

### For Local Development

See **[DEVELOPMENT.md](./DEVELOPMENT.md)** for detailed setup instructions.

**TL;DR:**
```bash
# Backend
cd Recipe-room-backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your configuration
python app.py

# Frontend (in a new terminal)
cd Recipe-room-frontend
npm install
cp .env.example .env
# Edit .env with backend URL
npm run dev
```

### For Production Deployment

See **[DEPLOYMENT.md](./DEPLOYMENT.md)** for complete deployment guide.

Use **[PRE_DEPLOYMENT_CHECKLIST.md](./PRE_DEPLOYMENT_CHECKLIST.md)** to ensure everything is ready.

## 📖 Documentation

- **[DEVELOPMENT.md](./DEVELOPMENT.md)** - Local development setup and workflow
- **[DEPLOYMENT.md](./DEPLOYMENT.md)** - Production deployment guide
- **[PRE_DEPLOYMENT_CHECKLIST.md](./PRE_DEPLOYMENT_CHECKLIST.md)** - Pre-deployment verification
- **[API_DOCUMENTATION.md](./API_DOCUMENTATION.md)** - API endpoints reference
- **[DATABASE_SCHEMA.md](./DATABASE_SCHEMA.md)** - Database schema documentation

## 🧪 Testing

### Backend Integration Tests
```bash
cd Recipe-room-backend
python test_integration.py
```

### Backend Unit Tests
```bash
cd Recipe-room-backend
source venv/bin/activate
pytest
```

## 🔑 Key Features

### Implemented
- ✅ User registration and authentication
- ✅ JWT-based authorization
- ✅ User profile management
- ✅ Recipe CRUD operations
- ✅ Group creation and management
- ✅ Image uploads with Cloudinary
- ✅ Payment processing with PayD
- ✅ Recipe search functionality
- ✅ CORS configured for frontend integration

### API Endpoints
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/profile` - Get user profile
- `PUT /api/auth/profile` - Update user profile
- `POST /api/auth/upload-image` - Upload profile image
- `GET /api/recipes` - Get all recipes
- `POST /api/recipes` - Create recipe
- `GET /api/groups` - Get user's groups
- `POST /api/groups` - Create group
- See [API_DOCUMENTATION.md](./API_DOCUMENTATION.md) for full list

## 📁 Project Structure

```
Recipe-room-backend/
├── app.py                          # Flask application entry point
├── config.py                       # Configuration management
├── models.py                       # Database models
├── database.py                     # Database initialization
├── utils.py                        # Utility functions
├── routes/                         # API route blueprints
│   ├── auth.py                    # Authentication endpoints
│   ├── recipes.py                 # Recipe CRUD endpoints
│   ├── groups.py                  # Group management endpoints
│   ├── payments.py                # Payment processing endpoints
│   └── search.py                  # Search functionality
├── tests/                          # Backend tests
├── Recipe-room-frontend/           # Frontend application
│   ├── src/
│   │   ├── components/            # React components
│   │   ├── pages/                 # Page components
│   │   ├── services/              # API services
│   │   ├── store/                 # Redux store
│   │   └── config/
│   │       └── api.config.js      # Centralized API config
│   ├── .env.example               # Frontend env template
│   └── package.json               # Frontend dependencies
├── .env.example                    # Backend env template
├── requirements.txt                # Python dependencies
├── DEVELOPMENT.md                  # Development guide
├── DEPLOYMENT.md                   # Deployment guide
└── PRE_DEPLOYMENT_CHECKLIST.md    # Deployment checklist
```

## 🌐 Environment Variables

See `.env.example` files in backend and frontend for complete configuration.

**Key variables:**
- `DATABASE_URL` - Database connection string
- `SECRET_KEY` - Flask secret key
- `JWT_SECRET_KEY` - JWT signing key
- `CORS_ORIGINS` - Allowed frontend origins
- `VITE_API_BASE_URL` - Backend API URL (frontend)

## 🔄 Development Workflow

1. **Start backend:**
   ```bash
   cd Recipe-room-backend
   source venv/bin/activate
   python app.py
   ```
   Backend runs on http://localhost:8000

2. **Start frontend:**
   ```bash
   cd Recipe-room-frontend
   npm run dev
   ```
   Frontend runs on http://localhost:5173

3. **Test integration:**
   ```bash
   python test_integration.py
   ```

## 🤝 Contributing

1. Create feature branch from `main`
2. Make changes following existing code style
3. Test changes locally (backend + frontend)
4. Run integration tests
5. Commit and push
6. Create pull request

## 📄 License

MIT

## 👥 Team

- Frontend: React + Vite
- Backend: Flask + PostgreSQL
- DevOps: Railway/Vercel/Render

## 🔗 Links

- **Local Backend:** http://localhost:8000
- **Local Frontend:** http://localhost:5173
- **Production:** [Add your production URLs after deployment]

## 📞 Support

For setup or deployment issues:
1. Check [DEVELOPMENT.md](./DEVELOPMENT.md)
2. Check [DEPLOYMENT.md](./DEPLOYMENT.md)
3. Review error logs
4. Test with `test_integration.py`

---

Made with ❤️ by the Recipe Room Team