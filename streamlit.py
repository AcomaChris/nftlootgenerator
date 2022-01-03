import streamlit as st

endpoint = st.sidebar.selectbox("Endpoints", ['Assets', 'Events', 'Rarity'])

st.header(f'Juno NFT Loot Inspector - {endpoint}')