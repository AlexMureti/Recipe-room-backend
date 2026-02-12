# Recipe Room - Deployment Guide

This guide will help you deploy both the backend (Flask API) and frontend (React + Vite) for production.

---

## 🎯 Pre-Deployment Checklist

### Backend Requirements
- [ ] Python 3.12+ installed
- [ ] PostgreSQL database (recommended for production)
- [ ] Environment variables configured
- [ ] CORS origins set to your frontend domain(s)

### Frontend Requirements
- [ ] Node.js 18+ installed
- [ ] Backend API URL configured
- [ ] Build tested locally
- [ ] Environment variables set

---

## 🔧 Configuration

### Backend Configuration

1. **Copy and configure environment variables:**
   ```bash
   cd Recipe-room-backend
   cp .env.example .env
   ```

2. **Edit `.env` file with production values:**
   ```bash
   # Production Example
   FLASK_ENV=production
   FLASK_DEBUG=False
   
   SECRET_KEY=your-strong-random-secret-key-change-this
   JWT_SECRET_KEY=your-strong-jwt-secret-key-change-this
   
   # PostgreSQL Database
   DATABASE_URL=postgresql://user:password@host:5432/recipe_room
   
   # CORS - Add your frontend domain(s)
   CORS_ORIGINS=https://yourapp.com,https://www.yourapp.com
   
   # PayD API Credentials
   PAYD_USERNAME=your_payd_username
   PAYD_PASSWORD=your_payd_password
   PAYD_API_SECRET=your_payd_api_secret
   PAYD_ACCOUNT_USERNAME=your_payd_account_username
   
   # Cloudinary (for image uploads)
   CLOUDINARY_CLOUD_NAME=your_cloud_name
   CLOUDINARY_API_KEY=your_api_key
   CLOUDINARY_API_SECRET=your_api_secret
   ```

3. **Generate secure secret keys:**
   ```bash
   # Generate SECRET_KEY
   python -c "import secrets; print(secrets.token_hex(32))"
   
   # Generate JWT_SECRET_KEY
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

### Frontend Configuration

1. **Copy and configure environment variables:**
   ```bash
   cd Recipe-room-frontend
   cp .env.example .env
   ```

2. **Edit `.env` file:**
   ```bash
   # Production API URL
   VITE_API_BASE_URL=https://your-backend-domain.com/api
   
   # Optional: PayD Public Key
   VITE_PAYD_PUBLIC_KEY=your_public_key
   
   VITE_ENV=production
   ```

---

## 🚀 Deployment Options

### Option 1: Deploy to Vercel (Frontend) + Railway/Render (Backend)

#### Deploy Backend to Railway

1. **Install Railway CLI:**
   ```bash
   npm i -g @railway/cli
   ```

2. **Login and initialize:**
   ```bash
   railway login
   railway init
   ```

3. **Add PostgreSQL database:**
   ```bash
   railway add --database postgresql
   ```

4. **Set environment variables:**
   - Go to Railway dashboard
   - Add all variables from `.env.example`
   - Railway will automatically provide `DATABASE_URL`

5. **Deploy:**
   ```bash
   railway up
   ```

6. **Get your backend URL and update frontend config**

#### Deploy Frontend to Vercel

1. **Install Vercel CLI:**
   ```bash
   npm i -g vercel
   ```

2. **Navigate to frontend and deploy:**
   ```bash
   cd Recipe-room-frontend
   vercel
   ```

3. **Set environment variables in Vercel:**
   - Go to Vercel dashboard → Settings → Environment Variables
   - Add `VITE_API_BASE_URL` with your Railway backend URL

4. **Deploy to production:**
   ```bash
   vercel --prod
   ```

5. **Update backend CORS:**
   - Add your Vercel domain to `CORS_ORIGINS` in Railway

---

### Option 2: Deploy to Render (Both Frontend & Backend)

#### Deploy Backend

1. Create new **Web Service** on Render
2. Connect your GitHub repository
3. Configure:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
4. Add environment variables from `.env.example`
5. Deploy

#### Deploy Frontend

1. Create new **Static Site** on Render
2. Configure:
   - **Build Command:** `cd Recipe-room-frontend && npm install && npm run build`
   - **Publish Directory:** `Recipe-room-frontend/dist`
3. Add environment variable:
   - `VITE_API_BASE_URL`: Your backend URL
4. Deploy

---

### Option 3: Traditional VPS Deployment (Ubuntu/Debian)

#### Backend Setup

```bash
# Install dependencies
sudo apt update
sudo apt install python3.12 python3-pip postgresql nginx

# Clone repository
git clone <your-repo-url>
cd Recipe-room-backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn

# Configure PostgreSQL
sudo -u postgres createuser recipe_user
sudo -u postgres createdb recipe_room
sudo -u postgres psql
# In psql: ALTER USER recipe_user WITH PASSWORD 'your_password';

