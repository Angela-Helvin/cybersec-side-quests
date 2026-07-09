
'''########################################################################################
Purpose: Just a little bit of simple stegonography in Python.

This script takes a plain text file and encodes it within a given image by replacing
low value elements (i.e. least significant bits) of an RGBA image with 0/1 bits of a
binary encoded ASCII message. The encoded image and recovered secret message are returned.
-------------------------------------------------------------------------------------------
Execution Instructions:

1. Save the image you wish to hide your message in as image.png
2. Save the message you want to hide as message.txt
3. From the terminal (MAC OS) type: python /Pathname/RGB_Stego_v3.py
   where Pathname is the location that THIS file has been saved to.

Alternatively, to hide the image only, run the code in the HIDE section below.
To recover an already encoded image only, run the code in the RECOVER section below.

-------------------------------------------------------------------------------------------
Technical Specifications:

Developed on MacOS HIgh Sierra with Python 2.7 and Pillow installed.
Pillow can be installed by opening a terminal window and calling e.g. $pip install Pillow
Pillow is called within Python as PIP.
-------------------------------------------------------------------------------------------
Inputs and Outputs

NB: All inputs and outputs are located/written to the working directory
Inputs:
Message to encode, as a text file, named "message.txt"
Image to hide the message in.

Outputs:
enc_imagename: The input image with the plain text message encoded inside it.
Secret.txt: Message recoverd from within the encoded image

###########################################################################################
'''
