# 🔋 German Battery Storage Dashboard

An interactive Streamlit dashboard for visualizing German battery storage data from the MaStR (Marktstammdatenregister) API with automated daily data updates via GitHub Actions.

## 🚀 Features

- **📍 Interactive Map**: Visualize battery storage locations across Germany
- **🔍 Advanced Filters**: Filter by status, power, capacity, Bundesland, and owner
- **📊 Real-time Statistics**: Dynamic summary statistics that update with filters
- **📈 Analytics Charts**: Status distribution, regional breakdown, and technology analysis
- **📋 Detailed Data Table**: View all filtered data in a sortable table
- **🤖 Automated Updates**: Daily data updates via GitHub Actions
- **🎨 Beautiful UI**: Modern, responsive design with custom styling

## 📋 Requirements

- Python 3.8+
- MaStR API key
- GitHub account (for automated updates)
- Internet connection for map tiles

## 🛠️ Installation

1. **Install dependencies**:
```bash
pip install -r requirements_dashboard.txt
```

2. **Set your API key**:
```bash
export MASTR_API_KEY="your_api_key_here"
```

## 🚀 Deployment to Streamlit Community Cloud

### Step 1: Prepare Your Repository
1. **Create a public GitHub repository** for your dashboard
2. **Push all files** to the repository:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Battery Storage Dashboard"
   git branch -M main
   git remote add origin https://github.com/yourusername/battery-dashboard.git
   git push -u origin main
   ```

### Step 2: Set Up GitHub Secrets
1. Go to your repository → Settings → Secrets and variables → Actions
2. Add the following secret:
   - **Name**: `MASTR_API_KEY`
   - **Value**: Your MaStR API key

### Step 3: Deploy to Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"
4. Select your repository and main branch
5. Set the path to your app: `battery_dashboard.py`
6. Click "Deploy"

## 📊 Data Collection

### Automated Daily Updates
The dashboard uses GitHub Actions to automatically update data daily at 6 AM UTC. The workflow:
- Runs your data collection script
- Commits changes if new data is found
- Ensures the dashboard always has fresh data

### Manual Data Collection
```bash
# Collect comprehensive data (recommended)
python3 collect_dashboard_data.py

# Use custom thresholds
python3 collect_dashboard_data.py --min-power 1000 --min-capacity 1000
```

## 🎯 Running Locally

```bash
streamlit run battery_dashboard.py
```

The dashboard will open in your browser at `http://localhost:8501`.

## 🎛️ Dashboard Features

### 📍 Interactive Map
- **Hover tooltips** show detailed battery information
- **Color-coded** by operating status (Green=Operating, Yellow=Planned, Red=Shutdown)
- **Size** of markers indicates power capacity
- **Zoom and pan** to explore different regions

### 🔍 Sidebar Filters
- **Status**: Operating, Planned, Temporarily Shutdown, Permanently Shutdown
- **Power Range**: Slider to filter by power capacity (MW)
- **Capacity Range**: Slider to filter by energy capacity (MWh)
- **Bundesland**: Filter by German federal state
- **Owner**: Filter by battery owner/operator

### 📊 Summary Statistics
- **Total Units**: Number of batteries matching filters
- **Total Power**: Combined power capacity (MW)
- **Total Capacity**: Combined energy capacity (MWh)
- **Average Power**: Mean power per unit (MW)
- **Status Breakdown**: Count by operating status
- **Technology Breakdown**: Count by battery technology

### 📈 Analytics Charts
- **Status Distribution**: Pie chart of operating statuses
- **Top Bundesländer**: Bar chart of units by federal state
- **Technology Distribution**: Pie chart of battery technologies

### 📋 Data Table
- **Sortable columns**: Click headers to sort
- **Filtered data**: Shows only units matching current filters
- **Key information**: Name, owner, status, power, capacity, location

## 🔧 GitHub Actions Workflow

The `.github/workflows/update_data.yml` file contains the automated workflow that:
- Runs daily at 6 AM UTC
- Collects fresh data from MaStR API
- Commits changes if new data is found
- Keeps the dashboard data current

### Manual Trigger
You can manually trigger the workflow:
1. Go to your repository → Actions
2. Select "Update Battery Data Daily"
3. Click "Run workflow"

## 🎨 Customization

### Adding New Filters
Edit `battery_dashboard.py` and add new filter widgets in the sidebar section:

```python
# Example: Add technology filter
tech_options = ['All'] + list(df['Batterietechnologie'].unique())
selected_tech = st.sidebar.selectbox("Technology", tech_options)
```

### Modifying Charts
Edit the `create_charts()` function in `battery_dashboard.py` to add new visualizations.

### Styling
Modify the CSS in the `st.markdown()` section to customize colors, fonts, and layout.

## 🔧 Troubleshooting

### No Data Found
- Ensure GitHub Actions workflow is running
- Check that your API key is set in GitHub secrets
- Verify JSON files are in the repository

### Map Not Loading
- Check internet connection (required for map tiles)
- Try refreshing the page
- Ensure coordinates are valid in the data

### Performance Issues
- Reduce data size by using higher thresholds in data collection
- Use smaller page sizes in the collection script
- Consider caching with `@st.cache_data`

## 📈 Data Insights

The dashboard reveals interesting patterns in German battery storage:

- **Geographic Distribution**: Which Bundesländer have the most storage
- **Size Trends**: Distribution of power and capacity ranges
- **Technology Mix**: Types of battery technologies being deployed
- **Development Status**: Ratio of operating vs. planned projects
- **Owner Analysis**: Major players in the battery storage market

## 🤝 Contributing

Feel free to enhance the dashboard by:
- Adding new filter options
- Creating additional visualizations
- Improving the UI/UX
- Adding export functionality
- Implementing real-time data updates

## 📄 License

This project is for educational and research purposes. Please respect the MaStR API terms of service.

## 🔗 Links

- **Streamlit Community Cloud**: [share.streamlit.io](https://share.streamlit.io)
- **GitHub Actions**: [docs.github.com/en/actions](https://docs.github.com/en/actions)
- **MaStR API**: [www.marktstammdatenregister.de](https://www.marktstammdatenregister.de) 