import streamlit as st
import pandas as pd
import plotly.express as px
import base64
import io
from io import *

def generate_excel_downloads_link(df):
    
    towrite = BytesIO()
    df.to_excel(towrite, encoding='utf-8', index=False, header=True)
    towrite.seek(0)  # reset pointer
    b64 = base64.b64encode(towrite.read()).decode()  # some strings
    href= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="myfilename.xlsx">Download excel file</a>'
    return st.markdown(href, unsafe_allow_html=True)


def generate_excel_downloads_link(fig):
    towrite = StringIO()
    fig = px.scatter(x=range(10), y=range(10))
    # fig.write_html("path/to/file.html")
    fig.write_html(towrite, include_plotlyjs='cdn')
    towrite = BytesIO(towrite.getvalue().encode())
    b64 = base64.b64encode(towrite.read()).decode()
    href = f'<a href="data:text/html;charset=utf-8;base64, {b64}" download="plot.html">Download plot</a>'
    return st.markdown(href, unsafe_allow_html=True) 


st.set_page_config(page_title='Excel Plotter')
st.title('Excel Plotter')
st.subheader('Feed me with your Excel file')


uploaded_file = st.file_uploader('Choose a XLSX file',type='xlsx')


if uploaded_file:
    st.markdown('---')
    df = pd.read_excel(uploaded_file,engine='openpyxl')
    st.dataframe(df)
    
    groupby_column = st.selectbox('What would you like to analyse?',('First Name','Last Name'
                                ,'Gender','Country','Age','Date','Id'),
                                )

    output_colmns = ['First Name','Age']
    df_grouped = df.groupby(by=[groupby_column], as_index=False)[output_colmns].sum()
    
    fig = px.bar(
        df_grouped,
        x=groupby_column,
        y='Age',
        color = 'First Name',
        color_continuous_scale=['red','yellow','green'],
        template='plotly_white',
        title = f'<b>Name and Ages by {groupby_column}</b>'
    )
    st.plotly_chart(fig)
    
    
    st.subheader('Downloads:') 
    generate_excel_downloads_link(df_grouped)
    generate_excel_downloads_link(fig)

