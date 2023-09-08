import streamlit as st

from src import (
    data_store, 
)


st.set_page_config(
    page_title='Brain', 
    layout='wide',
)


st.header('Brain/MINDS Marmoset Brain MRI Datasets')


if not data_store.check_store():
    data_store.create_store()
dfi, dfe = data_store.read_store()


st.subheader('NA216 (In Vivo)')
st.dataframe(dfi)


st.subheader('eNA91 (Ex Vivo)')
st.dataframe(dfe)
