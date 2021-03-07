
from rpi_ws281x import Color

def omplir(strip, color):
    if color:
        for i in range(strip.numPixels()):
            strip.setPixelColor(i,  color)
        strip.show()
	
	
def netejar(strip):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i,  Color(0, 0, 0))
    strip.show()

    
    

def wheelColor(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

        
        
def ObteVermell(pColor):
    return (pColor >> 16) & 0xff;

def ObteVerd(pColor):
    return (pColor >> 8) & 0xff;

def ObteBlau(pColor):
    return pColor & 0xff;   


def ObteVermellHex(pColor):
    return     int(           (float(ObteVermell(pColor))/float(0xFF))   *   float(0xFFFF)     )      

def ObteVerdHex(pColor):
    return     int(           (float(ObteVerd(pColor))/float(0xFF))   *   float(0xFFFF)     )      

def ObteBlauHex(pColor):
    return     int(           (float(ObteBlau(pColor))/float(0xFF))   *   float(0xFFFF)     )      
    
    