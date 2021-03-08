#pip install pillow
from PIL import Image, ImageFont, ImageDraw


ShowText = 'Python PIL'

font = ImageFont.truetype('arialbd.ttf', 10) #load the font
size = font.getsize(ShowText)  #calc the size of text in pixels
image = Image.new('1', size, 1)  #create a b/w image
draw = ImageDraw.Draw(image)
draw.text((0, 0), ShowText, font=font) #render the text to the bitmap
for rownum in range(size[1]): 
#scan the bitmap:
# print ' ' for black pixel and 
# print '#' for white one
    line = ''
    for colnum in range(size[0]):
        if image.getpixel((colnum, rownum)): line = line + ' ' #.append( ),
        else: line = line + '#' #line.append('#'),
    print (line)