import matplotlib.pyplot as plt
import numpy as np


def plot_trajectory(x, y):
    """
    Построение траектории движения тела.
    """
    if not isinstance(x, (np.ndarray, list)) or not isinstance(y, (np.ndarray, list)):
        raise ValueError("Ожидаются массивы для x и y.")

    plt.figure(figsize=(8, 5))
    plt.plot(x, y, label='Траектория движения')
    plt.xlabel('Дальность (м)')
    plt.ylabel('Высота (м)')
    plt.title('Траектория движения тела')
    plt.legend()
    plt.grid()
    plt.show()
