import streamlit as st

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
        df.columns,
        index=2
    )

st.text('')


if variable == groupby:
    ss = analysis.make_counts(df, variable)
    dfs = ss.to_frame().reset_index()
    dfs.columns = [variable, 'count']
    x = variable
    y = 'count'
else:
    ss = analysis.make_groupby(df, variable, groupby)
    dfs = ss.to_frame().reset_index()
    x = groupby
    y = variable
    
st.dataframe(dfs)
st.bar_chart(data=dfs, x=x, y=y)
