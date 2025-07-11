import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import re

# Load and Clean the Data
# @st.cache  # This function will be cached
# def load_and_clean_data():
#     # Load
#     data = pd.read_csv('/pier_data_project_July/day_approach_maskedID_timeseries.csv')
    
    
#     return data

# Load your data
df = pd.read_csv('day_approach_maskedID_timeseries.csv')

# Streamlit App
# st.title("Salary Estimates vs. Company Rating by Job Title")
st.markdown('<h1 style="font-size: 24px;">Injury Prediction for Competitive Runners</h1>', unsafe_allow_html=True)

# Crea categorie per km_tot (esempio: 0-5km, 5-10km, etc.)
# data['total km'] = pd.cut(data['total km'], 
#                                 bins=[0, 5, 10, 15, 20, float('inf')], 
#                                 labels=['0-5km', '5-10km', '10-15km', '15-20km', '20+km'])

# km_counts = data['total km'].value_counts().reset_index()
# km_counts.columns = ['km_category', 'count']

# data['km Z3-4'] = pd.cut(data['km Z3-4'], 
#                                 bins=[0, 5, 10, 15, 20, float('inf')], 
#                                 labels=['0-5km', '5-10km', '10-15km', '15-20km', '20+km'])

# km_counts_Z3 = data['total km'].value_counts().reset_index()
# km_counts_Z3.columns = ['km_category', 'count']

# data['km Z5-T1-T2'] = pd.cut(data['km Z5-T1-T2'], 
#                                 bins=[0, 1, 2, 3, 5, float('inf')], 
#                                 labels=['0-1km', '1-2km', '2-3km', '3-5km', '5+km'])

# km_counts_Z5T1 = data['km Z5-T1-T2'].value_counts().reset_index()
# km_counts_Z5T1.columns = ['km_category', 'count']

# create dropdown with two variables
data_selector = st.selectbox("Select Dataset", options=['km_counts', 'km_counts_Z3', 'km_counts_Z5T1'])

if data_selector == 'km_counts':
    st.subheader("Total km Distribution")
    fig = plt.hist(df['total km'].dropna(), bins=30, alpha=0.7)
    #fig = px.histogram(km_counts, x='km_category', y='count', title='Total km Distribution')
    st.plotly_chart(fig)
elif data_selector == 'km_counts_Z3':
    st.subheader("km Z3-4 Distribution")
    fig = plt.hist(df['km Z3-4'].dropna(), bins=30, alpha=0.7)
    #fig = px.histogram(km_counts_Z3, x='km_category', y='count', title='km Z3-4 Distribution')
    st.plotly_chart(fig)
elif data_selector == 'km_counts_Z5T1':
    st.subheader("km Z5-T1-T2 Distribution")
    fig = plt.hist(df['km Z5-T1-T2'].dropna(), bins=30, alpha=0.7)
    #fig = px.histogram(km_counts_Z5T1, x='km_category', y='count', title='km Z5-T1-T2 Distribution')
    st.plotly_chart(fig)



