import streamlit as st
import requests, json, math, sys, os
import urllib.request
import cardgenerator

# Import to allow image manipulation.
from PIL import Image, ImageFont, ImageDraw
from io import BytesIO

# Debug variables for additional logging 
log_image_urls = False

# Gets the current folder location.
filepath = os.path.dirname(os.path.realpath(sys.argv[0]))
print('Local filepath is: ' + filepath)

# Declaring the font we use for the title.
print(f'{filepath}\cardgeneration\PoetsenOne-Regular.ttf')
card_font = ImageFont.truetype(f'{filepath}\cardgeneration\PoetsenOne-Regular.ttf', 64)

######################
# Setup User Interface
######################
endpoint = st.sidebar.selectbox("Endpoints", ['Assets', 'Events', 'Rarity'])
st.header(f'Juno NFT Loot Inspector - {endpoint}')

st.sidebar.subheader("Filters")
collection = st.sidebar.text_input("Collection").lower()
owner = st.sidebar.text_input("Owner")
numberofassets = st.sidebar.number_input("Number of Assets", 0, 50, 1, 1)
offset = st.sidebar.number_input("Offset Token ID", 0, None, 0, 1)
order_direction = st.sidebar.selectbox("Order by",["asc","desc"])

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

    # Iterate through asset media and attempt to display.
    for asset in response["assets"]:

        # Generate a name for the asset
        nft_name = ''
        if asset['name']:
            nft_name = asset['name']
        else:
            nft_name = f"{asset['collection']['name']} #{asset['token_id']}"
        st.write(nft_name)

        # Check to see the type of asset and use the correct player.
        # TODO: Need a solution for SVGs and audio files.
        if asset['image_url'].endswith('mp4'):
            st.video(asset['image_url'])

        else:
            #st.image(asset['image_url'])

            folder = os.path.dirname(os.path.realpath(__file__)) + "\collections"

            img_data = requests.get(asset['image_url']).content

            # Check to see if we've already downloaded it.
            if os.path.exists(f'{folder}+"\\"+nft_name+".jpg"') or os.path.exists(f'{folder}+"\\"+nft_name+".png"'):
                print(f"  Data  -> [\u2713] (Already Downloaded)")

            # Test for jpg vs png files
            if asset['image_url'].endswith('jpg'):
                with open(folder+"\\"+nft_name+".jpg", 'wb') as handler:
                    handler.write(img_data)
                        # Try png files
            else:
                with open(folder+"\\"+nft_name+".png", 'wb') as handler:
                    handler.write(img_data)

            image_test = Image.open(".\collections\\"+nft_name+".png")
            st.image(image_test)
            
        # Log image urls is we've got that debug flag on.
        if(log_image_urls):
            print(asset['image_url'])

    st.write(r.json())