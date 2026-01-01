# Deployment Guide - Cashew Trade Analytics

## 🚀 Deployment Options

This guide covers deployment to **Streamlit Cloud** (recommended) and alternative platforms.

---

## Option 1: Streamlit Cloud (Recommended)

Streamlit Cloud offers free hosting for public repositories with automatic deployment from GitHub.

### Prerequisites
- GitHub account
- Streamlit Cloud account (sign up at [share.streamlit.io](https://share.streamlit.io))
- Public GitHub repository

### Step-by-Step Deployment

#### 1. Prepare Repository

Ensure your repository has:
- ✅ `requirements.txt` with all dependencies
- ✅ `dashboard/app.py` as the main application
- ✅ Sample data in `data/sample/`
- ✅ `.streamlit/config.toml` for configuration

#### 2. Push to GitHub

```bash
git add .
git commit -m "Prepare for Streamlit Cloud deployment"
git push origin main
```

#### 3. Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "New app"
3. Select your repository: `tuyetngth2558/cashew-trade-analytics`
4. Set main file path: `dashboard/app.py`
5. Click "Deploy"

#### 4. Configure Environment (if needed)

If you have environment variables, add them in Streamlit Cloud:
- Go to app settings → Secrets
- Add variables in TOML format:
```toml
# Example secrets
DATABASE_PATH = "data/database/contracts.db"
```

#### 5. Monitor Deployment

- Deployment typically takes 2-5 minutes
- Check logs for any errors
- Your app will be available at: `https://[your-app-name].streamlit.app`

### Automatic Updates

Streamlit Cloud automatically redeploys when you push to the main branch:
```bash
git add .
git commit -m "Update dashboard"
git push origin main
# App will auto-redeploy in ~2 minutes
```

---

## Option 2: Docker Deployment

Deploy using Docker on any platform (Render, Railway, Fly.io, etc.)

### Build and Run Locally

```bash
# Build image
docker build -t cashew-analytics .

# Run container
docker run -p 8501:8501 cashew-analytics

# Or use docker-compose
docker-compose up
```

### Deploy to Render

1. Create account at [render.com](https://render.com)
2. Create new "Web Service"
3. Connect GitHub repository
4. Configure:
   - **Environment**: Docker
   - **Dockerfile Path**: `./Dockerfile`
   - **Port**: 8501
5. Deploy

### Deploy to Railway

1. Create account at [railway.app](https://railway.app)
2. Create new project from GitHub
3. Railway auto-detects Dockerfile
4. Set environment variables if needed
5. Deploy

---

## Option 3: Heroku Deployment

### Prerequisites
- Heroku account
- Heroku CLI installed

### Setup Files

Create `setup.sh`:
```bash
mkdir -p ~/.streamlit/

echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
" > ~/.streamlit/config.toml
```

Create `Procfile`:
```
web: sh setup.sh && streamlit run dashboard/app.py
```

### Deploy

```bash
# Login to Heroku
heroku login

# Create app
heroku create cashew-analytics

# Push to Heroku
git push heroku main

# Open app
heroku open
```

---

## 🔧 Configuration

### Environment Variables

Set these environment variables for production:

```bash
# Database
DATABASE_PATH=/app/data/database/contracts.db

# Streamlit
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Optional: Analytics
GOOGLE_ANALYTICS_ID=UA-XXXXXXXXX-X
```

### Streamlit Configuration

Edit `.streamlit/config.toml`:

```toml
[server]
port = 8501
enableCORS = false
enableXsrfProtection = true

[browser]
gatherUsageStats = false

[theme]
primaryColor = "#FF6B35"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
```

---

## 📊 Post-Deployment

### 1. Verify Deployment

Check these after deployment:
- ✅ App loads without errors
- ✅ Sample data displays correctly
- ✅ All charts render properly
- ✅ Filters work as expected
- ✅ No console errors

### 2. Monitor Performance

Use Streamlit Cloud analytics:
- View app usage statistics
- Monitor response times
- Check error logs

### 3. Set Up Monitoring

Optional monitoring tools:
- **Sentry**: Error tracking
- **Google Analytics**: User analytics
- **Uptime Robot**: Availability monitoring

---

## 🔒 Security Best Practices

### For Public Deployment

1. **Never commit sensitive data**:
   - Use `.gitignore` for real data files
   - Only include sample/synthetic data
   
2. **Use environment variables**:
   - Store API keys in secrets
   - Never hardcode credentials

3. **Enable authentication** (if needed):
   - Use Streamlit authentication
   - Or implement custom auth

### For Private Deployment

1. **Use private repository**:
   - Streamlit Cloud supports private repos
   - Or deploy on private infrastructure

2. **Add access control**:
   - IP whitelisting
   - VPN access
   - OAuth integration

---

## 🐛 Troubleshooting

### Common Issues

#### App won't start
```bash
# Check logs
streamlit run dashboard/app.py --logger.level=debug

# Verify dependencies
pip install -r requirements.txt
```

#### Missing data
```bash
# Generate sample data
python scripts/generate_sample_data.py
```

#### Port already in use
```bash
# Use different port
streamlit run dashboard/app.py --server.port=8502
```

### Streamlit Cloud Specific

#### Build fails
- Check `requirements.txt` has all dependencies
- Ensure Python version compatibility
- Check logs in Streamlit Cloud dashboard

#### App crashes
- Check memory usage (free tier: 1GB limit)
- Optimize data loading
- Use caching with `@st.cache_data`

---

## 📈 Scaling

### Performance Optimization

1. **Use caching**:
```python
@st.cache_data
def load_data():
    return pd.read_csv('data/sample/sample_data.csv')
```

2. **Lazy loading**:
   - Load data only when needed
   - Use pagination for large datasets

3. **Optimize queries**:
   - Use database indexes
   - Limit result sets

### Upgrade Options

For production use:
- **Streamlit Cloud Teams**: $250/month
  - More resources
  - Private apps
  - Priority support

- **Self-hosted**: 
  - Full control
  - Unlimited resources
  - Custom domain

---

## 🔄 CI/CD Pipeline

### GitHub Actions

Automated workflows are set up in `.github/workflows/`:

1. **test.yml**: Runs on every push
   - Runs pytest
   - Checks code coverage
   - Lints code

2. **deploy.yml**: Runs on main branch
   - Validates deployment
   - Triggers Streamlit Cloud update

### Manual Deployment

```bash
# Run tests locally
pytest tests/ -v

# Generate sample data
python scripts/generate_sample_data.py

# Test app locally
streamlit run dashboard/app.py

# Push to production
git push origin main
```

---

## 📞 Support

### Resources
- [Streamlit Documentation](https://docs.streamlit.io)
- [Streamlit Community Forum](https://discuss.streamlit.io)
- [Project Issues](https://github.com/tuyetngth2558/cashew-trade-analytics/issues)

### Getting Help

1. Check logs in Streamlit Cloud dashboard
2. Review troubleshooting section above
3. Open issue on GitHub
4. Ask in Streamlit community forum

---

## ✅ Deployment Checklist

Before going live:

- [ ] All tests passing
- [ ] Sample data generated
- [ ] Environment variables configured
- [ ] `.gitignore` properly set up
- [ ] README updated with deployment URL
- [ ] Monitoring set up
- [ ] Security review completed
- [ ] Performance tested
- [ ] Documentation updated
- [ ] Backup strategy in place

---

**Last Updated**: 2026-01-01  
**Deployment Platform**: Streamlit Cloud  
**App URL**: TBD after deployment
