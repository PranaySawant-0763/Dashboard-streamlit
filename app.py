import streamlit as st
import plotly.express as px
import pandas as pd

 
st.set_page_config(
    page_title="Dashboard",
    page_icon="",
    layout="wide"
)
 
st.title("Dashboard")
st.caption("---")
col1,col2 = st.columns([1,1],gap="small")
with col1:
    flag=False
    df = None
    file = st.file_uploader("Upload your file",["csv","xlsx"])
    if file:
        read = pd.read_csv(file)
        df = pd.DataFrame(read)

    col3,col4,col5 = st.columns([1,1,1],gap="xsmall")

    with col3:
        if df is not None: 
            graph_selection = st.selectbox("Select the graph: ",["Select","Bar","Histogram","Line","Scatter","Pie"])
            if graph_selection == 'Histogram':
                flag=True
            if graph_selection == "Pie":
                choose_agg = st.selectbox("Choose Agg",["sum","count"])
        else:
            st.selectbox("Select the graph",['None'])

    with col4:
        if df is not None: 
            select_x = st.selectbox("Select the x-axis ",df.columns)
        else:
            st.selectbox("Select the x-axis",['None'])

    with col5:
        if df is not None: 
            select_y = st.selectbox("Select the y-axis ",df.columns,disabled=flag)
        else:
            st.selectbox("Select the y-axis",['None'])

    st.caption("---")
    if file:
    
        tab1,tab2 = st.tabs(['Head','Describe'])

        with tab1:
            st.write(df.head())
        with tab2:
            st.write(df.describe())


with col2:
    
    if file:
        fig = None

        if graph_selection != "Select":
            st.header(graph_selection)
        x = df[select_x]
        y = df[select_y]

        
        if graph_selection=="Bar":
            fig = px.bar(df,x,y)
    
        if graph_selection=="Line":
            fig = px.line(df,x,y)
           
        if graph_selection=="Scatter":
            fig = px.scatter(df,x,y)

        if graph_selection=="Histogram":
            fig = px.histogram(df,x)

        if graph_selection == "Pie":

            if choose_agg == "count":
                pie_data = df.groupby(select_x)[select_y].count()
            elif choose_agg == "sum":
                pie_data = df.groupby(select_x)[select_y].sum()

            fig = px.pie(
                values=pie_data.values,   # numbers
                names=pie_data.index      # labels
            )

        

        if fig:
            st.plotly_chart(fig)