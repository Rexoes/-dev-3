import numpy as np

# Test fonksiyonları

def schwefel(x):
    schwefel.optimum_position = [420.9687] * len(x)  # Her boyut için optimum pozisyon
    return 418.9829 * len(x) - sum([xi * np.sin(np.sqrt(abs(xi))) for xi in x])

def noisy_rastrigin(x, A=10):
    # Gürültü ekliyoruz
    noise = np.random.uniform(-0.5, 0.5)
    noisy_rastrigin.optimum_position = [0, 0]
    return A * len(x) + sum([(xi ** 2 - A * np.cos(2 * np.pi * xi)) for xi in x]) + noise

def rastrigin(x):
    A = 30
    # A = 30
    rastrigin.optimum_position = [0, 0]
    return A * len(x) + sum([(xi ** 2 - A * np.cos(2 * np.pi * xi)) for xi in x])

def ackley(x):
    ackley.optimum_position = [0, 0]
    return -20 * np.exp(-0.2 * np.sqrt(0.5 * sum([xi ** 2 for xi in x]))) - np.exp(0.5 * sum([np.cos(2 * np.pi * xi) for xi in x])) + 20 + np.e

def sphere(x):
    sphere.optimum_position = [0, 0]
    return sum([xi ** 2 for xi in x])

def rosenbrock(x):
    rosenbrock.optimum_position = [1, 1]
    return sum([100 * (x[i + 1] - xi ** 2) ** 2 + (1 - xi) ** 2 for i, xi in enumerate(x[:-1])])

def griewank(x):
    griewank.optimum_position = [0, 0]
    return 1 + sum([xi ** 2 / 4000 for xi in x]) - np.prod([np.cos(xi / np.sqrt(i + 1)) for i, xi in enumerate(x)])

def schaffer_n2(x):
    schaffer_n2.optimum_position = [0, 0]
    return 0.5 + (np.sin(x[0] ** 2 - x[1] ** 2) ** 2 - 0.5) / (1 + 0.001 * (x[0] ** 2 + x[1] ** 2)) ** 2

def beale(x):
    beale.optimum_position = [3, 0.5]
    return (1.5 - x[0] + x[0] * x[1])**2 + (2.25 - x[0] + x[0] * x[1]**2)**2 + (2.625 - x[0] + x[0] * x[1]**3)**2

def levi_n13(x):
    levi_n13.optimum_position = [1, 1]
    return np.sin(3 * np.pi * x[0])**2 + (x[0] - 1)**2 * (1 + np.sin(3 * np.pi * x[1])**2) + (x[1] - 1)**2 * (1 + np.sin(2 * np.pi * x[1])**2)

def easom(x):
    easom.optimum_position = [np.pi, np.pi]
    return -np.cos(x[0]) * np.cos(x[1]) * np.exp(-((x[0] - np.pi)**2 + (x[1] - np.pi)**2))

def michalewicz(x):
    michalewicz.optimum_position = [2.20, 1.57]
    m = 10
    return -sum([np.sin(xi) * (np.sin(i * xi**2 / np.pi)**(2 * m)) for i, xi in enumerate(x, 1)])

def booth(x):
    booth.optimum_position = [1, 3]
    return (x[0] + 2 * x[1] - 7)**2 + (2 * x[0] + x[1] - 5)**2

def himmelblau(x):
    himmelblau.optimum_position = [3, 2]
    return (x[0]**2 + x[1] - 11)**2 + (x[0] + x[1]**2 - 7)**2

# Fonksiyonlara göre bounds (sınır) değerleri
bounds_dict = {
    schwefel: (-500, 500),
    rastrigin: (-5.12, 5.12),
    # rastrigin: (-10, 10),
    noisy_rastrigin: (-10, 10),
    ackley: (-5, 5),
    sphere: (-5.12, 5.12),
    rosenbrock: (-2.048, 2.048),
    griewank: (-600, 600),
    schaffer_n2: (-10, 10),
    beale: (-4.5, 4.5),
    levi_n13: (-10, 10),
    easom: (-10, 10),
    michalewicz: (0, np.pi),
    booth: (-5, 5),
    himmelblau: (-5, 5)
}
