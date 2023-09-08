import streamlit as st
from st_pages import Page, show_pages

from src import (
    analysis,
    data_store, 
)


st.set_page_config(
    page_title='Brain', 
    # layout='wide',
)


st.subheader('Brain/MINDS Marmoset Brain MRI Data Analysis')


if not data_store.check_store():
    data_store.create_store()
dfi, dfe = data_store.read_store()


col1, col2, col3 = st.columns(3)

with col1:
    dataset = st.selectbox(
        'Dataset',
        ['In Vivo', 'Ex Vivo'],
        index=0,
    )

df = dfi if dataset == 'In Vivo' else dfe

with col2:
    variable = st.selectbox(
        'Variable',
        df.columns,
        index=6
    )

with col3:
    groupby = st.selectbox(
        'Groupby',
        [x for x in df.columns if x != variable],
        index=2
    )

st.text('')

ss = analysis.make_groupby(df, variable, groupby)
dfs = ss.to_frame().reset_index()

st.text('')

st.dataframe(dfs)
st.bar_chart(data=dfs, x=groupby, y=variable)