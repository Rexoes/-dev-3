import numpy as np
from matplotlib import pyplot as plt
from PIL import Image
from io import BytesIO

class Particle:
    def __init__(self, dimension, bounds):
        self.dimension = dimension
        self.bounds = bounds
        self.position = np.random.uniform(bounds[0], bounds[1], dimension)
        self.velocity = np.random.uniform(-1, 1, dimension)
        self.best_position = np.copy(self.position)
        self.best_score = float('inf')

    def update_velocity(self, w, c1, c2, pBest, gBest, velocity_rate):
        r1, r2 = np.random.rand(2)
        inertia = w * self.velocity
        cognitive = c1 * r1 * (self.best_position - self.position)
        social = c2 * r2 * (gBest - self.position)

        self.velocity += inertia + cognitive + social
        max_velocity = self.bounds[1] * velocity_rate / 100
        # print(f"Velocity Limit: [{-max_velocity}, {max_velocity}]")
        self.velocity = np.clip(self.velocity, -max_velocity, max_velocity)

    def update_position(self):
        self.position += self.velocity
        self.position = np.clip(self.position, self.bounds[0], self.bounds[1])

class PSO:
    def __init__(self, num_particle, max_iter, func, dimension, bounds, w_min, w_max, c1_init, c1_final, c2_init, c2_final, velocity_rate):
        # print(f"Gelen Değerler, num_particle: {num_particle}, max_iter: {max_iter}, func: {func}, dimension: {dimension}, bounds: {bounds}, w: {w}, c1: {c1}, c2: {c2}")
        # print(f"Function Test, f(1,1):{func([1,1])}, f(0,0):{func([0,0])})")
        self.num_particle = num_particle
        self.max_iter = max_iter
        self.func = func
        self.dimension = dimension
        self.bounds = bounds
        self.w_min = w_min
        self.w_max = w_max
        self.c1_init = c1_init
        self.c1_final = c1_final
        self.c2_init = c2_init
        self.c2_final = c2_final
        self.velocity_rate = velocity_rate

        self.swarm = [Particle(dimension, bounds) for _ in range(num_particle)]
        self.gBest_position = np.random.uniform(bounds[0], bounds[1], dimension)
        self.gBest_score = float('inf')

        self.frames_contour = []

    def optimize(self):
        for iter in range(1, self.max_iter + 1):

            w = self.w_max - (self.w_max - self.w_min) * (iter / self.max_iter)
            c1 = self.c1_init - (self.c1_init - self.c1_final) * (iter / self.max_iter)
            c2 = self.c2_init + (self.c2_final - self.c2_init) * (iter / self.max_iter)

            for particle in self.swarm:

                fitness = self.func(particle.position)
                if fitness < particle.best_score:
                    particle.best_score = fitness
                    particle.best_position = np.copy(particle.position)

                if fitness < self.gBest_score:
                    self.gBest_score = fitness
                    self.gBest_position = np.copy(particle.position)

            for particle in self.swarm:
                particle.update_velocity(w, c1, c2, particle.best_position, self.gBest_position, self.velocity_rate)
                particle.update_position()

            self.plot_swarm_contour(iter, w, c1, c2, show_particles=True)
            print(f"Iter {iter}/{self.max_iter}, w={w:.4f}, c1={c1:.4f}, c2={c2:.4f}, Best Score: {self.gBest_score:.2e}")

        print(f"{self.func.__name__} function best position: {self.gBest_position}")
        print(f"{self.func.__name__} function best score: {self.gBest_score}")

        return self.frames_contour


    def plot_swarm_contour(self, iter, w, c1, c2, show_particles=False):
        try:
            x = np.linspace(self.bounds[0], self.bounds[1], 100)
            y = np.linspace(self.bounds[0], self.bounds[1], 100)
            X, Y = np.meshgrid(x, y)
            Z = np.array([self.func([x, y]) for x, y in zip(np.ravel(X), np.ravel(Y))]).reshape(X.shape)

            fig, ax = plt.subplots(figsize=(8, 6))  # 6,4
            cp = ax.contourf(X, Y, Z, cmap='viridis', levels=50, alpha=0.8)

            # cmap alabileceği değerler; 'viridis', 'plasma', 'inferno', 'magma', 'cividis'

            #fig.colorbar(cp, ax=ax, shrink=0.85, aspect=10)

            # Colorbar oluştur ve label ekle
            color_bar = fig.colorbar(cp, ax=ax, shrink=0.85, aspect=10)
            color_bar.set_label(f"Fonksiyon Değeri ({self.func.__name__})", fontsize=12)

            # Eksen etiketlerini ekleyelim
            ax.set_xlabel("X", fontsize=12)
            ax.set_ylabel("Y", fontsize=12)

            # Parametreleri ve iterasyon numarasını ekleyelim
            #ax.set_title(f"Iteration= {iteration}, w={self.w}, c1={self.c1}, c2={self.c2}", fontsize=12, loc='center')
            ax.set_title(f"Iteration= {iter}, w={w:.2f}, c1={c1:.2f}, c2={c2:.2f}, p={self.num_particle}, Best Score={self.gBest_score:.4f}", fontsize=10, loc='center', fontweight='bold')

            if show_particles:
                ax.scatter([p.position[0] for p in self.swarm], [p.position[1] for p in self.swarm], color='red', marker='o', s=50, alpha=0.6, label='Particles', zorder=1)
                ax.scatter(self.gBest_position[0], self.gBest_position[1], color='blue', marker='H', s=150,
                           label='Global Best', zorder=3)


            if hasattr(self.func, "optimum_position"):
                ax.scatter(self.func.optimum_position[0], self.func.optimum_position[1], color='green', marker='s', s=100, label='Optimum', zorder=2)

            #x_margin = (self.bounds[1] - self.bounds[0]) * 0.1  # %10 marj ekleyerek genişletiyoruz
            #plt.xlim(self.bounds[0] - x_margin, self.bounds[1] + x_margin)

            plt.xlim(self.bounds[0], self.bounds[1])
            plt.ylim(self.bounds[0], self.bounds[1])
            plt.close(fig)

            buf = BytesIO()
            fig.savefig(buf, format="PNG")
            self.frames_contour.append(Image.open(buf))

        except Exception as e:
            print(f"Error in plot_swarm_contour: {e}")

