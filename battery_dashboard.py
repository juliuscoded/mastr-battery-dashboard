#!/usr/bin/env python3
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import os
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="German Battery Storage Dashboard",
    page_icon="🔋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #2E8B57;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #2E8B57;
    }
    .stSelectbox > div > div {
        background-color: white;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_battery_data():
    """Load and preprocess battery data from JSON file"""
    try:
        # Try to load the most recent battery data file
        data_files = [f for f in os.listdir('.') if (f.startswith('all_batterie_speicher_') or f.startswith('dashboard_batterie_speicher_')) and f.endswith('.json')]
        if not data_files:
            st.error("No battery data files found. Please run the data collection script first.")
            return None
        
        # Use the most recent file
        latest_file = sorted(data_files)[-1]
        with open(latest_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Convert to DataFrame
        df = pd.DataFrame(data)
        
        # Clean and preprocess data
        df = preprocess_data(df)
        
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

def preprocess_data(df):
    """Clean and preprocess the battery data"""
    if df.empty:
        return df
    
    # Convert date strings to datetime
    date_columns = ['DatumLetzteAktualisierung', 'EinheitRegistrierungsdatum', 'InbetriebnahmeDatum']
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col].str.replace('/Date(', '').str.replace(')/', ''), unit='ms', errors='coerce')
    
    # Clean numeric columns
    numeric_columns = ['Bruttoleistung', 'Nettonennleistung', 'NutzbareSpeicherkapazitaet']
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Clean coordinates
    if 'Breitengrad' in df.columns:
        df['Breitengrad'] = pd.to_numeric(df['Breitengrad'], errors='coerce')
    if 'Laengengrad' in df.columns:
        df['Laengengrad'] = pd.to_numeric(df['Laengengrad'], errors='coerce')
    
    # Create derived columns
    df['Power_MW'] = df['Bruttoleistung'] / 1000  # Convert kW to MW
    df['Capacity_MWh'] = df['NutzbareSpeicherkapazitaet'] / 1000  # Convert kWh to MWh
    
    # Create size categories
    df['Power_Category'] = pd.cut(
        df['Power_MW'], 
        bins=[0, 1, 10, 100, 1000, float('inf')], 
        labels=['<1 MW', '1-10 MW', '10-100 MW', '100-1000 MW', '>1000 MW']
    )
    
    df['Capacity_Category'] = pd.cut(
        df['Capacity_MWh'], 
        bins=[0, 1, 10, 100, 1000, float('inf')], 
        labels=['<1 MWh', '1-10 MWh', '10-100 MWh', '100-1000 MWh', '>1000 MWh']
    )
    
    return df

def create_map(df_filtered):
    """Create an interactive map of battery locations"""
    # Filter out rows without coordinates
    df_map = df_filtered.dropna(subset=['Breitengrad', 'Laengengrad'])
    
    if df_map.empty:
        st.warning("No battery locations with coordinates found in the filtered data.")
        return
    
    # Create the map
    fig = px.scatter_mapbox(
        df_map,
        lat='Breitengrad',
        lon='Laengengrad',
        size='Power_MW',
        color='BetriebsStatusName',
        hover_name='EinheitName',
        hover_data={
            'EinheitName': True,
            'AnlagenbetreiberName': True,
            'Power_MW': ':.1f',
            'Capacity_MWh': ':.1f',
            'Batterietechnologie': True,
            'BetriebsStatusName': True,
            'Bundesland': True,
            'Gemeinde': True,
            'Breitengrad': False,
            'Laengengrad': False
        },
        color_discrete_map={
            'In Betrieb': '#2E8B57',
            'In Planung': '#FFD700',
            'Vorübergehend stillgelegt': '#FF6347',
            'Endgültig stillgelegt': '#8B0000'
        },
        zoom=6,
        center={'lat': 51.1657, 'lon': 10.4515},  # Center of Germany
        title="German Battery Storage Locations"
    )
    
    fig.update_layout(
        mapbox_style="carto-positron",
        height=600,
        margin={"r":0,"t":30,"l":0,"b":0}
    )
    
    return fig

