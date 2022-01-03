# Import to allow image manipulation.
from PIL import Image, ImageFont, ImageDraw
import os

# Declaring the font we use for the title.
title_font = None
description_font = None

# Set the card fonts
def SetCardFonts(title_font_filepath, description_font_filepath):
    title_font = title_font_filepath
    description_font = description_font_filepath

#######################################
# Generate cards from downloaded images
#######################################
def CreateImageCard(filepath, collection_name, formatted_number, card_name, nft_input_location):
    
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
    # print(os.path)
    # final_image.save(f"{filepath}\collections\{collection_name}\{formatted_number}_card.png",format="png")

    # Return the new image
    return final_image

# Initialization complete
print("Card generator initialization complete.")