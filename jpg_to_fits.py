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
    # print(r_data.shape)

    ##############################################################################
    # Reshape the image arrays to be 2-dimensional:

    r_data = r_data.reshape(ysize, xsize) # data is now a matrix (ysize, xsize)
    g_data = g_data.reshape(ysize, xsize)
    b_data = b_data.reshape(ysize, xsize)
    # print(r_data.shape)

    ##############################################################################
    # Write out the channels as separate FITS images.
    # Add and visualize header info

    red = fits.PrimaryHDU(data=r_data)
    red.header['LATOBS'] = "32:11:56" # add spurious header info
    red.header['LONGOBS'] = "110:56"
    red.writeto('red.fits')

    green = fits.PrimaryHDU(data=g_data)
    green.header['LATOBS'] = "32:11:56"
    green.header['LONGOBS'] = "110:56"
    green.writeto('green.fits')

    blue = fits.PrimaryHDU(data=b_data)
    blue.header['LATOBS'] = "32:11:56"
    blue.header['LONGOBS'] = "110:56"
    blue.writeto('blue.fits')

    #red.writeto('images_fits/test_r.fits')
    #green.writeto('images_fits/test_g.fits')
    #blue.writeto('images_fits/test_b.fits')
    ##############################################################################
    # Delete the files created
    r = np.sum(red.data)
    b = np.sum(blue.data)
    g = np.sum(green.data)
    
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
    middled_data = [i - min(summed_data) for i in summed_data]
    clear_data = [i / max(middled_data) for i in middled_data]

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