def create_summary_stats(df_filtered):
    """Create summary statistics"""
    stats = {}
    
    # Basic counts
    stats['Total Units'] = len(df_filtered)
    stats['Total Power (MW)'] = df_filtered['Power_MW'].sum()
    stats['Total Capacity (MWh)'] = df_filtered['Capacity_MWh'].sum()
    
    # Averages
    if len(df_filtered) > 0:
        stats['Average Power (MW)'] = df_filtered['Power_MW'].mean()
        stats['Average Capacity (MWh)'] = df_filtered['Capacity_MWh'].mean()
    else:
        stats['Average Power (MW)'] = 0
        stats['Average Capacity (MWh)'] = 0
    
    # Status breakdown
    status_counts = df_filtered['BetriebsStatusName'].value_counts()
    stats['Status Breakdown'] = status_counts.to_dict()
    
    # Technology breakdown
    tech_counts = df_filtered['Batterietechnologie'].value_counts()
    stats['Technology Breakdown'] = tech_counts.to_dict()
    
    # Bundesland breakdown
    bundesland_counts = df_filtered['Bundesland'].value_counts()
    stats['Bundesland Breakdown'] = bundesland_counts.to_dict()
    
    return stats

def create_charts(df_filtered):
    """Create various charts"""
    charts = {}
    
    # Status distribution pie chart
    if not df_filtered.empty:
        status_counts = df_filtered['BetriebsStatusName'].value_counts()
        fig_status = px.pie(
            values=status_counts.values,
            names=status_counts.index,
            title="Operating Status Distribution",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        charts['status'] = fig_status
        
        # Technology distribution pie chart
        tech_counts = df_filtered['Batterietechnologie'].value_counts()
        fig_tech = px.pie(
            values=tech_counts.values,
            names=tech_counts.index,
            title="Battery Technology Distribution",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        charts['technology'] = fig_tech
        
        # Top Bundesländer bar chart
        bundesland_counts = df_filtered['Bundesland'].value_counts().head(10)
        fig_bundesland = px.bar(
            x=bundesland_counts.values,
            y=bundesland_counts.index,
            orientation='h',
            title="Top 10 Bundesländer by Number of Units",
            labels={'x': 'Number of Units', 'y': 'Bundesland'}
        )
        charts['bundesland'] = fig_bundesland
    
    return charts

def main():
    # Header
    st.markdown('<h1 class="main-header">🔋 German Battery Storage Dashboard</h1>', unsafe_allow_html=True)
    st.markdown("Interactive visualization of German battery storage data from MaStR (Marktstammdatenregister)")
    
    # Load data
    df = load_battery_data()
    if df is None:
        st.stop()
    
    # Sidebar filters
    st.sidebar.markdown("## 🔍 Filters")
    
    # Status filter
    st.sidebar.markdown("### Status")
    status_options = ['All'] + list(df['BetriebsStatusName'].unique())
    selected_status = st.sidebar.selectbox("Operating Status", status_options)
    
    # Power filter
    st.sidebar.markdown("### Power Range (MW)")
    power_min, power_max = st.sidebar.slider(
        "Power Range",
        min_value=float(df['Power_MW'].min()),
        max_value=float(df['Power_MW'].max()),
        value=(float(df['Power_MW'].min()), float(df['Power_MW'].max())),
        step=0.1
    )
    
    # Capacity filter
    st.sidebar.markdown("### Capacity Range (MWh)")
    capacity_min, capacity_max = st.sidebar.slider(
        "Capacity Range",
        min_value=float(df['Capacity_MWh'].min()),
        max_value=float(df['Capacity_MWh'].max()),
        value=(float(df['Capacity_MWh'].min()), float(df['Capacity_MWh'].max())),
        step=0.1
    )
    
    # Bundesland filter
    st.sidebar.markdown("### Bundesland")
    bundesland_options = ['All'] + list(df['Bundesland'].unique())
    selected_bundesland = st.sidebar.selectbox("Bundesland", bundesland_options)
    
    # Owner filter
    st.sidebar.markdown("### Owner")
    owner_options = ['All'] + list(df['AnlagenbetreiberName'].unique())
    selected_owner = st.sidebar.selectbox("Owner", owner_options)
    
    # Apply filters
    df_filtered = df.copy()
    
    if selected_status != 'All':
        df_filtered = df_filtered[df_filtered['BetriebsStatusName'] == selected_status]
    
    df_filtered = df_filtered[
        (df_filtered['Power_MW'] >= power_min) & 
        (df_filtered['Power_MW'] <= power_max)
    ]
    
    df_filtered = df_filtered[
        (df_filtered['Capacity_MWh'] >= capacity_min) & 
        (df_filtered['Capacity_MWh'] <= capacity_max)
    ]
    
    if selected_bundesland != 'All':
        df_filtered = df_filtered[df_filtered['Bundesland'] == selected_bundesland]
    
    if selected_owner != 'All':
        df_filtered = df_filtered[df_filtered['AnlagenbetreiberName'] == selected_owner]
    
    # Display filtered count
    st.sidebar.markdown(f"### 📊 Results")
    st.sidebar.markdown(f"**{len(df_filtered)}** batteries found")
    
    # Main content
    if len(df_filtered) == 0:
        st.warning("No batteries match the selected filters. Try adjusting your criteria.")
        return
    
    # Summary statistics
    st.markdown("## 📊 Summary Statistics")
    stats = create_summary_stats(df_filtered)
    
    # Display metrics in columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Units", f"{stats['Total Units']:,}")
    
    with col2:
        st.metric("Total Power", f"{stats['Total Power (MW)']:,.1f} MW")
    
    with col3:
        st.metric("Total Capacity", f"{stats['Total Capacity (MWh)']:,.1f} MWh")
    
    with col4:
        st.metric("Average Power", f"{stats['Average Power (MW)']:.1f} MW")
    
    # Interactive map
    st.markdown("## 📍 Interactive Map")
    map_fig = create_map(df_filtered)
    if map_fig:
        st.plotly_chart(map_fig, use_container_width=True)
    
    # Charts
    st.markdown("## 📈 Analytics")
    charts = create_charts(df_filtered)
    
    if charts:
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(charts['status'], use_container_width=True)
        
        with col2:
            st.plotly_chart(charts['technology'], use_container_width=True)
        
        st.plotly_chart(charts['bundesland'], use_container_width=True)
    
    # Detailed data table
    st.markdown("## 📋 Detailed Data")
    
    # Select columns to display
    display_columns = [
        'EinheitName', 'AnlagenbetreiberName', 'BetriebsStatusName', 
        'Power_MW', 'Capacity_MWh', 'Bundesland', 'Gemeinde', 'Batterietechnologie'
    ]
    
    # Filter and display data
    display_df = df_filtered[display_columns].copy()
    display_df['Power_MW'] = display_df['Power_MW'].round(2)
    display_df['Capacity_MWh'] = display_df['Capacity_MWh'].round(2)
    
    st.dataframe(
        display_df,
        use_container_width=True,
        column_config={
            "Power_MW": st.column_config.NumberColumn("Power (MW)", format="%.2f"),
            "Capacity_MWh": st.column_config.NumberColumn("Capacity (MWh)", format="%.2f")
        }
    )
    
    # Footer
    st.markdown("---")
    st.markdown(
        "Data source: [MaStR (Marktstammdatenregister)](https://www.marktstammdatenregister.de) | "
        "Last updated: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

if __name__ == "__main__":
    main() 