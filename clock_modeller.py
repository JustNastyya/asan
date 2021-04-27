from PIL import Image

im = Image.open('data/photos_for_model/clock_almost.png')

pixels = im.load() # список с пикселями
x, y = im.size # ширина (x) и высота (y) изображения
 
for i in range(x):  
    for j in range(y):
        r, g, b = pixels[i, j]
        if r != 0 or g != 0 or b != 0:
            pixels[i, j] = (255, 255, 255)

im.save("smth.png")