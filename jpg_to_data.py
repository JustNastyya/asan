import numpy as np
from PIL import Image
from astropy.io import fits
import os
from scipy.stats import gmean


def jpg_to_num(image, filename='-1'):
    # открывает фотку и добавляет ее ргб к data/raw_data.txt
    r, g, b = image.split()
    r_data = np.array(r.getdata()) # data is now an array of length ysize*xsize
    g_data = np.array(g.getdata())
    b_data = np.array(b.getdata())
    
    r = np.sum(r_data)
    b = np.sum(b_data)
    g = np.sum(g_data)
    
    if filename != '-1':
        with open("data//raw_data.txt", "a") as myfile:
            myfile.write(' '.join([filename[:-4], str(r.item()), str(b.item()), str(g.item()), '\n']))
    else:
        pass


def clear_data(filename):
    # открывает data//raw_data.txt очищает данные и сохраняет в filename
    raw_data = open('data//raw_data.txt')
    raw_data = [[int(j) for j in i.split()] for i in raw_data.readlines()]

    sorted_data = sorted(raw_data, key=lambda a: a[0], reverse=False)
    data = [sum(data[1:]) for data in sorted_data]

    clear_data = [i / max(data) for i in data]

    clear_data_file = open(filename, 'w')
    for data in clear_data:
        clear_data_file.write(str(data) + ' ')
    
    clear_data_file.close()


def jpg_to_clear_data(figure='circle', directory='data', real_dir='-1', print_done=False):
    # берет фотки из images//images_{figure}, сохраняет в data/raw_data.txt по каналам
    # вызывает clear_data и передает {directory}//{figure}_data.txt для сохранения чистых данных
    if real_dir == '-1':
        if 'raw_data.txt' in os.listdir('data'):
            os.remove('data//raw_data.txt')
        for f in os.listdir(f'images//images_{figure}'):
            image = Image.open(f'images/images_{figure}/{f[:-4]}.jpg')
            jpg_to_num(image, f)
        
        clear_data(f'{directory}//{figure}_data.txt')
    else:
        if 'raw_data.txt' in os.listdir('data'):
            os.remove('data//raw_data.txt')
        for f in os.listdir(directory):
            if f[-4:] != '.txt':
                image = Image.open(f'{directory}\\{f[:-4]}.jpg')
                jpg_to_num(image, f)
                if print_done:
                    print(f, '- обработан')
        
        clear_data(f'{directory}//data.txt')


def get_clear_data(directory):  # model//for_model_{figure}_data.txt
    with open(directory, 'r') as f:
        data = [float(i) for i in f.read().split()]
    return data


if __name__ == '__main__':
    jpg_to_clear_data(figure='clock', directory='data')
