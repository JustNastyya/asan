import numpy as np
from PIL import Image
from astropy.io import fits
import os


def jpg_to_fits(filename):
    image = Image.open(f'images_jpg/{filename[:-4]}.jpg')
    xsize, ysize = image.size

    ##############################################################################
    # Split the three channels (RGB) and get the data as Numpy arrays. The arrays
    # are flattened, so they are 1-dimensional:

    r, g, b = image.split()
    r_data = np.array(r.getdata()) # data is now an array of length ysize*xsize
    g_data = np.array(g.getdata())
    b_data = np.array(b.getdata())
    
    r = np.sum(r_data)
    b = np.sum(b_data)
    g = np.sum(g_data)
    
    with open("raw_data.txt", "a") as myfile:
        myfile.write(' '.join([filename[:-4], str(r.item()), str(b.item()), str(g.item()), '\n']))
        
    os.remove('red.fits')
    os.remove('green.fits')
    os.remove('blue.fits')


def clear_data():
    raw_data = open('raw_data.txt')
    raw_data = [[int(j) for j in i.split()[:-1]] for i in raw_data.readlines()]

    sorted_data = sorted(raw_data, key=lambda a: a[0], reverse=False)
    summed_data = [sum(data[1:]) for data in sorted_data]
    clear_data = [i / max(summed_data) for i in summed_data]

    clear_data_file = open('data.txt', 'w')
    for data in clear_data:
        clear_data_file.write(str(data) + ' ')
    
    clear_data_file.close()


def main():
    for f in os.listdir('images_jpg'):
        jpg_to_fits(f)
    
    clear_data()


if __name__ == '__main__':
    main()
