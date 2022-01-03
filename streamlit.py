import streamlit as st
import requests, json, math, sys, os
import urllib.request

#######################
# Import all the things
#######################

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

#######################################
# Generate cards from downloaded images
#######################################

title_font = ImageFont.truetype(f'{filepath}\cardgeneration\PoetsenOne-Regular.ttf', 40)
description_font = ImageFont.truetype(f'{filepath}\cardgeneration\PoetsenOne-Regular.ttf', 40)

def CreateImageCard(collection_name, formatted_number, card_name, nft_input_location):
    
    # Create variables for holding the images we want to merge.
    nft_image = Image.open(f"{nft_input_location}")
    background_image = Image.open(f"{filepath}\cardgeneration\card_background.png")
    trim_image = Image.open(f"{filepath}\cardgeneration\card_trim.png")

    # Convert all the images to RGBA
    nft_image.convert("RGBA")
    background_image.convert("RGBA")
    trim_image.convert("RGBA")

    # Grab the size of the background image and store as variables.
    background_size = background_image.size

    # Merge the images in the correct order.
    final_image = Image.new('RGBA' , (background_size[0],background_size[1]) , (255,255,255))
    final_image.paste(background_image,(0,0),background_image)
    final_image.paste(nft_image,(30,140),nft_image)
    final_image.paste(trim_image,(0,0),trim_image)

    # Add the text title to the card.
    title_text = card_name
    final_image_editable = ImageDraw.Draw(final_image)
    final_image_editable.text((60,40) , title_text , (50,50,50), font=title_font, align="center")

    # Save the image to disk
    print(os.path)
    final_image.save(f"{filepath}\collections\{formatted_number}_card.png",format="png")

    # Return the new image
    return final_image

# Initialization complete
print("Card generator initialization complete.")

#######################
# Create User Interface
#######################
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
        nft_name = f"{asset['collection']['name']} #{asset['token_id']}"
        collection_name = f"{asset['collection']['name']}"

        # TODO: Move all the images into their own collection folders again.
        if not os.path.exists(f'{filepath}\collections\{collection_name}'):
            os.mkdir(f'{filepath}\collections\{collection_name}')

        # TODO: Rehook up the JSON exporter for the image_data folder.
        if not os.path.exists(f'{filepath}\collections\{collection_name}\image_data'):
            os.mkdir(f'{filepath}\collections\{collection_name}\image_data')

        # if asset['name']:
        #     nft_name = asset['name']
        # else:
        #     nft_name = f"{asset['collection']['name']} #{asset['token_id']}"

        st.write(nft_name)

        # Check to see the type of asset and use the correct player.
        # TODO: Need a solution for SVGs and audio files.
        if asset['image_url'].endswith('mp4'):
            st.video(asset['image_url'])

        else:
            #st.image(asset['image_url'])

            folder = os.path.dirname(os.path.realpath(__file__)) + "\collections"

            img_data = requests.get(asset['image_url']).content
            img_location = ''

            # Check to see if we've already downloaded it.
            if os.path.exists(f'{folder}+"\\"+nft_name+".jpg"') or os.path.exists(f'{folder}+"\\"+nft_name+".png"'):
                print(f"  Data  -> [\u2713] (Already Downloaded)")

            # Test for jpg vs png files
            if asset['image_url'].endswith('jpg'):
                jpg_save_name = folder + "\\" + nft_name + ".jpg"
                img_location = jpg_save_name
                with open(jpg_save_name, 'wb') as handler:
                    handler.write(img_data)
            # Try png files
            else:
                png_save_name = folder + "\\" + nft_name + ".png"
                img_location = png_save_name
                with open(png_save_name, 'wb') as handler:
                    handler.write(img_data)

            # Image declaration for the final image
            # NOTE: The reason this is broken is that we're not saving the file
            # ...before we send final_image to the CreateImageCard
            interrim_image = Image.open(".\collections\\"+nft_name+".png")
            final_image = interrim_image.resize([613, 613], None)
            width, height = final_image.size
            print(width,height)

            # Render as a playing card
            final_image = CreateImageCard(asset['collection']['name'], asset['token_id'], nft_name, img_location)

            # Render the image
            st.image(final_image)
            
        # Log image urls is we've got that debug flag on.
        if(log_image_urls):
            print(asset['image_url'])

    st.write(r.json())