# Set environment variables
cp .env.example .env
nano .env  # Edit with production values

# Initialize database
python -c "from app import app, db; app.app_context().push(); db.create_all()"

# Test run
gunicorn --bind 0.0.0.0:8000 app:app
```

#### Configure Nginx for Backend

```nginx
# /etc/nginx/sites-available/recipe-room-api
server {
    listen 80;
    server_name api.yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/recipe-room-api /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# Setup SSL with Let's Encrypt
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d api.yourdomain.com
```

#### Create Systemd Service for Backend

```ini
# /etc/systemd/system/recipe-room.service
[Unit]
Description=Recipe Room Flask API
After=network.target

[Service]
User=www-data
WorkingDirectory=/path/to/Recipe-room-backend
Environment="PATH=/path/to/Recipe-room-backend/venv/bin"
ExecStart=/path/to/Recipe-room-backend/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:8000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Start service
sudo systemctl enable recipe-room
sudo systemctl start recipe-room
sudo systemctl status recipe-room
```

#### Frontend Setup

```bash
cd Recipe-room-frontend

# Install Node.js
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install nodejs

# Install dependencies
npm install

# Set environment variable
echo "VITE_API_BASE_URL=https://api.yourdomain.com/api" > .env

# Build
npm run build
```

#### Configure Nginx for Frontend

```nginx
# /etc/nginx/sites-available/recipe-room-frontend
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    root /path/to/Recipe-room-backend/Recipe-room-frontend/dist;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    # Cache static assets
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/recipe-room-frontend /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# Setup SSL
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

---

## 🔐 Security Best Practices

1. **Never commit `.env` files** - Already in `.gitignore`
2. **Use strong secret keys** - Generate with `secrets.token_hex(32)`
3. **Enable HTTPS** - Use Let's Encrypt or your hosting provider's SSL
4. **Restrict CORS** - Only allow your frontend domain(s)
5. **Use PostgreSQL in production** - SQLite is not recommended for production
6. **Set DEBUG=False** - Never run debug mode in production
7. **Use environment variables** - Never hardcode credentials
8. **Keep dependencies updated** - Regularly run `pip install --upgrade`

---

## 🧪 Testing Before Deployment

### Backend Tests
```bash
cd Recipe-room-backend
source venv/bin/activate
pytest
```

### Frontend Tests
```bash
cd Recipe-room-frontend
npm run build
npm run preview  # Test production build locally
```

### Integration Testing
1. Start backend locally with production-like settings
2. Build and preview frontend
3. Test all major user flows:
   - User registration & login
   - Recipe creation, editing, deletion
   - Group creation and member management
   - Image uploads
   - Payment flow (if configured)

---

## 🔍 Monitoring & Maintenance

### Health Checks

Backend health endpoint: `GET /health`
```json
{
  "status": "healthy",
  "service": "recipe-room-api"
}
```

### Logs

**Backend logs (systemd):**
```bash
sudo journalctl -u recipe-room -f
```

**Nginx logs:**
```bash
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```

### Database Backups

```bash
# Backup PostgreSQL
pg_dump -U recipe_user recipe_room > backup_$(date +%Y%m%d).sql

# Restore
psql -U recipe_user recipe_room < backup_20240101.sql
```

---

## 🆘 Troubleshooting

### CORS Errors
- **Problem:** Frontend can't connect to backend
- **Solution:** 
  1. Check `CORS_ORIGINS` in backend `.env`
  2. Ensure it matches your frontend domain exactly
  3. Include protocol (`https://`)
  4. Restart backend service

### Database Connection Issues
- **Problem:** `SQLALCHEMY_DATABASE_URI` error
- **Solution:**
  1. Verify PostgreSQL is running
  2. Check database credentials
  3. Ensure database exists
  4. Test connection: `psql -U recipe_user -d recipe_room`

### API Not Found (404)
- **Problem:** All API calls return 404
- **Solution:**
  1. Verify `VITE_API_BASE_URL` in frontend
  2. Check backend is running
  3. Ensure nginx proxy is configured correctly

### Image Upload Failures
- **Problem:** Profile images not uploading
- **Solution:**
  1. Verify Cloudinary credentials in backend `.env`
  2. Check Cloudinary dashboard for errors
  3. Ensure proper file size limits

---

## 📚 Additional Resources

- [Flask Deployment Documentation](https://flask.palletsprojects.com/en/latest/deploying/)
- [Vite Deployment Guide](https://vitejs.dev/guide/static-deploy.html)
- [Nginx Documentation](https://nginx.org/en/docs/)
- [Let's Encrypt](https://letsencrypt.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

---

## 📞 Support

For issues or questions:
1. Check this deployment guide
2. Review application logs
3. Test with health check endpoints
4. Verify environment variables are set correctly