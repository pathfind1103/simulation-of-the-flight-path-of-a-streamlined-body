import numpy as np

g = 9.81  # ускорение свободного падения

def trajectory_equations(v0, theta):
    """
    Возвращает аналитические выражения для движения тела без сопротивления воздуха.
    """
    theta = np.radians(theta)

    def x(t):
        return v0 * np.cos(theta) * t

    def y(t):
        return v0 * np.sin(theta) * t - 0.5 * g * t ** 2

    return x, y


def flight_params(v0, theta):
    """
    Вычисляет дальность полета, высоту подъема, время полета.
    """
    theta = np.radians(theta)
    T = 2 * v0 * np.sin(theta) / g  # Время полета
    H = (v0 ** 2 * np.sin(theta) ** 2) / (2 * g)  # Высота подъема
    L = (v0 ** 2 * np.sin(2 * theta)) / g  # Дальность полета
    return T, H, L
