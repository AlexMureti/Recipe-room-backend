# Recipe Room - Local Development Guide

This guide will help you run both frontend and backend locally and ensure they work well together.

---

## Quick Start

### Prerequisites

- **Backend:** Python 3.12+, pip
- **Frontend:** Node.js 18+, npm
- **Database:** PostgreSQL (recommended) or SQLite (development only)

---

## 🔧 Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd Recipe-room-backend
   ```

2. **Create virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   ```bash
   cp .env.example .env
   ```

5. **Edit `.env` for local development:**
   ```bash
   # Minimum required for local development:
   FLASK_ENV=development
   FLASK_DEBUG=True
   SECRET_KEY=dev-secret-key
   JWT_SECRET_KEY=dev-jwt-secret
   DATABASE_URL=sqlite:///recipe_room.db
   CORS_ORIGINS=http://localhost:5173,http://localhost:3000
   
   # Optional: Add PayD and Cloudinary credentials if testing those features
   ```

6. **Initialize database:**
   ```bash
   python -c "from app import app, db; app.app_context().push(); db.create_all()"
   ```

7. **Run the backend server:**
   ```bash
   python app.py
   ```
   
   Backend will run on: `http://localhost:8000`

8. **Test backend is running:**
   ```bash
   curl http://localhost:8000/health
   ```
   
   Expected response:
   ```json
   {
     "status": "healthy",
     "service": "recipe-room-api"
   }
   ```

---

## 🎨 Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd Recipe-room-frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Configure environment variables:**
   ```bash
   cp .env.example .env
   ```

4. **Verify `.env` settings:**
   ```bash
   # Should point to your local backend
   VITE_API_BASE_URL=http://localhost:8000/api
   VITE_ENV=development
   ```

5. **Run the development server:**
   ```bash
   npm run dev
   ```
   
   Frontend will run on: `http://localhost:5173`

6. **Open in browser:**
   ```
   http://localhost:5173
   ```

---

## ✅ Verify Integration

### Test 1: Backend API Discovery
Open: `http://localhost:8000/`

Expected response:
```json
{
  "name": "Recipe Room API",
  "version": "1.0.0",
  "description": "Backend API for Recipe Room application",
  "endpoints": {
    "auth": "/api/auth",
    "search": "/api/search",
    "recipes": "/api/recipes",
    "groups": "/api/groups",
    "payments": "/api/payments"
  }
}
```

### Test 2: CORS Configuration
1. Open frontend in browser (`http://localhost:5173`)
2. Open browser DevTools → Console
3. Try to register/login
4. **No CORS errors should appear**

If you see CORS errors:
- Check `CORS_ORIGINS` in backend `.env` includes `http://localhost:5173`
- Restart backend server after changing `.env`

### Test 3: User Registration
1. Navigate to registration page
2. Fill in user details
3. Submit form
4. Check browser Network tab - request should succeed (200/201)

### Test 4: Authentication Flow
1. Register a new user
2. Login with credentials
3. Check that JWT token is stored in browser localStorage
4. Navigate to protected routes (profile, recipes, etc.)

---

## 🔍 Troubleshooting

### Backend Issues

#### PostgreSQL connection error (DATABASE_URL override)
**Error:** `connection to server at "localhost" (127.0.0.1), port 5432 failed`

**Cause:** System environment variable `DATABASE_URL` is overriding your `.env` file

**Solution:**
```bash
# Quick fix: Use the startup script
./run_dev.sh

# OR manually unset before running
unset DATABASE_URL
python app.py

# Permanent fix: Remove from shell config files
grep -r "DATABASE_URL" ~/.bashrc ~/.bash_profile ~/.zshrc ~/.profile
# Edit the file and remove the DATABASE_URL line
```

See [FIX_DATABASE_ISSUE.md](./FIX_DATABASE_ISSUE.md) for detailed instructions.

#### Port 8000 already in use
```bash
# Find process using port 8000
lsof -i :8000  # On Mac/Linux
netstat -ano | findstr :8000  # On Windows

# Kill the process or change port in app.py
```

#### Database errors
```bash
# Delete and recreate database
rm recipe_room.db
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

#### Module not found errors
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Frontend Issues

#### Port 5173 already in use
```bash
# Vite will automatically try port 5174, 5175, etc.
# Or specify a custom port:
npm run dev -- --port 3000
```

#### API connection refused
1. **Check backend is running** on port 8000
2. **Verify** `VITE_API_BASE_URL` in `.env`
3. **Check browser console** for errors

#### Module not found errors
```bash
# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Integration Issues

#### CORS errors in browser console
**Error:** `Access to XMLHttpRequest blocked by CORS policy`

**Solution:**
1. Add your frontend URL to backend `CORS_ORIGINS`:
   ```bash
   # In backend .env
   CORS_ORIGINS=http://localhost:5173,http://localhost:3000
   ```
