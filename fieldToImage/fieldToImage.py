from PIL import Image

inputFile = 'layout.txt'
outputFile = 'output%0d.png'

L_image = Image.open('l.png')
J_image = Image.open('j.png')
T_image = Image.open('t.png')
O_image = Image.open('o.png')
I_image = Image.open('i.png')
S_image = Image.open('s.png')
Z_image = Image.open('z.png')
blank = None # Image.open('blank.png')

lookup = { 'L': L_image,
           'J': J_image,
           'T': T_image,
           'O': O_image,
           'I': I_image,
           'S': S_image,
           'Z': Z_image,
           '.': blank}
    
def processLines(lines, number):
    canvas = Image.new('RGB', (len(lines[0]) * L_image.size[0], len(lines) * L_image.size[0]), color=0)
    
    tileWidth = L_image.size[0]
    
    for y in range(len(lines)):
        line = lines[y]
        for x in range(len(line)):
            offset = (tileWidth * x, tileWidth* y)
            to_paste = lookup[lines[y][x]]
            if to_paste is not None:
                canvas.paste(to_paste,offset)
    
    canvas.save(outputFile % number)
    
if __name__ == '__main__':
    number = 0
    lines = []
    with open(inputFile, 'r') as f:
        for line in f:
            if len(line) > 2:
                lines.append(line.strip())
            else:
                if len(lines) > 4:
                    processLines(lines, number)
                    number += 1
                    lines = []
    

    
            
        
    
            
            