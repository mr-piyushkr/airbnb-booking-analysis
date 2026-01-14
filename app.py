import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

# Page config
st.set_page_config(page_title="Airbnb NYC Analysis", layout="wide", page_icon="🏙️")

# Enhanced CSS styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }
    
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(120deg, #FF5A5F 0%, #FF385C 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    .sub-header {
        font-size: 1.1rem;
        color: #717171;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 3rem;
        padding: 0 2rem;
        font-weight: 600;
    }
    
    section[data-testid="stSidebar"] {
        background-color: #2b2b2b;
    }
    
    section[data-testid="stSidebar"] * {
        color: #ffffff !important;
    }
    
    section[data-testid="stSidebar"] .stMarkdown {
        color: #ffffff !important;
    }
    
    .insight-box {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .stPlotlyChart {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("data/Airbnb NYC 2019.csv")
    df = df.dropna(subset=['price', 'neighbourhood_group', 'room_type'])
    df = df[df['price'] > 0]
    return df

df = load_data()

# Header
st.markdown('<p class="main-header">🏙️ Airbnb NYC Analytics Dashboard</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Discover pricing insights and booking trends across New York City neighborhoods</p>', unsafe_allow_html=True)

# Sidebar
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/6/69/Airbnb_Logo_B%C3%A9lo.svg/2560px-Airbnb_Logo_B%C3%A9lo.svg.png", width=150)
st.sidebar.markdown("### 🎯 Filter Your Data")

boroughs = ['All'] + sorted(df['neighbourhood_group'].unique().tolist())
selected_borough = st.sidebar.multiselect("🏙️ Borough", boroughs, default=['All'])

room_types = ['All'] + sorted(df['room_type'].unique().tolist())
selected_room_type = st.sidebar.multiselect("🏠 Room Type", room_types, default=['All'])

min_price = int(df['price'].min())
max_price = int(df['price'].quantile(0.95))
price_range = st.sidebar.slider("💵 Price Range ($)", min_price, max_price, (min_price, max_price))

# Apply filters
filtered_df = df.copy()
if 'All' not in selected_borough and len(selected_borough) > 0:
    filtered_df = filtered_df[filtered_df['neighbourhood_group'].isin(selected_borough)]
if 'All' not in selected_room_type and len(selected_room_type) > 0:
    filtered_df = filtered_df[filtered_df['room_type'].isin(selected_room_type)]
filtered_df = filtered_df[(filtered_df['price'] >= price_range[0]) & (filtered_df['price'] <= price_range[1])]

# Metrics
st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Quick Stats")
col_m1, col_m2 = st.sidebar.columns(2)
col_m1.metric("📍 Listings", f"{len(filtered_df):,}")
col_m2.metric("💰 Avg Price", f"${filtered_df['price'].mean():.0f}")
col_m3, col_m4 = st.sidebar.columns(2)
col_m3.metric("📉 Min Price", f"${filtered_df['price'].min():.0f}")
col_m4.metric("📈 Max Price", f"${filtered_df['price'].max():.0f}")

# Key Insights at top
st.markdown("### 💡 Key Insights")
col_i1, col_i2, col_i3, col_i4 = st.columns(4)

with col_i1:
    most_expensive = filtered_df.groupby('neighbourhood_group')['price'].mean().idxmax()
    st.markdown(f"""
    <div class="metric-card" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
        <div class="metric-label">Most Expensive</div>
        <div class="metric-value">{most_expensive}</div>
    </div>
    """, unsafe_allow_html=True)

with col_i2:
    most_affordable = filtered_df.groupby('neighbourhood_group')['price'].mean().idxmin()
    st.markdown(f"""
    <div class="metric-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
        <div class="metric-label">Most Affordable</div>
        <div class="metric-value">{most_affordable}</div>
    </div>
    """, unsafe_allow_html=True)

with col_i3:
    popular_room = filtered_df['room_type'].mode()[0]
    st.markdown(f"""
    <div class="metric-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
        <div class="metric-label">Popular Room</div>
        <div class="metric-value">{popular_room}</div>
    </div>
    """, unsafe_allow_html=True)

with col_i4:
    avg_reviews = filtered_df['number_of_reviews'].mean()
    st.markdown(f"""
    <div class="metric-card" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);">
        <div class="metric-label">Avg Reviews</div>
        <div class="metric-value">{avg_reviews:.0f}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📊 Price Analysis", "🗺️ Geographic Insights", "🔗 Correlations", "📈 Advanced Analytics"])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 💰 Average Price by Borough")
        avg_borough = filtered_df.groupby('neighbourhood_group')['price'].mean().sort_values(ascending=False).reset_index()
        fig1 = px.bar(avg_borough, x='neighbourhood_group', y='price', 
                     color='price', color_continuous_scale='Viridis',
                     labels={'neighbourhood_group': 'Borough', 'price': 'Average Price ($)'},
                     text='price')
        fig1.update_traces(texttemplate='$%{text:.2f}', textposition='outside')
        fig1.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        st.markdown("#### 🏠 Average Price by Room Type")
        avg_room = filtered_df.groupby('room_type')['price'].mean().sort_values(ascending=False).reset_index()
        fig2 = px.bar(avg_room, x='room_type', y='price',
                     color='price', color_continuous_scale='Plasma',
                     labels={'room_type': 'Room Type', 'price': 'Average Price ($)'},
                     text='price')
        fig2.update_traces(texttemplate='$%{text:.2f}', textposition='outside')
        fig2.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig2, use_container_width=True)
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("#### 📈 Price Distribution")
        fig3 = px.histogram(filtered_df, x='price', nbins=50,
                           labels={'price': 'Price ($)', 'count': 'Frequency'},
                           color_discrete_sequence=['#FF5A5F'])
        fig3.add_vline(x=filtered_df['price'].mean(), line_dash="dash", 
                      line_color="blue", annotation_text=f"Mean: ${filtered_df['price'].mean():.2f}")
        fig3.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig3, use_container_width=True)
    
    with col4:
        st.markdown("#### 📅 Price vs Availability")
        fig4 = px.scatter(filtered_df, x='availability_365', y='price',
                         color='neighbourhood_group', opacity=0.5,
                         labels={'availability_365': 'Availability (days/year)', 'price': 'Price ($)'},
                         color_discrete_sequence=px.colors.qualitative.Bold)
        fig4.update_layout(height=400)
        st.plotly_chart(fig4, use_container_width=True)

with tab2:
    st.markdown("#### 🗺️ Airbnb Listings Across NYC")
    
    map_df = filtered_df[['latitude', 'longitude', 'price', 'neighbourhood_group', 'room_type']].dropna()
    
    fig_map = px.scatter_mapbox(map_df, lat='latitude', lon='longitude',
                                color='neighbourhood_group', size='price',
                                hover_data={'price': True, 'room_type': True},
                                zoom=9.5, height=500,
                                color_discrete_sequence=px.colors.qualitative.Bold)
    fig_map.update_layout(mapbox_style="carto-positron", margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig_map, use_container_width=True)
    
    col5, col6 = st.columns(2)
    
    with col5:
        st.markdown("#### 🏘️ Top 10 Most Expensive Neighborhoods")
        top_neighborhoods = filtered_df.groupby('neighbourhood')['price'].mean().sort_values(ascending=False).head(10).reset_index()
        fig5 = px.bar(top_neighborhoods, y='neighbourhood', x='price', orientation='h',
                     color='price', color_continuous_scale='Reds',
                     labels={'neighbourhood': 'Neighborhood', 'price': 'Average Price ($)'},
                     text='price')
        fig5.update_traces(texttemplate='$%{text:.2f}', textposition='outside')
        fig5.update_layout(showlegend=False, height=450)
        st.plotly_chart(fig5, use_container_width=True)
    
    with col6:
        st.markdown("#### 🏘️ Top 10 Most Affordable Neighborhoods")
        bottom_neighborhoods = filtered_df.groupby('neighbourhood')['price'].mean().sort_values().head(10).reset_index()
        fig6 = px.bar(bottom_neighborhoods, y='neighbourhood', x='price', orientation='h',
                     color='price', color_continuous_scale='Greens',
                     labels={'neighbourhood': 'Neighborhood', 'price': 'Average Price ($)'},
                     text='price')
        fig6.update_traces(texttemplate='$%{text:.2f}', textposition='outside')
        fig6.update_layout(showlegend=False, height=450)
        st.plotly_chart(fig6, use_container_width=True)

with tab3:
    col7, col8 = st.columns([3, 2])
    
    with col7:
        st.markdown("#### 🔗 Feature Correlation Matrix")
        numeric_cols = filtered_df.select_dtypes(include=['float64', 'int64']).columns
        corr = filtered_df[numeric_cols].corr()
        
        fig7 = px.imshow(corr, text_auto='.2f', aspect='auto',
                        color_continuous_scale='RdBu_r', zmin=-1, zmax=1)
        fig7.update_layout(height=500)
        st.plotly_chart(fig7, use_container_width=True)
    
    with col8:
        st.markdown("#### 📊 Statistical Summary")
        st.dataframe(filtered_df[['price', 'number_of_reviews', 'availability_365', 'reviews_per_month']].describe().round(2),
                    use_container_width=True, height=500)

with tab4:
    col9, col10 = st.columns(2)
    
    with col9:
        st.markdown("#### 🎯 Listings Count by Borough")
        borough_count = filtered_df['neighbourhood_group'].value_counts().reset_index()
        borough_count.columns = ['Borough', 'Count']
        fig8 = px.pie(borough_count, values='Count', names='Borough', hole=0.4,
                     color_discrete_sequence=px.colors.qualitative.Set3)
        fig8.update_traces(textposition='inside', textinfo='percent+label')
        fig8.update_layout(height=400)
        st.plotly_chart(fig8, use_container_width=True)
    
    with col10:
        st.markdown("#### 🏠 Room Type Distribution")
        room_count = filtered_df['room_type'].value_counts().reset_index()
        room_count.columns = ['Room Type', 'Count']
        fig9 = px.pie(room_count, values='Count', names='Room Type', hole=0.4,
                     color_discrete_sequence=px.colors.qualitative.Pastel)
        fig9.update_traces(textposition='inside', textinfo='percent+label')
        fig9.update_layout(height=400)
        st.plotly_chart(fig9, use_container_width=True)
    
    st.markdown("#### 📊 Price Range Analysis by Borough and Room Type")
    fig10 = px.box(filtered_df, x='neighbourhood_group', y='price', color='room_type',
                  labels={'neighbourhood_group': 'Borough', 'price': 'Price ($)', 'room_type': 'Room Type'},
                  color_discrete_sequence=px.colors.qualitative.Bold)
    fig10.update_layout(height=450)
    st.plotly_chart(fig10, use_container_width=True)
    
    st.markdown("#### 🔥 Reviews vs Price Analysis")
    fig11 = px.scatter(filtered_df, x='number_of_reviews', y='price',
                      color='neighbourhood_group', size='availability_365',
                      hover_data=['room_type'],
                      labels={'number_of_reviews': 'Number of Reviews', 'price': 'Price ($)'},
                      color_discrete_sequence=px.colors.qualitative.Bold)
    fig11.update_layout(height=450)
    st.plotly_chart(fig11, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #717171; padding: 2rem 0;'>
        <p style='font-size: 0.9rem;'>📊 <b>Data Source:</b> Airbnb NYC 2019 Dataset</p>
        <p style='font-size: 0.9rem;'>🚀 Built with <b>Streamlit</b> • <b>Plotly</b> • <b>Python</b></p>
        <p style='font-size: 0.8rem; margin-top: 1rem;'>© 2024 Airbnb Analytics Dashboard</p>
    </div>
""", unsafe_allow_html=True)
