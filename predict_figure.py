from jpg_to_data import *
from models import *
from math import sqrt
import matplotlib.pyplot as plt
# D:\repnoe\test\images


def count_radius(rad, prev_rad, up):
    if up:
        if rad == 0.5:
            prev_rad = rad
            rad = rad * 1.5
        else:
            if prev_rad < rad:
                prev_rad = rad + (rad - prev_rad)
            copy = rad
            rad = (prev_rad + rad) / 2
            prev_rad = copy
    else:
        if rad == 0.5:
            prev_rad = rad
            rad = rad * 0.5
        else:
            if prev_rad > rad:
                prev_rad = rad - (prev_rad - rad)
            copy = rad
            rad = (prev_rad + rad) / 2
            prev_rad = copy
    return rad, prev_rad


def create_model_to_data(data, figure, data_middle_in_trans, before, after, directory='', button=None):
    middle_model = -3
    prev_radius = 1
    radius = 0.5
    length = len(data) - before - after

    while abs(round(middle_model, 2) - round(data_middle_in_trans, 2)) > 0.0001:
        model_photos(radius, length, figure, before=before, after=after)
        jpg_to_clear_data(figure=f'for_model_{figure}', directory='model')

        # if directory == '':
        middle_model = get_middle_in_trans(get_clear_data(f'model//for_model_{figure}_data.txt'))
        # else:
        #    middle_model = get_middle_in_trans(get_clear_data(f'{directory}//data.txt'))
        if middle_model < data_middle_in_trans:
            radius, prev_radius = count_radius(radius, prev_radius, False)
        else:
            radius, prev_radius = count_radius(radius, prev_radius, True)
        print(f'пока радиус под модель {figure} -', radius)
        # if button is not None:
            # button.setText(f'пока радиус под модель {figure} -' + str(radius))


def make_models(data, directory='', button=None):
    before, after = get_trans_parameters(data)
    data_middle_in_trans = get_middle_in_trans(data)
    print('до кривой -', before)
    print('после -', after)
    print('среднее в транзите -', data_middle_in_trans)

    create_model_to_data(data, 'circle', data_middle_in_trans, before, after, directory=directory, button=button)
    create_model_to_data(data, 'cube', data_middle_in_trans, before, after, directory=directory, button=button)
    create_model_to_data(data, 'clock', data_middle_in_trans, before, after, directory=directory, button=button)


def compare_with(figure, data):
    # сравнивает два списка 
    with open(f'model//for_model_{figure}_data.txt', 'r') as f:
        model = [float(i) for i in f.read().split()]
    
    diff = sqrt(sum([((data[i] - model[i]) ** 2) for i in range(len(data))]) / len(data))
    return diff


def figure_choice(data, directory='', button=None):
    # подгоняет модели
    make_models(data, directory=directory, button=button)
    # предоставляет значения в удобном виде
    probabilities = {
        'circle': compare_with('circle', data),
        'cube': compare_with('cube', data),
        'clock': compare_with('clock', data)
    }
    return probabilities


def main(directory):
    # данные из directory берет результат от figure_choice и красиво выводит
    data = get_clear_data(directory)
    # print('данные пользователя: \n', data)

    analys = figure_choice(data)
    maxx = 1
    for item in analys.keys():
        # print(item, '\t- error', round(analys[item], 5))
        if analys[item] < maxx:
            maxx = analys[item]
            maxx_name = item
    # print()
    # print('most probably:', maxx_name)

    # plot results
    with open(f'model//for_model_circle_data.txt', 'r') as f:
        circle = [float(i) for i in f.read().split()]

    with open(f'model//for_model_cube_data.txt', 'r') as f:
        cube = [float(i) for i in f.read().split()]

    with open(f'model//for_model_clock_data.txt', 'r') as f:
        clock = [float(i) for i in f.read().split()]

    fig, axs = plt.subplots(1, 3)
    axs[0].plot(list(range(len(data))), data, 'r')
    axs[0].plot(list(range(len(circle))), circle, label='circle')
    axs[0].legend(loc=1)
    
    axs[1].plot(list(range(len(data))), data, 'r')
    axs[1].plot(list(range(len(cube))), cube, label='cube')
    axs[1].legend(loc=1)
    
    axs[2].plot(list(range(len(data))), data, 'r')
    axs[2].plot(list(range(len(clock))), clock, label='clock')
    axs[2].legend(loc=1)
    
    plt.suptitle('models and data')
    plt.show()


def for_app(directory, button=None):
    # данные из directory берет результат от figure_choice и красиво выводит
    jpg_to_clear_data(directory=directory, real_dir='1')
    data = get_clear_data(directory + '\\data.txt')
    # print('данные пользователя: \n', data)

    analys = figure_choice(data, directory=directory, button=button)
    maxx = 1
    for item in analys.keys():
        # print(item, '\t- error', round(analys[item], 5))
        if analys[item] < maxx:
            maxx = analys[item]
            maxx_name = item
    # print()
    # print('most probably:', maxx_name)

    # plot results
    with open(f'model//for_model_circle_data.txt', 'r') as f:
        circle = [float(i) for i in f.read().split()]

    with open(f'model//for_model_cube_data.txt', 'r') as f:
        cube = [float(i) for i in f.read().split()]

    with open(f'model//for_model_clock_data.txt', 'r') as f:
        clock = [float(i) for i in f.read().split()]

    '''
    fig, axs = plt.subplots(1, 3)
    axs[0].plot(list(range(len(data))), data, 'r')
    axs[0].plot(list(range(len(circle))), circle, label='circle')
    axs[0].legend(loc=1)
    
    axs[1].plot(list(range(len(data))), data, 'r')
    axs[1].plot(list(range(len(cube))), cube, label='cube')
    axs[1].legend(loc=1)
    
    axs[2].plot(list(range(len(data))), data, 'r')
    axs[2].plot(list(range(len(clock))), clock, label='clock')
    axs[2].legend(loc=1)
    
    plt.suptitle('models and data')
    plt.show()
    '''

    return maxx_name, data, circle, cube, clock


if __name__ == '__main__':
    print(for_app('D:\\repnoe\\test\\images'))
