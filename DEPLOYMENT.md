# 🚀 Deployment Guide

Deploy SASDS to the cloud for free or low cost.

## Free Hosting Options

### 1. Streamlit Cloud (Recommended)

**Pros:** Easy deployment, free tier, no configuration

1. **Push code to GitHub**
   \`\`\`bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   \`\`\`

2. **Go to:** https://streamlit.io/cloud

3. **Click "New app"**

4. **Connect GitHub repo**
   - Select your GitHub account
   - Choose sasds repository
   - Select `app.py` as entry point

5. **Advanced settings:**
   - Python version: 3.10
   - Add environment variables:
     \`\`\`
     GEMINI_API_KEY=your_key_here
     DATABASE_URL=postgresql://...
     \`\`\`

6. **Deploy!** 🎉

**App will be at:** `https://your-username-sasds.streamlit.app`

### 2. Render.com (Free with Limitations)

**Pros:** Good for APIs, supports background jobs

1. **Create account** at https://render.com

2. **Create new Web Service**

3. **Connect GitHub**

4. **Settings:**
   - Build command: `pip install -r requirements.txt`
   - Start command: `streamlit run app.py --server.port $PORT`
   - Environment: Python 3.10
   - Add environment variables

5. **Add PostgreSQL database** (free tier)

6. **Deploy!**

**Note:** Free tier spins down after 15 min inactivity

### 3. Railway.app

**Pros:** Simple deployment, free tier credit

1. **Go to:** https://railway.app

2. **Create new project**

3. **Connect GitHub**

4. **Add PostgreSQL (free tier)**

5. **Deploy**

**Details:**
- Free tier: $5 credit/month
- After credit: Pay per use
- Great for hobbyist projects

### 4. Heroku (Paid - $7/month minimum)

Heroku free tier was discontinued, but still an option for paid deployment.

## Database for Deployed Apps

### Option 1: Neon.tech (Recommended)

\`\`\`
DATABASE_URL=postgresql://user:password@ep-xxxxx.neon.tech/database?sslmode=require
\`\`\`

- Free tier: 3 projects
- 3GB storage
- 20 connections
- No credit card

Sign up: https://neon.tech

### Option 2: Railway PostgreSQL

Create PostgreSQL plugin in Railway dashboard

### Option 3: Render Database

Create PostgreSQL database in Render dashboard

## Pre-Deployment Checklist

- ✅ Code pushed to GitHub
- ✅ .env not in repository (.gitignore added)
- ✅ requirements.txt up to date
- ✅ GEMINI_API_KEY ready
- ✅ DATABASE_URL configured
- ✅ App runs locally without errors
- ✅ All dependencies installed

## Environment Variables for Production

\`\`\`
GEMINI_API_KEY=your_api_key
DATABASE_URL=postgresql://user:pass@host/db
STREAMLIT_SERVER_PORT=8501
UPLOAD_DIR=./uploads
\`\`\`

## Post-Deployment

1. **Test the deployed app**
2. **Check logs** for errors
3. **Monitor performance**
4. **Set up auto-restart** if available

## Scaling Tips

- **Use PostgreSQL** instead of SQLite for production
- **Enable caching** in Streamlit config
- **Optimize database queries**
- **Set up monitoring** (logs, errors)
- **Consider load balancing** for high traffic

## Cost Breakdown

| Service | Free Tier | Cost |
|---------|-----------|------|
| Streamlit Cloud | ✅ | Free (community) |
| Render | ⚠️ Limited | $7+/month |
| Railway | ✅ $5 credit | Pay per use |
| Neon DB | ✅ | Free tier available |

---

**Your app is live! 🎉**