2. Restart backend server

#### 404 on all API calls
**Error:** All API endpoints return 404

**Solution:**
1. Verify backend is running on port 8000
2. Check `VITE_API_BASE_URL` in frontend `.env`
3. Ensure URL includes `/api` suffix: `http://localhost:8000/api`

#### Token not persisting
**Error:** User logged out on page refresh

**Solution:**
1. Check browser DevTools → Application → Local Storage
2. Verify token is being saved
3. Check for localStorage permissions/privacy settings

---

## Running Tests

### Backend Tests
```bash
cd Recipe-room-backend
source venv/bin/activate
pytest
pytest -v  # Verbose output
pytest tests/test_auth.py  # Specific test file
```

### Frontend Tests (if configured)
```bash
cd Recipe-room-frontend
npm test
```

---

## 📁 Project Structure

```
Recipe-room-backend/
├── app.py                 # Main Flask application
├── config.py              # Configuration
├── models.py              # Database models
├── routes/                # API endpoints
│   ├── auth.py
│   ├── recipes.py
│   ├── groups.py
│   ├── payments.py
│   └── search.py
├── tests/                 # Backend tests
├── .env                   # Environment variables (gitignored)
├── .env.example           # Example env file
└── requirements.txt       # Python dependencies

Recipe-room-frontend/
├── src/
│   ├── components/        # React components
│   ├── pages/             # Page components
│   ├── services/          # API services
│   ├── store/             # Redux store
│   ├── config/
│   │   └── api.config.js  # Centralized API config
│   └── main.jsx           # App entry point
├── .env                   # Environment variables (gitignored)
├── .env.example           # Example env file
├── vite.config.js         # Vite configuration
└── package.json           # Node dependencies
```

---

## 🔄 Development Workflow

### Making Changes

1. **Backend changes:**
   - Edit files in `routes/`, `models.py`, etc.
   - Flask auto-reloads in debug mode
   - Test endpoint in browser/Postman

2. **Frontend changes:**
   - Edit files in `src/`
   - Vite hot-reloads automatically
   - Check browser for updates

### Adding New API Endpoints

1. **Backend:** Add route in `routes/`
2. **Frontend:** Add endpoint to `src/config/api.config.js`
3. **Frontend:** Create/update service in `src/services/`
4. **Test** the integration

### Database Migrations (if using Flask-Migrate)

```bash
# Create migration
flask db migrate -m "Description of changes"

# Apply migration
flask db upgrade

# Rollback
flask db downgrade
```

---

## Environment Variables Reference

### Backend (.env)
| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `FLASK_ENV` | No | Environment mode | `development` |
| `FLASK_DEBUG` | No | Enable debug mode | `True` |
| `SECRET_KEY` | Yes | Flask secret key | `dev-secret-key` |
| `JWT_SECRET_KEY` | Yes | JWT signing key | `jwt-secret-key` |
| `DATABASE_URL` | Yes | Database connection | `sqlite:///recipe_room.db` |
| `CORS_ORIGINS` | Yes | Allowed origins | `http://localhost:5173` |
| `CLOUDINARY_*` | No | Image upload service | See `.env.example` |
| `PAYD_*` | No | Payment gateway | See `.env.example` |

### Frontend (.env)
| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `VITE_API_BASE_URL` | Yes | Backend API URL | `http://localhost:8000/api` |
| `VITE_PAYD_PUBLIC_KEY` | No | PayD public key | `pk_test_...` |
| `VITE_ENV` | No | Environment | `development` |

---

## 📚 Useful Commands

### Backend
```bash
# Activate virtual environment
source venv/bin/activate

# Install new package
pip install package-name
pip freeze > requirements.txt

# Run tests
pytest

# Check Flask routes
flask routes

# Python shell with app context
python
>>> from app import app, db
>>> app.app_context().push()
>>> # Now you can interact with models
```

### Frontend
```bash
# Install new package
npm install package-name

# Build for production
npm run build

# Preview production build
npm run preview

# Check bundle size
npm run build -- --mode=analyze
```

---

## 🎯 Next Steps

1. ✅ Backend and frontend running locally
2. ✅ Integration verified
3. 📖 Read [DEPLOYMENT.md](./DEPLOYMENT.md) for production deployment
4. 🔐 Configure Cloudinary for image uploads (optional)
5. 💳 Configure PayD for payments (optional)
6. 🧪 Write tests for new features

---

## 💡 Tips

- **Use browser DevTools** Network tab to debug API calls
- **Check backend logs** in terminal for errors
- **Use Postman/Thunder Client** to test API endpoints
- **Keep both servers running** in separate terminal windows
- **Use git branches** for new features

Happy coding! 
