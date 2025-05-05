import re
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Set page title
st.title("CSV File Uploader")

# Create file upload component
uploaded_file = st.file_uploader("Choose CSV file", type=["csv"])

# Process uploaded file
if uploaded_file is not None:
    # Display success message
    st.success("File uploaded successfully!")
    
    # Read uploaded file as pandas DataFrame
    df = pd.read_csv(uploaded_file)
    
    # Display data preview
    st.subheader("Data Preview")
    st.dataframe(df.head())
    
    # Display basic data information
    st.subheader("Basic Data Information")
    st.write(f"Rows: {df.shape[0]}")
    st.write(f"Columns: {df.shape[1]}")
    st.write("Column names:", list(df.columns))
    
    # Process tags column if it exists
    if 'tags' in df.columns:
        # Split and explode tags
        df_exploded = df['tags'].str.split(',').explode()
        
        # Count all tags
        value_counts = df_exploded.value_counts()
        
        # Count occurrences of 'yourgpt'
        yourgpt_count = df_exploded[df_exploded.str.contains('yourgpt', case=False)].shape[0]
        
        # Display counts in Streamlit
        st.subheader("Tag Statistics")
        
        # Display yourgpt count
        st.metric(label="YourgGPT Count", value=yourgpt_count)
        
        # Display all tag counts
        st.subheader("All Tags Count")
        st.bar_chart(value_counts)

    # Process Concern Category if it exists
    if 'Concern Category' in df.columns:
        # Count occurrences of each category
        df_concern = df['Concern Category'].value_counts()
        
        # Display concern category counts
        st.subheader("Concern Categories Count")
        
        # Show the count results as a dataframe
        st.dataframe(df_concern.reset_index().rename(
            columns={'index': 'Concern Category', 'Concern Category': 'Count'}
        ))
        
        # Show as chart
        st.bar_chart(df_concern)

