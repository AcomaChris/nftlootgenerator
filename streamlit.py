import streamlit as st
import requests, json

endpoint = st.sidebar.selectbox("Endpoints", ['Assets', 'Events', 'Rarity'])
st.header(f'Juno NFT Loot Inspector - {endpoint}')

st.sidebar.subheader("Filters")
collection = st.sidebar.text_input("Collection")
owner = st.sidebar.text_input("Owner")
numberofassets = st.sidebar.text_input("Number of Assets")


if endpoint == 'Assets':
    params = {}

    if collection:
        params['collection'] = collection
    if owner:
        params['owner'] = owner
    if numberofassets:
        params['limit'] = numberofassets

    r = requests.get("https://api.opensea.io/api/v1/assets", params=params)

    response = r.json()

    for asset in response["assets"]:
        if asset['image_url'].endswith('mp4'):
            st.video(asset['image_url'])
        else:
            st.image(asset['image_url'])

    st.write(r.json())