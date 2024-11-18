import numpy as np
from matplotlib import pyplot as plt
from PIL import Image
from io import BytesIO


class Particle:
    def __init__(self, dimensions, bounds):
        self.position = np.random.uniform(bounds[0], bounds[1], dimensions)
        self.velocity = np.random.uniform(-1, 1, dimensions)
        self.best_position = np.copy(self.position)
        self.best_score = float('inf')

class PSO:
    def __init__(self, func, dimensions, bounds, num_particles, max_iter, w_max=0.9, w_min=0.4, c1_initial=2.5, c1_final=0.5, c2_initial=0.5, c2_final=2.5, message_callback=None):
        self.func = func
        self.dimensions = dimensions
        self.bounds = bounds
        self.num_particles = num_particles
        self.max_iter = max_iter
        self.w=w_max
        self.c1=c1_initial
        self.c2=c2_final
        self.w_max = w_max
        self.w_min = w_min
        self.c1_initial = c1_initial
        self.c1_final = c1_final
        self.c2_initial = c2_initial
        self.c2_final = c2_final
        self.swarm = [Particle(dimensions, bounds) for _ in range(num_particles)]
        self.global_best_position = np.random.uniform(bounds[0], bounds[1], dimensions)
        self.global_best_score = float('inf')
        self.frames_contour = []
        self.frames_2d = []
        self.frames_3d = []
        self.message_callback = message_callback  # Callback fonksiyonu ekledik

    def optimize(self):
        for iter in range(1, self.max_iter + 1):

            # Adaptif w, c1, c2 hesaplama
            self.w = self.w_max - (self.w_max - self.w_min) * (iter / self.max_iter)
            self.c1 = (self.c1_final - self.c1_initial) * (iter / self.max_iter) + self.c1_initial
            self.c2 = (self.c2_final - self.c2_initial) * (1 - (iter / self.max_iter)) + self.c2_initial

            for particle in self.swarm:
                fitness = self.func(particle.position)
                if fitness < particle.best_score:
                    particle.best_score = fitness
                    particle.best_position = np.copy(particle.position)

                if fitness < self.global_best_score:
                    self.global_best_score = fitness
                    self.global_best_position = np.copy(particle.position)

            for particle in self.swarm:
                inertia = self.w * particle.velocity
                cognitive = self.c1 * np.random.rand(self.dimensions) * (particle.best_position - particle.position)
                social = self.c2 * np.random.rand(self.dimensions) * (self.global_best_position - particle.position)
                particle.velocity = inertia + cognitive + social
                particle.position += particle.velocity
                particle.position = np.clip(particle.position, self.bounds[0], self.bounds[1])


            self.plot_swarm_contour(iter, show_particles=True)
            self.plot_swarm_2d(iter, show_particles=True)

            # 3D görseli her iterasyonda kaydet
            self.plot_swarm_3d(iteration=iter, show_particles=True)

            print(f"Iter {iter}/{self.max_iter}, w={self.w:.4f}, c1={self.c1:.4f}, c2={self.c2:.4f}, Best Score: {self.global_best_score:.4f}")

            # Her iterasyon sonrası mesaj gönder
            if self.message_callback:
                message = f"Iter {iter}/{self.max_iter}, w={self.w:.4f}, c1={self.c1:.4f}, c2={self.c2:.4f}, Best Score: {self.global_best_score:.4e}"
                self.message_callback(message)

        # Optimize tamamlandığında gif oluştur
        self.combine_gifs_3d(output_path='pso_3d_animation.gif')

        print(f"{self.func} function best position: {self.global_best_position}")
        print(f"{self.func} function best score: {self.global_best_score}")



        return self.combine_gifs()

    def initialize_plot(self, show_particles=False):
        # Başlangıç durumunu göster
        self.plot_swarm_contour(0, show_particles)
        self.plot_swarm_2d(0, show_particles)

    def plot_swarm_contour(self, iteration, show_particles=False):
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
            color_bar.set_label("Fonksiyon Değeri", fontsize=12)

            # Eksen etiketlerini ekleyelim
            ax.set_xlabel("X", fontsize=12)
            ax.set_ylabel("Y", fontsize=12)

            # Parametreleri ve iterasyon numarasını ekleyelim
            #ax.set_title(f"Iteration= {iteration}, w={self.w}, c1={self.c1}, c2={self.c2}", fontsize=12, loc='center')
            ax.set_title(f"Iteration= {iteration}, w={self.w:.2f}, c1={self.c1:.2f}, c2={self.c2:.2f}, Best Score={self.global_best_score:.2e}", fontsize=10, loc='center')

            if show_particles:
                ax.scatter([p.position[0] for p in self.swarm], [p.position[1] for p in self.swarm], color='red', marker='o', s=50, alpha=0.6, label='Particles', zorder=1)
                ax.scatter(self.global_best_position[0], self.global_best_position[1], color='blue', marker='H', s=150,
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

    def plot_swarm_2d(self, iteration, show_particles=False):
        try:
            fig, ax = plt.subplots(figsize=(8, 6))  #8,4
            x = np.linspace(self.bounds[0], self.bounds[1], 100)
            y = [self.func([xi, 0]) for xi in x]
            ax.plot(x, y, 'k-', linewidth=1.5, label="Test Funct")

            # Parametreleri ve iterasyon numarasını ekleyelim
            #ax.set_title(f"Iteration={iteration}, w={self.w}, c1={self.c1}, c2={self.c2}", fontsize=12, loc='center')
            ax.set_title(f"Iteration={iteration}, w={self.w:.2f}, c1={self.c1:.2f}, c2={self.c2:.2f}, Best Score={self.global_best_score:.2e}", fontsize=10, loc='center')

            # Eksen etiketlerini ekleyelim
            ax.set_xlabel("Bounds", fontsize=12)
            ax.set_ylabel("Score", fontsize=12)

            if show_particles:
                ax.scatter([p.position[0] for p in self.swarm], [self.func([p.position[0], 0]) for p in self.swarm], color='red', s=50, alpha=0.6, label='Particles', zorder=1)
                ax.scatter(self.global_best_position[0], self.func([self.global_best_position[0], 0]), color='blue',
                           marker='H', s=150, label='Global Best', zorder=3)


            if hasattr(self.func, "optimum_position"):
                ax.scatter(self.func.optimum_position[0], self.func([self.func.optimum_position[0], 0]), color='green', marker='s', s=100,  label='Optimum', zorder=2)

            #plt.xlim(self.bounds[0], self.bounds[1])

            #ax.legend(loc='upper left', bbox_to_anchor=(1.1, 1.15), fontsize=8, frameon=True, handlelength=1,
             #         handleheight=1, handletextpad=0.5, borderaxespad=0.5, labelspacing=0.5)

            #ax.legend(loc='upper left')
            ax.legend(loc='upper left', bbox_to_anchor=(-0.17, 1.15), borderaxespad=0, fontsize=8, frameon=False, labelspacing=0.8, handletextpad=0.4, borderpad=1.0)

            #x_margin = (self.bounds[1] - self.bounds[0]) * 0.1  # %10 marj ekleyerek genişletiyoruz
            #plt.xlim(self.bounds[0] - x_margin, self.bounds[1] + x_margin)
            plt.xlim(self.bounds[0], self.bounds[1])
            plt.ylim(min(y) - 5, max(y) + 5)
            plt.close(fig)

            buf = BytesIO()
            fig.savefig(buf, format="PNG")
            self.frames_2d.append(Image.open(buf))
        except Exception as e:
            print(f"Error in plot_swarm_2d: {e}")

    def combine_gifs(self, output_path='combined_animation.gif'):
        try:
            combined_frames = []
            for frame1, frame2 in zip(self.frames_contour, self.frames_2d):
                combined_frame = Image.new('RGBA', (frame1.width + frame2.width, frame1.height))
                combined_frame.paste(frame1, (0, 0))
                combined_frame.paste(frame2, (frame1.width, 0))
                combined_frames.append(combined_frame)

            if combined_frames:
                combined_frames[0].save(output_path, save_all=True, append_images=combined_frames[1:], duration=200, loop=0)
                output_path = f'{self.func.__name__}_animation.gif'
                combined_frames[0].save(output_path, save_all=True, append_images=combined_frames[1:], duration=200,loop=0)
                return combined_frames
            else:
                print("No frames were generated for the animation.")
                return None
        except Exception as e:
            print(f"Error in combine_gifs: {e}")
            return None

    def plot_swarm_3d(self, iteration, show_particles=True):
        try:
            x = np.linspace(self.bounds[0], self.bounds[1], 100)
            y = np.linspace(self.bounds[0], self.bounds[1], 100)
            X, Y = np.meshgrid(x, y)
            Z = np.array([self.func([x, y]) for x, y in zip(np.ravel(X), np.ravel(Y))]).reshape(X.shape)

            fig = plt.figure(figsize=(10, 8))
            ax = fig.add_subplot(111, projection='3d')

            # Yüzey grafiği (alpha değeri düşük, zorder=1 ile)
            surf = ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='none', alpha=0.3, zorder=1)
            ax.contourf(X, Y, Z, zdir='z', offset=np.min(Z) - 10, cmap='viridis', levels=50, alpha=0.5)

            # Colorbar ekleyelim
            color_bar = fig.colorbar(surf, shrink=0.6, aspect=10)
            color_bar.set_label("Fonksiyon Değeri", fontsize=12)

            # Eksen etiketleri ve başlık
            ax.set_xlabel('X', labelpad=10)
            ax.set_ylabel('Y', labelpad=10)
            ax.set_zlabel('f(X, Y)', labelpad=10)
            ax.set_title(
                f"Iteration {iteration}, w={self.w:.2f}, c1={self.c1:.2f}, c2={self.c2:.2f}, Best Score={self.global_best_score:.2e}",
                fontsize=12, pad=20)

            # Eksen sınırlarını ayarlayarak kaymayı önleyin
            ax.set_xlim(self.bounds[0], self.bounds[1])
            ax.set_ylim(self.bounds[0], self.bounds[1])
            ax.set_zlim(np.min(Z) - 10, np.max(Z) + 10)

            # Parçacıkları göster (daha yüksek zorder ve depthshade kapalı)
            if show_particles:
                particles_x = [p.position[0] for p in self.swarm]
                particles_y = [p.position[1] for p in self.swarm]
                particles_z = [self.func([p.position[0], p.position[1]]) for p in self.swarm]
                ax.scatter(particles_x, particles_y, particles_z, color='black', s=80, marker='o', label='Particles',
                           zorder=6, depthshade=False)

            # Global best ve optimum noktaları göster (daha yüksek zorder ile)
            gbest_x, gbest_y = self.global_best_position[0], self.global_best_position[1]
            gbest_z = self.func(self.global_best_position)
            ax.scatter(gbest_x, gbest_y, gbest_z, color='red', marker='*', s=200, label='Global Best', zorder=7,
                       depthshade=False)

            if hasattr(self.func, "optimum_position"):
                opt_x, opt_y = self.func.optimum_position
                opt_z = self.func([opt_x, opt_y])
                ax.scatter(opt_x, opt_y, opt_z, color='lime', marker='s', s=150, label='Optimum', zorder=8,
                           depthshade=False)

            # Efsane (legend) ekle ve hizalamayı ayarla
            ax.legend(loc='upper left', fontsize=12, frameon=True, borderpad=1.0)

            # Görüş açısını ayarlayarak daha iyi bir perspektif elde edin
            ax.view_init(elev=30, azim=45)

            plt.tight_layout()
            plt.close(fig)

            # Görseli bellekte sakla
            buf = BytesIO()
            fig.savefig(buf, format="PNG")
            self.frames_3d.append(Image.open(buf))

        except Exception as e:
            print(f"Error in plot_swarm_3d: {e}")

    def combine_gifs_3d(self, output_path='pso_3d_animation.gif'):
        try:
            if self.frames_3d:
                self.frames_3d[0].save(output_path, save_all=True, append_images=self.frames_3d[1:], duration=200,
                                       loop=0)
                print(f"GIF kaydedildi: {output_path}")
            else:
                print("No frames generated for 3D animation.")
        except Exception as e:
            print(f"Error in combine_gifs_3d: {e}")
