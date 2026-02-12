# Pre-Deployment Checklist ✅

Use this checklist to ensure your Recipe Room application is ready for production deployment.

---

## 🔐 Security

- [ ] **Secret keys changed from defaults**
  - [ ] `SECRET_KEY` is a strong random value
  - [ ] `JWT_SECRET_KEY` is a strong random value
  - [ ] No default/development keys in production `.env`

- [ ] **Database secured**
  - [ ] Using PostgreSQL (not SQLite) in production
  - [ ] Database has strong password
  - [ ] Database is not publicly accessible

- [ ] **CORS configured properly**
  - [ ] `CORS_ORIGINS` set to specific frontend domain(s)
  - [ ] No wildcard (`*`) in production CORS

- [ ] **Debug mode disabled**
  - [ ] `FLASK_DEBUG=False` in production
  - [ ] `FLASK_ENV=production` in production

- [ ] **Sensitive data protected**
  - [ ] `.env` files in `.gitignore`
  - [ ] No credentials committed to git
  - [ ] Environment variables set in hosting platform

---

## ⚙️ Configuration

### Backend Configuration

- [ ] **Environment variables set:**
  - [ ] `SECRET_KEY`
  - [ ] `JWT_SECRET_KEY`
  - [ ] `DATABASE_URL` (PostgreSQL)
  - [ ] `CORS_ORIGINS` (your frontend domain)
  - [ ] `PAYD_*` credentials (if using payments)
  - [ ] `CLOUDINARY_*` credentials (if using image uploads)

- [ ] **Dependencies installed:**
  ```bash
  pip install -r requirements.txt
  ```

- [ ] **Database initialized:**
  ```bash
  python -c "from app import app, db; app.app_context().push(); db.create_all()"
  ```

### Frontend Configuration

- [ ] **Environment variables set:**
  - [ ] `VITE_API_BASE_URL` points to production backend
  - [ ] `VITE_ENV=production`

- [ ] **Dependencies installed:**
  ```bash
  npm install
  ```

- [ ] **Production build tested:**
  ```bash
  npm run build
  npm run preview
  ```

---

## 🧪 Testing

### Local Testing

- [ ] **Backend health check works:**
  ```bash
  curl http://localhost:8000/health
  # Expected: {"status": "healthy", "service": "recipe-room-api"}
  ```

- [ ] **API root endpoint works:**
  ```bash
  curl http://localhost:8000/
  # Should return API information
  ```

- [ ] **Frontend connects to backend:**
  - [ ] No CORS errors in browser console
  - [ ] API calls succeed in Network tab

### Integration Testing

- [ ] **User authentication flow:**
  - [ ] User can register
  - [ ] User can login
  - [ ] Token is saved and used for authenticated requests
  - [ ] Protected routes require authentication

- [ ] **Recipe management:**
  - [ ] User can create recipes
  - [ ] User can view recipes
  - [ ] User can edit own recipes
  - [ ] User can delete own recipes

- [ ] **Group functionality:**
  - [ ] User can create groups
  - [ ] User can add members to groups
  - [ ] User can add recipes to groups
  - [ ] Group members can view shared recipes

- [ ] **Image uploads (if configured):**
  - [ ] Profile images upload successfully
  - [ ] Uploaded images are accessible
  - [ ] Cloudinary credentials work

- [ ] **Payments (if configured):**
  - [ ] Payment flow initiates
  - [ ] Payment status updates correctly
  - [ ] PayD credentials work

### Automated Tests

- [ ] **Backend tests pass:**
  ```bash
  cd Recipe-room-backend
  pytest
  ```

- [ ] **No test failures or errors**

---

## 🚀 Deployment Platform

### Platform Selected

- [ ] Platform chosen (Vercel, Railway, Render, VPS, etc.)
- [ ] Account created and verified
- [ ] Payment method added (if required)

### Backend Deployment

- [ ] **Repository connected**
- [ ] **Environment variables configured**
- [ ] **Build/start commands set:**
  - Build: `pip install -r requirements.txt`
  - Start: `gunicorn app:app` or `python app.py`
- [ ] **Database provisioned and connected**
- [ ] **Deployment successful**
- [ ] **Backend URL obtained and tested**

