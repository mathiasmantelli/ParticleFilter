import pygame
import sys
import math
import random
import threading
import time
from agent import Agent
from drawing_pf import Game


class ParticleFilter:
    def __init__(self, landmarks, number_particles, robot, width, height):
        self.landmarks = landmarks
        self.number_particles = number_particles
        self.robot = robot
        self.width = width
        self.height = height
        self.particles = self.create_particles()

    # this function avoids that an agent is spawned on top of a landmark
    def conflict_landmarks(self, test_x, test_y):
        for landmark in self.landmarks:
            land_x, land_y = landmark
            if test_x == land_x:
                return True
            if test_y == land_y:
                return True
        return False

    def create_particles(self):
        column_rand_values = []
        row_rand_values = []
        tetha_rand_values = []
        x = 0

        # compute the pose of the particles to be evenly spread over the environment (but avoiding landmark poses)
        while x < self.number_particles:
            rand_x = random.randint(0, self.width)
            rand_y = random.randint(0, self.height)

            if not self.conflict_landmarks(rand_x, rand_y):
                column_rand_values.append(rand_x)
                row_rand_values.append(rand_y)
                tetha_rand_values.append(random.uniform(-180, 180))
                x += 1

        # create particles
        particle_set = []
        for particle in range(self.number_particles):
            noise_linear = random.uniform(-1.0, 1.0)
            noise_angular = random.uniform(-0.15, 0.15)
            noise_measurement = random.uniform(-1, 1)
            agnt = Agent(
                column_rand_values[particle],
                row_rand_values[particle],
                tetha_rand_values[particle],
                "pink",
                noise_linear,
                noise_angular,
                noise_measurement,
            )
            particle_set.append(agnt)
        return particle_set

    def gaussian(self, mu, sigma, x):
        return math.exp(-((mu - x) ** 2) / (2.0 * sigma**2)) / math.sqrt(
            2.0 * math.pi * sigma**2
        )

    def sampling_particles(self):
        # randomly get the linear and angular motion data to move both the robot and particles
        dist = random.uniform(0, 4.0)
        rot = random.uniform(-0.15, 0.15)

        # move the robot
        self.robot.move(dist, rot, self.width, self.height)

        # move each particle
        for particle in self.particles:
            particle.move(dist, rot, self.width, self.height)

    def weigting_particles(self):
        # get the robot's measurements
        robot_measurements = self.robot.observe(self.landmarks)

        # get each particle's measurements
        particles_measurements = []
        for particle in self.particles:
            particles_measurements.append(particle.observe(self.landmarks))

        # compare the robot's measurements and the particle's
        for particle_index in range(len(particles_measurements)):
            probability = 1.0
            for measurement_index in range(len(particles_measurements[particle_index])):
                probability *= self.gaussian(
                    robot_measurements[measurement_index],
                    15.0, #CHANGE THIS PARAMETER
                    particles_measurements[particle_index][measurement_index],
                )
            probability *= self.gaussian(
                self.robot.pose_theta,
                30.0, #CHANGE THIS PARAMETER
                self.particles[particle_index].pose_theta
            )
            self.particles[particle_index].weight = probability

    def resampling_particles(self):
        # normalize the weights
        total_weight = sum(particle.weight for particle in self.particles)
        if total_weight == 0:
            total_weight = 1
        normalized_weight = [
            particle.weight / total_weight for particle in self.particles
        ]

        # create a new set of 'good' particles
        new_particle_set = []
        for _ in range(len(self.particles)):
            selected_index = self.roulette_wheel_selection(normalized_weight)

            new_particle_set.append(
                Agent(
                    self.particles[selected_index].pose_x,
                    self.particles[selected_index].pose_y,
                    self.particles[selected_index].pose_theta,
                    self.particles[selected_index].color,
                    self.particles[selected_index].noise_linear,
                    self.particles[selected_index].noise_angular,
                    self.particles[selected_index].noise_measurement,
                )
            )
        # copy new particles into the old set
        for particle_index in range(len(new_particle_set)):
            std_pose = 1.5
            self.particles[particle_index].pose_x = (
                new_particle_set[particle_index].pose_x
                + new_particle_set[particle_index].noise_linear
            )
            self.particles[particle_index].pose_y = (
                new_particle_set[particle_index].pose_y
                + new_particle_set[particle_index].noise_linear
            )
            self.particles[particle_index].pose_theta = new_particle_set[
                particle_index
            ].normalize_angle_radians(
                new_particle_set[particle_index].pose_theta
                + new_particle_set[particle_index].noise_angular
            )
            self.particles[particle_index].color = new_particle_set[
                particle_index
            ].color
            self.particles[particle_index].weight = new_particle_set[
                particle_index
            ].weight
            self.particles[particle_index].noise_linear = random.uniform(-1.0, 1.0)
            self.particles[particle_index].noise_angular = random.uniform(-0.15, 0.15)
            self.particles[particle_index].noise_measurement = random.uniform(-1, 1)

    def roulette_wheel_selection(self, weights):
        # Roulette wheel selection based on normalized weights
        r = random.uniform(0, 1)
        cumulative_probability = 0

        for i, weight in enumerate(weights):
            cumulative_probability += weight
            if r <= cumulative_probability:
                return i

    # main function in PF. 1)Sampling; 2)Weighting; 3)Resampling
    def run_particle_filter(self):
        while True:
            # moving the robot and particles
            self.sampling_particles()

            # comparing particles' measurements against robot's
            self.weigting_particles()

            # replacing 'bad' particles with 'good' ones
            self.resampling_particles()

            time.sleep(0.15)


