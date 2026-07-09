
'''########################################################################################
Purpose:

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


###############################################################################
#################################   HIDE   ####################################
###############################################################################
from PIL import Image
import binascii
import optparse

# Create functions required to convert between formats:
#change hex representation of text to binary values.

def hex2bin(text):
	binary = bin(int(binascii.b2a_hex(text), 16))
	return binary[2:]


#change RGB values to hexadecimal representation

def rgb2hex(r, g, b):
	return '#{:02x}{:02x}{:02x}'.format(r, g, b)


#change hex to RGB values in format (rrr,ggg,bbb)

def hex2rgb(hexadecimal):
	return tuple(map(ord, trim(hexadecimal[1:]).decode('hex')))


#clear out the white space - can cause problems in hex2rgb otherwise

def trim(string1):
    string1 = string1.replace(' ', '')
    return string1


# hide: hides a text message within the least significant RGB bits of an image file.
# Note: this function (hide) is a modified version from the python steganography tutorial,
# available at: https://www.youtube.com/watch?v=q3eOOMx5qoo
# Extended to: clean up errors, convert image to RGBA, and use all RGB channels, not just blue.


def hide(filename, message):
	img = Image.open(filename)
	img = img.convert("RGBA")
	binary = hex2bin(message) + '1111111111111110'
	if img.mode in ('RGBA'):
		img = img.convert('RGBA')
		datas = img.getdata()
		newData = []
		digit = 0
		temp = ''
		for item in datas:
			if (digit < len(binary)):
				new_pixel = encode(rgb2hex(item[0],item[1],item[2]),binary[digit])
				if new_pixel == None:
					newData.append(item)
				else:
					r, g, b = hex2rgb(new_pixel)
					newData.append((r,g,b,255))
					digit += 1
			else:
				newData.append(item)
		img.putdata(newData)
		img.save("enc_" + filename, "PNG")
	return "Image is not in RGB mode - message not hidden"

# Code needed to HIDE hide the message bit in the least sig 4 bits of the RGB channels
def encode(hexadecimal, digit):
	if hexadecimal[-1] in ('0','1', '2', '3', '4', '5', '6', '7', '8', '9') or hexadecimal[-2] in ('0','1', '2', '3', '4', '5', '6', '7', '8', '9') or hexadecimal[0] in ('0','1', '2', '3', '4', '5', '6', '7', '8', '9'):
		hexadecimal = hexadecimal[:-1] + digit
		return hexadecimal
	else:
		return None

# Take the message to encode (in file message.txt) and hide it inside the specified
# image file #using the 'hide' function. (Both inputs must be stored in the working directory)

def tidy_up_texfile(string1):
    string1.replace('\n','')
    string1.replace('\t','')
    string1.replace(' ', '')
    return string1


def hide_message_txt(imagefile):
    x=open('message.txt')
    p = x.read()
    message = tidy_up_texfile(p)
    hide(imagefile, message)


#execute
#hide_message_txt("image.png")

###############################################################################
###############################   RECOVER   ###################################
###############################################################################
from PIL import Image
import binascii
import optparse

# Create functions required to convert between formats:
#change hex to binary representation
def bin2str(binary):
	message = binascii.unhexlify('%x' % (int('0b'+binary,2)))
	return message


#clear out the white space - can cause problems in hex2rgb otherwise
def trim(string1):
    string1 = string1.replace(' ', '')
    return string1


#change RGB values to hexadecimal representation
def rgb2hex(r, g, b):
	return '#{:02x}{:02x}{:02x}'.format(r, g, b)

#recover: recovers the hidden message and exports it in a text file named Secret.txt in the
#working directory.
# Note: this function (recover) is a modified version from the python steganography tutorial,
# available at: https://www.youtube.com/watch?v=q3eOOMx5qoo
def recover(filename):
	img = Image.open(filename)
	img = img.convert('RGBA')
	binary = ''
	if img.mode in ('RGBA'):
		datas = img.getdata()
		for item in datas:
			digit = decode(rgb2hex(item[0],item[1],item[2]))
			if digit == None:
				pass
			else:
				binary = binary + digit
				if (binary[-16:] == '1111111111111110'):
					return bin2str(binary[:-16])
		return bin2str(binary)
	return "Image is not in RGBA mode - message not hidden"


#code needed to retrieve the message bits encoded in the LSB's of RGB values in  function "encode"
def decode(hexadecimal):
	if hexadecimal[-1] in ('0', '1'):
		return hexadecimal[-1]
	else:
		return None

# recover the encoded message from within the image, using function "recover",
# and it write out to "Secret.txt" in the working directory
def recover_to_secret_txt(imagefile):
	secret = recover(imagefile)
	output = open("Secret.txt", "w")
	output.write(secret)
	output.close()


#execute:
#hide_message_txt("image.png")
#recover_to_secret_txt("enc_image.png")

#For Q1(i):
hide_message_txt("pumpkin.png")
recover_to_secret_txt("enc_pumpkin.png")
