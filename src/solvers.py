import numpy as np
from src.physics import g
from src.runge_kutta import runge_kutta_4  # Импортируем функцию из нового файла


class ProjectileMotion:
    def __init__(self, v0, theta, t_max, dt=0.01):
        self.v0 = v0
        self.theta = np.radians(theta)  # Преобразуем угол из градусов в радианы
        self.t_max = t_max
        self.dt = dt

        # Начальные условия: [x, vx, y, vy]
        self.y0 = [0, v0 * np.cos(self.theta), 0, v0 * np.sin(self.theta)]

    def projectile_motion_numerical(self, t, y, g):
        """
        Численное решение уравнений движения тела с использованием метода Рунге-Кутты.

        Параметры:
        t - время
        y - вектор состоящий из [x, vx, y, vy], где:
            x - положение по оси X (горизонтальное)
            vx - скорость по оси X
            y - положение по оси Y (вертикальное)
            vy - скорость по оси Y
        g - ускорение свободного падения

        Возвращает:
        - dx/dt = vx (горизонтальная скорость)
        - dvx/dt = 0 (горизонтальное ускорение равно нулю, так как сопротивление воздуха не учитывается)
        - dy/dt = vy (вертикальная скорость)
        - dvy/dt = -g (ускорение в вертикальном направлении, равное -g, где g - ускорение свободного падения)
        """
        x, vx, y, vy = y
        return [vx, 0, vy, -g]

    def solve_trajectory(self):
        """
        Решает задачу о движении тела численно методом Рунге-Кутты 4-го порядка.

        Параметры:
        v0 - начальная скорость тела (м/с)
        theta - угол запуска тела относительно горизонтали (градусы)
        t_max - максимальное время моделирования (секунды)
        dt - шаг времени для численного решения (по умолчанию 0.01)

        Возвращает:
        - t - массив временных точек
        - x - массив значений положения тела по оси X
        - y - массив значений положения тела по оси Y
        """
        # Инициализация временных точек
        t_vals = [0]
        y_vals = [self.y0]

        # Инициализируем параметры времени
        t = 0
        y = self.y0

        # Итеративное численное решение с шагом dt
        while t < self.t_max:
            y = runge_kutta_4(self.projectile_motion_numerical, t, y, self.dt, g)
            t += self.dt
            t_vals.append(t)
            y_vals.append(y)

        # Преобразуем список состояний в массив для удобства
        y_vals = np.array(y_vals)

        # Возвращаем временные точки и координаты
        return t_vals, y_vals[:, 0], y_vals[:, 2]  # Возвращаем x и y позиции


class ProjectileMotionWithAirResistance(ProjectileMotion):
    def __init__(self, v0, theta, t_max, g, Cd, rho, A, m, dt=0.01):
        super().__init__(v0, theta, t_max, dt)
        self.Cd = Cd  # Коэффициент сопротивления
        self.rho = rho  # Плотность воздуха
        self.A = A  # Площадь поперечного сечения тела
        self.m = m  # Масса тела
        self.g = g  # Ускорение свободного падения

    def projectile_motion_numerical(self, t, y, g):
        """Численное решение уравнений движения тела с учетом сопротивления воздуха."""
        x, vx, y, vy = y
        v = np.sqrt(vx ** 2 + vy ** 2)  # Модуль скорости
        # Сила сопротивления (направлена против скорости)
        Fx = -0.5 * self.Cd * self.rho * self.A * v * vx / self.m
        Fy = -0.5 * self.Cd * self.rho * self.A * v * vy / self.m

        # Уравнения движения с учетом сопротивления
        dxdt = vx
        dvxdt = Fx  # Горизонтальная сила сопротивления
        dydt = vy
        dvydt = -self.g + Fy  # Вертикальная сила: гравитация + сопротивление

        return [dxdt, dvxdt, dydt, dvydt]

    import numpy as np

    def solve_trajectory(self):
        """Решает задачу о движении тела с учетом сопротивления воздуха численно методом Рунге-Кутты 4-го порядка."""
        # Инициализация временных точек
        t_vals = [0]
        y_vals = [self.y0]

        # Инициализируем параметры времени
        t = 0
        y = self.y0

        # Итеративное численное решение с шагом dt
        while t < self.t_max:
            y = runge_kutta_4(self.projectile_motion_numerical, t, y, self.dt, self.g)
            t += self.dt
            t_vals.append(t)
            y_vals.append(y)

            # Проверяем, если снаряд упал ниже оси X
            if y[2] < 0:  # Если положение по Y меньше нуля (снаряд упал)
                y[2] = 0  # Обрезаем значение по Y до 0 (снаряд не может быть ниже земли)
                y[3] = 0  # Вертикальная скорость также становится 0, так как снаряд не двигается

        # Преобразуем список состояний в массив для удобства
        y_vals = np.array(y_vals)

        return t_vals, y_vals[:, 0], y_vals[:, 2]