# this function receives the number of landmarks and the dimensions of the world to create an environment with landmarks properly positioned
def prepare_landmarks(number, width, height, dist):
    width_coord = []
    height_coord = []
    if number <= 2:
        height_coord.append(int(height / 2.0))
        width_coord.append(dist)
        width_coord.append(width - dist)
    else:
        half_number = 0
        if number % 2 == 0:
            half_number = int(number / 2.0) - 1
        else:
            half_number = int((number + 1) / 2.0) - 1
        width_coord = [dist, width - dist]
        height_coord = [dist]
        height_dist = (height - (dist * 2)) / half_number

        for i in range(1, half_number):
            height_coord.append(((height_dist * i) + dist))
        height_coord.append(height - dist)
    create_landmarks = []
    count = 0
    for width_index in range(len(width_coord)):
        for height_index in range(len(height_coord)):
            if count < number:
                create_landmarks.append(
                    [width_coord[width_index], height_coord[height_index]]
                )
                count += 1
    return create_landmarks


if __name__ == "__main__":
    # checking input parameters
    if len(sys.argv) < 4:
        print(
            "This script requires the following parameters: <width> <height> <number_of_landmarks> <number_of_particles>"
            #example: python main_pf.py 900 400 3 2000
        )
        sys.exit(1)
    else:
        parameters = sys.argv[1:]

    # world's dimension
    width = int(parameters[0])
    height = int(parameters[1])

    # creating the landmarks
    number_landmarks = int(parameters[2])
    dist_from_borders = 50
    landmarks = prepare_landmarks(number_landmarks, width, height, dist_from_borders)

    # creating the robot
    noise_linear = random.uniform(-0.5, 0.5)
    noise_angular = random.uniform(-0.03, 0.03)
    noise_measurement = random.uniform(-2, 2)
    robot = Agent(
        width / 2.0,
        height / 2.0,
        0.0,
        "red",
        noise_linear,
        noise_angular,
        noise_measurement,
    )

    # creating particles
    number_particles = int(parameters[3])  # 800
    particle_filter = ParticleFilter(
        landmarks=landmarks,
        number_particles=number_particles,
        robot=robot,
        width=width,
        height=height,
    )

    # creating screen
    game = Game(
        width=width,
        height=height,
        landmarks=landmarks,
        robot=robot,
        particles=particle_filter.particles,
    )

    # creating threads
    run_pf = threading.Thread(target=particle_filter.run_particle_filter)
    thread_game = threading.Thread(target=game.run)

    # running threads
    run_pf.start()
    game.run()

    # finishing threads
    run_pf.join()
    thread_game.join()

    pygame.quit()
