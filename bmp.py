from struct import pack
from struct import unpack

class Bitmap():
    
    def __init__(s, width, height):
        s._bfType = 19778 # Bitmap signature
        s._bfReserved1 = 0
        s._bfReserved2 = 0
        s._bcPlanes = 1
        s._bcSize = 12
        s._bcBitCount = 24
        s._bfOffBits = 26
        s._bcWidth = width
        s._bcHeight = height
        s._bfSize = 26+s._bcWidth*3*s._bcHeight
        s.clear()


    def clear(s):
        s._graphics = [(0,0,0)]*s._bcWidth*s._bcHeight


    def setPixel(s, x, y, color):
        if isinstance(color, tuple):
            if x < 0 or y < 0 or x > s._bcWidth-1 or y > s._bcHeight-1:
                raise ValueError('Coords out of range')
            if len(color) != 3:
                raise ValueError('Color must be a tuple of 3 elems')
            s._graphics[y*s._bcWidth+x] = (color[2], color[1], color[0])
        else:
            raise ValueError('Color must be a tuple of 3 elems')


    def write(s, file):
        with open(file, 'wb') as f:
            f.write(pack('<HLHHL', 
                   s._bfType, 
                   s._bfSize, 
                   s._bfReserved1, 
                   s._bfReserved2, 
                   s._bfOffBits)) # Writing BITMAPFILEHEADER
            f.write(pack('<LHHHH', 
                   s._bcSize, 
                   s._bcWidth, 
                   s._bcHeight, 
                   s._bcPlanes, 
                   s._bcBitCount)) # Writing BITMAPINFO
            for px in s._graphics:
                f.write(pack('<BBB', *px))
            for i in range (0, (s._bcWidth*3) % 4):
                f.write(pack('B', 0))

def ReadBMP(path):

    image_file = open(path, "rb")

    image_file.seek(18)
    width = unpack('i', image_file.read(4))[0]
    height = unpack('i', image_file.read(4))[0]
    #print(width, height)
    image_file.seek(0,0)
    image_file.seek(54)

    rows = []
    row = []
    pixel_index = 0

    while True:
        if pixel_index == width:
            pixel_index = 0
            rows.insert(0, row)
            row = []
        pixel_index += 1

        r_string = image_file.read(1)
        g_string = image_file.read(1)
        b_string = image_file.read(1)

        if len(r_string) == 0:
            if len(rows) != height:
                print("Warning!!! Read to the end of the file at the correct sub-pixel (red) but we've not read 1080 rows!")
            break

        if len(g_string) == 0:
            print ("Warning!!! Got 0 length string for green. Breaking.")
            break

        if len(b_string) == 0:
            print ("Warning!!! Got 0 length string for blue. Breaking.")
            break

        r = ord(r_string)
        g = ord(g_string)
        b = ord(b_string)

        pixels = []
        pixels.append(b)
        pixels.append(g)
        pixels.append(r)
        row.append(pixels)
        #row.append(g)
        #row.append(r)

    image_file.close()

    return rows

def WriteBMP(pixels, filename):
    b = Bitmap(len(pixels[0]), len(pixels))
    for row in range(0, len(pixels)):
        for column in range (0, len(pixels[0])):
            #print(rows[i][j])
            b.setPixel(column, len(pixels)-row-1, tuple(pixels[row][column]))
    b.write(filename)
