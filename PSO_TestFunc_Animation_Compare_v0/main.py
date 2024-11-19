from sympy.physics.units import velocity

from pso import PSO
from functions import *
from PIL import Image

def combine_gifs(frames_contour0, frames_contour1, frames_contour2, frames_contour3, frames_contour4, frames_contour5, output_path = 'combined_anim.gif'):
    try:
        combined_frames = []
        for frame1, frame2, frame3, frame4, frame5, frame6 in zip(frames_contour0, frames_contour1, frames_contour2, frames_contour3, frames_contour4, frames_contour5):
            combined_frame = Image.new('RGBA', (frame1.width + frame2.width + frame3.width, frame1.height + frame3.height))
            combined_frame.paste(frame1, (0, 0))
            combined_frame.paste(frame2, (frame1.width, 0))
            combined_frame.paste(frame3, (frame1.width + frame2.width, 0))
            combined_frame.paste(frame4, (0, frame3.height))
            combined_frame.paste(frame5, (frame3.width, frame3.height))
            combined_frame.paste(frame6, (frame3.width + frame4.width, frame3.height))
            combined_frames.append(combined_frame)

        if combined_frames:
            combined_frames[0].save(output_path, save_all=True, append_images=combined_frames[1:], duration=300, loop=0)
            # output_path = f'{self.func.__name__}_animation.gif'
            # combined_frames[0].save(output_path, save_all=True, append_images=combined_frames[1:], duration=200,loop=0)
            return combined_frames
        else:
            print("No frames were generated for the animation.")
            return None
    except Exception as e:
        print(f"Error in combine_gifs: {e}")
        return None

if __name__ == "__main__":
    # func = schwefel
    # bounds = bounds_dict.get(schwefel)
    # parameters = [
    #     (0.1, 2, 2),
    #     (0.5, 2, 2),
    #     (0.9, 2, 2),
    #     (0.5, 0.5, 5.5),
    #     (0.5, 2.5, 2.5),
    #     (0.5, 5.5, 0.5)
    # ]

    # swarm_size = 10, iteration = 100, velocity_rate = 10
    # func = rastrigin
    # bounds = bounds_dict.get(rastrigin)
    # parameters = [
    #     (0.1, 2, 2),
    #     (0.5, 2, 2),
    #     (0.9, 2, 2),
    #     (0.1, 0.5, 2),
    #     (0.1, 2, 2),
    #     (0.1, 4, 2)
    # ]

    # swarm_size = 10, iteration = 100, velocity_rate = 10
    # func = rastrigin
    # bounds = bounds_dict.get(rastrigin)
    # parameters = [
    #     (0.1, 1.5, 1.5),
    #     (0.5, 1.5, 1.5),
    #     (0.9, 1.5, 1.5),
    #     (0.1, 2, 0.5),
    #     (0.1, 2, 2),
    #     (0.1, 2, 4)
    # ]

    # swarm_size = 20, iteration = 100, velocity_rate = 5
    # func = schwefel
    # bounds = bounds_dict.get(schwefel)
    # parameters = [
    #     (0.1, 2, 1.5),
    #     (0.5, 2, 1.5),
    #     (0.9, 2, 1.5),
    #     (0.5, 2, 0.5),
    #     (0.5, 2, 2),
    #     (0.5, 2, 4)
    # ]

    func = rastrigin
    bounds = bounds_dict.get(rastrigin)
    parameters = [
        (0.1, 0.5, 2, 5),
        (0.1, 0.5, 2, 10),
        (0.1, 0.5, 2, 20),
        (0.1, 2.5, 2.5, 5),
        (0.1, 2.5, 2.5, 10),
        (0.1, 2.5, 2.5, 20)
    ]

    print(f"Selected Function: {func.__name__}, Bounds: {bounds}")

    frames_contour00 = []
    frames_contour11 = []
    frames_contour22 = []
    frames_contour33 = []
    frames_contour44 = []
    frames_contour55 = []

    swarm_size = 10
    iteration = 100

    for i, (w, c1, c2, p) in enumerate(parameters):
        print(f"Değerler: ({i}), w:{w:.2f}, c1:{c1:.2f}, c2:{c2:.2f}, p:{p:.2f}")
        pso = PSO(num_particle=p, max_iter=iteration, velocity_rate=20, dimension=2, w_min=w, w_max=w, c1_init=c1, c1_final=c1, c2_init=c2, c2_final=c2, func=func, bounds=bounds)
        if i == 0:
            frames_contour00 = pso.optimize()
        elif i == 1:
            frames_contour11 = pso.optimize()
        elif i == 2:
            frames_contour22 = pso.optimize()
        elif i == 3:
            frames_contour33 = pso.optimize()
        elif i == 4:
            frames_contour44 = pso.optimize()
        elif i == 5:
            frames_contour55 = pso.optimize()

    # pso = PSO(num_particle=swarm_size, max_iter=iteration, func=func, bounds=bounds, dimension=2, w_min=0.4, w_max=0.9, c1_init=2.5, c1_final=0.5, c2_init=0.5, c2_final=2.5)
    # pso.optimize()
    # frames_contour33 = pso.optimize()
    #
    # pso = PSO(num_particle=20, max_iter=50, func=func, bounds=bounds, dimension=2, w_min=0.5, w_max=0.5, c1_init=2.5,c1_final=0.5, c2_init=1.5, c2_final=1.5)
    # frames_contour44 = pso.optimize()
    #
    # pso = PSO(num_particle=20, max_iter=50, func=func, bounds=bounds, dimension=2, w_min=0.5, w_max=0.5, c1_init=1.5,c1_final=1.5, c2_init=0.5, c2_final=2.5)
    # frames_contour55 = pso.optimize()

    combine_gifs(frames_contour00, frames_contour11, frames_contour22, frames_contour33, frames_contour44, frames_contour55, output_path = 'combined_anim.gif')

