# Fix: PostgreSQL Connection Error

## Problem

You have a **system environment variable** `DATABASE_URL` set to PostgreSQL:
```
DATABASE_URL=postgresql://recipe_user:your_password@localhost/recipe_room
```

This is overriding your `.env` file, causing the app to try connecting to PostgreSQL (which isn't running) instead of SQLite.

## ✅ Solution 1: Quick Fix (Temporary)

**Use the startup script:**
```bash
./run_dev.sh
```

This script automatically unsets the PostgreSQL variable and starts with SQLite.

## ✅ Solution 2: Permanent Fix (Recommended)

**Remove the system environment variable permanently:**

### For bash/zsh users:

1. **Find where it's set:**
   ```bash
   grep -r "DATABASE_URL" ~/.bashrc ~/.bash_profile ~/.zshrc ~/.profile 2>/dev/null
   ```

2. **Edit the file** and remove or comment out the `DATABASE_URL` line:
   ```bash
   # Open the file where it was found (e.g., ~/.bashrc)
   nano ~/.bashrc
   
   # Comment out or remove this line:
   # export DATABASE_URL=postgresql://...
   ```

3. **Reload your shell:**
   ```bash
   source ~/.bashrc  # or ~/.zshrc, etc.
   ```

4. **Verify it's removed:**
   ```bash
   env | grep DATABASE_URL
   # Should return nothing
   ```

### Alternative: Override in current session

```bash
unset DATABASE_URL
```

Then run normally:
```bash
python app.py
```

## 🧪 Verify the Fix

After applying the fix, test that SQLite is being used:

```bash
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('Database:', os.getenv('DATABASE_URL', 'Using default SQLite'))"
```

Expected output:
```
Database: sqlite:///recipe_room.db
```

## 🚀 Start the Server

After fixing, start normally:

```bash
source venv/bin/activate
python app.py
```

Or use the convenient script:
```bash
./run_dev.sh
```

Server will run on: http://localhost:8000

## 📝 Notes

- **SQLite** is perfect for local development (no separate database server needed)
- **PostgreSQL** is recommended for production deployment
- Your `.env` file is already correctly configured for SQLite
- The system environment variable was interfering with this configuration

## 🔍 Why This Happened

Environment variable priority:
1. **System environment variables** (highest priority)
2. `.env` file values
3. Default values in code

Your system had `DATABASE_URL` set, which took precedence over the `.env` file.

## ✅ Current Status

Your backend is now running successfully with SQLite! 🎉

Test it:
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "recipe-room-api"
}
``