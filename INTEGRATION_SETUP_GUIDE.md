# 🔧 Integration Setup & Troubleshooting Guide

## ✅ What's Been Configured

### 1. **Backend API** (Production Ready)
- ✅ Flask application deployed on Railway
- ✅ Endpoints documented and accessible
- ✅ Health checks passing
- ✅ JWT authentication configured
- ✅ Database schema created

### 2. **Frontend** (Connected to Backend)
- ✅ React app deployed on Vercel
- ✅ Environment variables configured
- ✅ API base URL: `https://recipe-room-backend-production.up.railway.app/api`

### 3. **Database Setup**
- ✅ PostgreSQL provisioned on Railway
- ✅ Local SQLite fully seeded with 9 users + recipes + groups
- ⚠️ Production PostgreSQL needs data sync

### 4. **CORS Configuration**
- ✅ Backend CORS origins updated
- ✅ Includes: localhost, and `https://flavor-hub-orpin.vercel.app`

---

## ❌ Current Blocker: Production Database Empty

**Symptom**: Login endpoint returns `{"error": "Invalid credentials"}`

**Why**: The PostgreSQL database on Railway doesn't have user data

---

## 🚀 How to Fix: Step-by-Step

### Option 1: Re-seed Production Database (Recommended)

**Step 1**: Ensure DATABASE_URL is set on Railway
```bash
# Go to Railway Dashboard → Recipe-room-backend → Variables
# Add or verify:
DATABASE_URL=postgresql://postgres:kEGdbWbeDHueUZpppxKvqBShElJYESSZ@shinkansen.proxy.rlwy.net:26274/railway
```

**Step 2**: Run the seed script locally pointing to production
```bash
cd /home/alex/final/Recipe-room-backend

export DATABASE_URL="postgresql://postgres:kEGdbWbeDHueUZpppxKvqBShElJYESSZ@shinkansen.proxy.rlwy.net:26274/railway"

timeout 180 python3 seed_data.py
```

**Expected Output**:
```
🌱 Clearing existing database...
✅ Database cleared and recreated
🌱 Seeding database with test data...
✅ Created 9 test users
✅ Created 5 test recipes
✅ Created 3 test groups
✅ Created 5 test ratings
✅ Created 5 test bookmarks
✅ Created test comments

🎉 Database seeding complete!
```

**Step 3**: Verify with a test login
```bash
curl -X POST https://recipe-room-backend-production.up.railway.app/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"john@example.com","password":"password123"}'

# Should return:
# {"access_token": "eyJ...", "user": {...}}
```

---

### Option 2: Deploy Backend with Automatic Seeding (Advanced)

Modify `app.py` to automatically seed database on first startup:

```python
# In create_app() function, after db.create_all()
with app.app_context():
    if User.query.count() == 0:
        print("🌱 Database empty, auto-seeding...")
        seed_database()  # Call seed function
```

---

## 🧪 Testing Checklist

Once data is loaded, test the flow:

### 1. **Backend Health**
```bash
✅ GET https://recipe-room-backend-production.up.railway.app/health
   Should return: {"status": "healthy"}
```

### 2. **Login Flow**
```bash
✅ POST https://recipe-room-backend-production.up.railway.app/api/auth/login
   Body: {"email":"john@example.com","password":"password123"}
   Should return: {"access_token": "...", "user": {...}}
```

### 3. **Get Recipes** (requires token)
```bash
✅ GET https://recipe-room-backend-production.up.railway.app/api/recipes
   Header: Authorization: Bearer <token>
   Should return: [{"id": 1, "recipe_title": "...", ...}, ...]
```

### 4. **Get Groups** (requires token)
```bash
✅ GET https://recipe-room-backend-production.up.railway.app/api/groups
   Header: Authorization: Bearer <token>
   Should return: [{"id": 1, "name": "...", ...}, ...]
```

### 5. **Frontend Login Test**
1. Go to https://flavor-hub-orpin.vercel.app
2. Navigate to Login page
3. Use: `john@example.com` / `password123`
4. Should redirect to dashboard with recipes/groups loaded

---

## 📋 Available Test Accounts

All have password: `password123`

| Username | Email |
|----------|-------|
| john_chef | john@example.com |
| sarah_cook | sarah@example.com |
| mike_baker | mike@example.com |
| emma_foodie | emma@example.com |
| sasha_lisa | sasha@example.com |
| joy_kori | joy@example.com |
| derrick | derrick@example.com |
| ian | ian@example.com |
| alex_maingi | alex@example.com |

---

## 🔗 Key Resources

- **Live Backend Docs**: https://recipe-room-backend-production.up.railway.app/api-docs
- **Frontend**: https://flavor-hub-orpin.vercel.app
- **Backend**: https://recipe-room-backend-production.up.railway.app
- **GitHub**: https://github.com/AlexMureti/Recipe-room-backend

---

## 💡 If Seeding Still Fails

**Possible causes & solutions**:

1. **Connection Timeout**: Increase timeout in seed command
   ```bash
   timeout 300 python3 seed_data.py  # 5 minutes
   ```

2. **Environment Variable Not Set**: Use inline
   ```bash
   python3 -c "
   import os
   os.environ['DATABASE_URL'] = 'postgresql://...'
   from seed_data import seed_database
   seed_database()
   "
   ```

3. **Railway Database Service Down**: Check Railway dashboard status

4. **Seed Script Errors**: Check for SQL constraint violations
   ```bash
   python3 seed_data.py 2>&1 | tail -50  # Show last 50 lines of errors
   ```

---

## 📊 Summary of Current State

| Component | Local | Production | Status |
|-----------|-------|-----------|--------|
| **Backend API** | ✅ Code Ready | ✅ Deployed | ✅ Ready |
| **Frontend** | ✅ Ready | ✅ Deployed | ✅ Ready |
| **SQLite DB** | ✅ Seeded | N/A | ✅ Full Data |
| **PostgreSQL DB** | N/A | ⚠️ Empty | 🔧 **NEEDS SEEDING** |
| **CORS Config** | ✅ Set | ✅ Updated | ✅ Ready |
| **API Docs** | ✅ Available | ✅ Live | ✅ Ready |

---

**Next Action**: Run production database seeding command to unblock integration testing! 🚀
