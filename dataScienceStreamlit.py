# The grapghs arent really working out, if seeked the help of gpt but i dont seem
# to be a able to get it fixed. I hope its ok. 
# GPT is saying its a streamlit problem but i doubt that since you were able to do it
#in class for the line and scatetr graph.

import streamlit as st 
import pandas as pd 
import numpy as np 
import io 

st.set_page_config(page_title="Analyze Your Data",page_icon='📊',layout='wide')

st.title('Analyze Your Data')
st.write('Upload a **CSV** or an **Excel** File to Analyze/Explore your Data Interactively')

# To upload a data file
uploaded_file = st.file_uploader('Upload a CSV or Excel file',type=['csv','xlsx'])

if uploaded_file is not None:
    try:
        # -------- TASK 1 : CSV + Excel --------
        if uploaded_file.name.endswith('.csv'):
            data = pd.read_csv(uploaded_file)
        else:
            data = pd.read_excel(uploaded_file)

        # converting boolean columns as str
        bool_columns = data.select_dtypes(include=['bool']).columns
        data[bool_columns] = data[bool_columns].astype('str')

    except Exception as e:
        st.error('File could not be read. Please check file format!')
        st.exception(e)
        st.stop()
        
    st.success('File has been uploaded **Successfully**!')
    st.write('### Preview of the dataset')
    st.dataframe(data.head(10))
    
    st.write('Data overview')
    st.write('Number of rows : ',data.shape[0])
    st.write('Number of Columns :',data.shape[1])
    st.write('Number of Missing Values :',data.isnull().sum().sum())
    st.write('Number of Duplicate Values :',data.duplicated().sum())
    
    st.write('###Complete Summary of The Dataset')
    buffer = io.StringIO()
    data.info(buf=buffer)
    i = buffer.getvalue()
    st.text(i)
    
    st.write('###Statistical Summary For Numerical Features In The Dataset')
    st.dataframe(data.describe())

    # -------- TASK 2 : Show only if non-numerical exists --------
    non_num_cols = data.select_dtypes(include=['object','bool']).columns
    if len(non_num_cols) > 0:
        st.write('###Statistical Summary For Non Numerical Features In The Dataset')
        st.dataframe(data.describe(include=['object','bool']))
    
    st.write('###Select the Desired Columns For Analysis')
    selected_columns = st.multiselect('Pick The Columns',data.columns.tolist())
    
    if selected_columns:
        st.dataframe(data[selected_columns].head(10))
    else :
        st.info('No Columns Selected. Displaying Full Data Analysis')
        st.dataframe(data.head(10))
        
    st.write('###Data Visualization')
    st.write('Select **Columns** For Visualization')
    columns = data.columns.tolist()
    x_axis = st.selectbox('Select a Column For X-Axis',options=columns)
    y_axis = st.selectbox('Select a Column For Y-Axis',options=columns)
    
    # Creating buttons for different charts
    col1, col2, col3 = st.columns(3)
    
    with col1:
        line_btn = st.button('Line Graph')
    with col2:
        scatter_btn = st.button('Scatter Graph')
    with col3:
        bar_btn = st.button('Bar Graph')

    col4, col5 = st.columns(2)
    with col4:
        hist_btn = st.button('Histogram')
    with col5:
        box_btn = st.button('Box Plot')

    # -------- LINE GRAPH --------
    if line_btn:
        if data[y_axis].dtype != 'object':
            st.line_chart(data[y_axis])
        else:
            st.warning('Line graph requires numerical data')

    # -------- SCATTER GRAPH --------
    if scatter_btn:
        if data[x_axis].dtype != 'object' and data[y_axis].dtype != 'object':
            st.scatter_chart(data[[x_axis, y_axis]])
        else:
            st.warning('Scatter graph requires numerical data')

    # -------- BAR GRAPH --------
    if bar_btn:
        if data[y_axis].dtype != 'object':
            st.bar_chart(data[y_axis])
        else:
            st.warning('Bar graph requires numerical data')

    # -------- HISTOGRAM --------
    if hist_btn:
        if data[x_axis].dtype != 'object':
            st.bar_chart(data[x_axis].value_counts())
        else:
            st.warning('Histogram requires numerical data')

    # -------- BOX PLOT (simple version) --------
    if box_btn:
        if data[y_axis].dtype != 'object':
            st.write(data[y_axis].describe())
        else:
            st.warning('Box plot requires numerical data')
