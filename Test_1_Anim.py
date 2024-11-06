import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

# PSO parametreleri
#num_particles = 30  # Parçacık sayısı
num_particles = 60  # Parçacık sayısı
num_dimensions = 2  # Çözüm uzayının boyutu (örneğin, 2D)
iterations = 100  # Maksimum iterasyon sayısı

w = 0.5  # Atalet katsayısı
c1 = 1.5  # Kognitif katsayı
c2 = 1.5  # Sosyal katsayı


# Hedef uygunluk fonksiyonu (örneğin, Rastrigin fonksiyonu)
def fitness_function(x):
    return np.sum(x ** 2 - 10 * np.cos(2 * np.pi * x) + 10)


# Parçacıkların başlangıç pozisyonları ve hızları
positions = np.random.uniform(-10, 10, (num_particles, num_dimensions))
velocities = np.random.uniform(-1, 1, (num_particles, num_dimensions))

# Parçacıkların kendi en iyi konumları ve en iyi skorları
personal_best_positions = positions.copy()
personal_best_scores = np.array([fitness_function(pos) for pos in positions])

# Sürünün en iyi konumu ve en iyi skoru
global_best_position = personal_best_positions[np.argmin(personal_best_scores)]
global_best_score = min(personal_best_scores)

# Grafik ayarları
fig, ax = plt.subplots()
ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)
scat = ax.scatter(positions[:, 0], positions[:, 1], c='blue', label="Particles")
best_point = ax.scatter(global_best_position[0], global_best_position[1], c='red', label="Global Best")
ax.set_title("PSO Optimization - Particle Movement")
ax.legend(loc="upper right")


# Güncelleme fonksiyonu
def update(frame):
    global positions, velocities, global_best_position, global_best_score

    for i in range(num_particles):
        # Uygunluk değerini hesapla
        score = fitness_function(positions[i])

        # Kendi en iyi konum ve skor güncelleme
        if score < personal_best_scores[i]:
            personal_best_scores[i] = score
            personal_best_positions[i] = positions[i]

        # Sürünün en iyi konum ve skor güncelleme
        if score < global_best_score:
            global_best_score = score
            global_best_position = positions[i]

        # Hız güncelleme
        r1, r2 = np.random.rand(2)  # Rastgelelik faktörleri
        velocities[i] = (w * velocities[i] +
                         c1 * r1 * (personal_best_positions[i] - positions[i]) +
                         c2 * r2 * (global_best_position - positions[i]))

        # Pozisyon güncelleme
        positions[i] += velocities[i]

    # Parçacıkların pozisyonlarını güncelleme
    scat.set_offsets(positions)
    best_point.set_offsets(global_best_position)
    ax.set_title(f"PSO Optimization - Iteration {frame + 1} - Best Score: {global_best_score:.4f}")


# Animasyon oluşturma ve GIF olarak kaydetme
ani = FuncAnimation(fig, update, frames=iterations, interval=300, blit=False, repeat=False)

# GIF olarak kaydetme
ani.save("pso_animation4.gif", writer=PillowWriter(fps=5))
plt.show()
