from PIL import Image, ImageDraw
from jpg_to_data import *


def get_middle_in_trans(data):
    return min(data)
    '''
    minn = min(data)
    in_trans, out_trans = -1, -1
    for i in range(len(data)):
        if (round(minn, 2) - round(data[i], 2)) < 0.005 and in_trans == -1:
            in_trans = i
        if (round(minn, 2) - round(data[i], 2)) < 0.005 and in_trans != -1:
            out_trans = i
    
    middle_in_trans = sum(data[in_trans: out_trans + 1]) / (out_trans - in_trans + 1)
    return middle_in_trans
    '''


def get_trans_parameters(data):
    # возвращает кол-во кадров вне транзита вначале и в конце
    beginning = 1
    while round(data[beginning], 2) == round(data[beginning - 1], 2) or data[beginning - 1] == 1.0:
        beginning += 1

    end = len(data) - 1
    while round(data[end], 2) == round(data[end - 1], 2) or data[end] == 1.0:
        end -= 1

    return beginning, len(data) - end


def delete_photos(directory):
    for f in os.listdir(directory):
        os.remove(directory + '//' + f)


def draw_circle(disk, radius, x, width, heights):
    # рисует сферу в опеределенном месте на диске
    new = disk.copy()
    drawer = ImageDraw.Draw(new)

    drawer.ellipse(((x, width // 2 - radius), (x + radius * 2, width // 2 + radius)), 'black')
    return new


def draw_cube(disk, radius, x, width, heights):
    # рисует куб в определенном месте на диске
    new = disk.copy()
    drawer = ImageDraw.Draw(new)
    drawer.rectangle(((x, width // 2 - radius), (x + radius * 2, width // 2 + radius)), 'black')
    return new


def draw_clock(disk, radius, x, width, heights):
    # рисует часы в определенном месте на диске
    new = disk.copy()
    clock = Image.open(f'data/photos_for_model/clock.png')
    w, h = clock.size
    clock_width = int((w / h) * radius)
    clock = clock.resize((clock_width, radius))
    new.paste(clock, (x, width // 2 - radius), clock)#, (x + radius * 2, width // 2 + radius)))
    return new


def model_photos(radius, length, figure, before=0, after=0):
    # перебирает позиции сферы и сохраняет фотки
    delete_photos(f'images/images_for_model_{figure}')  # удаление предыдущей модели

    disk = Image.open(f'data/photos_for_model/disk.png')
    width, heights = disk.size
    
    circle_radius = int(heights * radius)
    pix_per_cadr = (heights * 1.5 + circle_radius) // length
    
    for i in range(before):
        new = disk.copy()
        new.save(f'images/images_for_model_{figure}/{i}.jpg')

    for i in range(before, length + before):
        x = int((i - before) * pix_per_cadr - circle_radius * 2)
        if figure == 'circle':
            with_bal = draw_circle(disk, circle_radius, x, width, heights)
        elif figure == 'cube':
            with_bal = draw_cube(disk, circle_radius, x, width, heights)
        elif figure == 'clock':
            with_bal = draw_clock(disk, circle_radius, x, width, heights)
        with_bal.save(f'images/images_for_model_{figure}/{i}.jpg')

    for i in range(length + before, length + before + after):
        new = disk.copy()
        new.save(f'images/images_for_model_{figure}/{i}.jpg')


def create_model(radius, length):
    model_photos(radius, length, 'circle')
    jpg_to_clear_data('for_model_circle', 'model')


def create_model_for_user():
    radius = 0.2
    length = 30
    figure = 'clock'
    before = 0
    after = 0
    model_photos(radius, length, figure, before=before, after=after)


if __name__ == '__main__':
    # create_model(0.2, 30)
    create_model_for_user()
    #jpg_to_clear_data('for_model_clock', 'model')
