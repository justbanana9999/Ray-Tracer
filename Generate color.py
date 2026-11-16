from PIL import Image

black = Image.new('RGB',(10,10),(0,0,0))
white = Image.new('RGB',(10,10),(255,255,255))

black.save('black.png')
white.save('white.png')