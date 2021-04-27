import matplotlib.pyplot as plt
import scipy as sp


def mnkGP(x, y):
    # полиномическая функция для графика
    d = 6 # степень полинома
    fp, residuals, rank, sv, rcond = sp.polyfit(x, y, d, full=True) # Модель
    f = sp.poly1d(fp) # аппроксимирующая функция
    y1=[fp[0] * x[i] ** 2 + fp[1] * x[i] + fp[2] for i in range(0, len(x))] # значения функции a*x**2+b*x+c
    so = round(sum([abs(y[i] - y1[i]) for i in range(0, len(x))]) / (len(x) * sum(y)) * 100, 4) # средняя ошибка
    print('Average quadratic deviation '+str(so)) 
    fx = sp.linspace(x[0], x[-1] + 1, len(x)) # можно установить вместо len(x) большее число для интерполяции
    plt.plot(x, y, label='Original data', markersize=10)
    plt.plot(fx, f(fx), label='experiment model', linewidth=2)
    plt.grid(True)


def show_data(figure):
    with open(f'data//{figure}_data.txt', 'r') as f:
        data = [float(i) for i in f.read().split()]
    
    plt.plot(list(range(len(data))), data, 'r', label='model', markersize=10)
    #mnkGP(list(range(len(data))), data)


def show_model(figure):
    with open(f'model//for_model_{figure}_data.txt', 'r') as f:
        data = [float(i) for i in f.read().split()]
    
    plt.plot(list(range(len(data))), data, 'r', label='model', markersize=10)


if __name__ == '__main__':
    show_model('cube')
    # show_cube_model()
    # show_clock_model()
    plt.show()
