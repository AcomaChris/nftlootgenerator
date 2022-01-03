import streamlit as st
import requests, json

endpoint = st.sidebar.selectbox("Endpoints", ['Assets', 'Events', 'Rarity'])
st.header(f'Juno NFT Loot Inspector - {endpoint}')

st.sidebar.subheader("Filters")
collection = st.sidebar.text_input("Collection")
owner = st.sidebar.text_input("Owner")
offset = st.sidebar.number_input("Token Offset", 0.0, None, 0.0, 1.0)
order_direction = st.sidebar.selectbox("Order by,",['asc','desc'])
numberofassets = st.sidebar.text_input("Number of Assets")


if endpoint == 'Assets':
    params = {}

    if collection:
        params['collection'] = collection
    if owner:
        params['owner'] = owner
    if offset:
        params['offset'] = int(offset)
    if numberofassets:
        params['limit'] = numberofassets
    if order_direction:
        params['order_direction'] = order_direction

    r = requests.get("https://api.opensea.io/api/v1/assets", params=params)

    response = r.json()

    for asset in response["assets"]:
        
        # Display the name of the asset
        # If null, use collection and token ID
        if(asset['name']):
           st.write(asset['name'])
        else:
            st.write(f"{asset['collection']['name']} #{asset['token_id']}")
        
        # Display the asset
        if asset['image_url'].endswith('mp4') or asset['image_url'].endswith('mov'):
            st.video(asset['image_url'])
        else:
            st.image(asset['image_url'])

    st.write(r.json())