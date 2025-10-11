# This Python file uses the following encoding: latin-1

#pip install pillow
from PIL import Image, ImageFont, ImageDraw


#In ASCII table, printable caracters goes from 32 to 254
#i want a max 10 px height letter.
#Firts, we will print letters > 10 px to manually cut in a text editor
#Next, we will repeat proces but print letters <= 10 px. 
#The output format will be an array of binary numbers in arduino text file


lletres_grans={36,40,41,64,91,93,106,123,124,125,175,182,192,193,194,195,196,197,198,200,201,202,203,204,205,206,207,208,209,210,211,212,213,214,215,216,217,218,219,220,221}

cadenes =[None,None,None]
print (ord('Ç'))
for lletres in range(199,200):
    lletra= chr(lletres)

    if lletres in lletres_grans:
        font = ImageFont.truetype('arialbd.ttf', 11) #load the font
    else:
        if lletres == 199: font = ImageFont.truetype('arialbd.ttf', 10) #load the font
        else: font = ImageFont.truetype('arialbd.ttf', 13) #load the font

    size = font.getsize(lletra)  #calc the size of text in pixels
    image = Image.new('1', size, 1)  #create a b/w image
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), lletra, font=font) #render the text to the bitmap
    cadena = str(lletres) + ',' #+ str(size[0]) + ',' #+ str(10) + ','
    for colnum in range(size[0]):
        line = ''
        for rownum in range(size[1]-10,size[1]): 
            if image.getpixel((colnum, rownum)): line = line + '0'
            else: line = line + '1' 
        cadena= cadena + '0b' + line + ","
    cadenes.append([str(size[0]),lletra,cadena[0:len(cadena)-1] ])
    
    
    
print('//Declare an array for Arduino.')
print('//ASCII code / Column 1 / Column 2 / ...')

for mida in range (0,20):
    primera=0
    for cadena in cadenes:
        if cadena is not None:
            if mida == int(cadena[0]): 
                if primera == 0 : 
                    print ('const int ABECEDARI' + str(mida) + '[] PROGMEM = {')
                    primera = 1
                else: print(',')
                print("\t//"+cadena[1])
                print('\t'+cadena[2], end ="")
        
    if primera != 0: print('};')
    

print('')
print('//Array pointer to generated chars')
print('long TotesLesFonts[]  = {    ')
for mida in range (0,20):
    primera=0
    for cadena in cadenes:
        if cadena is not None:
            if mida == int(cadena[0]): 
                if primera == 0 : 
                    print('\t\t(int*)&ABECEDARI'+str(mida)+',')
                    primera = 1
print('};')


print('')
print('//width of the char of each array')
print('unsigned int TotesLesFontsAmplada[] ={')
for mida in range (0,20):
    primera=0
    for cadena in cadenes:
        if cadena is not None:
            if mida == int(cadena[0]): 
                if primera == 0 : 
                    print('\t\t'+str(mida)+',')
                    primera = 1
print('};')


print('')
print('//How many elements has each array')
print('int TotesLesFontsQuantes[] ={')
quantes = 0
for mida in range (0,20):
    primera=0
    for cadena in cadenes:
        if cadena is not None:
            if mida == int(cadena[0]): 
                if primera == 0 : 
                    print('\t\tsizeof(ABECEDARI'+str(mida)+') / sizeof(ABECEDARI'+str(mida)+'[0]) /  (TotesLesFontsAmplada['+str(quantes)+']+1),')
                    primera = 1
                    quantes = quantes + 1
print('};')

print('')
print('byte QuantesTaulesFonts = sizeof(TotesLesFontsAmplada)/sizeof(TotesLesFontsAmplada[0]);')