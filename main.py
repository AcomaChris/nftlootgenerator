# 11/28/2021
# Made by DanChan
# NFT Stealer (OpenSea)

import requests
import os
import json
import math
import sys

# Import to allow image manipulation.
from PIL import Image, ImageFont, ImageDraw

# Gets the current folder location.
filepath = sys.path[0]
print('Local filepath is: ' + filepath)

# Declaring the name of the collection we want to download.
# TODO: Make this an input variable in the future.
CollectionName = "BoredApeYachtClub".lower()

# Declaring the font we use for the title.
card_font = ImageFont.truetype(f'{filepath}\cardgeneration\PoetsenOne-Regular.ttf', 64)

# Image manipulation functions.
def CreateImageCard(CollectionName, formatted_number, cardName):
    
    # Create variables for holding the images we want to merge.
    nft_image = Image.open(f"{filepath}\collections\{CollectionName}\{formatted_number}.png")
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
    title_text = "Bored Ape #0"
    final_image_editable = ImageDraw.Draw(final_image)
    final_image_editable.text((60,40) , title_text , (50,50,50), font=card_font, align="center")

    # Save the image to disk
    print(os.path)
    final_image.save(f"{filepath}\collections\{CollectionName}\{formatted_number}_card.png",format="png")

# Get information regarding collection
collection = requests.get(f"http://api.opensea.io/api/v1/collection/{CollectionName}?format=json")

if collection.status_code == 429:
    print("Server returned HTTP 429. Request was throttled. Please try again in about 5 minutes.")

if collection.status_code == 404:
    print("NFT Collection not found.\n\n(Hint: Try changing the name of the collection in the Python script, line 11.)")
    exit()

collectioninfo = json.loads(collection.content.decode())

# Create image folder if it doesn't exist.
if not os.path.exists('{filepath}'):
    os.mkdir('{filepath}')

if not os.path.exists(f'{filepath}\collections\{CollectionName}'):
    os.mkdir(f'{filepath}\collections\{CollectionName}')

if not os.path.exists(f'{filepath}\collections\{CollectionName}\image_data'):
    os.mkdir(f'{filepath}\collections\{CollectionName}\image_data')

# Get total NFT count
count = int(collectioninfo["collection"]["stats"]["count"])

# Opensea limits to 50 assets per API request, so here we do the division and round up.
iter = math.ceil(count / 50)

print(f"\nBeginning download of \"{CollectionName}\" collection.\n")

# Define variables for statistics
stats = {
"DownloadedData": 0,
"AlreadyDownloadedData": 0,
"DownloadedImages": 0,
"AlreadyDownloadedImages": 0,
"FailedImages": 0
}

# Iterate through every unit
for i in range(iter):
    offset = i * 50
    card_name = ''
    data = json.loads(requests.get(f"https://api.opensea.io/api/v1/assets?order_direction=asc&offset={offset}&limit=50&collection={CollectionName}&format=json").content.decode())

    if "assets" in data:
        for asset in data["assets"]:
          formatted_number = f"{int(asset['token_id']):04d}"

          print(f"\n#{formatted_number}:")

          # Check if data for the NFT already exists, if it does, skip saving it
          if os.path.exists(f'{filepath}\collections\{CollectionName}\image_data\{formatted_number}.json'):
              print(f"  Data  -> [\u2713] (Already Downloaded)")
              stats["AlreadyDownloadedData"] += 1
          else:
                # Take the JSON from the URL, and dump it to the respective file.
                dfile = open(f"{filepath}\collections\{CollectionName}\image_data\{formatted_number}.json", "w+")
                json.dump(asset, dfile, indent=3)
                dfile.close()
                print(f"  Data  -> [\u2713] (Successfully downloaded)")
                stats["DownloadedData"] += 1

          # Check if image already exists, if it does, skip saving it
          if os.path.exists(f'{filepath}\collections\{CollectionName}\{formatted_number}.png'):
              print(f"  Image -> [\u2713] (Already Downloaded)")
              stats["AlreadyDownloadedImages"] += 1
          else:
            # Make the request to the URL to get the image
            if not asset["image_original_url"] == None:
              image = requests.get(asset["image_original_url"])
            else:
              image = requests.get(asset["image_url"])

          # If the URL returns status code "200 Successful", save the image into the "images" folder.
            if image.status_code == 200:
                file = open(f"{filepath}\collections\{CollectionName}\{formatted_number}.png", "wb+")
                file.write(image.content)
                file.close()
                print(f"  Image -> [\u2713] (Successfully downloaded)")
                stats["DownloadedImages"] += 1

                # Generate a card.
                CreateImageCard(CollectionName, formatted_number, '')

            # If the URL returns a status code other than "200 Successful", alert the user and don't save the image
            else:
                print(f"  Image -> [!] (HTTP Status {image.status_code})")
                stats["FailedImages"] += 1
                continue

print(f"""
Finished downloading collection.
Statistics
-=-=-=-=-=-
Total of {count} units in collection "{CollectionName}".
Downloads:
  JSON Files ->
    {stats["DownloadedData"]} successfully downloaded
    {stats["AlreadyDownloadedData"]} already downloaded
  Images ->
    {stats["DownloadedImages"]} successfully downloaded
    {stats["AlreadyDownloadedImages"]} already downloaded
    {stats["FailedImages"]} failed
You can find the images in the images/{CollectionName} folder.
The JSON for each NFT can be found in the images/{CollectionName}/image_data folder.
Press enter to exit...""")
input()