### Frontend Deployment

- [ ] **Repository connected**
- [ ] **Environment variables configured:**
  - [ ] `VITE_API_BASE_URL` set to production backend URL
- [ ] **Build command set:**
  - Build: `npm install && npm run build`
  - Output: `dist`
- [ ] **Deployment successful**
- [ ] **Frontend URL obtained and tested**

---

## 🔗 Post-Deployment Configuration

- [ ] **Update backend CORS:**
  - [ ] Add production frontend URL to `CORS_ORIGINS`
  - [ ] Redeploy backend

- [ ] **Test production integration:**
  - [ ] Open frontend in browser
  - [ ] Check browser console for errors
  - [ ] Test user registration/login
  - [ ] Test creating/viewing recipes
  - [ ] Test group functionality

---

## 🌐 DNS & Domain (Optional)

- [ ] **Custom domain purchased**
- [ ] **DNS configured:**
  - [ ] Frontend domain points to hosting platform
  - [ ] Backend domain/subdomain configured
- [ ] **SSL/HTTPS enabled:**
  - [ ] Frontend has valid SSL certificate
  - [ ] Backend has valid SSL certificate
  - [ ] HTTP redirects to HTTPS

---

## 📊 Monitoring & Maintenance

- [ ] **Error tracking set up:**
  - [ ] Error logs accessible
  - [ ] Error notifications configured (optional)

- [ ] **Health monitoring:**
  - [ ] `/health` endpoint accessible
  - [ ] Uptime monitoring configured (optional)

- [ ] **Database backups:**
  - [ ] Backup strategy in place
  - [ ] Restore procedure tested

- [ ] **Performance monitoring (optional):**
  - [ ] Application performance monitoring tools
  - [ ] Database query optimization

---

## 📝 Documentation

- [ ] **README.md updated:**
  - [ ] Deployment links added
  - [ ] Production URLs documented

- [ ] **Environment variables documented:**
  - [ ] `.env.example` files complete and accurate

- [ ] **API documentation available:**
  - [ ] Endpoint documentation up to date

---

## 🎉 Final Checks

- [ ] **Production URLs work:**
  - [ ] Frontend: `https://your-frontend-domain.com`
  - [ ] Backend: `https://your-backend-domain.com`
  - [ ] API: `https://your-backend-domain.com/api`

- [ ] **All features tested in production:**
  - [ ] User registration/login
  - [ ] Recipe CRUD operations
  - [ ] Group management
  - [ ] Image uploads (if applicable)
  - [ ] Payments (if applicable)

- [ ] **No errors in production:**
  - [ ] Browser console clean
  - [ ] Backend logs clean
  - [ ] No CORS errors

- [ ] **Performance acceptable:**
  - [ ] Pages load quickly
  - [ ] API responses are fast
  - [ ] No timeout errors

---

## 🚨 Rollback Plan

In case of deployment issues:

- [ ] **Backup plan ready:**
  - [ ] Previous version tagged in git
  - [ ] Database backup available
  - [ ] Can quickly revert deployment

- [ ] **Emergency contacts:**
  - [ ] Team members notified
  - [ ] Hosting support contact info saved

---

## 📞 Post-Deployment Support

After deployment:

1. **Monitor application for 24-48 hours**
2. **Check error logs regularly**
3. **Test all critical user flows**
4. **Gather user feedback**
5. **Address any issues promptly**

---

## ✅ Deployment Complete!

Once all items are checked:

- [ ] **Deployment successful** ✅
- [ ] **Application is live** 🎉
- [ ] **Team notified** 📢
- [ ] **Users can access** 👥

---

### Useful Commands for Quick Checks

```bash
# Check backend health
curl https://your-backend-url.com/health

# Check backend API root
curl https://your-backend-url.com/

# Test frontend loads
curl -I https://your-frontend-url.com

# Check SSL certificate
curl -vI https://your-frontend-url.com 2>&1 | grep -i "SSL\|TLS"
```

---

**Remember:** It's normal to encounter issues during first deployment. Stay calm, check logs, and refer to [DEPLOYMENT.md](./DEPLOYMENT.md) for troubleshooting steps.