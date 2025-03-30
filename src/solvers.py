import numpy as np
from scipy.integrate import solve_ivp
from src.physics import g

def projectile_motion_numerical(t, y, g):
    """
    Численное решение уравнений движения тела.
    y = [x, vx, y, vy]
    """
    x, vx, y, vy = y
    return [vx, 0, vy, -g]

def solve_trajectory(v0, theta, t_max, dt=0.01):
    """
    Решает задачу о движении тела численно методом Рунге-Кутты.
    """
    theta = np.radians(theta)
    y0 = [0, v0 * np.cos(theta), 0, v0 * np.sin(theta)]
    t_eval = np.linspace(0, t_max, int(t_max / dt))  # Исправлено на linspace
    sol = solve_ivp(projectile_motion_numerical, [0, t_max], y0, t_eval=t_eval, args=(g,))
    return sol.t, sol.y[0], sol.y[2]
