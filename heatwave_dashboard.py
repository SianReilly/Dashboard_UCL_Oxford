import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Set page config
st.set_page_config(page_title="UK Heatwave Projections", layout="wide")

# Remove whitespace and branding
st.markdown("""
<style>
header.stAppHeader {
    background-color: transparent;
}
section.stMain .block-container {
    padding-top: 0rem;
    z-index: 1;
}
</style>""", unsafe_allow_html=True)

hide_streamlit_style = """
                <style>
                div[data-testid="stToolbar"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                div[data-testid="stDecoration"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                div[data-testid="stStatusWidget"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                #MainMenu {
                visibility: hidden;
                height: 0%;
                }
                header {
                visibility: hidden;
                height: 0%;
                }
                footer {
                visibility: hidden;
                height: 0%;
                }
                </style>
                """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Custom CSS - Hot/Fire theme
st.markdown(
    """
    <style>
        .stApp {
            background: linear-gradient(135deg, #1a0000 0%, #330000 50%, #4d0000 100%);
            color: white;
        }
        div.stMultiSelect label, div.stSelectbox label, div.stSlider label {
            color: white !important;
        }
        div[data-baseweb="tag"] {
            background-color: #ff4500 !important;
            color: white !important;
        }
        /* Slider styling */
        div[data-baseweb="slider"] [role="slider"] {
            background-color: #ff4500 !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('Annual_Count_of_Hot_Days___Projections__12km_grid__-7336973101011391426.csv', 
                     encoding='utf-8-sig')
    return df

try:
    df = load_data()
    
    # Title
    st.markdown("<h1 style='text-align: center; color: #ff6b35;'>🔥 UK Hot Summer Days Projections 🔥</h1>", unsafe_allow_html=True)
    
    st.markdown(
        """
        <p style='text-align: center; color: white; font-size: 24px;'>
        by Siân Reilly
        </p>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown(
        """
        <p style='text-align: center; color: white; font-size: 18px; max-width: 1000px; margin: 0 auto; line-height: 1.6;'>
        Analysis of projected annual hot summer days across the UK under different global warming scenarios. 
        Data from the Met Office shows how climate change will dramatically increase the frequency of extremely hot days, 
        with projections ranging from 1.5°C to 4°C of global warming above pre-industrial levels.
        </p>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Data overview
    st.markdown("### 📊 Dataset Overview")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Grid Points", f"{len(df):,}")
    with col2:
        st.metric("Lat Range", f"{df['Latitude'].min():.1f}° to {df['Latitude'].max():.1f}°")
    with col3:
        st.metric("Long Range", f"{df['Longitude'].min():.1f}° to {df['Longitude'].max():.1f}°")
    with col4:
        st.metric("Warming Scenarios", "5 (1.5°C to 4°C)")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Interactive Filters
    st.markdown("### 🎛️ Filter Data")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        warming_scenario = st.selectbox(
            "Select Warming Scenario",
            ['1.5°C', '2°C', '2.5°C', '3°C', '4°C'],
            index=2
        )
    
    with col2:
        confidence_level = st.selectbox(
            "Confidence Level",
            ['lower', 'median', 'upper'],
            index=1
        )
    
    with col3:
        baseline = st.selectbox(
            "Baseline Period",
            ['1981-2000', '2001-2020'],
            index=0
        )
    
    # Create column names based on selections
    scenario_col = f'HSD {warming_scenario} {confidence_level}'
    baseline_col = f'HSD baseline {baseline} {confidence_level}'
    
    # Calculate change
    df['change'] = df[scenario_col] - df[baseline_col]
    df['change_pct'] = ((df[scenario_col] - df[baseline_col]) / (df[baseline_col] + 0.001)) * 100
    
    # Calculate statistics
    current_avg = df[baseline_col].mean()
    future_avg = df[scenario_col].mean()
    increase = future_avg - current_avg
    increase_pct = (increase / (current_avg + 0.001)) * 100
    
    # Display key metrics
    st.markdown("### 🔥 Key Projections")
    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
    
    with metric_col1:
        st.markdown(f"""
            <div style='text-align: center; padding: 20px; background-color: rgba(255, 107, 53, 0.2); border-radius: 10px; border: 2px solid #ff6b35;'>
                <h2 style='color: #ff6b35; margin: 0;'>{current_avg:.1f}</h2>
                <p style='color: white; margin: 5px 0; font-size: 14px;'>Baseline Hot Days/Year</p>
                <p style='color: #ffaa80; font-size: 11px;'>({baseline})</p>
            </div>
        """, unsafe_allow_html=True)
    
    with metric_col2:
        st.markdown(f"""
            <div style='text-align: center; padding: 20px; background-color: rgba(255, 69, 0, 0.3); border-radius: 10px; border: 2px solid #ff4500;'>
                <h2 style='color: #ff4500; margin: 0;'>{future_avg:.1f}</h2>
                <p style='color: white; margin: 5px 0; font-size: 14px;'>Projected Hot Days/Year</p>
                <p style='color: #ff9966; font-size: 11px;'>({warming_scenario} warming)</p>
            </div>
        """, unsafe_allow_html=True)
    
    with metric_col3:
        st.markdown(f"""
            <div style='text-align: center; padding: 20px; background-color: rgba(220, 20, 60, 0.3); border-radius: 10px; border: 2px solid #dc143c;'>
                <h2 style='color: #dc143c; margin: 0;'>+{increase:.1f}</h2>
                <p style='color: white; margin: 5px 0; font-size: 14px;'>Increase in Hot Days</p>
                <p style='color: #ff6b9d; font-size: 11px;'>Absolute Change</p>
            </div>
        """, unsafe_allow_html=True)
    
    with metric_col4:
        st.markdown(f"""
            <div style='text-align: center; padding: 20px; background-color: rgba(178, 34, 34, 0.3); border-radius: 10px; border: 2px solid #b22222;'>
                <h2 style='color: #ff6347; margin: 0;'>+{increase_pct:.0f}%</h2>
                <p style='color: white; margin: 5px 0; font-size: 14px;'>Percentage Increase</p>
                <p style='color: #ff9999; font-size: 11px;'>Relative Change</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # ============ MAP 1: Current Projected Hot Days ============
    fig_map1 = px.scatter_mapbox(
        df,
        lat='Latitude',
        lon='Longitude',
        color=scenario_col,
        size=scenario_col,
        color_continuous_scale='Hot',
        mapbox_style='carto-darkmatter',
        zoom=4.5,
        center={'lat': 54, 'lon': -2},
        title=f'<b>Projected Hot Days: {warming_scenario} Warming ({confidence_level})</b>',
        hover_data={
            'Latitude': ':.2f',
            'Longitude': ':.2f',
            scenario_col: ':.1f',
            baseline_col: ':.1f'
        },
        height=550
    )
    
    fig_map1.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', size=12),
        title_x=0.5,
        title_font=dict(size=16, color='white'),
        coloraxis_colorbar=dict(
            title='Hot Days/Year',
            tickfont=dict(color='white'),
            titlefont=dict(color='white')
        ),
        margin=dict(l=0, r=0, t=40, b=0)
    )
    
    # ============ MAP 2: Baseline (Historical) Hot Days ============
    fig_map2 = px.scatter_mapbox(
        df,
        lat='Latitude',
        lon='Longitude',
        color=baseline_col,
        size=baseline_col,
        color_continuous_scale='Blues',
        mapbox_style='carto-darkmatter',
        zoom=4.5,
        center={'lat': 54, 'lon': -2},
        title=f'<b>Baseline Hot Days: {baseline}</b>',
        hover_data={
            'Latitude': ':.2f',
            'Longitude': ':.2f',
            baseline_col: ':.1f'
        },
        height=550
    )
    
    fig_map2.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', size=12),
        title_x=0.5,
        title_font=dict(size=16, color='white'),
        coloraxis_colorbar=dict(
            title='Hot Days/Year',
            tickfont=dict(color='white'),
            titlefont=dict(color='white')
        ),
        margin=dict(l=0, r=0, t=40, b=0)
    )
    
    # ============ MAP 3: Change Map (Difference) ============
    fig_map3 = px.scatter_mapbox(
        df,
        lat='Latitude',
        lon='Longitude',
        color='change',
        size=abs(df['change']) + 0.1,
        color_continuous_scale='RdYlBu_r',
        mapbox_style='carto-darkmatter',
        zoom=4.5,
        center={'lat': 54, 'lon': -2},
        title=f'<b>Increase in Hot Days: {warming_scenario} vs Baseline</b>',
        hover_data={
            'Latitude': ':.2f',
            'Longitude': ':.2f',
            'change': ':.1f',
            scenario_col: ':.1f',
            baseline_col: ':.1f'
        },
        height=550
    )
    
    fig_map3.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', size=12),
        title_x=0.5,
        title_font=dict(size=16, color='white'),
        coloraxis_colorbar=dict(
            title='Change (days/year)',
            tickfont=dict(color='white'),
            titlefont=dict(color='white')
        ),
        margin=dict(l=0, r=0, t=40, b=0)
    )
    
    # ============ MAP 4: Density Heatmap ============
    fig_map4 = px.density_mapbox(
        df,
        lat='Latitude',
        lon='Longitude',
        z=scenario_col,
        radius=15,
        mapbox_style='carto-darkmatter',
        zoom=4.5,
        center={'lat': 54, 'lon': -2},
        title=f'<b>Heat Intensity Map: {warming_scenario} Warming</b>',
        color_continuous_scale='Hot',
        height=550
    )
    
    fig_map4.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', size=12),
        title_x=0.5,
        title_font=dict(size=16, color='white'),
        coloraxis_colorbar=dict(
            title='Hot Days/Year',
            tickfont=dict(color='white'),
            titlefont=dict(color='white')
        ),
        margin=dict(l=0, r=0, t=40, b=0)
    )
    
    # ============ MAP 5: Percentage Change Map ============
    # Filter out extreme outliers for better visualization
    df_filtered = df[df['change_pct'] < 1000].copy()
    
    fig_map5 = px.scatter_mapbox(
        df_filtered,
        lat='Latitude',
        lon='Longitude',
        color='change_pct',
        size=abs(df_filtered['change_pct']) + 1,
        color_continuous_scale='Plasma',
        mapbox_style='carto-darkmatter',
        zoom=4.5,
        center={'lat': 54, 'lon': -2},
        title=f'<b>Percentage Increase in Hot Days</b>',
        hover_data={
            'Latitude': ':.2f',
            'Longitude': ':.2f',
            'change_pct': ':.0f',
            scenario_col: ':.1f',
            baseline_col: ':.1f'
        },
        height=550
    )
    
    fig_map5.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', size=12),
        title_x=0.5,
        title_font=dict(size=16, color='white'),
        coloraxis_colorbar=dict(
            title='% Increase',
            tickfont=dict(color='white'),
            titlefont=dict(color='white')
        ),
        margin=dict(l=0, r=0, t=40, b=0)
    )
    
    # ============ CHART: Comparison Across Warming Scenarios ============
    warming_scenarios = ['1.5°C', '2°C', '2.5°C', '3°C', '4°C']
    scenario_data = []
    
    for scenario in warming_scenarios:
        col_name = f'HSD {scenario} {confidence_level}'
        scenario_data.append({
            'Scenario': scenario,
            'Average Hot Days': df[col_name].mean(),
            'Maximum': df[col_name].max(),
            'Minimum': df[col_name].min()
        })
    
    scenario_df = pd.DataFrame(scenario_data)
    
    fig_bar = go.Figure()
    
    fig_bar.add_trace(go.Bar(
        name='Average',
        x=scenario_df['Scenario'],
        y=scenario_df['Average Hot Days'],
        marker_color='#ff6b35',
        text=scenario_df['Average Hot Days'].round(1),
        textposition='outside',
        textfont=dict(color='white', size=13)
    ))
    
    fig_bar.add_trace(go.Scatter(
        name='Maximum',
        x=scenario_df['Scenario'],
        y=scenario_df['Maximum'],
        mode='lines+markers',
        line=dict(color='#dc143c', width=3),
        marker=dict(size=10)
    ))
    
    fig_bar.add_trace(go.Scatter(
        name='Minimum',
        x=scenario_df['Scenario'],
        y=scenario_df['Minimum'],
        mode='lines+markers',
        line=dict(color='#ff9966', width=3),
        marker=dict(size=10)
    ))
    
    fig_bar.update_layout(
        title='<b>Hot Days Across Warming Scenarios</b>',
        title_x=0.5,
        title_font=dict(size=16, color='white'),
        xaxis_title='Warming Scenario',
        yaxis_title='Hot Days per Year',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', size=12),
        height=550,
        xaxis=dict(
            gridcolor='rgba(255,255,255,0.1)',
            tickfont=dict(color='white')
        ),
        yaxis=dict(
            gridcolor='rgba(255,255,255,0.1)',
            tickfont=dict(color='white')
        ),
        legend=dict(font=dict(color='white')),
        margin=dict(l=50, r=20, t=50, b=50)
    )
    
    # ============ CHART: Regional Breakdown ============
    # Create regions
    regions_data = []
    regions = {
        'Scotland': (df['Latitude'] >= 55),
        'Northern England': (df['Latitude'] >= 53) & (df['Latitude'] < 55),
        'Midlands': (df['Latitude'] >= 52) & (df['Latitude'] < 53),
        'Southern England': (df['Latitude'] < 52)
    }
    
    for region_name, mask in regions.items():
        region_df = df[mask]
        regions_data.append({
            'Region': region_name,
            'Baseline': region_df[baseline_col].mean(),
            'Projected': region_df[scenario_col].mean(),
            'Change': region_df['change'].mean()
        })
    
    regions_df = pd.DataFrame(regions_data)
    
    fig_regions = go.Figure()
    
    fig_regions.add_trace(go.Bar(
        name='Baseline',
        x=regions_df['Region'],
        y=regions_df['Baseline'],
        marker_color='#4169e1',
        text=regions_df['Baseline'].round(1),
        textposition='outside',
        textfont=dict(color='white', size=12)
    ))
    
    fig_regions.add_trace(go.Bar(
        name='Projected',
        x=regions_df['Region'],
        y=regions_df['Projected'],
        marker_color='#ff4500',
        text=regions_df['Projected'].round(1),
        textposition='outside',
        textfont=dict(color='white', size=12)
    ))
    
    fig_regions.update_layout(
        title=f'<b>Regional Breakdown: {warming_scenario} Warming</b>',
        title_x=0.5,
        title_font=dict(size=16, color='white'),
        xaxis_title='Region',
        yaxis_title='Hot Days per Year',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', size=12),
        height=550,
        barmode='group',
        xaxis=dict(
            tickfont=dict(color='white'),
            showgrid=False
        ),
        yaxis=dict(
            gridcolor='rgba(255,255,255,0.1)',
            tickfont=dict(color='white')
        ),
        legend=dict(font=dict(color='white')),
        margin=dict(l=50, r=20, t=50, b=50)
    )
    
    # ============ Display Section 1: Side-by-Side Comparison Maps ============
    st.markdown("### 🗺️ Geographic Comparison: Baseline vs Future")
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(fig_map2, use_container_width=True)
        st.markdown("""
            <p style='color: white; font-size: 14px; line-height: 1.6; padding: 10px; background-color: rgba(0,0,0,0.3); border-radius: 5px;'>
            <b>Historical Context:</b> The baseline map (blue scale) shows historical hot days were relatively rare across most of the UK, 
            with very few regions experiencing significant numbers. Notice the cooler colors dominating the map—
            this is what "normal" used to look like.
            </p>
        """, unsafe_allow_html=True)
    
    with col2:
        st.plotly_chart(fig_map1, use_container_width=True)
        st.markdown("""
            <p style='color: white; font-size: 14px; line-height: 1.6; padding: 10px; background-color: rgba(0,0,0,0.3); border-radius: 5px;'>
            <b>Future Projections:</b> Under warming scenarios, the transformation is dramatic. The red-orange "hot" scale 
            reveals significant increases across all regions, with southern areas showing the most intense changes. 
            Compare bubble sizes to see the exponential increase in hot day frequency.
            </p>
        """, unsafe_allow_html=True)
    
    # ============ Display Section 2: Change & Intensity Maps ============
    st.markdown("### 🔥 Change Analysis: Where Heat Will Increase Most")
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(fig_map3, use_container_width=True)
        st.markdown("""
            <p style='color: white; font-size: 14px; line-height: 1.6; padding: 10px; background-color: rgba(0,0,0,0.3); border-radius: 5px;'>
            <b>Absolute Change:</b> This difference map shows the raw increase in hot days per year. Red areas indicate 
            the largest absolute increases—some regions could see 10+ additional extremely hot days per year. 
            Southern England faces the most severe changes, while Scotland shows more moderate increases.
            </p>
        """, unsafe_allow_html=True)
    
    with col2:
        st.plotly_chart(fig_map4, use_container_width=True)
        st.markdown("""
            <p style='color: white; font-size: 14px; line-height: 1.6; padding: 10px; background-color: rgba(0,0,0,0.3); border-radius: 5px;'>
            <b>Heat Intensity Zones:</b> The density heatmap reveals geographic clustering of extreme heat. 
            Bright red zones indicate areas where multiple grid points show very high values—these are the future 
            "heat islands" where infrastructure, health services, and cooling systems will face maximum stress.
            </p>
        """, unsafe_allow_html=True)
    
    # ============ Display Section 3: Statistical Analysis ============
    st.markdown("### 📊 Statistical Analysis & Regional Patterns")
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(fig_map5, use_container_width=True)
        st.markdown("""
            <p style='color: white; font-size: 14px; line-height: 1.6; padding: 10px; background-color: rgba(0,0,0,0.3); border-radius: 5px;'>
            <b>Relative Change:</b> Percentage increases tell a different story than absolute numbers. Areas starting 
            from near-zero baselines show dramatic percentage jumps (purple/yellow zones). While southern regions 
            have higher absolute values, northern areas may experience greater relative disruption to established norms.
            </p>
        """, unsafe_allow_html=True)
    
    with col2:
        st.plotly_chart(fig_bar, use_container_width=True)
        st.markdown("""
            <p style='color: white; font-size: 14px; line-height: 1.6; padding: 10px; background-color: rgba(0,0,0,0.3); border-radius: 5px;'>
            <b>Non-Linear Escalation:</b> The relationship between warming and hot days accelerates dramatically. 
            The gap between 3°C and 4°C scenarios is far larger than 1.5°C to 2°C—demonstrating that every fraction 
            of a degree matters immensely. Maximum values (red line) reach extreme levels under 4°C warming.
            </p>
        """, unsafe_allow_html=True)
    
    # ============ Display Section 4: Regional Breakdown ============
    st.markdown("### 🏴󠁧󠁢󠁥󠁮󠁧󠁿 Regional Impact Analysis")
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.plotly_chart(fig_regions, use_container_width=True)
    
    with col2:
        st.markdown("""
            <div style='padding: 20px; background-color: rgba(0,0,0,0.3); border-radius: 10px; border-left: 4px solid #ff6b35;'>
            <h4 style='color: #ff6b35; margin-top: 0;'>Key Regional Insights</h4>
            <p style='color: white; font-size: 14px; line-height: 1.8;'>
            <b>Scotland:</b> Starting from the lowest baseline, Scotland faces dramatic relative changes. 
            Infrastructure and ecosystems adapted to cool climates will face unprecedented heat stress.<br><br>
            
            <b>Northern England:</b> Shows moderate absolute increases but significant relative change. 
            Urban areas like Manchester and Leeds will need substantial adaptation measures.<br><br>
            
            <b>Midlands:</b> The transition zone experiences both absolute and relative increases. 
            Critical transport and industrial infrastructure concentrated here faces compounding heat risks.<br><br>
            
            <b>Southern England:</b> Already experiencing the most hot days in baseline period, this region 
            faces the highest absolute increases. London and southeastern cities will require comprehensive 
            cooling strategies and public health interventions.
            </p>
            </div>
        """, unsafe_allow_html=True)
    
    # Data table
    st.markdown("### 📋 Raw Data Sample")
    display_cols = ['Latitude', 'Longitude', baseline_col, scenario_col, 'change', 'change_pct']
    st.dataframe(
        df[display_cols].head(30).style.background_gradient(cmap='Reds', subset=[scenario_col]),
        use_container_width=True
    )
    
    # Summary statistics
    st.markdown("### 📈 Summary Statistics")
    stats_col1, stats_col2, stats_col3 = st.columns(3)
    
    with stats_col1:
        st.markdown(f"""
            <div style='padding: 15px; background-color: rgba(255, 107, 53, 0.2); border-radius: 8px; border: 2px solid #ff6b35;'>
                <h4 style='color: #ff6b35; margin: 0;'>Most Affected Area</h4>
                <p style='color: white; margin: 10px 0 5px 0; font-size: 20px;'>{df.loc[df[scenario_col].idxmax(), 'Latitude']:.2f}°N, {df.loc[df[scenario_col].idxmax(), 'Longitude']:.2f}°W</p>
                <p style='color: #ffaa80; font-size: 14px; margin: 0;'>{df[scenario_col].max():.1f} hot days/year projected</p>
            </div>
        """, unsafe_allow_html=True)
    
    with stats_col2:
        st.markdown(f"""
            <div style='padding: 15px; background-color: rgba(255, 69, 0, 0.2); border-radius: 8px; border: 2px solid #ff4500;'>
                <h4 style='color: #ff4500; margin: 0;'>Largest Increase</h4>
                <p style='color: white; margin: 10px 0 5px 0; font-size: 20px;'>{df.loc[df['change'].idxmax(), 'Latitude']:.2f}°N, {df.loc[df['change'].idxmax(), 'Longitude']:.2f}°W</p>
                <p style='color: #ff9966; font-size: 14px; margin: 0;'>+{df['change'].max():.1f} days/year increase</p>
            </div>
        """, unsafe_allow_html=True)
    
    with stats_col3:
        median_change = df['change'].median()
        st.markdown(f"""
            <div style='padding: 15px; background-color: rgba(220, 20, 60, 0.2); border-radius: 8px; border: 2px solid #dc143c;'>
                <h4 style='color: #dc143c; margin: 0;'>Median UK Change</h4>
                <p style='color: white; margin: 10px 0 5px 0; font-size: 20px;'>+{median_change:.1f} days/year</p>
                <p style='color: #ff6b9d; font-size: 14px; margin: 0;'>Typical increase across UK</p>
            </div>
        """, unsafe_allow_html=True)
    
    # Footer
    st.markdown(
        """
        <style>
            .footer {
                position: static;
                bottom: 0;
                left: 0;
                width: 100%;
                text-align: center;
                font-size: 14px;
                color: rgba(255, 255, 255, 0.6);
                background: linear-gradient(135deg, #1a0000 0%, #330000 100%);
                padding: 20px 0;
                margin-top: 40px;
                border-top: 2px solid rgba(255, 107, 53, 0.3);
            }
        </style>
        <div class="footer">
            © 2025 UK Heatwave Projections Dashboard | Data Source: Met Office Climate Data Portal<br>
            <a href="https://climatedataportal.metoffice.gov.uk" style="color: #ff6b35; text-decoration: none;">Visit Met Office Climate Portal</a> | 
            Analysis following Edward Tufte's visualization principles
        </div>
        """,
        unsafe_allow_html=True
    )

except FileNotFoundError:
    st.error("❌ CSV file not found! Make sure 'Annual_Count_of_Hot_Days___Projections__12km_grid__-7336973101011391426.csv' is in the same directory as this script.")
    st.info("💡 Make sure your CSV file is uploaded to GitHub in the same directory as this Python file.")
except Exception as e:
    st.error(f"❌ Error loading data: {str(e)}")
    st.info("Check the Streamlit Cloud logs for more details about what went wrong.")
