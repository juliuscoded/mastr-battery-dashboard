# 🚀 Deployment Guide: Battery Storage Dashboard

This guide will walk you through deploying your battery storage dashboard to Streamlit Community Cloud with automated data updates via GitHub Actions.

## 📋 Prerequisites

- GitHub account
- MaStR API key
- Python 3.8+ (for local testing)

## 🎯 Step-by-Step Deployment

### Step 1: Create GitHub Repository

1. **Go to GitHub** and create a new repository:
   - Name: `battery-dashboard` (or your preferred name)
   - **Important**: Make it **public** (required for Streamlit Community Cloud)
   - Don't initialize with README (we'll add our files)

2. **Clone the repository locally**:
   ```bash
   git clone https://github.com/yourusername/battery-dashboard.git
   cd battery-dashboard
   ```

### Step 2: Prepare Your Files

1. **Copy all dashboard files** to your repository:
   ```bash
   # Copy all the files from your current directory
   cp -r /path/to/your/dashboard/files/* .
   ```

2. **Verify you have these key files**:
   - `battery_dashboard.py` (main dashboard)
   - `collect_dashboard_data.py` (data collection)
   - `.github/workflows/update_data.yml` (GitHub Actions)
   - `requirements_dashboard.txt` (dependencies)
   - `.streamlit/config.toml` (Streamlit config)

### Step 3: Set Up GitHub Secrets

1. **Go to your repository** → Settings → Secrets and variables → Actions
2. **Click "New repository secret"**
3. **Add your MaStR API key**:
   - **Name**: `MASTR_API_KEY`
   - **Value**: Your actual MaStR API key
4. **Click "Add secret"**

### Step 4: Push to GitHub

1. **Add all files**:
   ```bash
   git add .
   git commit -m "Initial commit: Battery Storage Dashboard"
   git push origin main
   ```

### Step 5: Deploy to Streamlit Cloud

1. **Go to [share.streamlit.io](https://share.streamlit.io)**
2. **Sign in with GitHub**
3. **Click "New app"**
4. **Fill in the details**:
   - **Repository**: Select your `battery-dashboard` repository
   - **Branch**: `main`
   - **Main file path**: `battery_dashboard.py`
   - **App URL**: Leave as default (or customize)
5. **Click "Deploy"**

### Step 6: Test the Deployment

1. **Wait for deployment** (usually 1-2 minutes)
2. **Visit your app URL** (e.g., `https://yourusername-battery-dashboard-app-xxxxx.streamlit.app`)
3. **Test the features**:
   - Map visualization
   - Filters
   - Data table
   - Analytics charts

## 🔧 GitHub Actions Setup

### Verify Workflow is Active

1. **Go to your repository** → Actions tab
2. **You should see** "Update Battery Data Daily" workflow
3. **Click on it** to see the workflow details

### Test Manual Trigger

1. **In the Actions tab**, click "Update Battery Data Daily"
2. **Click "Run workflow"** → "Run workflow"
3. **Monitor the execution** to ensure it works

### Schedule Verification

The workflow runs daily at 6 AM UTC. You can verify it's working by:
- Checking the Actions tab daily
- Looking for new commits with data updates
- Monitoring the repository for new JSON files

## 🔍 Troubleshooting

### Common Issues

#### 1. **"No data found" error**
- **Solution**: Check GitHub Actions workflow ran successfully
- **Check**: Repository → Actions → "Update Battery Data Daily"
- **Fix**: Manually trigger the workflow

#### 2. **API key not working**
- **Solution**: Verify the secret is set correctly
- **Check**: Repository → Settings → Secrets and variables → Actions
- **Fix**: Re-add the `MASTR_API_KEY` secret

#### 3. **Map not loading**
- **Solution**: Check internet connection and browser console
- **Fix**: Refresh the page or try a different browser

#### 4. **Streamlit deployment fails**
- **Solution**: Check the deployment logs
- **Common issues**:
  - Missing dependencies in `requirements_dashboard.txt`
  - Syntax errors in Python files
  - Missing files referenced in the code

### Debugging Steps

1. **Check GitHub Actions logs**:
   - Repository → Actions → Click on failed workflow
   - Look for error messages in the logs

2. **Check Streamlit deployment logs**:
   - Go to your app URL
   - Look for error messages in the browser console

3. **Test locally first**:
   ```bash
   pip install -r requirements_dashboard.txt
   streamlit run battery_dashboard.py
   ```

## 📊 Monitoring Your Deployment

### Daily Checks

1. **GitHub Actions**: Verify daily data updates are running
2. **Data freshness**: Check if new JSON files are being created
3. **App performance**: Monitor load times and responsiveness

### Weekly Maintenance

1. **Check for errors**: Review GitHub Actions and Streamlit logs
2. **Update dependencies**: Keep packages up to date
3. **Monitor API usage**: Ensure you're within MaStR API limits

## 🎉 Success Indicators

Your deployment is successful when:

✅ **Dashboard loads** without errors  
✅ **Map displays** battery locations  
✅ **Filters work** and update statistics  
✅ **GitHub Actions** run daily and create commits  
✅ **Data updates** appear in the dashboard  

## 🔗 Useful Links

- **Your Dashboard**: `https://yourusername-battery-dashboard-app-xxxxx.streamlit.app`
- **GitHub Repository**: `https://github.com/yourusername/battery-dashboard`
- **GitHub Actions**: `https://github.com/yourusername/battery-dashboard/actions`
- **Streamlit Community Cloud**: [share.streamlit.io](https://share.streamlit.io)

## 🆘 Getting Help

If you encounter issues:

1. **Check the troubleshooting section** above
2. **Review GitHub Actions logs** for detailed error messages
3. **Test locally** to isolate deployment vs. code issues
4. **Check Streamlit documentation** for deployment-specific issues

---

**🎊 Congratulations!** Your battery storage dashboard is now live and will automatically update daily with fresh data from the MaStR API! 