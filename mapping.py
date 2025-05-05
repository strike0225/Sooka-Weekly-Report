import re
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np

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

    # Count entries with "TroubleShooting" in subject column
    if 'subject' in df.columns:
        # Count rows containing "TroubleShooting"
        troubleshooting_count = df[df['subject'].str.contains('TroubleShooting', case=False, na=False)].shape[0]
        
        # Display the count
        st.subheader("TroubleShooting Count")
        st.metric(label="Entries with 'TroubleShooting' in subject", value=troubleshooting_count)
        
        # Show percentage of total
        percentage = (troubleshooting_count / df.shape[0]) * 100
        st.write(f"Percentage of total entries: {percentage:.2f}%")
        
        # Create a new column for TroubleShooting tickets
        df['is_troubleshooting'] = df['subject'].str.contains('TroubleShooting', case=False, na=False)
        
        # Display the dataframe with the new column
        st.subheader("Data with TroubleShooting Column")
        st.dataframe(df[['subject', 'is_troubleshooting']].head())
    
    # Calculate and display channel counts if channel column exists
    if 'channel' in df.columns:
        # Calculate value counts
        channel_counts = df['channel'].value_counts(dropna=False)
        
        # Display channel counts
        st.subheader("Channel Distribution")
        
        # Display as table
        st.dataframe(channel_counts.reset_index().rename(
            columns={'index': 'Channel', 'channel': 'Count'}
        ))
        
        # Display as chart
        st.bar_chart(channel_counts)
        
        # Display percentages
        st.subheader("Channel Percentages")
        channel_percentages = (channel_counts / channel_counts.sum() * 100).round(2)
        st.dataframe(channel_percentages.reset_index().rename(
            columns={'index': 'Channel', 'channel': 'Percentage (%)'}
        ))

    # Calculate and display status counts if status column exists
    if 'status' in df.columns:
        # Calculate value counts
        status_counts = df['status'].value_counts()
        
        # Display status counts
        st.subheader("Status Distribution")
        
        # Display as table
        st.dataframe(status_counts.reset_index().rename(
            columns={'index': 'Status', 'status': 'Count'}
        ))
        
        # Display as chart
        st.bar_chart(status_counts)
        
        # Display percentages
        st.subheader("Status Percentages")
        status_percentages = (status_counts / status_counts.sum() * 100).round(2)
        st.dataframe(status_percentages.reset_index().rename(
            columns={'index': 'Status', 'status': 'Percentage (%)'}
        ))

    # Extract and analyze Issue Types if description column exists
    if 'description' in df.columns:
        # Create a section for Issue Type analysis
        st.subheader("Issue Type Analysis")
        
        # Extract Issue Type from description using regex
        df['Issue_Type'] = df['description'].str.extract(r'Issue Type\s*:\s*([^\n]+)')
        
        # Calculate value counts
        issue_counts = df['Issue_Type'].value_counts(dropna=False)
        
        # Display issue type counts
        st.subheader("Issue Type Distribution")
        
        # Display as table
        st.dataframe(issue_counts.reset_index().rename(
            columns={'index': 'Issue Type', 'Issue_Type': 'Count'}
        ))
        
        # Display as chart
        st.bar_chart(issue_counts)
        
        # Display percentages
        st.subheader("Issue Type Percentages")
        issue_percentages = (issue_counts / issue_counts.sum() * 100).round(2)
        st.dataframe(issue_percentages.reset_index().rename(
            columns={'index': 'Issue Type', 'Issue_Type': 'Percentage (%)'}
        ))
        
        # Analysis of BUFFERING_ISSUE and VIDEO_FREEZE issues by content type
        st.subheader("Buffering and Video Freeze Analysis")
        
        # Create a copy of the dataframe for filtering
        df_issues = df.copy()
        
        # Filter only for BUFFERING_ISSUE and VIDEO_FREEZE
        if 'Issue_Type' in df_issues.columns:
            df_issues = df_issues[df_issues['Issue_Type'].isin(['BUFFERING_ISSUE', 'VIDEO_FREEZE'])]
            
            # Extract Content Name
            df_issues['Content_Name'] = df_issues['description'].str.extract(r'Content Name\s*:\s*([^\n]+)')
            
            # Create a new column "Type" based on (L) prefix
            df_issues['Type'] = np.where(df_issues['Content_Name'].str.startswith('(L)'), 'Live', 'Watch')
            
            # If Content_Name is NaN, set Type as 'None'
            df_issues.loc[df_issues['Content_Name'].isna(), 'Type'] = 'None'
            
            # Count occurrences of each unique Content_Name
            content_counts = df_issues.groupby(['Content_Name', 'Type']).size().reset_index(name='Count')
            
            # Sort by Count in descending order
            content_counts = content_counts.sort_values(by='Count', ascending=False)
            
            # Display the total number of issues
            total_issues = df_issues.shape[0]
            st.metric(label="Total BUFFERING_ISSUE & VIDEO_FREEZE count", value=total_issues)
            
            # Calculate and display Live vs Watch totals
            type_counts = df_issues['Type'].value_counts()
            
            # Create columns for displaying metrics side by side
            col1, col2, col3 = st.columns(3)
            
            # Display the counts
            with col1:
                if 'Live' in type_counts:
                    st.metric(label="Total Live Issues", value=type_counts['Live'])
                else:
                    st.metric(label="Total Live Issues", value=0)
            
            with col2:
                if 'Watch' in type_counts:
                    st.metric(label="Total Watch Issues", value=type_counts['Watch'])
                else:
                    st.metric(label="Total Watch Issues", value=0)
            
            with col3:
                if 'None' in type_counts:
                    st.metric(label="Unclassified Issues", value=type_counts['None'])
                else:
                    st.metric(label="Unclassified Issues", value=0)
            
            # Display pie chart for type distribution
            st.subheader("Distribution of Live vs Watch Issues")
            fig, ax = plt.subplots()
            type_counts.plot(kind='pie', autopct='%1.1f%%', ax=ax)
            st.pyplot(fig)
            
            # Display detailed content counts table
            st.subheader("Issues by Content Name")
            st.dataframe(content_counts)

    # Analyze Platform information for API channel
    st.subheader("API Channel Platform Analysis")

    # Check if channel column exists
    if uploaded_file is not None and 'channel' in df.columns:
        # Filter for API channel entries
        df_api = df[df['channel'] == 'api'].copy()
        
        if not df_api.empty:
            # Extract Platform information from description
            df_api['Platform'] = df_api['description'].str.extract(r'Platform\s*:\s*([^\n]+)', expand=True)
            
            # Count occurrences of each Platform
            platform_counts = df_api['Platform'].value_counts(dropna=False)
            
            # Display the count as a table
            st.dataframe(platform_counts.reset_index().rename(
                columns={'index': 'Platform', 'Platform': 'Count'}
            ))
            
            # Display as chart
            st.bar_chart(platform_counts)
            
            # Calculate and display percentages
            platform_percentages = (platform_counts / platform_counts.sum() * 100).round(2)
            
            # Display pie chart for platform distribution
            st.subheader("Platform Distribution for API Channel")
            fig, ax = plt.subplots()
            platform_counts.plot(kind='pie', autopct='%1.1f%%', ax=ax)
            plt.axis('equal')
            st.pyplot(fig)
            
            # Show total API channel entries
            st.metric(label="Total API Channel Entries", value=df_api.shape[0])
        else:
            st.write("No API channel entries found in the dataset.")

